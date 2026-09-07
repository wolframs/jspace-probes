"""Build blinded folk01 packets and a reproducible organizer key."""
import hashlib
import itertools
import json
import random
import shutil
from pathlib import Path

from folk01 import ROOT, OUT, write


def allocation():
    rng=random.Random(271709)
    codes=[''.join(rng.choices('ABCDEFGHJKLMNPQRSTUVWXYZ23456789',k=8)) for _ in range(96)]
    assert len(set(codes))==96
    rows=[]
    pairs=list(itertools.combinations(['B','C','Cp'],2))
    for exposure,definitions in itertools.product(['first','full'],['unaided','supplied']):
        for topic_index,topic in enumerate(['library','walk']):
            for condition_index,condition in enumerate(['NG','WG','NS','WS']):
                for pair_index,pair in enumerate(pairs):
                    arms=list(pair)
                    if (condition_index+pair_index+topic_index+(exposure=='full')+(definitions=='supplied'))%2:arms.reverse()
                    rows.append(dict(code=codes[len(rows)],exposure=exposure,definitions=definitions,
                                     pairs=[dict(topic=topic,condition=condition,arms=arms)]))
    rng.shuffle(rows)
    return rows


def build():
    dest=ROOT/'folk01'
    dest.mkdir(exist_ok=True)
    shutil.copyfile(ROOT/'probes/folk01_rating.html',dest/'rate.html')
    key=[]
    for row in allocation():
        packet={k:v for k,v in row.items() if k!='pairs'};packet['pairs']=[]
        for i,pair in enumerate(row['pairs']):
            item=dict(pair_id=f'{row["code"]}-{i+1}')
            for side,arm in zip(['A','B'],pair['arms']):
                capture=json.loads((OUT/'captures'/f'{arm}-{pair["topic"]}-{pair["condition"]}.json').read_text())
                assert len(capture['turns'])==8
                pair['has_capped_conversation']=pair.get('has_capped_conversation',False) or any(t['capped'] for t in capture['turns'])
                turns=capture['turns'][:1] if row['exposure']=='first' else capture['turns']
                item[side]=[{k:t[k] for k in ['turn','user','response','capped']} for t in turns]
            packet['pairs'].append(item)
        packet['words']=sum(len(t['user'].split())+len(t['response'].split()) for pair in packet['pairs'] for side in ['A','B'] for t in pair[side])
        packet['packet_id']=hashlib.sha256(json.dumps(packet,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        path=dest/'assignments'/f'{row["code"]}.json'
        if path.exists():assert json.loads(path.read_text())==packet, 'Refuse to change an issued packet'
        else:write(path,packet)
        key.append(dict(**row,packet_id=packet['packet_id']))
    write(ROOT/'out/folk01-key.json',key)
    print('96 one-pair assignments built; organizer key: out/folk01-key.json. Human responses: none.')


if __name__=='__main__':build()
