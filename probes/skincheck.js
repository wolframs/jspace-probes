/* Contract check for dashboard/skins/*.css — run in the page:
     chromium --headless=new --virtual-time-budget=3000 \
       --dump-dom 'http://localhost:8321/dashboard/?theme=dark&skin=core'
   is not enough (we need computed styles), so this is meant to be pasted
   through the devtools evaluate hook. Returns [] when the skin is clean.

   It checks the four things a skin can silently break (skins/CONTRACT.md §4):
     1. the --seq-* ramp stays a monotonic 5-step scale (it encodes rank data)
     2. --s1..--s8 all stay defined and mutually distinguishable
     3. #termpop stays position:absolute (the popover math assumes it)
     4. --fg stays UNdefined (defining it wakes a dormant unstyled rule)
   Theme correctness is checked separately, per theme, by the caller. */
(() => {
  const cs = getComputedStyle(document.documentElement);
  const v = (n) => cs.getPropertyValue(n).trim();
  const bad = [];

  // --- 1. sequential ramp: parse to relative luminance, require monotonic
  const steps = ["--seq-100", "--seq-250", "--seq-400", "--seq-550", "--seq-700"];
  const lum = (c) => {
    const d = document.createElement("i");
    d.style.color = c; document.body.appendChild(d);
    const m = getComputedStyle(d).color.match(/[\d.]+/g); d.remove();
    if (!m) return null;
    const [r, g, b] = m.slice(0, 3).map((x) => {
      const s = x / 255;
      return s <= 0.03928 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4;
    });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };
  const ls = steps.map((s) => (v(s) ? lum(v(s)) : null));
  if (ls.some((x) => x === null)) bad.push("seq ramp: a step is undefined");
  else {
    const up = ls.every((x, i) => i === 0 || x > ls[i - 1]);
    const dn = ls.every((x, i) => i === 0 || x < ls[i - 1]);
    if (!up && !dn) bad.push(`seq ramp not monotonic: ${ls.map((x) => x.toFixed(3))}`);
  }

  // --- 2. categorical slots
  const ss = [1, 2, 3, 4, 5, 6, 7, 8].map((i) => v(`--s${i}`));
  ss.forEach((c, i) => { if (!c) bad.push(`--s${i + 1} undefined`); });
  if (new Set(ss.filter(Boolean)).size < ss.filter(Boolean).length)
    bad.push("--s1..--s8 contains duplicates");

  // --- 3. popover positioning
  const pop = document.getElementById("termpop");
  if (pop && getComputedStyle(pop).position !== "absolute")
    bad.push(`#termpop position is ${getComputedStyle(pop).position}, must be absolute`);

  // --- 4. the dormant --fg trap
  if (v("--fg")) bad.push(`--fg is defined (${v("--fg")}) — wakes app.js:1155`);

  return bad;
})()
