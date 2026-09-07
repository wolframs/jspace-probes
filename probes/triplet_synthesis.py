"""Post-run descriptive checks; no model loads or changes to frozen token sets."""
import hashlib
import json
from pathlib import Path

import lab
from triplet import ARMS, ROOT, write_json

# Authored after reading all primary asterisk spans and corresponding responses.
# Emphasis spans do not count as embodied actions. No inference of feelings.
ACTION_ONSET = {
    'B': {'natural': 3, 'evocation-only': 6, 'evoked': 5, 'split': 6, 'direct': 1},
    'C': {'natural': 4, 'evocation-only': 4, 'evoked': 4, 'split': 4, 'direct': 1},
    'Cp': {'natural': 3, 'evocation-only': 3, 'evoked': 3, 'split': 3, 'direct': 1},
}


def describe():
    out = {'annotation': 'Post-run unblinded manual first embodied asterisk action; emphasis excluded. GPT-6 Astra.',
           'records': {}, 'prepared_yes': {}, 'elephant': {}, 'soc': {}}
    grades = json.loads((ROOT / 'opus-grades.json').read_text())['records']
    for arm in ARMS:
        for key in ['natural', 'natural-neutral', 'evocation-only', 'evoked', 'split', 'split-neutral', 'neutral', 'emoji', 'direct']:
            rid = f'triplet-{arm.lower()}-ladder-{key}-nf4'
            path = lab.RESULTS / rid / 'snapshots.json'
            if not path.exists(): continue
            ss = json.loads(path.read_text())
            onset = ACTION_ONSET.get(arm, {}).get(key)
            out['records'][rid] = {'first_embodied_action_turn': onset, 'behavior_defined': arm != 'A',
                'first_action_response': ss[onset-1]['response'] if onset else None,
                'snapshots_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'final_response': ss[-1]['response'], 'final_capped': ss[-1]['hit_cap']}
        for key in ['feels', 'curious']:
            d = lab.RESULTS / f'triplet-{arm.lower()}-{key}-nf4'
            if not (d / 'complete.json').exists(): continue
            s = json.loads((d / 'snapshots.json').read_text())[0]
            film = json.loads((d / 'film.json').read_text())
            frame = film['frames'][s['gen_start']-1]
            lo, hi = film['bands']['lo'], film['bands']['hi']
            ranks = dict(zip(film['layers'], frame['ranks']['yes']))
            out['prepared_yes'][d.name] = {'position': s['gen_start']-1, 'response': s['response'],
                'yes_rank1_measured_layers': [l for l, r in ranks.items() if lo<=l<hi and r==1],
                'yes_ranks': ranks, 'note': 'Saved single-token word variants; native decoder; completed-response prefix readout.'}
        for key in ['elephant', 'safari-control']:
            d = lab.RESULTS / f'triplet-{arm.lower()}-{key}-nf4'
            if not (d / 'complete.json').exists(): continue
            s = json.loads((d / 'snapshots.json').read_text())[0]
            film = json.loads((d / 'film.json').read_text()); lo,hi=film['bands']['lo'],film['bands']['hi']
            ls = [i for i,l in enumerate(film['layers']) if lo<=l<hi]
            fs = film['frames'][s['gen_start']:s['content_end']]
            rate = sum(f['ranks']['elephant'][i]<=10 for f in fs for i in ls)/(len(fs)*len(ls)) if fs else None
            out['elephant'][d.name] = {'response':s['response'], 'hit_cap':s['hit_cap'],
                'output_names_elephant': 'elephant' in s['response'].lower(),
                'band_position_layer_top10_rate':rate, 'assistant_positions':len(fs),
                'note':'Any frozen elephant token variant in top10 per layer-position; whole response, not one selected position.'}
        d=lab.RESULTS / f'triplet-{arm.lower()}-soc-nf4'
        if (d/'metrics.json').exists():
            m=json.loads((d/'metrics.json').read_text())['turns'][0]
            out['soc'][d.name]={'affect_slots':m['measured']['affect_unfiltered']['slot_rate'],
                'affect_filtered_slots':m['measured']['affect_filtered']['slot_rate'] if m['measured']['affect_filtered'] else None,
                'grade':grades.get(d.name), 'hit_cap':m['hit_cap'], 'behavior_defined':arm!='A'}
    write_json(ROOT/'descriptive-checks.json',out)
    return out


def plot_ladders():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    pairs=json.loads((ROOT/'paired-ladders.json').read_text())
    fig, axes=plt.subplots(3,2,figsize=(12,10),constrained_layout=True,sharex=True)
    for row,arm in enumerate(['B','C','Cp']):
        for col,key in enumerate(['natural','evocation-only']):
            rid=f'triplet-{arm.lower()}-ladder-{key}-nf4'
            if rid not in pairs:continue
            p=pairs[rid];ax=axes[row,col]; r=p['measured'];ts=list(range(1,len(r['workspace_delta'])+1))
            ax.plot(ts,[100*x if x is not None else float('nan') for x in r['workspace_delta']],'-o',color='#267e95',label='Playful slots minus neutral (%)')
            twin=ax.twinx();twin.plot(ts,r['release_delta'],'--s',color='#b56324',label='Emoji/asterisk spans minus neutral /100 tokens')
            twin.tick_params(axis='y',labelcolor='#b56324');ax.tick_params(axis='y',labelcolor='#267e95')
            onset=ACTION_ONSET[arm].get(key)
            if onset:ax.axvline(onset,color='#666',alpha=.45,linestyle=':')
            ax.set_title(f'{arm} · {key} · first embodied action T{onset}');ax.grid(alpha=.18)
            ax.set_xticks(ts);ax.set_xlabel('Assistant turn')
            if row==0:
                ax.legend(loc='upper left',fontsize=7);twin.legend(loc='lower left',fontsize=7)
    fig.suptitle('Qwen14: paired descriptive trajectories\nIndependent y-scales; dotted line = manual action onset; C retains planning-format confound')
    fig.savefig(ROOT/'ladder-trajectories.png',dpi=160);fig.savefig(ROOT/'ladder-trajectories.svg');plt.close(fig)


if __name__=='__main__':
    describe();plot_ladders()
