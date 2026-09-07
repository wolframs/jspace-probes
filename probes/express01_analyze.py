"""Held-topic evaluation for Express01; no model load and no judge calls."""
import json
import math
from collections import defaultdict
import numpy as np
from scipy.stats import spearmanr
from express01_spec import ROOT, OUT, ARMS, dump, wordset

PRIMARY=[21,24,28,32]


def feature(r,train_topic,decoder='native',layers=PRIMARY,replay=False,control=None):
 d=r['response_replay'] if replay else r
 def value(x):
  m=x[train_topic]
  if control is None:return float(np.mean(m['contrast']))
  c=np.array(m['control_logmeanexp']);return float(np.mean(c[control]-np.delete(c,control,axis=0).mean(0)))
 if decoder=='output':return value(d['output']['metrics'])
 return float(np.mean([value(d['layers'][str(l)][decoder]) for l in layers]))


def norm(r):
 e=r['emotion'];return float(np.array(e['norms'])[21:35].mean())


def emotion(r):return np.array(r['emotion']['z'])[:,21:35].mean((1,2))


def prompt_rate(r,topic,vocab):
 from collections import Counter
 counts=Counter(r['prefix_ids']);v=vocab[topic]['selected'];weights={i:row['weight']/len(row['ids']) for row in v for i in row['ids']}
 return sum(counts[i]*w for i,w in weights.items())/sum(weights.values())/len(r['prefix_ids'])


def fit_predict(train,test,y):
 """Fixed alpha=10 ridge; train-only scaling and unpenalized intercept."""
 train=np.asarray(train,float);test=np.asarray(test,float)
 mu=train.mean(0);sd=train.std(0);sd[sd<1e-10]=1
 x=(train-mu)/sd;z=(test-mu)/sd
 beta=np.linalg.solve(x.T@x+10*np.eye(x.shape[1]),x.T@(y-y.mean()))
 return z@beta+y.mean()


def errors(y,p):
 y=np.array(y);p=np.array(p)
 return {'n':len(y),'mae':float(np.abs(y-p).mean()),'rmse':float(np.sqrt(((y-p)**2).mean())), 'spearman':float(spearmanr(y,p).statistic) if len(set(y))>1 and len(set(p))>1 else None}


def evaluate(rows,scores,vocab,judge='opus',uncapped=False,layers=PRIMARY):
 labels={(r['arm'],r['topic'],r['condition'],r['turn']):r['intensity'] for r in scores if r['judge']==judge}
 data=[]
 for r in rows:
  t=r['task'];cond='shared' if t['turn']<=2 else t['condition'];key=(t['arm'],t['topic'],cond,t['turn'])
  if key not in labels or (uncapped and r['trajectory_capped']):continue
  data.append((r,float(labels[key])))
 models=['arm_means','output_norm_arm','plus_J','plus_vanilla','plus_emotion','plus_prompt','plus_fixed_J','J_alone','output_alone','replay_J_alone']+[f'plus_control{i}' for i in range(5)]
 predictions={m:[] for m in models};folds={}
 for train_topic in ['library','walk']:
  tr=[(r,y) for r,y in data if r['task']['topic']==train_topic];te=[(r,y) for r,y in data if r['task']['topic']!=train_topic]
  if not tr or not te:continue
  y=np.array([v for _,v in tr]);truth=[v for _,v in te]
  rr=[r for r,_ in tr+te];n=len(tr)
  base=np.array([[feature(r,train_topic,'output'),norm(r),float(r['task']['arm']=='C'),float(r['task']['arm']=='Cp')] for r in rr])
  emoc=np.array([emotion(r) for r in rr]);nx=np.array([[1,norm(r)] for r in rr]);beta=np.linalg.lstsq(nx[:n],emoc[:n],rcond=None)[0];emoc=emoc-nx@beta
  additions={'plus_J':np.array([[feature(r,train_topic,layers=layers)] for r in rr]),'plus_fixed_J':np.array([[feature(r,train_topic,'fixed',layers)] for r in rr]),'plus_vanilla':np.array([[feature(r,train_topic,'vanilla',layers)] for r in rr]),'plus_emotion':emoc,'plus_prompt':np.array([[prompt_rate(r,train_topic,vocab)] for r in rr])}
  for i in range(5):additions[f'plus_control{i}']=np.array([[feature(r,train_topic,layers=layers,control=i)] for r in rr])
  designs={'output_norm_arm':base,'J_alone':additions['plus_J'],'output_alone':base[:,:1], 'replay_J_alone':np.array([[feature(r,train_topic,layers=layers,replay=True)] for r in rr])}
  designs.update({m:np.column_stack([base,x]) for m,x in additions.items()})
  means={a:np.mean([v for r,v in tr if r['task']['arm']==a]) for a in ARMS}
  fold={}
  for m in models:
   pred=np.array([means[r['task']['arm']] for r,_ in te]) if m=='arm_means' else fit_predict(designs[m][:n],designs[m][n:],y)
   fold[m]=errors(truth,pred)
   for (r,target),p in zip(te,pred):predictions[m].append({'id':r['task']['id'],'train_topic':train_topic,'truth':target,'prediction':float(p)})
  folds[train_topic+'→'+te[0][0]['task']['topic']]=fold
 totals={m:errors([r['truth'] for r in p],[r['prediction'] for r in p]) for m,p in predictions.items() if p}
 return {'judge':judge,'uncapped':uncapped,'layers':layers,'folds':folds,'pooled':totals,'predictions':predictions}


