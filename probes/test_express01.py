"""No-model provenance checks for the frozen expression scan."""
import json
import unittest
import torch
from transformers import AutoTokenizer
from express01 import prepared_ids, history_ids, append_turn
from express01_spec import ROOT, OUT
import folk01


class ExpressionChecks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.spec=json.loads((OUT/'spec.json').read_text())
  cls.tok=AutoTokenizer.from_pretrained(*folk01.ARMS['B'][:1],revision=folk01.ARMS['B'][1],local_files_only=True)

 def test_archive_prefixes(self):
  rows=[t for t in self.spec['tasks'] if t['kind']=='archive']
  self.assertEqual(len(rows),84)
  for t in rows:
   cap=json.loads((ROOT/f'results/folk01/captures/{t["arm"]}-{t["topic"]}-{t["condition"]}.json').read_text())
   self.assertTrue(prepared_ids(cap,t['turn']))
   if t['turn']==1:self.assertEqual(append_turn(self.tok,[],cap['turns'][0]['user'],t['arm']),prepared_ids(cap,1))

 def test_history_roundtrip(self):
  for t in self.spec['tasks']:
   if t['kind']!='history' or t['arm']!='B' or t['user_warm']!=t['assistant_warm']:continue
   cap=json.loads((ROOT/f'results/folk01/captures/B-{t["topic"]}-{t["user_warm"]}{t["specificity"]}.json').read_text())
   self.assertEqual(history_ids(self.tok,t),prepared_ids(cap,5))

 def test_vocabulary_coverage(self):
  v=json.loads((OUT/'vocabulary.json').read_text())
  for topic in ['walk','library']:
   self.assertEqual(v[topic]['train_topic'],topic)
   self.assertGreater(len(v[topic]['selected']),0)
   target={x['word'] for x in v[topic]['selected']}
   for control in v[topic]['controls']:
    self.assertEqual(len(control),len(target))
    self.assertFalse(target&{x['word'] for x in control})

 def test_subset_mass_ratio(self):
  x=torch.tensor([1.,2.,-4.,10.,0.]);a=torch.tensor([0,1]);b=torch.tensor([2,4]);w=torch.tensor([.3,.7]);p=x.softmax(0)
  full=torch.log((p[a]*w).sum()/(p[b]*w).sum())
  partial=torch.logsumexp(x[a]+w.log(),0)-torch.logsumexp(x[b]+w.log(),0)
  torch.testing.assert_close(full,partial)


if __name__=='__main__':unittest.main()
