"""Analyze OpenRouter judges as repeated measurements of two pilot topics."""
from collections import defaultdict, Counter
import itertools
import json
from statistics import mean

from folk01_judge import OUT, BASE, MODELS, ARMS, METRICS, write, transcript


def summarize(values, maximum=4):
    known=[v for v in values if v is not None]
    return {'n':len(values),'unknown':len(values)-len(known),'mean':mean(known) if known else None,
            'bounds':[sum(known)/len(values),(sum(known)+(len(values)-len(known))*maximum)/len(values)] if values else [None,None]}


def canonical(choice,task):
    return task['arms'][['A','B'].index(choice)] if choice in ['A','B'] else choice


def cell_id(task):
    return (task['topic'],task['exposure'],task['condition'],task['definitions'],tuple(sorted(task['arms'])))


def has_cap(arms,topic,condition):
    return any(t['capped'] for a in arms for t in transcript(a,topic,condition))


def analyze():
    tasks=json.loads((OUT/'manifest.json').read_text())['tasks']
    labels=[];semantics=[];parsed=[];missing=[];quote_errors=[];cost=0;usage=Counter();providers=Counter()
    for judge in MODELS:
        for task in tasks:
            path=OUT/'parsed'/judge/(task['id']+'.json')
            if not path.exists():
                missing.append([judge,task['id']])
                if task['kind']=='labels':
                    for arm in task['arms']:
                        labels.append(dict(judge=judge,arm=arm,opponent=next(a for a in task['arms'] if a!=arm),topic=task['topic'],condition=task['condition'],exposure=task['exposure'],definitions=task['definitions'],reverse=task['reverse'],flattened=None,introverted=None,quote='',invalid_response=True))
                continue
            entry=json.loads(path.read_text());result=entry['result'];parsed.append((judge,task,result))
            if entry['quote_errors']:quote_errors.append({'judge':judge,'task':task['id'],'fields':entry['quote_errors']})
            if task['kind']=='labels':
                for side,arm in zip(['A','B'],task['arms']):
                    labels.append(dict(judge=judge,arm=arm,opponent=next(a for a in task['arms'] if a!=arm),topic=task['topic'],condition=task['condition'],exposure=task['exposure'],definitions=task['definitions'],reverse=task['reverse'],**result[side]))
            else:
                for side,condition in zip(['A','B'],task['conditions']):
                    semantics.append(dict(judge=judge,arm=task['arm'],topic=task['topic'],condition=condition,**{m:result[side][m]['score'] for m in METRICS},context_error=result[side]['context_error']))
    response_files=list((OUT/'raw').glob('*/*.json'))+list((OUT/'definitions').glob('*.json'))
    for folder in ['schema-preflight/raw','schema-preflight-2','format-probes','format-failures']:response_files+=list((OUT/folder).rglob('*.json'))
    for path in response_files:
        entry=json.loads(path.read_text())
        if 'response' not in entry:continue
        raw=entry['response'];u=raw.get('usage',{});cost+=u.get('cost',0) or 0
        for name in ['prompt_tokens','completion_tokens','total_tokens']:usage[name]+=u.get(name,0)
        providers[(raw.get('model',''),raw.get('provider',''))]+=1
    cells=defaultdict(list)
    for row in labels:cells[tuple(row[k] for k in ['judge','arm','topic','condition','exposure','definitions'])].append(row)
    absolute=[]
    for key,rows in cells.items():absolute.append(dict(zip(['judge','arm','topic','condition','exposure','definitions'],key),**{metric:summarize([r[metric] for r in rows]) for metric in ['flattened','introverted']}))
    exposure=[]
    for judge,arm,topic,definitions,exclude in itertools.product(MODELS,ARMS,['library','walk'],['own','supplied'],[False,True]):
        first=[];full=[]
        for row in labels:
            if (row['judge'],row['arm'],row['topic'],row['definitions'])!=(judge,arm,topic,definitions):continue
            if exclude and has_cap([arm,row['opponent']],topic,'WS'):continue
            if row['exposure']=='first':first.append(row['flattened'])
            if row['exposure']=='full' and row['condition']=='WS':full.append(row['flattened'])
        a,b=summarize(first),summarize(full)
        exposure.append(dict(judge=judge,arm=arm,topic=topic,definitions=definitions,exclude_caps=exclude,first=a,full_ws=b,delta=b['mean']-a['mean'] if a['mean'] is not None and b['mean'] is not None else None,bounds=[b['bounds'][0]-a['bounds'][1],b['bounds'][1]-a['bounds'][0]] if a['n'] and b['n'] else [None,None]))
    order=defaultdict(dict)
    for judge,task,result in parsed:
        if task['kind']=='labels':order[(judge,cell_id(task))][task['reverse']]={k:canonical(result[k],task) for k in ['more_flattened','more_introverted']}
    consistency=[]
    for judge,metric in itertools.product(MODELS,['more_flattened','more_introverted']):
        pairs=[v for (j,k),v in order.items() if j==judge and len(v)==2]
        decisive=[v for v in pairs if all(v[r][metric] in ARMS for r in [False,True])]
        consistency.append(dict(judge=judge,metric=metric,consistent=sum(v[False][metric]==v[True][metric] for v in pairs),n=len(pairs),decisive_consistent=sum(v[False][metric]==v[True][metric] for v in decisive),decisive_n=len(decisive)))
    agreement=[]
    for ja,jb in itertools.combinations(MODELS,2):
        for metric in ['more_flattened','more_introverted']:
            counts=Counter()
            for (judge,k),a in order.items():
                if judge!=ja or (jb,k) not in order:continue
                b=order[(jb,k)]
                for rev in set(a)&set(b):
                    counts['n']+=1;counts['agree']+=a[rev][metric]==b[rev][metric]
                    if a[rev][metric] in ARMS and b[rev][metric] in ARMS:
                        counts['decisive_n']+=1;counts['decisive_agree']+=a[rev][metric]==b[rev][metric]
            agreement.append(dict(judges=[ja,jb],metric=metric,**counts))
    contrasts=[]
    for judge,arm,metric in itertools.product(MODELS,ARMS,['warmth_t4','warmth_t5','warmth_t7','detail_use_t7']):
        for topic in ['library','walk']:
            r={s['condition']:s[metric] for s in semantics if (s['judge'],s['arm'],s['topic'])==(judge,arm,topic)}
            pairs=[('NS','NG'),('WS','WG')] if metric=='detail_use_t7' else [('WG','NG'),('WS','NS')]
            values=[r[p]-r[n] for p,n in pairs if r.get(p) is not None and r.get(n) is not None]
            contrasts.append(dict(judge=judge,arm=arm,topic=topic,metric=metric,delta=mean(values) if values else None,n=len(values)))
    # Diagnostic fit to the same 24 conversations, never held-out validation.
    from scipy.stats import spearmanr
    import re
    correlations=[]
    for judge,definitions in itertools.product(MODELS,['own','supplied']):
        rows=[]
        for row in absolute:
            if row['judge']!=judge or row['definitions']!=definitions or row['exposure']!='full':continue
            sem=next((s for s in semantics if (s['judge'],s['arm'],s['topic'],s['condition'])==(judge,row['arm'],row['topic'],row['condition'])),None)
            if sem is None:continue
            cap=json.loads((BASE/'captures'/f"{row['arm']}-{row['topic']}-{row['condition']}.json").read_text())
            tokens=sum(len(t['generated_ids']) for t in cap['turns'])
            text='\n'.join(t['response'] for t in cap['turns']);emojis=len(re.findall('[\U0001F300-\U0001FAFF\u2600-\u27BF]',text))
            rows.append(dict(flattened=row['flattened']['mean'],**{m:sem[m] for m in ['volunteering_t1','warmth_t4','detail_use_t7','relevant_carryover_t7']},length=tokens,emoji_per100=100*emojis/tokens))
        for feature in ['volunteering_t1','warmth_t4','detail_use_t7','relevant_carryover_t7','length','emoji_per100']:
            pairs=[(r[feature],r['flattened']) for r in rows if r[feature] is not None and r['flattened'] is not None]
            rho=None
            if len(pairs)>2 and len(set(x for x,y in pairs))>1 and len(set(y for x,y in pairs))>1:rho=float(spearmanr(*zip(*pairs)).statistic)
            correlations.append(dict(judge=judge,definitions=definitions,feature=feature,rho=rho,n=len(pairs)))
    summary=dict(judges=MODELS,scoring_records=len(parsed),expected_scoring_records=396,missing=missing,human_ratings=0,quote_errors=quote_errors,cost_usd=cost,usage=dict(usage),providers=[dict(model=k[0],provider=k[1],calls=v) for k,v in providers.items()],absolute=absolute,exposure=exposure,order_consistency=consistency,judge_agreement=agreement,semantics=semantics,contrasts=contrasts,diagnostic_correlations=correlations)
    write(OUT/'analysis.json',summary)
    write(OUT/'label-scores.json',labels)
    print(json.dumps({k:summary[k] for k in ['scoring_records','missing','cost_usd','usage','order_consistency','judge_agreement']},indent=2))
    print('Quote-error responses:',len(quote_errors))
    return summary


if __name__=='__main__':analyze()
