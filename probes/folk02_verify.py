"""Verify the archived judging run without network or credentials."""
import json
from pathlib import Path
import folk02 as f


def verify():
    m=json.loads((f.OUT/'manifest.json').read_text())
    a=json.loads((f.OUT/'transport-amendment.json').read_text())
    assert f.sha((f.OUT/'runner-initial.py.txt').read_bytes())==m['source_sha256']
    assert f.sha((f.ROOT/'probes/folk02.py').read_bytes())==a['runner_sha256']
    for p,h in m['capture_sha256'].items():assert f.sha((f.ROOT/p).read_bytes())==h
    tasks={t['id']:t for t in m['tasks']}
    valid=0;invalid=[];models={};normalizations=0
    for p in sorted((f.OUT/'raw').glob('*.json')):
        j,taskid=p.stem.split('-',1);task=tasks[taskid];x=json.loads(p.read_text())
        assert x['request']==f.body(task,j,m)
        returned=x['response']['model'];models.setdefault(j,set()).add(returned)
        allowed={f.MODELS[j][0],'gemini-3.1-pro-preview'} if j=='gemini' else {f.MODELS[j][0], 'anthropic/claude-sonnet-5'} if j=='sonnet' else {f.MODELS[j][0]}
        assert returned in allowed
        parsed=f.OUT/'parsed'/p.name
        try:data=f.parse(x['response'],task)
        except (AssertionError,ValueError,KeyError,TypeError):
            assert not parsed.exists();invalid.append(p.name);continue
        assert data==json.loads(parsed.read_text());valid+=1
        if taskid=='fixture':assert all(f.fixture_check(data,m['fixtures_expected']).values())
    ledger=json.loads((f.OUT/'ledger.json').read_text());total=0
    for e in ledger:
        cost=e.get('actual_usd',e.get('usage_bound_usd',e['reserved_usd']))
        assert cost<=e['reserved_usd']+1e-6 and cost>=0
        # Retrospective conservative bounds also fit each request's reservation.
        assert total+e['reserved_usd']<=m['budget_usd']+1e-6,(e['id'],total,e['reserved_usd'])
        total+=cost
    assert total<=m['budget_usd']
    result={'capture_hashes':24,'original_runner_hash':True,'amended_runner_hash':True,'valid_responses_including_fixtures':valid,'unusable_completed_responses':invalid,'returned_models':{j:sorted(v) for j,v in models.items()},'attempts':len(ledger),'conservative_bound_usd':round(total,6),'budget_usd':m['budget_usd'],'all_reservations_within_budget':True}
    f.dump(f.OUT/'verification.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':verify()
