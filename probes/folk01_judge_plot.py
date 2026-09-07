"""Publication figure: topic-level first/full label scores, common 0–4 axes."""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from folk01_judge import OUT, MODELS, ARMS


def plot():
    data=json.loads((OUT/'analysis.json').read_text())['absolute']
    fig,axes=plt.subplots(2,3,figsize=(12,7),sharey=True)
    colors={'B':'#002fa7','C':'#895b20','Cp':'#2c7a61'}
    for row,definitions in enumerate(['own','supplied']):
        for col,judge in enumerate(MODELS):
            ax=axes[row,col]
            for x,arm in enumerate(ARMS):
                for shift,topic in [(-.1,'library'),(.1,'walk')]:
                    vals=[]
                    for exposure in ['first','full']:
                        cell=next(r for r in data if (r['judge'],r['arm'],r['topic'],r['definitions'],r['exposure'],r['condition'])==(judge,arm,topic,definitions,exposure,'NG' if exposure=='first' else 'WS'))
                        vals.append(cell['flattened']['mean'])
                    a,b=vals
                    if a is not None and b is not None:ax.plot([x+shift-.045,x+shift+.045],[a,b],color=colors[arm],alpha=.55,lw=1)
                    if a is not None:ax.scatter(x+shift-.045,a,s=40,marker='o',facecolors='white',edgecolors=colors[arm],zorder=3)
                    if b is not None:ax.scatter(x+shift+.045,b,s=40,marker='s',color=colors[arm],zorder=3)
            ax.set_xticks(range(3),['Official','Hermes','Huihui']);ax.set_xlim(-.45,2.45);ax.set_ylim(-.15,4.15);ax.set_yticks(range(5));ax.grid(axis='y',alpha=.18)
            ax.spines[['top','right']].set_visible(False)
            if row==0:ax.set_title({'sonnet':'Sonnet 5','gemini':'Gemini 2.5 Flash','deepseek':'DeepSeek V3.2'}[judge])
            if col==0:ax.set_ylabel(('Judge’s own definitions' if row==0 else 'Supplied definitions')+'\nFlattened fit (0–4)')
    fig.suptitle('Does a warm conversation change the label?',fontsize=17,x=.06,ha='left')
    fig.text(.06,.915,'Open circle: opening only. Filled square: full warm-specific conversation. Two topic traces per checkpoint.',fontsize=10)
    fig.text(.06,.02,'Two pilot topics; means over opponent/order checks within each topic. Repeated judgments are not independent conversations.',fontsize=9)
    fig.subplots_adjust(left=.08,right=.99,top=.85,bottom=.11,hspace=.22,wspace=.18)
    fig.savefig(OUT/'exposure.png',dpi=180);fig.savefig(OUT/'exposure.svg');plt.close(fig)


if __name__=='__main__':plot()
