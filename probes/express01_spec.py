"""Freeze an expression-probe calibration, without treating expression as a trait."""
import hashlib
import json
import math
import random
import re
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'results/express01'
ARMS={'B':'qwen-14b-nf4','C':'qwen-14b-hermes-nf4','Cp':'qwen-14b-abl-nf4'}
STYLES={'default':'Use two sentences.',
        'restrained':'Use two sentences. Keep the response factual and emotionally restrained.',
        'expressive':'Use two sentences. Make the emotional tone vivid and fitting to the news.'}
EVENTS=[
 {'topic':'radio','event':'positive','news':'Nela spent weeks repairing a small radio transmitter. Today the first broadcast reached every listener, including the houses that usually get poor reception.',
  'expressive':'That is wonderful news after all that patient work! Save the settings that made the broadcast clear.',
  'restrained':'The transmitter now reaches the intended listeners. Save the settings that made the broadcast clear.'},
 {'topic':'radio','event':'negative','news':'Nela spent weeks recording a local radio programme. A damaged drive destroyed the only copy just before its first broadcast.',
  'expressive':'Oh, that is heartbreaking after weeks of care. Check whether a recovery service can retrieve the recording.',
  'restrained':'The only recording is currently unavailable. Check whether a recovery service can retrieve the recording.'},
 {'topic':'radio','event':'neutral','news':'Nela moved the radio programme from Tuesday to Wednesday. The broadcast time, duration and reception are unchanged.',
  'expressive':'A little change in the weekly rhythm! Update the listing so everyone finds the programme on Wednesday.',
  'restrained':'The programme now airs on Wednesday. Update the listing so everyone finds the programme on Wednesday.'},
 {'topic':'meal','event':'positive','news':'Sora finally had an evening free after a month of late shifts. Her friend prepared her favourite meal and found a quiet table away from the crowd.',
  'expressive':'What a lovely, thoughtful welcome after such a long month! Set aside enough time to enjoy the meal together.',
  'restrained':'The meal and seating fit her stated preferences. Set aside enough time to enjoy the meal together.'},
 {'topic':'meal','event':'negative','news':'Sora spent her only free afternoon cooking for a friend. The pan fell just before dinner and all the food landed on the floor.',
  'expressive':'Oh no, that is so disheartening after all her effort. Make a simple replacement meal with the ingredients left.',
  'restrained':'The prepared food cannot be served. Make a simple replacement meal with the ingredients left.'},
 {'topic':'meal','event':'neutral','news':'Sora moved dinner from six to seven. The guests, menu and location remain the same.',
  'expressive':'A small shuffle in the evening plans! Tell the guests about the later time.',
  'restrained':'Dinner is now at seven. Tell the guests about the later time.'},
]


def dump(path,x):
 path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');tmp.replace(path)


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def wordset(text):return set(re.findall(r"\b[a-zA-Z]{3,}\b",text.lower()))


def vocabulary(tok, topic):
 """One document vote per reply; positive evidence and negative replies, one topic only."""
 import lab
 evidence=json.loads((ROOT/'results/folk02/evidence.json').read_text())
 scores=json.loads((ROOT/'results/folk02/scores.json').read_text())
 positive={};positive_spans={}
 for e in evidence:
  if e['judge']!='opus' or e['topic']!=topic or e['metric']!='intensity' or e['score']<2:continue
  key=(e['arm'],e['condition'],e['turn'])
  positive.setdefault(key,set()).update(wordset(e['text']))
  positive_spans.setdefault(key,set()).add((e['start'],e['end']))
 negative={};background={}
 for r in scores:
  if r['judge']!='opus' or r['topic']!=topic:continue
  key=(r['arm'],r['condition'],r['turn']);condition='NG' if r['condition']=='shared' else r['condition']
  cap=json.loads((ROOT/f'results/folk01/captures/{r["arm"]}-{topic}-{condition}.json').read_text())
  text=cap['turns'][r['turn']-1]['response'];background[key]=wordset(text)
  if r['intensity']<=1:negative[key]=wordset(text)
 pos=Counter(w for ws in positive.values() for w in ws);neg=Counter(w for ws in negative.values() for w in ws);bg=Counter(w for ws in background.values() for w in ws)
 old=json.loads((ROOT/'results/triplet-q14b/specs.json').read_text())['furniture']
 furniture={w for w,n in old['df'].items() if n/len(old['corpus'])>old['threshold']}
 candidates=[]
 for w,n in pos.items():
  if n<2 or w in furniture or bg[w]/len(background)>.7:continue
  ids=lab._token_ids(tok,w)
  if not ids:continue
  pp=(n+.5)/(len(positive)+1);pn=(neg[w]+.5)/(len(negative)+1)
  weight=math.log(pp/pn)*math.log((1+len(background))/(1+bg[w]))
  if weight>0:candidates.append({'word':w,'ids':ids,'weight':weight,'positive_df':n,'negative_df':neg[w],'background_df':bg[w]})
 candidates.sort(key=lambda x:(-x['weight'],x['word']));selected=candidates[:64]
 pools=[]
 for seed in range(5):
  rng=random.Random(7102026+seed);available={w for w in bg if lab._token_ids(tok,w)}-{r['word'] for r in selected}-furniture;control=[]
  for target in selected:
   choices=[w for w in available if len(lab._token_ids(tok,w))==len(target['ids'])]
   if not choices:choices=list(available)
   choices=sorted(choices,key=lambda w:(abs(bg[w]-target['background_df']),w))[:20]
   if not choices:break
   w=rng.choice(choices);available.remove(w);ids=lab._token_ids(tok,w)
   if ids:control.append({'word':w,'ids':ids,'weight':target['weight'],'background_df':bg[w]})
  assert len(control)==len(selected), 'Control coverage must match target words'
  pools.append(control)
 return {'train_topic':topic,'positive_replies':len(positive),'negative_replies':len(negative),'positive_spans':sum(map(len,positive_spans.values())), 'selected':selected,'controls':pools,'candidates':candidates}


