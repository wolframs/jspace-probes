"""Durable single-model queue; any failure stops before the next load."""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'results/folk01'


def main():
    log=[]
    for arm in ['B','C','Cp']:
        if (OUT/f'complete-{arm}.json').exists(): continue
        with (OUT/f'run-{arm}.log').open('a') as stream:
            child=subprocess.Popen([str(ROOT/'.venv/bin/python'),'-u',str(ROOT/'probes/folk01.py'),arm],cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
            entry=dict(arm=arm,pid=child.pid,parent_pid=os.getpid(),started=datetime.now(timezone.utc).isoformat())
            log.append(entry);(OUT/'queue.json').write_text(json.dumps(log,indent=2)+'\n')
            code=child.wait();entry.update(exit_code=code,ended=datetime.now(timezone.utc).isoformat())
            (OUT/'queue.json').write_text(json.dumps(log,indent=2)+'\n')
            if code: sys.exit(137 if code==-9 else code)


if __name__=='__main__': main()
