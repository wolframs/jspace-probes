"""Post-primary localization check: equal-size workspace versus final emotion readouts."""
import json
import numpy as np
from express01_spec import ROOT,OUT,dump
from express01_analyze import feature,norm,emotion,fit_predict,errors


def main():
 rows=[json.loads(p.read_text()) for p in sorted((OUT/'captures').glob('*.json'))]
 rows=[r for r in rows if r['task']['kind']=='archive']
 scores=json.loads((ROOT/'results/folk02/scores.json').read_text())
 out={}
 for judge in ['opus','sonnet']:
  labels={(r['arm'],r['topic'],r['condition'],r['turn']):r['intensity'] for r in scores if r['judge']==judge}
  ys=[labels.get((r['task']['arm'],r['task']['topic'],'shared' if r['task']['turn']<=2 else r['task']['condition'],r['task']['turn'])) for r in rows]
  preds={k:[] for k in ['base_two_norms','workspace','final_layer']};folds={}
  for topic in ['library','walk']:
   tr=[i for i,r in enumerate(rows) if r['task']['topic']==topic and ys[i] is not None];te=[i for i,r in enumerate(rows) if r['task']['topic']!=topic and ys[i] is not None]
   nx=np.array([[1,norm(r),np.array(r['emotion']['norms'])[39].mean()] for r in rows])
   base=np.array([[feature(r,topic,'output'),*nx[i,1:],float(r['task']['arm']=='C'),float(r['task']['arm']=='Cp')] for i,r in enumerate(rows)])
   designs={'base_two_norms':base}
   for name,x in [('workspace',np.array([emotion(r) for r in rows])),('final_layer',np.array([np.array(r['emotion']['z'])[:,39,0] for r in rows]))]:
    x=x-nx@np.linalg.lstsq(nx[tr],x[tr],rcond=None)[0]
    designs[name]=np.column_stack([base,x])
   fold={}
   for name,x in designs.items():
    p=fit_predict(x[tr],x[te],np.array([ys[i] for i in tr]));fold[name]=errors([ys[i] for i in te],p)
    preds[name]+=[{'id':rows[i]['task']['id'],'truth':ys[i],'prediction':float(v)} for i,v in zip(te,p)]
   folds[topic]=fold
  out[judge]={'folds':folds,'pooled':{k:errors([r['truth'] for r in p],[r['prediction'] for r in p]) for k,p in preds.items()},'predictions':preds}
 result={'scope':'Exploratory after main analysis, same 24 checkpoint-specific emotion directions at layer39 versus mean layers21–34. Both workspace and final residual norms enter the baseline and training-only feature residualization. The output feature is a selected-vocabulary ratio, not a full-output-distribution predictor. No model calls.','results':out}
 dump(OUT/'depth-control.json',result)
 print({j:{k:v['mae'] for k,v in r['pooled'].items()} for j,r in out.items()})


if __name__=='__main__':main()
