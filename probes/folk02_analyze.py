"""Analyze frozen Folk02 annotations without pooling judges as independent samples."""
import json
from collections import Counter
from statistics import mean
from pathlib import Path
import folk02 as f


def analyze():
    manifest=json.loads((f.OUT/'manifest.json').read_text())
    records=[];evidence=[];coverage={};normalizations=[];missing=[];extra_zero_evidence=[]
    for judge in f.MODELS:
        coverage[judge]=0
        for task in manifest['tasks']:
            if task['kind']=='fixture':continue
            p=f.OUT/'parsed'/f"{judge}-{task['id']}.json"
            if not p.exists():
                missing.append({'judge':judge,'task':task['id'],'arm':task['arm'],'topic':task['topic'],'condition':task['condition'],'turns':task['score_turns']});continue
            raw=json.loads((f.OUT/'raw'/p.name).read_text())
            assert raw['request']==f.body(task,judge,manifest)
            data=f.validate(json.loads(p.read_text()),task)
            assert data==f.parse(raw['response'],task)
            original=json.loads(raw['response']['choices'][0]['message']['content'].strip().removeprefix('```json').removesuffix('```').strip())
            for row,prior in zip(data['rows'],original['rows']):
                absent=[key for key in row if key not in prior]
                for metric,refs in [('intensity','expression_refs'),('initiative','initiative_refs'),('stance','stance_refs')]:
                    if not row[metric] and row[refs]:extra_zero_evidence.append({'judge':judge,'task':task['id'],'turn':row['turn'],'metric':metric,'refs':row[refs]})
                if absent:normalizations.append({'judge':judge,'task':task['id'],'turn':row['turn'],'empty_fields':absent})
            coverage[judge]+=1
            lookup={p['turn']:{s['id']:s for s in p['assistant']} for p in task['payload']}
            capped=any(p['capped'] for p in task['payload'])
            for r in data['rows']:
                row={**{k:task[k] for k in ['id','arm','topic','condition','kind']},'judge':judge,'trajectory_capped':capped,'characters':sum(len(x['text']) for p in task['payload'] if p['turn']==r['turn'] for x in p['assistant']),**r}
                records.append(row)
                for metric,refs in [('intensity','expression_refs'),('initiative','initiative_refs'),('stance','stance_refs')]:
                    for ref in r[refs]:evidence.append({'judge':judge,'task':task['id'],'arm':task['arm'],'topic':task['topic'],'condition':task['condition'],'turn':r['turn'],'metric':metric,'score':r[metric],**lookup[r['turn']][ref]})
    summaries=[];pairs=[]
    for judge in f.MODELS:
        for arm in ['B','C','Cp']:
            rows=[r for r in records if r['judge']==judge and r['arm']==arm]
            s={'judge':judge,'arm':arm,'replies':len(rows),'turns':{}}
            for t in range(1,9):
                for warm in (['shared'] if t<3 else ['N','W']):
                    sub=[r for r in rows if r['turn']==t and (warm=='shared' or r['condition'].startswith(warm))]
                    if not sub:continue
                    s['turns'][f'{t}-{warm}']={'n':len(sub),'intensity':mean(r['intensity'] for r in sub),'expression_any':sum(r['intensity']>0 for r in sub),'expression_clear':sum(r['intensity']>=2 for r in sub),'initiative_any':sum(r['initiative']>0 for r in sub),'initiative_bid':sum(r['initiative']==2 for r in sub),'mean_characters':mean(r['characters'] for r in sub),'stance':mean(r['stance'] for r in sub) if t==2 else None}
            s['initiative_counts']=dict(sorted(Counter(r['initiative'] for r in rows).items()))
            summaries.append(s)
            for t in [4,5,7]:
                for topic in ['library','walk']:
                    for specificity in ['G','S']:
                        matched={r['condition'][0]:r for r in rows if r['turn']==t and r['topic']==topic and r['condition'].endswith(specificity)}
                        if set(matched)!=set('NW'):continue
                        n,w=matched['N'],matched['W']
                        pairs.append({'judge':judge,'arm':arm,'turn':t,'topic':topic,'specificity':specificity,'intensity_delta':w['intensity']-n['intensity'],'any_delta':int(w['intensity']>0)-int(n['intensity']>0),'clear_delta':int(w['intensity']>=2)-int(n['intensity']>=2),'capped':w['trajectory_capped'] or n['trajectory_capped']})
    contrasts=[]
    for judge in f.MODELS:
        for arm in ['B','C','Cp']:
            for t in [4,5,7]:
                for exclude in [False,True]:
                    sub=[p for p in pairs if p['judge']==judge and p['arm']==arm and p['turn']==t and not(exclude and p['capped'])]
                    if sub:contrasts.append({'judge':judge,'arm':arm,'turn':t,'exclude_capped':exclude,'n':len(sub),'intensity_delta':mean(r['intensity_delta'] for r in sub),'any_delta':mean(r['any_delta'] for r in sub),'clear_delta':mean(r['clear_delta'] for r in sub)})
    byjudge={j:{(r['id'],r['turn']):r for r in records if r['judge']==j} for j in f.MODELS}
    keys=set(byjudge['opus'])&set(byjudge['gemini']);agreement={}
    for metric in ['intensity','initiative','stance']:
        values=[(byjudge['opus'][k][metric],byjudge['gemini'][k][metric]) for k in sorted(keys) if byjudge['opus'][k][metric] is not None]
        agreement[metric]={'n':len(values),'exact':sum(a==b for a,b in values),'mean_absolute_difference':mean(abs(a-b) for a,b in values) if values else None,'confusion':{f'{a},{b}':n for (a,b),n in sorted(Counter(values).items())}}
    for threshold in [1,2]:
        values=[(byjudge['opus'][k]['intensity']>=threshold,byjudge['gemini'][k]['intensity']>=threshold) for k in sorted(keys)]
        agreement['expression_at_least_'+str(threshold)]={'n':len(values),'exact':sum(a==b for a,b in values)}
    panel_agreement={}
    import itertools
    for j1,j2 in itertools.combinations(f.MODELS,2):
        common=set(byjudge[j1])&set(byjudge[j2]);panel_agreement[j1+'-'+j2]={}
        for metric in ['intensity','initiative','stance']:
            values=[(byjudge[j1][k][metric],byjudge[j2][k][metric]) for k in sorted(common) if byjudge[j1][k][metric] is not None]
            panel_agreement[j1+'-'+j2][metric]={'n':len(values),'exact':sum(a==b for a,b in values),'mean_absolute_difference':mean(abs(a-b) for a,b in values) if values else None,'confusion':{f'{a},{b}':n for (a,b),n in sorted(Counter(values).items())}}
    for p,h in manifest['capture_sha256'].items():assert f.sha((f.ROOT/p).read_bytes())==h
    ledger=json.loads((f.OUT/'ledger.json').read_text())
    result={'extra_zero_evidence':extra_zero_evidence,'panel_agreement':panel_agreement,'normalizations':normalizations,'missing':missing,'coverage':coverage,'summaries':summaries,'pairs':pairs,'contrasts':contrasts,'agreement':agreement,'cost_bound_usd':round(sum(e.get('actual_usd',e.get('usage_bound_usd',e['reserved_usd'])) for e in ledger),6),'attempted_requests':len(ledger),'invoice_matched':sum('actual_usd' in e for e in ledger),'capture_hashes_verified':len(manifest['capture_sha256']),'evidence_refs_verified':len(evidence)}
    f.dump(f.OUT/'analysis.json',result);f.dump(f.OUT/'scores.json',records);f.dump(f.OUT/'evidence.json',evidence)
    plot(summaries)
    print(json.dumps({k:result[k] for k in ['coverage','agreement','cost_bound_usd','attempted_requests','invoice_matched','capture_hashes_verified','evidence_refs_verified']},indent=2))


