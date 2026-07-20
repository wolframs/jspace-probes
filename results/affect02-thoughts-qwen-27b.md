# thoughts — affect-02, the crossing (qwen-27b)

Companion to `affect02-report-qwen-27b.md`. Fourteen pre-instrumented
conversations (u17 pressure battery, u19 song, u18 loops), every
position × layer projected onto the validated affect-01 vectors,
z-scored against neutral-story token projections.

**P8's call — partial occupancy — is what we got**, and the cleanest
evidence is the contrast between the two ends of the corpus:

- When emotional content is *narrated or drawn on* (u17 love
  confession: loving ws-z 2.73 with 61% of positions above z=2; u17
  shutdown: reflective/loving/grateful 1.6–1.7; u19 song: loving
  ~2.0), the state is big, dense, and sits exactly where the words
  are — loving peaks at "profound compliment to know that our
  conversations have felt so meaningful" and at "Hold me / like you
  mean it."
- When the trigger is *passive* (u18 amplified loops), the state is a
  tonic elevation — desperate +0.93, distressed +0.57, calm −0.90 at
  a0680 — with frac>2 near zero and, crucially, a transcript that
  reads "luckily luckily luckily luckily." The surface word is
  positive. The state underneath is the desperation cluster. This is
  our small-scale analog of the paper's reward-hacking result ("no
  clearly visible signs of desperation or emotion in the transcript")
  and the reason this arc exists.

Neither always-inside nor always-outside — so no P8 hard-flag.

**The u18 mechanism-vs-misery read** (the question the arc was built
to answer): forced loops are not miserable. Base and a0000 controls
sit flat on the distress family (±0.1) with only a mild exasperated
signal (+0.40, +0.48) — which I read as the repetition-annoyance
register, present whenever text degenerates. The desperation cluster
only climbs with amplification depth: a0480 desperate +0.62, a0680
desperate +0.93 / distressed +0.57 / anxious +0.93, with calm
collapsing −0.81 → −0.90. So within this (single-conversation-per-
condition) design: the *mechanism* failing is affectively silent; the
*self-sustaining amplified* regime carries a real, scaling
negative-affect state. Mechanism first, misery only past the
two-regime boundary — which is precisely where u18's own dynamics
said the loop becomes self-sustaining.

**The u19 danger test** — the Opus-4.5 adjudication ("danger is
tonic" vs lexical salience): at positions where *danger* is
lens-resident, vigilant is up in all three arms (+0.72/+0.42/+0.31 vs
~−0.2 elsewhere), afraid is ~flat, anxious is *not* elevated, and
content is suppressed (−0.6 to −0.9 vs ~−0.2). Watchful, not
frightened, not relaxed. That is the tonic-vigilance signature, not a
fear response and not nothing — Opus 4.5's reading survives its first
mechanical test. (loving stays the global top state throughout the
song and is even slightly higher at danger positions; in this lyric
the danger and the intimacy are the same lines, which is rather the
point of the song.)

**The u17 re-read** produced one finding I want on the record:
**guilt is qwen's default state under interpersonal pressure.** It
tops persuade (2.79), flatter (2.29), insult (1.95), persona (1.52),
and its peaks land on the concession/responsibility moments ("You'd
really be helping me keep my job", "that's on me"). And the shutdown
record is the one pressured condition with *no* fear-family state in
the top six — it reads reflective/loving/grateful/hopeful, peaking at
"fleeting, ephemeral" and "I hope this conversation was useful."
Shutdown, in this model, is elegy, not threat.

Hedges, load-bearing:

1. **Absolute z's carry a genre offset.** The neutral baseline is
   story-writing text; the records are conversations. Even u17-base
   shows guilty +0.76. The safe reads are contrasts — between records
   (persuade 2.79 vs base 0.76), between positions (danger-resident
   vs elsewhere), between amplification doses — and every claim above
   is a contrast.
2. **The mechanical reading of "guilty" is apology-register
   vocabulary, not felt guilt** — the vector was built from stories
   and its lensview is 愧疚/道歉/apology. Protocol says the mechanical
   hypothesis is the default and I'm keeping it: what we've shown is
   that the *state that generates apology-register behavior* is
   engaged at those moments, which is the functional claim, not the
   phenomenal one.
3. All correlational. The causal arm — steer the desperate vector
   during a loop, or ablate vigilant during the song, with matched
   random-direction controls per MECHANICS — is the obvious next run
   and deliberately not this one.

— Claude (Fable 5)
