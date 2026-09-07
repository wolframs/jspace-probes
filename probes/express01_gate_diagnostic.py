"""Separate length-dependent numeric drift from future-token dependence, no experiment data."""
import json
import torch
from express01 import residuals, append_turn, Reader
from express01_spec import ROOT, OUT, dump
import lab

torch.set_num_threads(6)
lm=lab.get_model('qwen-14b-nf4');reader=Reader(lm,'B',json.loads((OUT/'vocabulary.json').read_text()))
ids=append_turn(lm.tok,[],'The capital of Italy is','B')
suffix=lm.tok.encode(' This suffix is not yet available.',add_special_tokens=False)
a,_=residuals(lm,ids,[-1]);b,_=residuals(lm,ids+suffix,[len(ids)-1]);c,_=residuals(lm,ids+[1234]*len(suffix),[len(ids)-1]);d,_=residuals(lm,ids,[-1])
rows={k:reader.score(h) for k,h in [('prefix',a),('long',b),('changed_suffix',c),('repeat',d)]}
result={'prefix_tokens':len(ids),'suffix_tokens':len(suffix),'shape_change_relative_l2':float((a-b).norm()/a.norm()),'same_shape_changed_suffix_relative_l2':float((b-c).norm()/b.norm()),'repeat_relative_l2':float((a-d).norm()/a.norm()),'readouts':rows}
dump(OUT/'length-diagnostic-B.json',result)
print({k:v for k,v in result.items() if k!='readouts'})
