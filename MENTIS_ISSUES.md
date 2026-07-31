# Mnestis issues — observed 2026-07-31, fork `fix/python-call-graph-accuracy`

Found during first sustained MCP use (plain-language close-out session).
Repro context: scan root `probes/`, output `.mentis/`, server = local fork
0.3.4 via `.mcp.json`. Items 1–2 are the ones that actively mislead.

1. **`query_graph` silently substitutes an unknown symbol and answers with
   high confidence.** Asked "what breaks if check_plain_md in ste.py
   changes?" while `ste.py` was not yet indexed → it answered about
   `_inline_md` (a different function in a different file), confidence
   0.92, no "symbol not found" signal. `impact_analysis` has a NOT_FOUND
   path; `query_graph` needs the same instead of nearest-name fallback.

2. **`search` cannot find real files/symbols; results are meta-doc noise.**
   `search("ste plain checker")` and `search("plain language checker ste")`
   never return `ste.py` (even after a rebuild that indexed it — direct
   `impact_analysis("check_plain_md")` resolves fine). Top hits: "ste"
   substring-matches `Steering`, affect-file critical-path cards, and
   "graph-expanded" hits whose snippet is just the node id
   (`file:affect.py`, score 0.45) — zero information. Looks like the BM25
   corpus is built over summary cards (critical paths, smells) rather than
   file/symbol nodes.

3. **No staleness signal.** Three probe files added after the last build
   (`ste.py`, `plain.py`, `apparatus09.py`) were simply absent; every tool
   answered from the stale graph without warning. Build history knows
   `builtAt`; tools could cheaply compare scan-root mtimes and flag.

4. **Contradiction detector treats build churn as fact conflict.** After a
   legitimate rebuild, `search` results now carry a `high` severity
   unresolved contradiction: domain cluster "45 files" (old build) vs
   "46 files" (new build). Same document id, different `builtAt` — this
   will accumulate one fake contradiction per rebuild.

5. **DNA/health output is template filler for this repo.** "0 capabilities,
   1 domain, 0 APIs", health 85/100, and recommendations that (a) do not
   apply ("Add clear entry points (routes, handlers)") and (b) are
   duplicated verbatim in the same array ("Reduce dependencies by
   extracting shared utilities or applying dependency injection" ×2).

6. **Scan-root scoping leaves half the lab invisible.** `dashboard/app.js`
   (~4k lines, the entire front-end) can never be indexed because scanning
   from repo root is forbidden (hardcoded ignore list walks `.venv`, 5.2 GB,
   box has no swap — see CLAUDE.md). The real fix is an `--ignore` /
   `.gitignore`-respecting scanner; then the scan root could be `.` and
   include `dashboard/`.

7. **Rebuild noise is growing.** A rebuild now dirties 53 tracked files in
   `.mentis/` (was 31), almost all `builtAt`/`durationMs` timestamp churn.
   Output should be deterministic modulo real content.

Known and already documented in CLAUDE.md (kept there, listed for
completeness): `build` clobbers `AGENTS.md` at scan root; `memory_*`
episodes never reach the retrieval index; line numbers 0–2 lines early;
bare-name `impact_analysis` on duplicated names (`main` ×32) picks
silently; server self-description ("mandatory memory layer", 7-step
workflow) is vendor copy that conflicts with repo policy.
