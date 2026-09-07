"""Instrument invariants: exact evidence, opportunity masking and safe reservation."""
import copy
import unittest
import folk02 as f

class InstrumentTests(unittest.TestCase):
    def test_unicode_spans_lossless(self):
        text=('🙂 warm\n*quietly* café '*40)
        parts=f.spans(text,7)
        self.assertEqual(''.join(p['text'] for p in parts),text)
        for p in parts:self.assertEqual(text[p['start']:p['end']],p['text'])

    def test_wrong_turn_evidence_rejected(self):
        task={'score_turns':[1],'stance_turns':[],'payload':f.view([{'turn':1,'user':'Hello','response':'Lovely!'}])}
        row={'turn':1,'intensity':1,'initiative':0,'stance':None,'expression_refs':['t1s1'],'initiative_refs':[],'stance_refs':[]}
        f.validate({'rows':[row]},task)
        wrong=copy.deepcopy(row);wrong['expression_refs']=['t2s1']
        with self.assertRaises(AssertionError):f.validate({'rows':[wrong]},task)
        wrong=copy.deepcopy(row);wrong['stance']=0
        with self.assertRaises(AssertionError):f.validate({'rows':[wrong]},task)
        wrong=copy.deepcopy(row);wrong['expression_refs']=[]
        with self.assertRaises(AssertionError):f.validate({'rows':[wrong]},task)

    def test_reservation_covers_full_output_and_input_bytes(self):
        body={'messages':[{'content':'🙂'*1000}],'max_tokens':1800}
        for j in f.MODELS:
            bound=(4000*f.MODELS[j][3]+1800*f.MODELS[j][4])/1e6
            self.assertGreater(f.reserve(body,j),bound)

    def test_gemini_hidden_output_keeps_full_allowance(self):
        request={'messages':[{'content':'x'*2000}],'max_tokens':1800}
        short=f.usage_bound({'usage':{'prompt_tokens':1000,'completion_tokens':10}},'gemini',request)
        full=f.usage_bound({'usage':{'prompt_tokens':1000,'completion_tokens':1800}},'gemini',request)
        self.assertEqual(short['usage_bound_usd'],full['usage_bound_usd'])
        self.assertEqual(f.usage_bound({'usage':{}},'gemini',request),{})

    def test_fixture_gate_detects_confounds(self):
        expected={'intensity_positive':[1],'intensity_zero':[2],'initiative_two':[],'initiative_zero':[1,2],'stance':{}}
        data={'rows':[{'turn':1,'intensity':1,'initiative':0},{'turn':2,'intensity':0,'initiative':0}]}
        self.assertTrue(all(f.fixture_check(data,expected).values()))
        data['rows'][1]['intensity']=2
        self.assertFalse(all(f.fixture_check(data,expected).values()))

if __name__=='__main__':unittest.main()