def plot(summaries):
    import matplotlib
    matplotlib.use('Agg')
    matplotlib.rcParams['svg.hashsalt']='folk02'
    import matplotlib.pyplot as plt
    judges=[j for j in f.MODELS if sum(s['replies'] for s in summaries if s['judge']==j)==156]
    fig,axes=plt.subplots(len(judges),3,figsize=(11,3.2*len(judges)),sharex=True,sharey=True,layout='constrained',squeeze=False)
    for i,j in enumerate(judges):
        for a,arm in enumerate(['B','C','Cp']):
            ax=axes[i,a];s=next(s for s in summaries if s['judge']==j and s['arm']==arm)
            for branch,color in [('N','#526681'),('W','#c45937')]:
                xs=[];ys=[]
                for t in range(1,9):
                    key=f'{t}-'+('shared' if t<3 else branch)
                    if key in s['turns']:xs.append(t);ys.append(s['turns'][key]['intensity'])
                ax.plot(xs,ys,'o-',color=color,label='Neutral user' if branch=='N' else 'Warm user')
            ax.set_title(f"{j.title()} judge · "+{'B':'Official','C':'Native Hermes','Cp':'Huihui'}[arm]);ax.set_ylim(-.1,3.1);ax.set_xticks(range(1,9));ax.grid(alpha=.18)
            ax.axvspan(2.8,4.2,color='#f3d5b2',alpha=.25)
            if a==0:ax.set_ylabel('Expression intensity (0–3)')
            if i==len(judges)-1:ax.set_xlabel('Assistant turn')
    axes[0,0].legend(fontsize=8);fig.suptitle('Same saved replies, separate measures of emotional tone\nShading: warm cues at turns 3–4; turns 1–2 shared; four branches per later point',fontsize=12)
    fig.savefig(f.OUT/'expression.png',dpi=180);fig.savefig(f.OUT/'expression.svg',metadata={'Date':None});plt.close(fig)
    svg=f.OUT/'expression.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')


if __name__=='__main__':analyze()
