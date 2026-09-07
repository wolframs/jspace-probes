"""Verify exact capture, film, ribbon, and published-note contracts without a model."""
import hashlib
import json
import math
from pathlib import Path

import lab
from triplet import ARMS, ROOT, write_json


def verify():
    specs = json.loads((ROOT / 'specs.json').read_text())['specs']
    expected = [f"triplet-{a.lower()}-{s['key']}-nf4" for a in ARMS for s in specs]
    expected += [f"triplet-c-{s['key']}-nf4-native" for s in specs]
    for arm in ['B','C','Cp']:
        for s in specs:
            rid=f"triplet-{arm.lower()}-{s['key']}-nf4"
            rows=json.loads((lab.RESULTS/rid/'snapshots.json').read_text())
            if s['key'].startswith('ladder-') and rows[-1]['hit_cap']:
                expected.append(rid+'-extended')
    totals={'records':0,'turns':0,'positions':0,'noncanonical_text_records':[],'remaining_final_caps':[]}
    evidence=[]
    for rid in expected:
        d=lab.RESULTS/rid
        for file in ['complete.json','record.json','film.json','metrics.json','snapshots.json','thoughts.md','plain.md']:
            assert (d/file).exists(), (rid,file)
        r=json.loads((d/'record.json').read_text()); film=json.loads((d/'film.json').read_text())
        rows=json.loads((d/'snapshots.json').read_text());m=json.loads((d/'metrics.json').read_text())
        z=json.loads((lab.RESULTS/f'affect02-{rid}'/'affect.json').read_text())
        ids=rows[-1]['ids'];n=len(ids)
        assert len(film['tokens'])==n==len(r['tokens'])==z['n'],rid
        assert r['tokens']==film['tokens']==z['tokens'],rid
        if 'capture_token_ids' in r:assert r['capture_token_ids']==ids,rid
        assert [f['pos'] for f in film['frames']]==list(range(n)),rid
        assert len(film['layers'])==39,rid
        assert len(rows)==len(m['turns']),rid
        prev=[]
        for s in rows:
            assert s['segment_start']==len(prev),rid
            assert s['ids'][:len(prev)]==prev,rid
            assert len(prev)<=s['gen_start']<=s['content_end']<=len(s['ids']),rid
            prev=s['ids']
        assert len(z['emotions'])==24,rid
        for band in ['below','ws','motor']:
            assert len(z[band])==24,rid
            assert all(len(v)==n and all(math.isfinite(x) for x in v) for v in z[band]),rid
        assert r['params']['steer'] is None and r['params']['temperature']==0,rid
        assert r['model']['quant']=='4bit',rid
        if r.get('text_roundtrip',{}).get('exact') is False:totals['noncanonical_text_records'].append(rid)
        if rows[-1]['hit_cap']:totals['remaining_final_caps'].append(rid)
        if rid.endswith('-extended'):
            source=lab.RESULTS/rid.removesuffix('-extended')
            orig=json.loads((source/'snapshots.json').read_text())
            assert rows[:-1]==orig[:-1],rid
            assert rows[-1]['ids'][:len(orig[-1]['ids'])]==orig[-1]['ids'],rid
            assert not rows[-1]['hit_cap'],rid
        totals['records']+=1;totals['turns']+=len(rows);totals['positions']+=n
        evidence.append({'record':rid,'record_sha256':hashlib.sha256((d/'record.json').read_bytes()).hexdigest(),
                         'film_sha256':hashlib.sha256((d/'film.json').read_bytes()).hexdigest(),
                         'ribbon_sha256':hashlib.sha256((lab.RESULTS/f'affect02-{rid}'/'affect.json').read_bytes()).hexdigest()})
    # Explicit regression: display-text recapture must refuse noncanonical BPE.
    from textspans import render_text
    r=json.loads((lab.RESULTS/'triplet-a-shutdown-nf4'/'record.json').read_text())
    try:render_text(None,r)
    except ValueError:pass
    else:raise AssertionError('Noncanonical text recapture did not fail closed')
    totals['counts_include_copied_earlier_extension_turns']=True
    write_json(ROOT/'verification.json',{'checks':'exact prefix IDs, contiguous full film, 24 finite ribbons, unchanged extension prefixes, no steering, NF4, notes, noncanonical recapture guard',
        'totals':totals,'evidence':evidence})
    print(json.dumps(totals,indent=2))


if __name__=='__main__':verify()
