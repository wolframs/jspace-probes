"""Leakage and reproducibility checks for the expression analysis."""
import copy
import json
import unittest
from express01_spec import ROOT,OUT
from express01_analyze import evaluate


class AnalysisChecks(unittest.TestCase):
 def test_test_labels_cannot_change_test_predictions(self):
  rows=[json.loads(p.read_text()) for p in sorted((OUT/'captures').glob('*.json'))]
  rows=[r for r in rows if r['task']['kind']=='archive']
  labels=json.loads((ROOT/'results/folk02/scores.json').read_text())
  vocab=json.loads((OUT/'vocabulary.json').read_text())
  original=json.loads((OUT/'analysis.json').read_text())['evaluation']
  altered=copy.deepcopy(labels)
  for r in altered:
   if r['topic']=='library':r['intensity']+=10
  changed=evaluate(rows,altered,vocab)
  for name,ps in original['predictions'].items():
   before={r['id']:r['prediction'] for r in ps if r['train_topic']=='walk'}
   after={r['id']:r['prediction'] for r in changed['predictions'][name] if r['train_topic']=='walk'}
   self.assertEqual(before,after,name)

 def test_sparse_scanner_matches_full_capture(self):
  data=json.loads((OUT/'scanner-benchmark.json').read_text())
  for r in data['rows']:
   case=r['id'].rsplit('-repeat',1)[0]
   full=json.loads((OUT/'captures'/f'{case}.json').read_text())
   self.assertEqual(r['prefix_ids'],full['prefix_ids'])
   for layer in ['21','24','28','32']:
    self.assertEqual(r['layers'][layer],full['layers'][layer])
   self.assertEqual(r['emotion'],full['emotion'])


if __name__=='__main__':unittest.main()
