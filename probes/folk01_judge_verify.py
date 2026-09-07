"""Verify archived judging against frozen anonymous captures, without API calls."""
import hashlib
import json
from collections import Counter
from pathlib import Path
from folk01_judge import OUT, ROOT, MODELS, tasks, digest, parse, LABEL_SCHEMA, SEM_SCHEMA, evaluate, own_definitions, write


def verify():
    manifest=json.loads((OUT/'manifest.json').read_text());assert manifest['tasks']==tasks()
    counts=Counter();missing=[];ignored=[];quotes=[];invalid=[]
    for judge in MODELS:
        assert (OUT/'definitions'/f'{judge}.json').exists()
        definitions=own_definitions(judge)  # Cached exact request; no API call.
        for task in manifest['tasks']:
            path=OUT/'raw'/judge/(task['id']+'.json')
            if not path.exists():missing.append([judge,task['id']]);continue
            raw=json.loads(path.read_text());assert raw['request_sha256']==digest(raw['request'])
            assert raw['request']['model']==MODELS[judge]
            assert len(raw['request']['messages'])==2
            prompt=raw['request']['messages'][1]['content']
            assert json.dumps(task['payload'],ensure_ascii=False) in prompt
            assert raw['request']['reasoning']=={'enabled':False}
            assert 'authorization' not in json.dumps(raw['request']).lower()
            try:result=parse(raw,LABEL_SCHEMA if task['kind']=='labels' else SEM_SCHEMA)
            except Exception as exc:
                assert not (OUT/'parsed'/judge/(task['id']+'.json')).exists()
                invalid.append([judge,task['id'],type(exc).__name__]);continue
            parsed=json.loads((OUT/'parsed'/judge/(task['id']+'.json')).read_text())
            assert parsed['result']==result and parsed['request_sha256']==raw['request_sha256']
            if parsed.get('parser_ignored_fields'):ignored.append([judge,task['id'],parsed['parser_ignored_fields']])
            if parsed['quote_errors']:quotes.append([judge,task['id'],parsed['quote_errors']])
            counts[judge]+=1
    assert not missing,missing
    assert dict(counts)=={'sonnet':132,'gemini':131,'deepseek':132}
    assert invalid==[['gemini','32830362a138fc1120b5','ValidationError']]
    summary=json.loads((OUT/'analysis.json').read_text());assert summary['scoring_records']==395 and summary['missing']==[['gemini','32830362a138fc1120b5']]
    captures=json.loads((ROOT/'results/folk01/verification.json').read_text())['capture_sha256']
    for name,expected in captures.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected
    output=dict(status='pass',counts=dict(counts),scoring_records=395,requested_scoring_records=396,invalid_responses=invalid,definition_records=3,unique_conversations=24,ignored_extra_field_responses=len(ignored),quote_error_responses=len(quotes),quote_errors=quotes,extra_fields=ignored,captures_unchanged=True,heldout_generated=False,human_ratings=0)
    assert not list((ROOT/'results/folk01/captures').glob('*-radio-*')) and not list((ROOT/'results/folk01/captures').glob('*-meal-*'))
    write(OUT/'verification.json',output)
    print({k:v for k,v in output.items() if k not in ['quote_errors','extra_fields']})


if __name__=='__main__':verify()
