"""Render the Qwen14 scientific report with tables, plots, and record links."""
import importlib.util
import re
from pathlib import Path
from urllib.parse import urljoin

from markdown_it import MarkdownIt


def render():
    root = Path(__file__).resolve().parent.parent
    spec = importlib.util.spec_from_file_location('triplet_static_style', root/'probes/site.py')
    style = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(style)
    text = (root/'results/triplet-q14b/findings.md').read_text()
    def target(match):
        label, href = match.groups()
        href = urljoin('/results/triplet-q14b/', href)
        record = re.fullmatch(r'/results/([^/]+)/(?:plain|thoughts)\.md', href)
        if record and (root/'results'/record[1]/'record.json').exists():
            href='/r/'+record[1]+'.html'
        return f'{label}({href})'
    text = re.sub(r'(!?\[[^\]\n]+\])\(([^)]+)\)', target, text)
    body = MarkdownIt('commonmark', {'html': False}).enable('table').render(text)
    body=body.replace('<table>','<div class="report-table"><table>').replace('</table>','</table></div>')
    html = style.head('Qwen14 lineage · J-Space Probes',
        'Four checkpoints, full emotion instruments, and conversation controls: report policy changes without a validated causal gate.',
        style.BASE+'/qwen14.html',style.BASE+'/og/site.png')
    html += '<style>.qwen-report img{max-width:100%;height:auto}.report-table{overflow-x:auto}.qwen-report td,.qwen-report th{white-space:normal;min-width:90px}</style>'
    html += '<nav><a href="/dashboard/">Lab dashboard</a> · <a href="/results/triplet-q14b/findings.md">Report source</a> · <a href="/results/triplet-q14b/endpoints.md">All endpoints</a></nav>'
    html += '<article class="essay qwen-report">'+body+'</article>'+style.FOOT
    (root/'qwen14.html').write_text(html)
    print('Qwen14 report: qwen14.html')


if __name__=='__main__':render()
