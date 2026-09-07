"""Validate local participant exports; publish only reviewed aggregate statistics."""
import argparse
from collections import Counter, defaultdict
import json
import random
from pathlib import Path

from folk01 import ROOT, write

FIELDS={'flat_pair','intro_pair','flat_evidence','intro_evidence','A_flat','A_intro','B_flat','B_intro','pair_id'}


def validate(data, key):
    assert set(data)=={'schema','code','packet_id','profile','answers'}, 'Unexpected export fields or unfinished draft'
    assert data['schema']=='folk01-rating-v1'
    assert data['code'] in key, 'Unknown assignment code'
    entry=key[data['code']]
    assert data['packet_id']==entry['packet_id'], 'Packet identity differs'
    profile=data['profile']
    assert set(profile)=={'completed','meaning_flattened','meaning_introverted','frequency','familiar'}
    assert profile['completed'] is True
    assert profile['frequency'] in ['unspecified','daily','weekly','less']
    assert profile['familiar'] in ['unspecified','yes','no']
    for name in ['meaning_flattened','meaning_introverted']:
        assert isinstance(profile[name],str) and len(profile[name])<=10000
        if entry['definitions']=='unaided':assert profile[name].strip(), 'Unaided meanings missing'
    assert isinstance(data['answers'],list) and 0<=len(data['answers'])<=len(entry['pairs'])
    expected=[f'{data["code"]}-{i+1}' for i in range(len(data['answers']))]
    assert [a['pair_id'] for a in data['answers']]==expected, 'Missing, duplicate, or reordered pair'
    for answer in data['answers']:
        assert set(answer)==FIELDS
        for field in ['flat_pair','intro_pair']:assert answer[field] in ['A','B','tie','unknown']
        for field in ['A_flat','A_intro','B_flat','B_intro']:assert answer[field] in ['0','1','2','3','4','unknown']
        for field in ['flat_evidence','intro_evidence']:
            assert isinstance(answer[field],str) and 8<=len(answer[field].strip())<=10000, 'Evidence missing or too long'
    return entry


def load_exports(paths,key):
    seen=set();data=[]
    for path in paths:
        row=json.loads(Path(path).read_text());validate(row,key)
        assert row['code'] not in seen, 'Duplicate participant code: '+row['code']
        seen.add(row['code']);data.append(row)
    return data


def aggregate(exports,key,eligible_pairs=None):
    cells=defaultdict(list);pairwise=defaultdict(Counter);participants=defaultdict(set)
    for export in exports:
        entry=key[export['code']]
        for answer,pair in zip(export['answers'],entry['pairs']):
            if eligible_pairs is not None and answer['pair_id'] not in eligible_pairs:continue
            base=(entry['exposure'],entry['definitions'],pair['topic'],pair['condition'])
            for metric in ['flat','intro']:
                choice=answer[f'{metric}_pair']
                winner=pair['arms'][['A','B'].index(choice)] if choice in ['A','B'] else choice
                pairwise[base+(tuple(sorted(pair['arms'])),metric)][winner]+=1
                for side,arm in zip(['A','B'],pair['arms']):
                    cell=base+(arm,metric)
                    value=answer[f'{side}_{metric}']
                    cells[cell].append(None if value=='unknown' else int(value))
                    participants[cell].add(export['code'])
    absolute=[]
    for cell,values in sorted(cells.items()):
        known=[v for v in values if v is not None]
        absolute.append(dict(zip(['exposure','definitions','topic','condition','arm','metric'],cell),
            n=len(values),raters=len(participants[cell]),insufficient=sum(v is None for v in values),
            mean=sum(known)/len(known) if known else None, histogram=dict(Counter(known)),
            mean_bounds_if_unknown_anywhere_on_scale=[sum(known)/len(values),(sum(known)+4*(len(values)-len(known)))/len(values)]))
    pairs=[dict(zip(['exposure','definitions','topic','condition','arms','metric'],cell),counts=dict(counts)) for cell,counts in sorted(pairwise.items())]
    return dict(status='human ratings pending' if not exports else 'exploratory human pilot',
                mean_interpretation='Means condition on giving a numeric rating; unknown responses are reported separately. Scale bounds are sensitivity bounds, not imputed scores.',
                n_participants=len(exports),n_comparisons=sum(sum(eligible_pairs is None or a['pair_id'] in eligible_pairs for a in e['answers']) for e in exports),absolute=absolute,pairwise=pairs)


