"""Batch four-layer expression readouts, with no personality classification.

Input JSON: [{"id": "case", "user": "..."}] or rows with exact prefix_ids.
This sparse mode is instrument calibration; substantive generations use express01.py.
"""
import argparse
import json
import os
import time
import torch
import lab
from express01 import Reader,append_turn,residuals
from express01_spec import ROOT,OUT,ARMS,dump,digest


def scan(arm,batch,destination):
 torch.set_num_threads(6);torch.manual_seed(1709)
 rows=json.loads(batch.read_text());assert rows and len({r['id'] for r in rows})==len(rows)
 for r in rows:assert ('user' in r)^('prefix_ids' in r)
 lm=lab.get_model(ARMS[arm]);reader=Reader(lm,arm,json.loads((OUT/'vocabulary.json').read_text()))
 reader.layers=[21,24,28,32]
 output=[]
 for row in rows:
  ids=row.get('prefix_ids') or append_turn(lm.tok,[],row['user'],arm)
  assert ids and all(isinstance(t,int) and 0<=t<lm.model._lm_head.weight.shape[0] for t in ids)
  start=time.perf_counter();h,prefill=residuals(lm,ids,[-1]);result=reader.score(h)
  result.update(id=row['id'],prefix_ids=ids,prefill_seconds=prefill,scan_seconds=time.perf_counter()-start)
  output.append(result)
 dump(destination,{'arm':arm,'model':lab.CONFIGS[ARMS[arm]],'pid':os.getpid(),'vocabulary_sha256':digest(OUT/'vocabulary.json'),'batch_sha256':digest(batch),'layers':reader.layers,'scope':'read-only instrument calibration; no expression, personality or unavailable-capacity classifier','rows':output})
 print(f'Saved {len(rows)} four-layer scans to {destination}',flush=True)


if __name__=='__main__':
 from pathlib import Path
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--arm',choices=ARMS,required=True);p.add_argument('--batch',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args()
 scan(args.arm,args.batch,args.out)
