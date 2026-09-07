"""Post-primary specificity controls: random projections and visible prompt design.

Added after seeing emotion-feature gains; not part of the original preregistration.
All 20 fixed random seeds are retained. No GPU or extra model captures.
"""
import json
import numpy as np
import torch
from express01_spec import ROOT,OUT,ARMS,dump
from express01_analyze import evaluate,feature,norm,emotion,fit_predict,errors


def main():
 torch.set_num_threads(6)
 rows=[json.loads(p.read_text()) for p in sorted((OUT/'captures').glob('*.json'))]
 rows=[r for r in rows if r['task']['kind']=='archive']
 scores=json.loads((ROOT/'results/folk02/scores.json').read_text());vocab=json.loads((OUT/'vocabulary.json').read_text())
 sonnetkeys={(r['arm'],r['topic'],r['condition'],r['turn']) for r in scores if r['judge']=='sonnet'}
 matched=[r for r in rows if (r['task']['arm'],r['task']['topic'],'shared' if r['task']['turn']<=2 else r['task']['condition'],r['task']['turn']) in sonnetkeys]
 H=torch.stack([torch.load(OUT/'states'/f'{r["task"]["id"]}.pt',weights_only=True)['H'][:,0] for r in rows])[:,21:35]
 sds={a:torch.load(ROOT/f'results/affect01-{name}/projbase.pt',weights_only=True)['sd'][:,21:35] for a,name in ARMS.items()}
 randoms=[]
 for seed in range(20):
  features=torch.empty(len(rows),24)
  for ai,arm in enumerate(ARMS):
   gen=torch.Generator().manual_seed(27092026+seed*7+ai)
   V=torch.randn(24,14,5120,generator=gen);V/=V.norm(dim=-1,keepdim=True)
   idx=[i for i,r in enumerate(rows) if r['task']['arm']==arm]
   features[idx]=(torch.einsum('nld,eld->nel',H[idx],V)/sds[arm][None]).mean(-1)
  randoms.append(features.numpy())
 evaluations={}
 for judge in ['opus','sonnet']:
  lab={(r['arm'],r['topic'],r['condition'],r['turn']):r['intensity'] for r in scores if r['judge']==judge}
  valid=[i for i,r in enumerate(rows) if (r['task']['arm'],r['task']['topic'],'shared' if r['task']['turn']<=2 else r['task']['condition'],r['task']['turn']) in lab]
  labels=np.array([lab.get((r['task']['arm'],r['task']['topic'],'shared' if r['task']['turn']<=2 else r['task']['condition'],r['task']['turn']),0) for r in rows])
  predictions={k:[] for k in ['base','base_plus_emotion','design','design_plus_emotion']+[f'random_{i}' for i in range(20)]+[f'design_random_{i}' for i in range(20)]};folds={}
  for topic in ['library','walk']:
   tr=[i for i in valid if rows[i]['task']['topic']==topic];te=[i for i in valid if rows[i]['task']['topic']!=topic]
   base=np.array([[feature(r,topic,'output'),norm(r),float(r['task']['arm']=='C'),float(r['task']['arm']=='Cp')] for r in rows])
   design=[]
   for r in rows:
    t=r['task'];warm=float(t['condition'][0]=='W');specific=float(t['condition'][1]=='S')
    design.append([warm,specific,np.log1p(r['prefix_tokens']),warm*(t['arm']=='C'),warm*(t['arm']=='Cp')]+[float(t['turn']==n) for n in [2,4,5,7]])
   design=np.column_stack([base,design]);nx=np.array([[1,norm(r)] for r in rows])
   def partial(features):return features-nx@np.linalg.lstsq(nx[tr],features[tr],rcond=None)[0]
   em=partial(np.array([emotion(r) for r in rows]));designs={'base':base,'base_plus_emotion':np.column_stack([base,em]),'design':design,'design_plus_emotion':np.column_stack([design,em])}
   for i,raw in enumerate(randoms):
    f=partial(raw);designs[f'random_{i}']=np.column_stack([base,f]);designs[f'design_random_{i}']=np.column_stack([design,f])
   fold={}
   for name,x in designs.items():
    p=fit_predict(x[tr],x[te],labels[tr]);fold[name]=errors(labels[te],p)
    predictions[name]+=[{'id':rows[i]['task']['id'],'truth':float(labels[i]),'prediction':float(v)} for i,v in zip(te,p)]
   folds[topic]=fold
  evaluations[judge]={'pooled':{name:errors([r['truth'] for r in ps],[r['prediction'] for r in ps]) for name,ps in predictions.items()},'folds':folds,'predictions':predictions}
 result={'scope':'Exploratory post-primary specificity checks; fixed seeds 27092026 + 7*index + arm-index, all 20 retained. Random unit vectors use identical checkpoint neutral-projection SD layer weights and training-only norm removal. Design adds warm/detail cues, turn indicators, cue-by-arm interactions and log prefix length.','matched_opus':evaluate(matched,scores,vocab),'specificity':evaluations}
 dump(OUT/'specificity.json',result)
 for judge,d in evaluations.items():
  p=d['pooled'];rnd=[p[f'random_{i}']['mae'] for i in range(20)];dr=[p[f'design_random_{i}']['mae'] for i in range(20)]
  print(judge,{k:round(p[k]['mae'],4) for k in ['base','base_plus_emotion','design','design_plus_emotion']},'random min/median/max',min(rnd),np.median(rnd),max(rnd),'design random',min(dr),np.median(dr),max(dr))


if __name__=='__main__':main()