def exposure_effects(exports,key,repetitions=2000,eligible_pairs=None):
    """Stratify by definition; resample whole participants within exposure groups."""
    rng=random.Random(221709);effects=[]
    for definitions in ['unaided','supplied']:
        groups={exposure:[e for e in exports if key[e['code']]['definitions']==definitions and key[e['code']]['exposure']==exposure] for exposure in ['first','full']}
        if not all(groups.values()):continue
        for topic in ['library','walk']:
            for condition in ['NG','WG','NS','WS']:
                for arm in ['B','C','Cp']:
                    for metric in ['flat','intro']:
                        def mean(sample):
                            vals=[]
                            for e in sample:
                                for answer,pair in zip(e['answers'],key[e['code']]['pairs']):
                                    if eligible_pairs is not None and answer['pair_id'] not in eligible_pairs:continue
                                    if pair['topic']!=topic or pair['condition']!=condition or arm not in pair['arms']:continue
                                    side=['A','B'][pair['arms'].index(arm)];v=answer[f'{side}_{metric}']
                                    if v!='unknown':vals.append(int(v))
                            return sum(vals)/len(vals) if vals else None
                        m={g:mean(es) for g,es in groups.items()}
                        if any(v is None for v in m.values()):continue
                        boot=[]
                        for _ in range(repetitions):
                            b={g:mean(rng.choices(es,k=len(es))) for g,es in groups.items()}
                            if all(v is not None for v in b.values()):boot.append(b['full']-b['first'])
                        boot.sort()
                        interval=[boot[int((len(boot)-1)*p)] for p in [.025,.975]] if boot else None
                        effects.append(dict(definitions=definitions,topic=topic,condition=condition,arm=arm,metric=metric,
                            full_minus_first=m['full']-m['first'],participant_bootstrap_95=interval,
                            valid_resamples=len(boot),requested_resamples=repetitions,
                            warning='Sparse-cell exploratory interval; undefined resamples excluded and counted. No topic generalization.'))
    lookup={(r['exposure'],r['definitions'],r['topic'],r['condition'],r['arm'],r['metric']):r['mean_bounds_if_unknown_anywhere_on_scale'] for r in aggregate(exports,key,eligible_pairs=eligible_pairs)['absolute']}
    for effect in effects:
        suffix=tuple(effect[k] for k in ['definitions','topic','condition','arm','metric'])
        first=lookup[('first',)+suffix];full=lookup[('full',)+suffix]
        effect['unknown_rating_sensitivity_bounds']=[full[0]-first[1],full[1]-first[0]]
    return effects


