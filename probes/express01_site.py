"""Render the expression calibration with the existing lab page style."""
import importlib.util
import re
from urllib.parse import urljoin
from markdown_it import MarkdownIt
from express01_spec import ROOT,OUT


def render():
 spec=importlib.util.spec_from_file_location('expression_style',ROOT/'probes/site.py')
 style=importlib.util.module_from_spec(spec);spec.loader.exec_module(style)
 for source,target,title in [('findings.md','express01.html','Can an internal readout predict expression?'),('protocol.md','express01/protocol.html','Expression probe protocol'),('plain.md','express01/plain.html','Expression probe in plain language'),('outputs.md','express01/outputs.html','All expression-control outputs')]:
  text=(OUT/source).read_text()
  text=re.sub(r'(!?\[[^\]\n]+\])\(([^)]+)\)',lambda m:f'{m[1]}({urljoin("/results/express01/",m[2])})',text)
  body=MarkdownIt('commonmark',{'html':False}).enable('table').render(text)
  body=body.replace('<table>','<div class="wide"><table>').replace('</table>','</table></div>')
  page=style.head(title+' · J-Space Probes','A read-only test of default expression, prompted expression and conversation history. Exact prefixes, held-out vocabulary, full emotion instruments and explicit calibration limits.',style.BASE+'/'+target,style.BASE+'/og/site.png')
  page+='<style>.expression-report img{max-width:100%;height:auto}.wide{overflow-x:auto}.expression-report td,.expression-report th{white-space:normal;min-width:85px}.expression-report pre{overflow-x:auto}</style>'
  page+='<nav><a href="/dashboard/">Lab dashboard</a> · <a href="/express01.html">Expression probe</a> · <a href="/express01/protocol.html">Protocol</a> · <a href="/express01/outputs.html">All outputs</a> · <a href="/folk02.html">Prior behavior codes</a></nav>'
  page+='<article class="essay expression-report">'+body+'</article>'+style.FOOT
  path=ROOT/target;path.parent.mkdir(exist_ok=True);path.write_text(page)
 print('Express01 report, protocol, plain summary and outputs rendered.')


if __name__=='__main__':render()
