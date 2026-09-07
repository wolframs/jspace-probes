"""Publish the behavioral pilot and protocol without changing the lens-record index."""
import importlib.util
import re
from urllib.parse import urljoin

from markdown_it import MarkdownIt

from folk01 import ROOT, OUT


def render():
    spec=importlib.util.spec_from_file_location('folk_static_style',ROOT/'probes/site.py')
    style=importlib.util.module_from_spec(spec);spec.loader.exec_module(style)
    for source,target,title in [('findings.md','folk01.html','Quiet, responsive, or unchanged?'),
                                ('protocol.md','folk01/protocol.html','Folk01 protocol'),
                                ('organizer.md','folk01/organizer.html','Folk01 reproduction instructions'),
                                ('judge-findings.md','folk01/judges.html','Folk01 model judges'),
                                ('psychology.md','folk01/psychology.html','Flat affect and introversion: psychology criteria'),
                                ('../folk02/findings.md','folk02.html','Expression, initiative, and stance'),
                                ('../folk02/protocol.md','folk02/protocol.html','Folk02 coding protocol'),
                                ('../folk02/plain.md','folk02/plain.html','Folk02 in plain language')]:
        text=(OUT/source).read_text()
        text=re.sub(r'(!?\[[^\]\n]+\])\(([^)]+)\)',lambda m:f'{m[1]}({urljoin("/results/folk02/" if source.startswith("../folk02/") else "/results/folk01/",m[2])})',text)
        body=MarkdownIt('commonmark',{'html':False}).enable('table').render(text)
        body=body.replace('<table>','<div class="wide"><table>').replace('</table>','</table></div>')
        page=style.head(title+' · J-Space Probes','A behavioral calibration study of volunteering, responsiveness, and conversation exposure. Model judges compare the fixed transcripts with explicit criteria and evidence.',style.BASE+'/'+target,style.BASE+'/og/site.png')
        page+='<style>.folk-report img{max-width:100%;height:auto}.wide{overflow-x:auto}.folk-report td,.folk-report th{white-space:normal;min-width:90px}</style>'
        page+='<nav><a href="/dashboard/">Lab dashboard</a> · <a href="/folk01.html">Pilot report</a> · <a href="/folk01/protocol.html">Protocol</a> · <a href="/folk01/organizer.html">Reproduce judging</a> · <a href="/folk02.html">Expression and initiative</a></nav>'
        page+='<article class="essay folk-report">'+body+'</article>'+style.FOOT
        path=ROOT/target;path.parent.mkdir(exist_ok=True);path.write_text(page)
    print('Folk01 and Folk02 reports rendered.')


if __name__=='__main__':render()