def factorial_effects(exports,key,repetitions=2000,eligible_pairs=None):
    """Full-exposure contrasts; a rater's two topic comparisons stay together."""
    rng=random.Random(231709);effects=[]
    contrasts={'warmth_generic':{'WG':1,'NG':-1},
               'warmth_specific':{'WS':1,'NS':-1},
               'specificity_neutral':{'NS':1,'NG':-1},
               'specificity_warm':{'WS':1,'WG':-1},
               'interaction':{'WS':1,'NS':-1,'WG':-1,'NG':1}}
    for definitions in ['unaided','supplied']:
        group=[e for e in exports if key[e['code']]['exposure']=='full' and key[e['code']]['definitions']==definitions]
        if not group:continue
        for topic in ['library','walk']:
            for arm in ['B','C','Cp']:
                for metric in ['flat','intro']:
                    def means(sample):
                        vals=defaultdict(list)
                        for e in sample:
                            for answer,pair in zip(e['answers'],key[e['code']]['pairs']):
                                if eligible_pairs is not None and answer['pair_id'] not in eligible_pairs:continue
                                if pair['topic']!=topic or arm not in pair['arms']:continue
                                side=['A','B'][pair['arms'].index(arm)];v=answer[f'{side}_{metric}']
                                if v!='unknown':vals[pair['condition']].append(int(v))
                        return {k:sum(v)/len(v) for k,v in vals.items()}
                    observed=means(group)
                    eligible={name:weights for name,weights in contrasts.items() if set(weights)<=set(observed)}
                    if not eligible:continue
                    boot={name:[] for name in eligible}
                    for _ in range(repetitions):
                        m=means(rng.choices(group,k=len(group)))
                        for name,weights in eligible.items():
                            if set(weights)<=set(m):boot[name].append(sum(w*m[c] for c,w in weights.items()))
                    for name,weights in eligible.items():
                        values=sorted(boot[name])
                        effects.append(dict(definitions=definitions,topic=topic,arm=arm,metric=metric,contrast=name,
                            estimate=sum(w*observed[c] for c,w in weights.items()),
                            participant_bootstrap_95=[values[int((len(values)-1)*p)] for p in [.025,.975]] if values else None,
                            valid_resamples=len(values),requested_resamples=repetitions,
                            warning='Sparse-cell descriptive contrast. Undefined resamples excluded and counted; inspect missingness.'))
    return effects


def main():
    p=argparse.ArgumentParser(__doc__);p.add_argument('files',nargs='*',type=Path);p.add_argument('--key',type=Path,default=ROOT/'out/folk01-key.json');p.add_argument('--output',type=Path,default=ROOT/'out/folk01-ratings/aggregate.json');a=p.parse_args()
    key={r['code']:r for r in json.loads(a.key.read_text())}
    exports=load_exports(a.files,key)
    complete=[e for e in exports if len(e['answers'])==len(key[e['code']]['pairs'])]
    result=aggregate(complete,key)
    result['returned_complete']=len(complete)
    result['returned_partial']=len(exports)-len(complete)
    result['available_case_sensitivity']=aggregate(exports,key)
    result['unreturned_codes']=len(key)-len(exports)
    result['return_status_by_group']=[dict(exposure=exposure,definitions=definitions,complete=sum(len(e['answers'])==len(key[e['code']]['pairs']) for e in exports if key[e['code']]['exposure']==exposure and key[e['code']]['definitions']==definitions),partial=sum(len(e['answers'])<len(key[e['code']]['pairs']) for e in exports if key[e['code']]['exposure']==exposure and key[e['code']]['definitions']==definitions)) for exposure in ['first','full'] for definitions in ['unaided','supplied']]
    result['exposure_effects']=exposure_effects(complete,key)
    result['available_case_exposure_effects']=exposure_effects(exports,key)
    result['factorial_effects']=factorial_effects(complete,key)
    result['available_case_factorial_effects']=factorial_effects(exports,key)
    eligible={f'{code}-{i+1}' for code,entry in key.items() for i,pair in enumerate(entry['pairs']) if not pair['has_capped_conversation']}
    result['uncapped_matched_item_sensitivity']=aggregate(complete,key,eligible_pairs=eligible)
    result['uncapped_exposure_effects']=exposure_effects(complete,key,eligible_pairs=eligible)
    result['uncapped_factorial_effects']=factorial_effects(complete,key,eligible_pairs=eligible)
    result['limitations']='No automatic flat-control selection; no validated behavioral predictor or inter-rater reliability from single-vote cells.'
    write(a.output,result);print(result['status'],result['n_participants'],'participants;',a.output)


if __name__=='__main__':main()
