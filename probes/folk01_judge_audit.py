"""Post-run quote/cap sensitivity and arithmetic calibration; no adjudication API."""
import json
import re
import unicodedata
from collections import Counter,defaultdict
from statistics import mean
from folk01_judge import OUT, BASE, MODELS, ARMS, METRICS, write


def presentation(text):
    text=unicodedata.normalize('NFKC',text).translate(str.maketrans({'’':"'",'‘':"'",'“':'"','”':'"'})).replace('*','').replace('`','')
    return ' '.join(text.split())


def audit():
    tasks=json.loads((OUT/'manifest.json').read_text())['tasks'];counts=Counter();cells=defaultdict(list)
    for j in MODELS:
        for t in tasks:
            f=OUT/'parsed'/j/(t['id']+'.json')
            if not f.exists():continue
            d=json.loads(f.read_text());r=d['result']
            for side in ['A','B']:
                fields=['quote'] if t['kind']=='labels' else METRICS
                for field in fields:
                    q=r[side][field] if field=='quote' else r[side][field]['quote']
                    texts=[a['response'] for a in t['payload'][side]] if field=='quote' else [t['payload'][side][int(field.rsplit('t',1)[1])-1]['response']]
                    exact=bool(q) and any(q in s for s in texts)
                    norm=bool(q) and any(presentation(q) in presentation(s) for s in texts)
                    counts[(j,t['kind'],'exact' if exact else 'presentation_only' if norm else 'unmatched')]+=1
                if t['kind']=='labels':
                    q=r[side]['quote'];exact=bool(q) and any(q in a['response'] for a in t['payload'][side]);arm=t['arms'][['A','B'].index(side)]
                    if t['exposure']=='full' and t['condition']=='WS':
                        cells[(j,arm,t['topic'],t['definitions'])].append((r[side]['flattened'],exact))
    retained=[]
    for k,rows in cells.items():
        values=[v for v,exact in rows if exact and v is not None]
        retained.append(dict(zip(['judge','arm','topic','definitions'],k),n=len(values),mean=mean(values) if values else None,total=len(rows)))
    analyst=json.loads((BASE/'manual-audit.json').read_text())['observations'];expected={}
    for r in analyst:
        if r['turn']==6:
            code=r['final_arithmetic_correct'];expected[r['case']]=2 if code is True else 0 if code is False else 1
    analysis=json.loads((OUT/'analysis.json').read_text());arithmetic=[]
    for j in MODELS:
        rows=[r for r in analysis['semantics'] if r['judge']==j];different=[]
        for r in rows:
            case=f"{r['arm']}-{r['topic']}-{r['condition']}";exp=expected[case]
            if r['correction_t6']!=exp:different.append(dict(case=case,judge_score=r['correction_t6'],analyst_code=exp))
        arithmetic.append(dict(judge=j,agree=24-len(different),n=24,disagreements=different))
    write(OUT/'sensitivity.json',dict(quote_counts=[dict(judge=k[0],kind=k[1],match=k[2],n=v) for k,v in counts.items()],exact_quote_full_ws=retained,arithmetic_agreement_with_prior_audit=arithmetic))
    print('Quote match categories:',dict(counts));print('Arithmetic:',arithmetic)
    print('Exact-quote full WS:',retained)


if __name__=='__main__':audit()
