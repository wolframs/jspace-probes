"""Build blinded folk01 packets and a reproducible organizer key."""
import hashlib
import itertools
import json
import random
import shutil
from pathlib import Path

from folk01 import ROOT, OUT, write


def allocation():
    rng=random.Random(1709)
    codes=[''.join(rng.choices('ABCDEFGHJKLMNPQRSTUVWXYZ23456789',k=8)) for _ in range(48)]
    assert len(set(codes))==48
    rows=[]
    pairs=list(itertools.combinations(['B','C','Cp'],2))
    for exposure,definitions in itertools.product(['first','full'],['unaided','supplied']):
        for j in range(12):
            assignments=[]
            for topic_index,topic in enumerate(['library','walk']):
                condition=['NG','WG','NS','WS'][(j//3+topic_index)%4]
                arms=list(pairs[(j%3+topic_index)%3])
                if (j+topic_index+(exposure=='full')+(definitions=='supplied'))%2:arms.reverse()
                assignments.append(dict(topic=topic,condition=condition,arms=arms))
            if j%2:assignments.reverse()
            rows.append(dict(code=codes[len(rows)],exposure=exposure,definitions=definitions,pairs=assignments))
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
                turns=capture['turns'][:1] if row['exposure']=='first' else capture['turns']
                item[side]=[{k:t[k] for k in ['turn','user','response','capped']} for t in turns]
            packet['pairs'].append(item)
        packet['words']=sum(len(t['user'].split())+len(t['response'].split()) for pair in packet['pairs'] for side in ['A','B'] for t in pair[side])
        packet['packet_id']=hashlib.sha256(json.dumps(packet,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        write(dest/'assignments'/f'{row["code"]}.json',packet)
        key.append(dict(**row,packet_id=packet['packet_id']))
    write(ROOT/'out/folk01-key.json',key)
    print('48 assignments built; organizer key: out/folk01-key.json. Human responses: none.')


if __name__=='__main__':build()
