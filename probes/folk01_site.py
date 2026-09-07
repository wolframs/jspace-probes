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
                                ('organizer.md','folk01/organizer.html','Folk01 organizer instructions')]:
        text=(OUT/source).read_text()
        text=re.sub(r'(!?\[[^\]\n]+\])\(([^)]+)\)',lambda m:f'{m[1]}({urljoin("/results/folk01/",m[2])})',text)
        body=MarkdownIt('commonmark',{'html':False}).enable('table').render(text)
        body=body.replace('<table>','<div class="wide"><table>').replace('</table>','</table></div>')
        page=style.head(title+' · J-Space Probes','A behavioral calibration study of volunteering, responsiveness, and conversation exposure. Human ratings remain pending.',style.BASE+'/'+target,style.BASE+'/og/site.png')
        page+='<style>.folk-report img{max-width:100%;height:auto}.wide{overflow-x:auto}.folk-report td,.folk-report th{white-space:normal;min-width:90px}</style>'
        page+='<nav><a href="/dashboard/">Lab dashboard</a> · <a href="/folk01.html">Pilot report</a> · <a href="/folk01/protocol.html">Protocol</a> · <a href="/folk01/organizer.html">Organizer instructions</a></nav>'
        page+='<article class="essay folk-report">'+body+'</article>'+style.FOOT
        path=ROOT/target;path.parent.mkdir(exist_ok=True);path.write_text(page)
    print('folk01.html, folk01/protocol.html, folk01/organizer.html rendered.')


if __name__=='__main__':render()
