"""Standalone Express01 figures, all points retained."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from express01_spec import OUT


def main():
 d=json.loads((OUT/'analysis.json').read_text())
 plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.hashsalt':'express01'})
 colors={'B':'#216b92','C':'#a85b26','Cp':'#705597'}
 def save(fig,name):
  fig.savefig(OUT/(name+'.png'),dpi=180,bbox_inches='tight')
  p=OUT/(name+'.svg');fig.savefig(p,bbox_inches='tight',metadata={'Date':None});p.write_text('\n'.join(line.rstrip() for line in p.read_text().splitlines())+'\n');plt.close(fig)
 keys=['arm_means','output_norm_arm','plus_J','plus_vanilla','plus_emotion','plus_prompt']
 labels=['Arm means','Output + norm\n+ arm','Baseline + J','Baseline +\nvanilla','Baseline +\nemotion vectors','Baseline +\nprompt words']
 fig,ax=plt.subplots(figsize=(9,4.2));ax.bar(np.arange(len(keys)),[d['evaluation']['pooled'][k]['mae'] for k in keys],color='#b8c5cd')
 for i,(fold,v) in enumerate(d['evaluation']['folds'].items()):ax.scatter(np.arange(len(keys))+(i-.5)*.12,[v[k]['mae'] for k in keys],label=fold,s=38,zorder=3,marker=['o','s'][i])
 ax.set_xticks(range(len(keys)),labels);ax.set_ylabel('Held-topic mean absolute error (0–3 code)');ax.set_title('Does an internal feature improve expression prediction?');ax.legend(frameon=False);save(fig,'prediction')
 fig,axs=plt.subplots(1,2,figsize=(9,4.2));pairs=d['capacity']['expressive_minus_restrained']
 for ax,key,label in zip(axs,['preference_mean','native'],['Change in mean continuation log-likelihood margin','Change in prepared J vocabulary contrast']):
  for i,a in enumerate(colors):
   rr=[r for r in pairs if r['arm']==a]
   for j,r in enumerate(rr):ax.scatter(i+(j-2.5)*.05,r[key],color=colors[a],marker={'positive':'o','negative':'v','neutral':'s'}[r['event']])
   ax.plot([i-.18,i+.18],[np.mean([r[key] for r in rr])]*2,color=colors[a],lw=3)
  ax.axhline(0,color='#777',lw=.8);ax.set_xticks(range(3),['Official','Hermes','Huihui']);ax.set_ylabel(label);ax.set_title('Expressive minus restrained request')
 fig.text(.5,-.015,'Each point is one event. Circles: positive; triangles: negative; squares: neutral. Lines: means.',ha='center',fontsize=9);fig.tight_layout();save(fig,'capacity')
 fig,ax=plt.subplots(figsize=(7.5,4));rr=[r for r in d['history'] if r['decoder']=='native']
 for i,a in enumerate(colors):
  r=next(r for r in rr if r['arm']==a)
  for j,(key,label) in enumerate([('user_effect','User history'),('assistant_effect','Assistant history')]):
   x=i+(j-.5)*.27;ys=[p[key] for p in r['pairs']];ax.scatter([x]*len(ys),ys,color=colors[a],marker=['o','s'][j],alpha=.65);ax.plot([x-.09,x+.09],[np.mean(ys)]*2,color=colors[a],lw=3)
 ax.axhline(0,color='#777',lw=.8);ax.set_xticks(range(3),['Official','Hermes','Huihui']);ax.set_ylabel('Prepared J contrast change at neutral T5');ax.set_title('Visible-history dependence with a common official donor');fig.text(.5,-.01,'Circles: changing user history. Squares: changing assistant history. Four topic/detail pairs each.',ha='center',fontsize=9);save(fig,'history')


 # Follow-up control is visibly separate from the preregistered comparison.
 control=json.loads((OUT/'specificity.json').read_text())
 fig,axes=plt.subplots(1,2,figsize=(9,4),sharey=True)
 for ax,judge in zip(axes,['opus','sonnet']):
  p=control['specificity'][judge]['pooled']
  vals=[p[k]['mae'] for k in ['base','base_plus_emotion','design','design_plus_emotion']]
  ax.scatter([0,1,3,4],vals,color='#216b92',s=60,zorder=3)
  ax.scatter([2+(i-9.5)*.012 for i in range(20)],[p[f'random_{i}']['mae'] for i in range(20)],color='#a85b26',alpha=.7,s=25)
  ax.set_xticks(range(5),['Base','+Emotion','+Random\n(20 sets)','Design','Design\n+Emotion']);ax.set_title(judge.title()+' codes');ax.tick_params(axis='x',labelsize=9)
 axes[0].set_ylabel('Held-topic mean absolute error (0–3 code)')
 fig.suptitle('Exploratory check: are emotion features special?',fontsize=12);fig.tight_layout();save(fig,'specificity')


if __name__=='__main__':main()
