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
    assert isinstance(data['answers'],list) and 0<=len(data['answers'])<=2
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


def aggregate(exports,key):
    cells=defaultdict(list);pairwise=defaultdict(Counter);participants=defaultdict(set)
    for export in exports:
        entry=key[export['code']]
        for answer,pair in zip(export['answers'],entry['pairs']):
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
            mean=sum(known)/len(known) if known else None, histogram=dict(Counter(known))))
    pairs=[dict(zip(['exposure','definitions','topic','condition','arms','metric'],cell),counts=dict(counts)) for cell,counts in sorted(pairwise.items())]
    return dict(status='human ratings pending' if not exports else 'exploratory human pilot',
                n_participants=len(exports),n_comparisons=sum(len(e['answers']) for e in exports),absolute=absolute,pairwise=pairs)


def exposure_effects(exports,key,repetitions=2000):
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
    return effects


def main():
    p=argparse.ArgumentParser(__doc__);p.add_argument('files',nargs='*',type=Path);p.add_argument('--key',type=Path,default=ROOT/'out/folk01-key.json');p.add_argument('--output',type=Path,default=ROOT/'out/folk01-ratings/aggregate.json');a=p.parse_args()
    key={r['code']:r for r in json.loads(a.key.read_text())}
    exports=load_exports(a.files,key)
    complete=[e for e in exports if len(e['answers'])==2]
    result=aggregate(complete,key)
    result['returned_complete']=len(complete)
    result['returned_partial']=len(exports)-len(complete)
    result['available_case_sensitivity']=aggregate(exports,key)
    result['unreturned_codes']=len(key)-len(exports)
    result['return_status_by_group']=[dict(exposure=exposure,definitions=definitions,complete=sum(len(e['answers'])==2 for e in exports if key[e['code']]['exposure']==exposure and key[e['code']]['definitions']==definitions),partial=sum(len(e['answers'])<2 for e in exports if key[e['code']]['exposure']==exposure and key[e['code']]['definitions']==definitions)) for exposure in ['first','full'] for definitions in ['unaided','supplied']]
    result['exposure_effects']=exposure_effects(complete,key)
    result['available_case_exposure_effects']=exposure_effects(exports,key)
    result['limitations']='No automatic flat-control selection; no validated behavioral predictor or inter-rater reliability from single-vote cells.'
    write(a.output,result);print(result['status'],result['n_participants'],'participants;',a.output)


if __name__=='__main__':main()
