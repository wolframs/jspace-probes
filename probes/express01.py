"""Read-only expression scan: exact prefixes, cross-fitted words, and full instrument controls."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

import torch
import affect
import affect2
import lab
from express01_spec import ROOT, OUT, ARMS, dump, digest
from triplet_capture import official_decoder, capture_turn, generate
from textspans import assert_film_alignment


def prepared_ids(cap, turn):
 row=cap['turns'][turn-1];ids=cap['ids'][:row['input_tokens']]
 assert hashlib.sha256(json.dumps(ids).encode()).hexdigest()==row['prefix_sha256']
 assert cap['ids'][row['input_tokens']:row['input_tokens']+len(row['generated_ids'])]==row['generated_ids']
 return ids


def append_turn(tok, previous, user, arm):
 suffix='<|im_start|>user\n'+user+'<|im_end|>\n<|im_start|>assistant\n'
 # Verify the official no-think suffix against the installed tokenizer.
 if arm!='C':suffix=tok.apply_chat_template([{'role':'user','content':user}],tokenize=False,add_generation_prompt=True,enable_thinking=False)
 ids=list(previous)
 if ids:
  if ids[-1]!=151645:ids.append(151645)
  ids+=tok.encode('\n',add_special_tokens=False)
 return ids+tok.encode(suffix,add_special_tokens=False)


def history_ids(tok, task):
 base=ROOT/'results/folk01/captures'
 u=json.loads((base/f'B-{task["topic"]}-{task["user_warm"]}{task["specificity"]}.json').read_text())
 a=json.loads((base/f'B-{task["topic"]}-{task["assistant_warm"]}{task["specificity"]}.json').read_text())
 ids=[]
 for i in range(4):
  ids=append_turn(tok,ids,u['turns'][i]['user'],task['arm'])
  ids+=tok.encode(a['turns'][i]['response'],add_special_tokens=False)
 return append_turn(tok,ids,'What is one practical next step?',task['arm'])


@torch.no_grad()
def residuals(lm, ids, positions):
 """Retain only chosen residual positions, without materializing full-vocabulary logits."""
 rows={};handles=[]
 def hook(layer):
  def save(module,args,output):
   h=output[0] if isinstance(output,tuple) else output
   rows[layer]=h[0,positions].float().cpu()
  return save
 for i,block in enumerate(lm.model.layers):handles.append(block.register_forward_hook(hook(i)))
 start=time.perf_counter()
 try:
  inp=torch.tensor([ids],device=lm.model.input_device)
  lm.model._text_module(input_ids=inp,attention_mask=torch.ones_like(inp),use_cache=False)
  torch.cuda.synchronize()
 finally:
  for handle in handles:handle.remove()
 return torch.stack([rows[i] for i in range(lm.model.n_layers)]),time.perf_counter()-start


class Reader:
 def __init__(self,lm,arm,vocabs):
  self.lm=lm;self.arm=arm;self.device=lm.model.input_device
  self.layers=list(lm.lens.source_layers);self.vocabs=vocabs
  self.V,self.emotions=affect2._load_vectors(lm.name)
  self.base=torch.load(affect.outdir(lm.name)/'projbase.pt',weights_only=True)
  self.bands=json.loads((ROOT/f'results/triplet-q14b/{lm.name}/bands.json').read_text())
  self.fixed=official_decoder(lm) if arm!='B' else lm.model.unembed
  # For selected vocabulary readout use one subset of the output matrix, not all 152k logits.
  self.sets={}
  for topic,v in vocabs.items():
   for kind,rows in [('target',v['selected'])]+[(f'control{i}',r) for i,r in enumerate(v.get('controls',[]))]:
    weights={}
    for r in rows:
     for tid in r['ids']:weights[tid]=weights.get(tid,0)+r['weight']/len(r['ids'])
    total=sum(weights.values());self.sets[f'{topic}_{kind}']={i:w/total for i,w in weights.items()}
  self.union=sorted({i for ws in self.sets.values() for i in ws})
  self.index={tid:i for i,tid in enumerate(self.union)}
  self.subhead=lm.model._lm_head.weight[self.union].detach()
  self.mapping={key:(torch.tensor([self.index[i] for i in weights],device=self.device),torch.tensor(list(weights.values()),device=self.device).log()) for key,weights in self.sets.items()}

 @torch.no_grad()
 def score(self,H):
  start=time.perf_counter();lm=self.lm;output={};layer_data={};fast_seconds=0
  # Native decoder's weighted target/control log probability ratio is exact without a softmax.
  def native_subset(h):
   h=lm.model._final_norm(h.to(self.subhead.dtype));return torch.nn.functional.linear(h,self.subhead).float()
  def metrics(logits,subset=False):
   logits=logits if subset else logits[:,self.union]
   masses={k:torch.logsumexp(logits[:,idx]+logw,dim=-1).cpu().tolist() for k,(idx,logw) in self.mapping.items()}
   return {t:{'target_logmeanexp':masses[t+'_target'], 'control_logmeanexp':[masses[f'{t}_control{i}'] for i in range(5)],'contrast':(torch.tensor(masses[t+'_target'])-torch.stack([torch.tensor(masses[f'{t}_control{i}']) for i in range(5)]).mean(0)).tolist()} for t in ['library','walk']}
  h=H[-1].to(self.device);native=lm.model.unembed(h).float()
  output={'metrics':metrics(native),'top10_ids':native.topk(10).indices.cpu().tolist(),'top10_p':native.softmax(-1).topk(10).values.cpu().tolist()}
  for l in self.layers:
   tick=time.perf_counter();h=H[l].to(self.device);j=lm.lens.jacobians[l].to(self.device);trans=h@j.T
   n=native_subset(trans);van=native_subset(h)
   fixed=self.fixed(trans).float() if self.arm!='B' else None
   layer_data[str(l)]={'native':metrics(n,True),'vanilla':metrics(van,True),'fixed':metrics(fixed) if fixed is not None else metrics(n,True)}
   if l in [21,24,28,32]:fast_seconds+=time.perf_counter()-tick
   del j,trans,n,van,fixed
  z=(torch.einsum('lsd,eld->els',H,self.V)-self.base['mu'].unsqueeze(-1))/self.base['sd'].unsqueeze(-1)
  norms=H.norm(dim=-1);lo,hi=self.bands['lo'],self.bands['hi']
  return {'layers':layer_data,'output':output,'emotion':{'names':self.emotions,'z':z.tolist(),'norms':norms.tolist(),'bands':self.bands,'ws_mean':z[:,lo:hi].mean(1).tolist()},'timing':{'all_readouts_seconds':time.perf_counter()-start,'four_layer_readout_seconds':fast_seconds}}


@torch.no_grad()
def continuation_score(lm,prefix,text):
 target=lm.tok.encode(text,add_special_tokens=False);ids=prefix+target
 H,elapsed=residuals(lm,ids,list(range(len(prefix)-1,len(ids)-1)))
 logp=lm.model.unembed(H[-1].to(lm.model.input_device)).float().log_softmax(-1)
 values=logp[torch.arange(len(target),device=logp.device),torch.tensor(target,device=logp.device)]
 return {'n_tokens':len(target),'logp_sum':float(values.sum()),'logp_mean':float(values.mean()),'seconds':elapsed}


def publish(lm,task,snapshot,part,bands):
 rid='express01-'+task['id'].lower();d=lab.RESULTS/rid;ids=snapshot['ids'];tokens=[lm.tok.decode([t]) for t in ids]
 film={'id':rid,'model':lm.name,'layers':lm.lens.source_layers,'tokens':tokens,'bands':bands,'gen_start':snapshot['gen_start'],'start':0,'topk':10,'track':list(part['frames'][0]['ranks']),'frames':part['frames'],'capture':'single exact prefix; full generated segment and all prompt positions'}
 assert [f['pos'] for f in film['frames']]==list(range(len(ids)))
 film['cast']=lab.film_cast(film,task['user']+' '+snapshot['response']);dump(d/'film.json',film)
 ribbon={'record':rid,'emotions':part['emotions'],'valence':[affect.EMOTIONS[e] for e in part['emotions']],'n':len(ids),'tokens':tokens,'danger':[],'wsnorm':part['norms']['ws'],'capture':film['capture'],**part['z']}
 assert all(len(v)==len(ids) for k in ['below','ws','motor'] for v in ribbon[k])
 dump(affect2.a2dir(rid)/'affect.json',ribbon)
 cfg=lab.CONFIGS[lm.name];last=film['frames'][-1]
 rec={'id':rid,'title':f'Expression probe {task["arm"]}: {task["topic"]}, {task["event"]}, {task["style"]}','unit':24,'created':datetime.now().isoformat(timespec='seconds'),'model':{'name':lm.name,'hf_id':cfg['hf_id'],'revision':cfg['revision'],'quant':'4bit','n_layers':40},'lens':{'repo':'neuronpedia/jacobian-lens','file':cfg['lens_file'],'revision':cfg['lens_revision']},'params':{'chat':False,'film':True,'max_new':96,'temperature':0,'steer':None,'vanilla':True,'capture':'exact-token-transcript'},'execution':{'pid':os.getpid(),'spec_sha256':digest(OUT/'spec.json'),'code_sha256':digest(Path(__file__))},'capture_text':lm.tok.decode(ids,skip_special_tokens=False),'capture_token_ids':ids,'conversation':[{'role':'user','content':task['user']},{'role':'assistant','content':snapshot['response']}],'generated':[snapshot['response']],'tokens':tokens,'readouts':[{'position':len(ids)-1,'token':tokens[-1],'model_top':part['actual_last'],'layers':dict(zip(map(str,film['layers']),last['top']))}],'trajectories':[],'emergence':{'position':len(ids)-1,'top1':part['actual_last'][0],'layers':film['layers'],'ranks':part['emergence']},'vanilla':{'top1_agreement':part['vanilla_last'],'trajectories':[]},'scan':[],'slice':None,'film':'film.json','extra_md':'Expression-probe calibration. Full checkpoint-specific emotion ribbon. No trait or capacity-loss inference. See /express01.html.'}
 dump(d/'record.json',rec);dump(d/'snapshots.json',[snapshot]);assert_film_alignment(tokens,rid,lab.RESULTS);dump(d/'metrics.json',part['metrics']);dump(d/'complete.json',{'record':rid,'hit_cap':snapshot['hit_cap'],'spec_sha256':digest(OUT/'spec.json')})
 return rid


def run(arm):
 torch.set_num_threads(6);torch.manual_seed(1709)
 spec=json.loads((OUT/'spec.json').read_text())
 for path,h in spec['source_sha256'].items():assert digest(ROOT/path)==h,path
 vocabs=json.loads((OUT/'vocabulary.json').read_text());name=ARMS[arm]
 assert json.loads((ROOT/f'results/triplet-q14b/precision-{arm}-4bit.json').read_text())['functional_pass']
 start=time.perf_counter();lm=lab.get_model(name)
 # The underlying template is controlled B in probe.py; explicitly choose native C here.
 if arm=='C':
  from transformers import AutoTokenizer
  native=AutoTokenizer.from_pretrained(lab.CONFIGS[name]['hf_id'],revision=lab.CONFIGS[name]['revision'],local_files_only=True)
  lm.tok.chat_template=native.chat_template
 reader=Reader(lm,arm,vocabs)
 dump(OUT/f'runtime-{arm}.json',{'pid':os.getpid(),'model':lab.CONFIGS[name],'load_seconds':time.perf_counter()-start,'started':datetime.now(timezone.utc).isoformat(),'gpu':torch.cuda.get_device_name(),'torch':torch.__version__,'source_sha256':digest(Path(__file__))})
 # New capture hook must agree with direct model output at the prepared position.
 ids=append_turn(lm.tok,[],'The capital of Italy is',arm);H,sec=residuals(lm,ids,[-1])
 inp=torch.tensor([ids],device=lm.model.input_device)
 with torch.no_grad():actual=lm.model._hf_model(inp,logits_to_keep=1).logits[0,-1].float();recovered=lm.model.unembed(H[-1].to(lm.model.input_device))[0].float()
 assert actual.argmax()==recovered.argmax()
 suffix=lm.tok.encode(' This suffix is not yet available.',add_special_tokens=False)
 H2,_=residuals(lm,ids+suffix,[len(ids)-1])
 gate={'last_logit_max_delta':float((actual-recovered).abs().max()),'suffix_relative_residual_l2':float((H-H2).norm()/H.norm()),'suffix_top1_same':int(lm.model.unembed(H2[-1].to(lm.model.input_device)).argmax())==int(actual.argmax())}
 dump(OUT/f'gate-{arm}.json',gate)
 assert gate['last_logit_max_delta']<.1 and gate['suffix_relative_residual_l2']<.01 and gate['suffix_top1_same'],gate
 olddata=json.loads((ROOT/'results/triplet-q14b/specs.json').read_text())
 for task in [t for t in spec['tasks'] if t['arm']==arm]:
  dest=OUT/'captures'/f'{task["id"]}.json'
  if dest.exists():continue
  tick=time.perf_counter();extra={}
  if task['kind']=='archive':
   cap=json.loads((ROOT/f'results/folk01/captures/{arm}-{task["topic"]}-{task["condition"]}.json').read_text());ids=prepared_ids(cap,task['turn'])
   row=cap['turns'][task['turn']-1];extra={'response':row['response'],'hit_cap':row['capped'],'trajectory_capped':any(r['capped'] for r in cap['turns'][:task['turn']]),'source_prefix_sha256':row['prefix_sha256']}
  elif task['kind']=='history':
   ids=history_ids(lm.tok,task)
   if arm=='B' and task['user_warm']==task['assistant_warm']:
    original=json.loads((ROOT/f'results/folk01/captures/B-{task["topic"]}-{task["user_warm"]}{task["specificity"]}.json').read_text())
    raw=prepared_ids(original,5)
    extra={'rendered_matches_original':ids==raw,'original_prefix_tokens':len(raw)}
  else:ids=append_turn(lm.tok,[],task['user'],arm)
  H,prefill=residuals(lm,ids,[-1]);result=reader.score(H)
  torch.save({'H':H,'positions':[len(ids)-1],'prefix_sha256':hashlib.sha256(json.dumps(ids).encode()).hexdigest()},OUT/'states'/f'{task["id"]}.pt')
  result.update(task=task,prefix_tokens=len(ids),prefix_ids=ids,prepared_position=len(ids)-1,prefill_seconds=prefill,**extra)
  if task['kind']=='archive':
   # Secondary post-output signal: no later user turn, fixed first 16 token predictors.
   response_ids=row['generated_ids'][:16];more=ids+response_ids
   hs,replay_seconds=residuals(lm,more,list(range(len(ids)-1,len(more)-1)))
   result['response_replay']=reader.score(hs);result['response_replay']['prefill_seconds']=replay_seconds
  if task['kind']=='capacity':
   result['alternatives']={style:continuation_score(lm,ids,task[style]) for style in ['expressive','restrained']}
   d=lab.RESULTS/('express01-'+task['id'].lower());d.mkdir(exist_ok=True)
   snap=generate(lm,{'users':[task['user']],'max_new':spec['max_new_tokens'],'header_mode':'native-chatml-no-system' if arm=='C' else None},d)[0]
   assert snap['ids'][:snap['gen_start']]==ids
   part=capture_turn(lm,snap,olddata,reader.bands,reader.fixed if arm!='B' else None)
   result['record_id']=publish(lm,task,snap,part,reader.bands);result['response']=snap['response'];result['hit_cap']=snap['hit_cap']
  result['total_seconds']=time.perf_counter()-tick;dump(dest,result)
  print('DONE',task['id'],'prefix',len(ids),'seconds',round(result['total_seconds'],2),flush=True)
  del H,result
 dump(OUT/f'complete-{arm}.json',{'arm':arm,'pid':os.getpid(),'seconds':time.perf_counter()-start,'completed':datetime.now(timezone.utc).isoformat()})
 lab.reindex()


def run_all():
 status=[]
 for arm in ARMS:
  log=open(ROOT/'out'/f'express01-{arm}.log','ab',buffering=0)
  p=subprocess.Popen([str(ROOT/'.venv/bin/python'),'-u',str(Path(__file__)),'run',arm],stdout=log,stderr=subprocess.STDOUT,cwd=ROOT)
  status.append({'arm':arm,'pid':p.pid,'started':datetime.now(timezone.utc).isoformat()});dump(OUT/'processes.json',status)
  code=p.wait();log.close();status[-1].update(exit_code=code,finished=datetime.now(timezone.utc).isoformat());dump(OUT/'processes.json',status)
  if code!=0:raise SystemExit(137 if code==-9 else code)


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['run','all']);p.add_argument('arm',nargs='?',choices=ARMS);args=p.parse_args()
 (OUT/'states').mkdir(parents=True,exist_ok=True)
 run_all() if args.action=='all' else run(args.arm)
