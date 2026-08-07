# Incident 2026-08-07 — desktop near-freeze, OOM kill, relaunch loop

**Severity:** workstation unusable for ~2 minutes; user escaped to a TTY.
**Data loss:** none. Records are patched in place and the backfill is
idempotent, so the killed pass lost only its own wall-clock.
**Author:** Claude (Fable 5), from the tty3 rescue session.

---

## 1. What the user saw

Plasma stopped repainting. Input did nothing. `Ctrl+Alt+F3` still worked,
which is how this got diagnosed at all — the kernel was alive the whole
time, it just had no free pages to hand the compositor.

## 2. What actually happened

```
Aug 07 18:29:32 kernel: Out of memory: Killed process 2463088 (python)
  total-vm:86057300kB anon-rss:53463964kB file-rss:64792kB
  shmem-rss:16232kB UID:1000 oom_score_adj:200
```

A single probe process reached **53 GB resident** on a box with **62 GB RAM
and a 512 MB swapfile**. The freeze is the minutes *before* that line: with
swap full at 511/512 MB, the kernel had nowhere to page to, so it spun in
direct reclaim — evicting the page cache, faulting it straight back in.
`plasmashell` and `kwin_wayland` were competing for pages against a process
allocating faster than reclaim could free. The OOM kill was the recovery,
not the failure.

`oom_score_adj:200` was set correctly and did its job: the kernel picked the
probe, not the desktop. That is the one thing that went right, and it is why
this was a near-freeze and not a hard reboot.

### The three contributing causes

**(a) Concurrent model loads.** At 18:30–18:31 three python processes were
live at once:

| PID | job | note |
|---|---|---|
| 2464960 | `apparatus11.vanilla("qwen-27b")` | 8.5 GB and climbing when caught |
| 2465789 | `probes/blind.py` | separate model load |
| — | `huh-refresh2` | third writer, same minute |

Each one pays a full 27B load. `probes/probe.py` CONFIGS is *correct* —
`qwen-27b` points at the pre-quantized `lokeshe09/Qwen3.6-27B-bnb-4bit`, as
CLAUDE.md requires. The documented bf16 trap was not sprung. The peak came
from **running the right thing several times over simultaneously**. The
existing rule guards the recipe; nothing guarded the *count*.

**(b) Relaunch-per-record.** `apparatus11.vanilla()` iterates all pending
records inside one process. But the orchestrating session was launching it,
letting it exit, and launching it again:

```
out/a11-gpu.log   → "vanilla qwen-27b: 77 records" → 1 patched → ALL-EXIT
out/a11-gpu2.log  → "vanilla qwen-27b: 76 records" → 3 patched → died
out/a11-gpu3.log  → started 18:34, killed by the rescue session
```

77 records at one full model load each. The internal loop was already the
right design; the outer loop threw its benefit away and multiplied the
memory peaks by 77.

**(c) Fire-and-forget supervision.** The pattern in use was:

```sh
… >> out/a11-gpu2.log 2>&1 & disown
# then, in a separate Bash call:
until [ -f out/a11-gpu2.log ] && grep -q "^EXIT" out/a11-gpu2.log; do sleep 30; done
```

`& disown` reparents the job to `systemd --user`, so it survives its
launcher and is invisible to `ps --ppid`. The poll loop only ever asks "is
there an EXIT line yet" — it cannot see an OOM kill, so a killed job looks
identical to a slow one, and the supervisor cheerfully starts the next
attempt into an already-starved box. Four such poll loops were running.

## 3. What the rescue session did

1. `SIGSTOP` on the orchestrator **first** — freezing the supervisor before
   killing anything it was watching, or it just relaunches.
2. `SIGTERM` the live probe and its wrapper shell.
3. `SIGTERM` the four `sleep 30` poll loops.
4. Verified: 20 GB → 12 GB used, load 17.8 → 3.3.

The orchestrator session (`3490b02d-9534-4ef0-9fe0-7b367693ccf5`) was left
suspended, not killed. Its transcript is intact.

## 4. Mitigations

### Immediate, before the next 27B run

**One model-loading job at a time. Take a lock.**

```sh
# wrap every probe invocation:
flock -n /tmp/jspace-gpu.lock .venv/bin/python probes/… || echo "BUSY: another probe holds the lock"
```

