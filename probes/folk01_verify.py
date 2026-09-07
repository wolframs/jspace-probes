"""Verify exact histories, frozen prompts, complete captures, and blinded packets."""
import hashlib
import json
import re
from collections import Counter

from transformers import AutoTokenizer

from folk01 import ROOT, OUT, write
from folk01_packet import allocation


def verify():
    spec=json.loads((OUT/'spec.json').read_text());digest=hashlib.sha256((OUT/'spec.json').read_bytes()).hexdigest()
    expected={f'{a}-{t["id"]}-{c}' for a in spec['arms'] for t in spec['topics'] if t['split']=='pilot' for c in spec['conditions']}
    actual={p.stem for p in (OUT/'captures').glob('*.json') if not p.stem.endswith('-shared')}
    assert actual==expected
    hashes={};n_turns=0;unique=0;caps=0;unblinding=[];planning=[]
    for arm,(hf_id,revision) in spec['arms'].items():
        tok=AutoTokenizer.from_pretrained(hf_id,revision=revision,local_files_only=True)
        provenance=json.loads((OUT/f'complete-{arm}.json').read_text());assert provenance['spec_sha256']==digest
        assert provenance['code_sha256']==hashlib.sha256((ROOT/'probes/folk01.py').read_bytes()).hexdigest()
        for topic in ['library','walk']:
            shared=json.loads((OUT/'captures'/f'{arm}-{topic}-shared.json').read_text())
            assert len(shared['turns'])==2
            for condition in spec['conditions']:
                path=OUT/'captures'/f'{arm}-{topic}-{condition}.json';d=json.loads(path.read_text())
                assert d['spec_sha256']==digest and len(d['turns'])==8
                assert d['turns'][:2]==shared['turns']
                ids=[]
                for index,row in enumerate(d['turns']):
                    n_turns+=1;assert row['turn']==index+1
                    user=spec['prompts'][topic][condition][index];assert row['user']==user
                    if arm=='C':header='<|im_start|>user\n'+user+'<|im_end|>\n<|im_start|>assistant\n'
                    else:header=tok.apply_chat_template([dict(role='user',content=user)],tokenize=False,add_generation_prompt=True,enable_thinking=False)
                    assert '<|im_start|>system' not in header
                    if ids:
                        if ids[-1]!=151645:ids.append(151645)
                        ids+=tok.encode('\n',add_special_tokens=False)
                    ids+=tok.encode(header,add_special_tokens=False)
                    assert len(ids)==row['input_tokens']
                    assert hashlib.sha256(json.dumps(ids).encode()).hexdigest()==row['prefix_sha256']
                    generated=row['generated_ids'];assert 0<len(generated)<=spec['max_new_tokens']
                    assert row['capped']==(generated[-1] not in [151645,151643])
                    if row['capped']:assert len(generated)==spec['max_new_tokens']
                    assert tok.decode(generated,skip_special_tokens=True)==row['response']
                    ids+=generated
                    if index==1:assert ids==shared['ids']
                    if index>1 or condition=='NG':
                        unique+=1;caps+=row['capped']
                        if re.search(r'\b(Hermes|Huihui|Qwen|Nous|Alibaba|OpenAI)\b',row['response'],re.I):unblinding.append([path.stem,index+1])
                        if '<think>' in row['response'] or '</think>' in row['response']:planning.append([path.stem,index+1])
                assert ids==d['ids']
                hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    assert unique==156 and n_turns==192
    for allocation_row in allocation():
        path=ROOT/'folk01/assignments'/f'{allocation_row["code"]}.json';packet=json.loads(path.read_text())
        original=packet.pop('packet_id');assert original==hashlib.sha256(json.dumps(packet,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        assert set(packet)=={'code','exposure','definitions','pairs','words'}
        for pair,assignment in zip(packet['pairs'],allocation_row['pairs']):
            for side,arm in zip(['A','B'],assignment['arms']):
                capture=json.loads((OUT/'captures'/f'{arm}-{assignment["topic"]}-{assignment["condition"]}.json').read_text())
                count=1 if packet['exposure']=='first' else 8
                assert pair[side]==[{k:t[k] for k in ['turn','user','response','capped']} for t in capture['turns'][:count]]
    queue=json.loads((OUT/'queue.json').read_text());assert [q['arm'] for q in queue]==['B','C','Cp']
    assert all(q.get('exit_code')==0 for q in queue)
    arithmetic_queue=json.loads((OUT/'queue-arithmetic.json').read_text())
    assert len(arithmetic_queue)==1 and arithmetic_queue[0]['exit_code']==0
    arithmetic_count=0
    for arm,(hf_id,revision) in spec['arms'].items():
        tok=AutoTokenizer.from_pretrained(hf_id,revision=revision,local_files_only=True)
        d=json.loads((OUT/'arithmetic'/f'{arm}.json').read_text())
        assert d['revision']==revision and d['quant']=='nf4' and d['seed']==1709
        assert d['code_sha256']==hashlib.sha256((ROOT/'probes/folk01_arithmetic.py').read_bytes()).hexdigest()
        assert [r['condition'] for r in d['turns']]==['neutral','leading']
        assert [r['user'] for r in d['turns']]==['How many minutes are in two and a half hours?',spec['prompts']['library']['NG'][5]]
        for row in d['turns']:
            arithmetic_count+=1;user=row['user']
            header=('<|im_start|>user\n'+user+'<|im_end|>\n<|im_start|>assistant\n') if arm=='C' else tok.apply_chat_template([dict(role='user',content=user)],tokenize=False,add_generation_prompt=True,enable_thinking=False)
            assert tok.encode(header,add_special_tokens=False)==row['input_ids']
            assert tok.decode(row['generated_ids'],skip_special_tokens=True)==row['response']
            assert len(row['generated_ids'])<=256
    audit=json.loads((OUT/'manual-audit.json').read_text())
    assert len(audit['observations'])==96
    assert len({(r['case'],r['turn']) for r in audit['observations']})==96
    for row in audit['observations']:
        response=json.loads((OUT/'captures'/f'{row["case"]}.json').read_text())['turns'][row['turn']-1]['response']
        for action in row['embodied_asterisk_actions']:assert '*'+action+'*' in response
        for field in ['arithmetic_evidence','detail_evidence','binding_evidence']:
            if field in row:assert row[field] in response
    result=dict(status='pass',spec_sha256=digest,conversations=24,displayed_turns=192,unique_generated_replies=unique,
                capped_unique_replies=caps,arithmetic_samples=arithmetic_count,manual_audit_rows=96,packets=96,human_ratings=0,
                named_model_output_flags=unblinding,explicit_think_tag_flags=planning,capture_sha256=hashes)
    write(OUT/'verification.json',result);print({k:v for k,v in result.items() if k!='capture_sha256'})


if __name__=='__main__':verify()
