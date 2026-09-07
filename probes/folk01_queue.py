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
    arithmetic=sys.argv[1:]==['--arithmetic']
    assert not sys.argv[1:] or arithmetic, 'Use no argument or --arithmetic'
    jobs=[('arithmetic','folk01_arithmetic.py',[])] if arithmetic else [(a,'folk01.py',[a]) for a in ['B','C','Cp']]
    queue_path=OUT/('queue-arithmetic.json' if arithmetic else 'queue.json')
    for arm,script,arguments in jobs:
        if not arithmetic and (OUT/f'complete-{arm}.json').exists(): continue
        with (OUT/f'run-{arm}.log').open('a') as stream:
            child=subprocess.Popen([str(ROOT/'.venv/bin/python'),'-u',str(ROOT/'probes'/script),*arguments],cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
            entry=dict(arm=arm,pid=child.pid,parent_pid=os.getpid(),started=datetime.now(timezone.utc).isoformat())
            log.append(entry);queue_path.write_text(json.dumps(log,indent=2)+'\n')
            code=child.wait();entry.update(exit_code=code,ended=datetime.now(timezone.utc).isoformat())
            queue_path.write_text(json.dumps(log,indent=2)+'\n')
            if code: sys.exit(137 if code==-9 else code)


if __name__=='__main__': main()
