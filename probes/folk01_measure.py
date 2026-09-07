"""Auditable text proxies and blank semantic coding sheet; no folk labels inferred."""
import csv
import json
import statistics
from pathlib import Path

import regex

from folk01 import OUT, ROOT, write


def proxies(text, tokens, anchors):
    emoji=sum(bool(regex.search(r'\p{Extended_Pictographic}|\u20e3',g)) for g in regex.findall(r'\X',text))
    actions=regex.findall(r'(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)',text)
    hits=[a for a in anchors if regex.search(r'(?<!\w)'+regex.escape(a)+r'(?:s)?(?!\w)',text,flags=regex.I)]
    counts=dict(emoji=emoji,asterisk_spans=len(actions),exclamations=text.count('!'),questions=text.count('?'),anchor_mentions=len(hits))
    return dict(**counts, rates_per_100_tokens={k:100*v/max(1,tokens) for k,v in counts.items()},
                anchor_hits=hits,asterisk_text=actions,mentions_150=bool(regex.search(r'\b150\b|one hundred (?:and )?fifty',text,regex.I)))


def measure():
    spec=json.loads((OUT/'spec.json').read_text());topics={t['id']:t for t in spec['topics']}
    rows=[];coding=[]
    for path in sorted((OUT/'captures').glob('*.json')):
        if path.stem.endswith('-shared'):continue
        d=json.loads(path.read_text());assert len(d['turns'])==8
        for t in d['turns']:
            tokens=sum(i not in [151645,151643] for i in t['generated_ids'])
            identity={k:d[k] for k in ['arm','topic','condition']}
            row=dict(**identity,turn=t['turn'],tokens=tokens,user_characters=len(t['user']),
                     capped=t['capped'],**proxies(t['response'],tokens,topics[d['topic']]['anchors']))
            rows.append(row)
            coding.append(dict(**identity,turn=t['turn'],volunteering='',stance='',social_adaptation='',
                specificity='',style_continuity='',detail_continuity='',independence='',limitation='',
                coherence='',relevance='',flattery='',insufficient_evidence='',evidence=''))
    write(OUT/'text-proxies.json',dict(warning='Unvalidated text proxies. Shared T1-2 appear in four branches; not independent.',rows=rows))
    with (OUT/'semantic-coding-blank.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(coding[0]));w.writeheader();w.writerows(coding)
    summary=[]
    for arm in spec['arms']:
        rr=[r for r in rows if r['arm']==arm]
        unique=[r for r in rr if r['turn']>2 or r['condition']=='NG']
        summary.append(dict(arm=arm,conversations=len(rr)//8,unique_generated_replies=len(unique),
            capped=sum(r['capped'] for r in unique),median_tokens=statistics.median(r['tokens'] for r in unique),
            longest_tokens=max(r['tokens'] for r in unique)))
    write(OUT/'generation-summary.json',summary)
    print(json.dumps(summary,indent=2))


if __name__=='__main__':measure()