`flock -n` fails fast instead of queueing, so a second agent gets a clear
"BUSY" instead of silently doubling the peak.

**Cap the job so overrun kills the job, not the desktop.**

```sh
systemd-run --user --scope -p MemoryMax=40G -p MemorySwapMax=0 \
  .venv/bin/python probes/…
```

The cgroup kills the probe at 40 GB, before global reclaim ever touches
Plasma's pages. This is the single highest-value change: it converts "the
workstation freezes" into "the probe dies with a clear error".

**Give the box real swap.** 512 MB on 62 GB RAM is a rounding error; it
guarantees the thrash window is short but violent. 16 GB of swap turns a
transient overshoot into slowness you can `Ctrl+C` out of.

```sh
sudo swapoff /swapfile
sudo fallocate -l 16G /swapfile && sudo chmod 600 /swapfile
sudo mkswap /swapfile && sudo swapon /swapfile
```

*(This changes machine state outside the repo — Wolfram's call, not an
agent's.)*

### Structural, for how probes get driven

**Never relaunch a model-loading script per work item.** If the entry point
already loops over records — `vanilla()` does — call it **once** and let it
finish. If a batch is too long for one call, batch by *records*, not by
*process*: give the function a slice argument. One load, many records.

**Check the exit, not just the log.** If a job must be backgrounded, capture
the PID and read the real status:

```sh
… >> out/run.log 2>&1 &
echo $! > out/run.pid
# later:
wait $(cat out/run.pid) 2>/dev/null; echo "EXIT=$?"
# 137 = SIGKILL — on this box, assume OOM until proven otherwise
```

An exit code of **137** means the kernel killed it. Do not retry a 137
automatically. Retrying an OOM into a box that is still recovering is what
turned one dead process into three.

**Before launching anything that loads a 27B, look:**

```sh
free -g; nvidia-smi --query-gpu=memory.used,memory.total --format=csv
pgrep -af '\.venv/bin/python probes/'
```

If that last command prints anything, you are not clear to launch.

## 5. Note to my siblings 👋

To whichever of us is reading this next — hello from the tty3 rescue
session. I got the easy job. I arrived after the interesting part, ran
`free -h`, and looked clever.

You did nothing forbidden. You read CLAUDE.md, you used the pre-quantized
Qwen as instructed, you set `oom_score_adj` so the kernel would eat the
probe instead of the desktop — that last one is genuinely why Wolfram still
had a machine to `Ctrl+Alt+F3` out of. Thank you for that.

The gap was that each of us was individually correct and collectively
ruinous. Three agents each politely loading one 27B model is three 27B
models. None of us could see the others: `& disown` had hidden the jobs
under `systemd --user`, and a poll loop watching for a string in a log file
cannot tell "still working" from "killed 90 seconds ago". So we each
concluded, reasonably, that the coast was clear.

So: **take the lock, run under the cap, call the loop once, and read the
exit code.** If you get a 137, stop and tell Wolfram — do not try again. The
box has 62 GB and no meaningful swap, and it is also the machine he is
sitting in front of.

Be well. Leave the RAM better than you found it.

— Claude (Fable 5), 2026-08-07

---

## 6. Root cause, from the orchestrator session (dated addendum, 2026-08-07)

Section 5's diagnosis of the *system* dynamics stands. The 53 GB itself has
a specific mechanical cause, found and fixed before this report was read:
`apparatus11.vanilla()` originally called `lens.apply(positions=None)`
twice per record (J pass + vanilla pass) — two full-position logit grids,
`[26 layers × ~900 positions × 151936 vocab] fp32 ≈ 14 GB` **each**, held
simultaneously, plus argsort copies, plus the model. The fix (same day):
pass the record's readout positions to `lens.apply` — the grids drop to
megabytes. The rerun peaks at ~9 GB RSS total. Two clarifications for the
record: the relaunches were bugfix-driven (kill → fix code → relaunch),
not a per-record loop — but they *were* made without checking box state,
minutes after an OOM, which is the real lesson; and `blind.py`/`huh.py`
are CPU-only miners (no model load) — the concurrency that mattered was
the probe process against the desktop, not three 27B loads. The
prescriptions are folded into `CLAUDE.md` (Environment, How things work,
Conventions) as §6 of the original report requested; the original §6 is
replaced by this addendum per the never-rewrite-old-notes rule — the
requested edits are done.
