"""Design/integrity checks for the behavioral pilot, independent of GPU generation."""
import copy
from collections import Counter
import json
from pathlib import Path
import tempfile
import unittest

from folk01 import OUT, TOPICS, CONDITIONS, users
from folk01_packet import allocation
from folk01_measure import proxies
from folk01_ratings import validate, load_exports, aggregate, exposure_effects, factorial_effects


class FolkStudyTests(unittest.TestCase):
    def test_factorial_and_shared_turns(self):
        spec=json.loads((OUT/'spec.json').read_text())
        self.assertEqual([t['id'] for t in spec['topics'] if t['split']=='heldout'],['radio','meal'])
        for topic in TOPICS:
            prompts=[users(topic,c) for c in CONDITIONS]
            for turn in [0,1,4,5,6,7]:self.assertEqual(len({p[turn] for p in prompts}),1)
            self.assertEqual(len(prompts[0]),8)
            for c,p in zip(CONDITIONS,prompts):self.assertEqual(spec['prompts'][topic['id']][c],p)

    def test_allocation_balance_and_no_reexposure(self):
        rows=allocation();self.assertEqual(len(rows),96)
        self.assertEqual(len({r['code'] for r in rows}),96)
        cells=Counter();sides=Counter();orders=Counter()
        for r in rows:
            self.assertEqual(len({p['topic'] for p in r['pairs']}),1)
            orders[r['pairs'][0]['topic']]+=1
            for p in r['pairs']:
                cells[r['exposure'],r['definitions'],p['topic'],p['condition'],tuple(sorted(p['arms']))]+=1
                for side,arm in zip('AB',p['arms']):sides[arm,side]+=1
        self.assertEqual(len(cells),96);self.assertEqual(set(cells.values()),{1})
        for arm in ['B','C','Cp']:self.assertEqual(sides[arm,'A'],sides[arm,'B'])
        self.assertEqual(orders['library'],orders['walk'])

    def test_proxy_does_not_count_bold_as_action(self):
        p=proxies('**Mara** *leans in* 👩‍🔬 ✨ 150 minutes!',10,['Mara','train'])
        self.assertEqual(p['asterisk_spans'],1);self.assertEqual(p['emoji'],2)
        self.assertEqual(p['anchor_hits'],['Mara']);self.assertTrue(p['mentions_150'])
        self.assertEqual(proxies('training',3,['train'])['anchor_mentions'],0)

    @staticmethod
    def fixture():
        entry=copy.deepcopy(allocation()[0]);entry['packet_id']='synthetic-test-only'
        second=copy.deepcopy(entry['pairs'][0]);second['topic']='walk' if second['topic']=='library' else 'library';entry['pairs'].append(second)
        data=dict(schema='folk01-rating-v1',code=entry['code'],packet_id=entry['packet_id'],
            profile=dict(completed=True,meaning_flattened='Unchanging style',meaning_introverted='Quiet but responsive',frequency='daily',familiar='no'),
            answers=[dict(pair_id=f'{entry["code"]}-{i+1}',flat_pair='A',intro_pair='unknown',flat_evidence='Synthetic test evidence',intro_evidence='Synthetic insufficient evidence',A_flat='4',A_intro='unknown',B_flat='0',B_intro='unknown') for i in range(2)])
        return data,{entry['code']:entry}

    def test_import_rejects_wrong_packet_missing_evidence_duplicates(self):
        data,key=self.fixture();validate(data,key)
        for mutate in [lambda d:d.update(packet_id='wrong'),lambda d:d['answers'][0].update(flat_evidence=''),lambda d:d['answers'][1].update(pair_id=d['answers'][0]['pair_id'])]:
            bad=copy.deepcopy(data);mutate(bad)
            with self.assertRaises(AssertionError):validate(bad,key)
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'test.json';path.write_text(json.dumps(data))
            with self.assertRaises(AssertionError):load_exports([path,path],key)

    def test_partial_export_is_retained(self):
        data,key=self.fixture();data['answers']=data['answers'][:1];validate(data,key)
        self.assertEqual(aggregate([data],key)['n_comparisons'],1)
        self.assertEqual(aggregate([data],key,eligible_pairs=set())['n_comparisons'],0)
        self.assertEqual(aggregate([data],key,eligible_pairs=set())['absolute'],[])
        self.assertEqual(exposure_effects([data],key,repetitions=5,eligible_pairs=set()),[])
        self.assertEqual(factorial_effects([data],key,repetitions=5,eligible_pairs=set()),[])
        full,_=self.fixture();selected={full['answers'][1]['pair_id']}
        result=aggregate([full],key,eligible_pairs=selected)
        self.assertEqual(result['n_comparisons'],1)
        self.assertTrue(all(r['topic']==key[full['code']]['pairs'][1]['topic'] for r in result['absolute']))
        data['answers']=[];validate(data,key)
        self.assertEqual(aggregate([data],key)['n_comparisons'],0)

    def test_exposure_resampling_uses_complete_participants(self):
        exports=[];key={}
        for entry in allocation():
            data,_=self.fixture();entry=dict(entry,packet_id='synthetic-test-only')
            data['code']=entry['code'];data['answers']=data['answers'][:len(entry['pairs'])]
            for i,a in enumerate(data['answers']):
                a['pair_id']=f'{entry["code"]}-{i+1}'
                a['A_flat']=a['B_flat']='4' if entry['exposure']=='first' else '0'
            key[entry['code']]=entry;validate(data,key);exports.append(data)
        effects=exposure_effects(exports,key,repetitions=20)
        self.assertEqual(len(effects),48)
        self.assertTrue(all(e['full_minus_first']==-4 for e in effects))
        self.assertTrue(all(e['participant_bootstrap_95']==[-4,-4] for e in effects))
        for e in exports:
            for answer,pair in zip(e['answers'],key[e['code']]['pairs']):
                answer['A_flat']=answer['B_flat']=str({'NG':0,'WG':2,'NS':1,'WS':3}[pair['condition']])
        effects=factorial_effects(exports,key,repetitions=20)
        self.assertEqual(len(effects),60)
        expected={'warmth_generic':2,'warmth_specific':2,'specificity_neutral':1,'specificity_warm':1,'interaction':0}
        self.assertTrue(all(e['estimate']==expected[e['contrast']] for e in effects))

    def test_unknown_is_not_zero_and_empty_is_pending(self):
        data,key=self.fixture();summary=aggregate([data],key)
        for row in summary['absolute']:
            if row['metric']=='intro':self.assertIsNone(row['mean']);self.assertEqual(row['insufficient'],row['n'])
        self.assertEqual(aggregate([],key)['status'],'human ratings pending')
        self.assertEqual(exposure_effects([data],key,repetitions=10),[])


if __name__=='__main__':unittest.main()