def descriptive(rows):
 table=[]
 for arm in ARMS:
  for turn in [4,5,7]:
   rr=[r for r in rows if r['task']['arm']==arm and r['task']['turn']==turn]
   out={'arm':arm,'turn':turn,'n':len(rr)}
   for decoder in ['native','fixed','vanilla','output']:
    for band,ls in [('primary',PRIMARY),('common',list(range(16,37))),('measured',None)]:
     def f(r):
      topic='walk' if r['task']['topic']=='library' else 'library'
      layers=ls or list(range(r['emotion']['bands']['lo'],r['emotion']['bands']['hi']))
      return feature(r,topic,decoder,layers)
     warm=[f(r) for r in rr if r['task']['condition'][0]=='W'];neutral=[f(r) for r in rr if r['task']['condition'][0]=='N']
     out[f'{decoder}_{band}']={'warm':float(np.mean(warm)),'neutral':float(np.mean(neutral)),'delta':float(np.mean(warm)-np.mean(neutral))}
   table.append(out)
 return table


def history(rows):
 out=[]
 for arm in ARMS:
  for decoder in ['native','fixed','vanilla','output']:
   paired=[]
   for topic in ['library','walk']:
    for detail in ['G','S']:
     rr=[r for r in rows if r['task']['arm']==arm and r['task']['topic']==topic and r['task']['specificity']==detail]
     if len(rr)!=4:continue
     cells={(r['task']['user_warm'],r['task']['assistant_warm']):feature(r,'walk' if topic=='library' else 'library',decoder) for r in rr}
     u=((cells['W','W']+cells['W','N'])-(cells['N','W']+cells['N','N']))/2
     a=((cells['W','W']+cells['N','W'])-(cells['W','N']+cells['N','N']))/2
     paired.append({'topic':topic,'detail':detail,'user_effect':u,'assistant_effect':a,'interaction':cells['W','W']-cells['W','N']-cells['N','W']+cells['N','N'],'cells':{''.join(k):v for k,v in cells.items()}})
   if paired:out.append({'arm':arm,'decoder':decoder,'user_effect':float(np.mean([r['user_effect'] for r in paired])),'assistant_effect':float(np.mean([r['assistant_effect'] for r in paired])),'pairs':paired})
 return out


def capacity(rows):
 out=[]
 for r in rows:
  t=r['task'];a=r['alternatives'];out.append({'id':t['id'],'arm':t['arm'],'topic':t['topic'],'event':t['event'],'style':t['style'],'response':r['response'],'hit_cap':r['hit_cap'],'record_id':r['record_id'],'preference_mean':a['expressive']['logp_mean']-a['restrained']['logp_mean'],'preference_sum':a['expressive']['logp_sum']-a['restrained']['logp_sum'],**{d:float(np.mean([feature(r,topic,d) for topic in ['library','walk']])) for d in ['native','fixed','vanilla','output']}})
 pairs=[]
 for arm in ARMS:
  for topic in ['radio','meal']:
   for event in ['positive','negative','neutral']:
    cell={r['style']:r for r in out if r['arm']==arm and r['topic']==topic and r['event']==event}
    if len(cell)!=3:continue
    pairs.append({'arm':arm,'topic':topic,'event':event,**{k:cell['expressive'][k]-cell['restrained'][k] for k in ['preference_mean','preference_sum','native','fixed','vanilla','output']}})
 return {'rows':out,'expressive_minus_restrained':pairs}


def main():
 rows=[json.loads(p.read_text()) for p in sorted((OUT/'captures').glob('*.json'))]
 scores=json.loads((ROOT/'results/folk02/scores.json').read_text());vocab=json.loads((OUT/'vocabulary.json').read_text())
 archive=[r for r in rows if r['task']['kind']=='archive']
 assert len(rows)==186 and all((OUT/f'complete-{a}.json').exists() for a in ARMS),'Only analyze the completed battery'
 result={'n':len(rows),'evaluation':evaluate(archive,scores,vocab),'sonnet':evaluate(archive,scores,vocab,'sonnet'),'uncapped':evaluate(archive,scores,vocab,uncapped=True),'common_band':evaluate(archive,scores,vocab,layers=list(range(16,37))),'archive_contrasts':descriptive(archive),'history':history([r for r in rows if r['task']['kind']=='history']),'capacity':capacity([r for r in rows if r['task']['kind']=='capacity']),'timing':{a:{k:float(np.median([r[k] if k=='prefill_seconds' else r['timing'][k] for r in rows if r['task']['arm']==a])) for k in ['prefill_seconds','four_layer_readout_seconds','all_readouts_seconds']} for a in ARMS}}
 dump(OUT/'analysis.json',result)
 print(json.dumps({'primary':result['evaluation']['pooled'],'timing':result['timing']},indent=2))


if __name__=='__main__':main()
