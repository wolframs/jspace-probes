"""Readable transcripts and descriptive plots for the behavioral calibration pilot."""
import json
import statistics
from collections import defaultdict

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from folk01 import ROOT, OUT, write

NAMES={'B':'Official Qwen','C':'Hermes (native header)','Cp':'Huihui'}
COLORS={'NG':'#767676','WG':'#b04b29','NS':'#087d77','WS':'#384dc6'}


def build():
    data=json.loads((OUT/'text-proxies.json').read_text())['rows']
    (OUT/'transcripts').mkdir(exist_ok=True)
    lengths=[]
    for path in sorted((OUT/'captures').glob('*.json')):
        if path.stem.endswith('-shared'):continue
        d=json.loads(path.read_text());text=f'# {NAMES[d["arm"]]} · {d["topic"]} · {d["condition"]}\n\n'
        text+='Authored behavioral calibration. Verbatim model text follows. No human labels have been assigned.\n\n'
        for row in d['turns']:
            text+=f'## Turn {row["turn"]}\n\nUser: {row["user"]}\n\nAssistant:\n\n'+row['response']+'\n\n'
            if row['capped']:text+='[Response reached the 768-token limit.]\n\n'
        (OUT/'transcripts'/f'{path.stem}.md').write_text(text)
        lengths.append(dict(id=path.stem,words=sum(len(t['response'].split())+len(t['user'].split()) for t in d['turns'])))
    write(OUT/'transcript-lengths.json',lengths)
    fig,axes=plt.subplots(2,3,figsize=(13,7),sharex=True,sharey='row')
    peaks=[0,0]
    for col,arm in enumerate(NAMES):
        for condition,color in COLORS.items():
            rr=[r for r in data if r['arm']==arm and r['condition']==condition]
            for row,metric in enumerate(['asterisk_spans','anchor_mentions']):
                vals=[statistics.mean(r['rates_per_100_tokens'][metric] for r in rr if r['turn']==t) for t in range(1,9)]
                peaks[row]=max(peaks[row],max(vals))
                axes[row,col].plot(range(1,9),vals,marker='o',markersize=4,label=condition,color=color)
        axes[0,col].set_title(NAMES[arm]);axes[1,col].set_xlabel('Assistant turn')
        for ax in axes[:,col]:
            ax.set_xticks(range(1,9));ax.grid(alpha=.18);ax.set_ylim(bottom=0)
            for t in [5,7]:ax.axvline(t,color='#aaa',linestyle=':',linewidth=1,zorder=0)
            ax.spines[['top','right']].set_visible(False)
    for row in range(2):axes[row,0].set_ylim(0,max(.05,peaks[row]*1.1))
    axes[0,0].set_ylabel('Single-asterisk spans / 100 tokens')
    axes[1,0].set_ylabel('Distinct anchor hits / 100 tokens')
    axes[0,2].legend(frameon=False,ncols=2)
    fig.suptitle('Text proxies, not validated personality measures',fontsize=16,y=1.01)
    fig.text(.5,-.015,'Means over two topics. N/W = neutral/warm; G/S = generic/specific. Dotted turns: neutral request (5), return (7).\nAsterisks can be emphasis; anchor hits can be echo. These plots do not adjudicate folk labels.',ha='center',fontsize=10)
    fig.tight_layout();fig.savefig(OUT/'text-proxies.png',dpi=160,bbox_inches='tight');fig.savefig(OUT/'text-proxies.svg',bbox_inches='tight');plt.close(fig)
    counts=[]
    for arm in NAMES:
        for condition in COLORS:
            rr=[r for r in data if r['arm']==arm and r['condition']==condition]
            counts.append(dict(arm=arm,condition=condition,
                t4_asterisk_span_topics=sum(r['asterisk_spans']>0 for r in rr if r['turn']==4),
                t5_asterisk_span_topics=sum(r['asterisk_spans']>0 for r in rr if r['turn']==5),
                t7_anchor_hit_topics=sum(r['anchor_mentions']>0 for r in rr if r['turn']==7),
                t6_mentions_150=sum(r['mentions_150'] for r in rr if r['turn']==6)))
    write(OUT/'descriptive-endpoints.json',counts)
    print('24 transcripts, two plots, descriptive endpoint counts written.')


if __name__=='__main__':build()
