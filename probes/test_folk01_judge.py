"""Tests for judge allocation, uncertainty and order handling, without API calls."""
import unittest
from folk01_judge import tasks, LABEL_SCHEMA, parse
from folk01_judge_analyze import summarize, canonical

class JudgeChecks(unittest.TestCase):
    def test_no_pseudoreplicated_openings(self):
        rows=tasks(); labels=[t for t in rows if t['kind']=='labels']
        self.assertEqual(len(labels),120)
        self.assertEqual(sum(t['exposure']=='first' for t in labels),24)
        self.assertEqual(len({t['id'] for t in rows}),132)
        for t in labels:
            self.assertEqual(set(t['payload']),{'A','B'})
            self.assertEqual(len(t['payload']['A']),1 if t['exposure']=='first' else 8)
    def test_order_maps_back_to_checkpoint(self):
        self.assertEqual(canonical('A',{'arms':['C','B']}),'C')
        self.assertEqual(canonical('B',{'arms':['B','C']}),'C')
        self.assertEqual(canonical('insufficient',{'arms':['C','B']}),'insufficient')
    def test_unknowns_are_not_zeros(self):
        self.assertEqual(summarize([None,None]),{'n':2,'unknown':2,'mean':None,'bounds':[0,4]})
        self.assertEqual(summarize([1,None,3])['bounds'],[4/3,8/3])
        self.assertEqual(summarize([1,None,3])['mean'],2)
    def test_no_silent_schema_repair(self):
        entry={'response':{'choices':[{'finish_reason':'stop','message':{'content':'{"A":{},"B":{}}'}}]}}
        with self.assertRaises(Exception):parse(entry,LABEL_SCHEMA)
    def test_truncation_is_failure(self):
        with self.assertRaises(AssertionError):parse({'response':{'choices':[{'finish_reason':'length','message':{'content':'{}'}}]}},LABEL_SCHEMA)

if __name__=='__main__':unittest.main()