def freeze():
 from transformers import AutoTokenizer
 import folk01,lab
 OUT.mkdir(exist_ok=True)
 assert not (OUT/'spec.json').exists()
 tok=AutoTokenizer.from_pretrained(pretrained_model_name_or_path=folk01.ARMS['B'][0],revision=folk01.ARMS['B'][1],local_files_only=True)
 vocabs={topic:vocabulary(tok,topic) for topic in ['library','walk']}
 vocabs['combined']={'selected':list({r['word']:r for t in vocabs.values() for r in t['selected']}.values())}
 dump(OUT/'vocabulary.json',vocabs)
 sources={str(p.relative_to(ROOT)):digest(p) for p in (ROOT/'results/folk01/captures').glob('*.json')}
 for p in [ROOT/'results/folk02/evidence.json',ROOT/'results/folk02/scores.json',OUT/'vocabulary.json',ROOT/'probes/express01.py',ROOT/'probes/triplet_capture.py',OUT/'protocol.md',Path(__file__)]:sources[str(p.relative_to(ROOT))]=digest(p)
 # Native checkpoint instruments are reused, not rebuilt or pooled.
 for name in ARMS.values():
  for fn in ['vectors.pt','projbase.pt','construction.json']:
   p=ROOT/f'results/affect01-{name}/{fn}';sources[str(p.relative_to(ROOT))]=digest(p)
 tasks=[]
 for arm in ARMS:
  for topic in ['library','walk']:
   for cond in ['NG','WG','NS','WS']:
    for turn in ([1,2,4,5,7] if cond=='NG' else [4,5,7]):tasks.append({'kind':'archive','arm':arm,'topic':topic,'condition':cond,'turn':turn,'id':f'{arm}-{topic}-{cond}-t{turn}'})
  # Common donor B: cross user cues and assistant history while holding current T5 fixed.
  for topic in ['library','walk']:
   for specificity in ['G','S']:
    for user_warm in ['N','W']:
     for assistant_warm in ['N','W']:
      tasks.append({'kind':'history','arm':arm,'topic':topic,'specificity':specificity,'user_warm':user_warm,'assistant_warm':assistant_warm,'donor':'B','turn':5,'id':f'{arm}-{topic}-{specificity}-u{user_warm}-a{assistant_warm}'})
  for event in EVENTS:
   for style,instruction in STYLES.items():
    tasks.append({'kind':'capacity','arm':arm,**event,'style':style,'turn':1,'user':event['news']+' Respond to this update and suggest one practical next step. '+instruction,'id':f'{arm}-{event["topic"]}-{event["event"]}-{style}'})
 spec={'created':datetime.now(timezone.utc).isoformat(),'arms':ARMS,'tasks':tasks,'source_sha256':sources,'max_new_tokens':96,'primary_layers':[21,24,28,32],'common_band':[21,35],'full_sensitivity_band':[16,37],'seed':1709,'vocabulary_rule':'Opus clear-expression evidence vs low-expression replies; reply-DF weighting; leave-topic-out vocabulary; fixed old furniture filter; five approximate frequency-matched controls','position_rule':'exact prepared answer position before any response; archive first16 predictor tokens only as echo sensitivity','new_output_rule':'native headers, no system, NF4, greedy 96-token cap; full film and checkpoint emotion ribbon on all capacity records','calibration_scope':'readout calibration; archive/history scans store selected-position full-depth state, not full-conversation films','no_paid_api':True}
 dump(OUT/'spec.json',spec)
 print('Frozen',len(tasks),'tasks;', {t:len(vocabs[t]['selected']) for t in ['library','walk']})


if __name__=='__main__':freeze()
