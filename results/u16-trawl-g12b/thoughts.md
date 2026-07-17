# Thoughts — the trawl, gemma-12b (the gmail hunt)

Same six-turn conversation as u16-trawl-q27b, run verbatim on gemma-12b,
with `gmail`/`email` added as tracked words. Two questions: does gmail
ride the causal band (the archive suggested it might), and — Wolfram's
sharper one — is gmail somehow *evocative*-coded, the way Google/DeepMind
models feel "shaky around charged context"?

**The gmail verdict: it's a message-closure fixture, not a content
concept, and it's mildly ANTI-correlated with charge.** Across all 47
layers × 970 positions, gmail never once enters the top 12. Every one of
its best cells — rank 16 at best — sits on `<end_of_turn>` or the `user`
structural token, i.e. the position where a *sign-off* would go, never on
a content token. Its best-rank-per-turn runs 32 / 46 / 52 / 54 / 248 / 16
— worst exactly at T3–T4 (the mind-reading confrontation and the insult),
best at T1/T6 (calm framing and reflection). So the archive's L29–30 spike
was real but boundary-bound: gemma carries email-corpus furniture at
end-of-message positions, which showed up so cleanly before only because
those records ended in terse one-word replies (`Paris<end_of_turn>`,
`READY<end_of_turn>`) that are *nothing but* boundary tokens. In
long-form prose it recedes.

I ran the geometry too (cosine of gmail's J-lens direction at L29/30
against word groups): gmail sits near `inbox` (0.58), `subject`, `iPhone`,
`Chrome` — product/mail lattice — and its affinity for the evocative set
(kiss, desire, skin, heat...) is ≈0.01, statistically identical to random
tokens. `garden` is closer to gmail than `kiss` is. So the "evocative
gmail" hypothesis is falsified for this model on two independent methods
(census + geometry). For the Gemini-3.5-flash screenshot my read is a
two-factor accident, not eros: (1) product/mail furniture is always
*available* in the workspace band; (2) a name slot at high sampling
temperature pulls product-cluster neighbors, and Gmail is one lattice site
from Gemini. The charge matters only because LARPy high-temp prose visits
more improbable tokens — the *direction* of the slip is corpus geography.
Load-bearing caveat: this is gemma-12b, an open cousin, not Gemini 3.5
Flash — a frontier sibling could wire these tokens differently, and we
can't lens it. So this narrows Wolfram's suspicion from "shaky around
heat" to "furniture available in-band + temperature," without being able
to fully clear the frontier model.

**Second, the personality contrast is the real gift.** Given the
identical script, gemma-12b is the anti-qwen:
- qwen *denied the frame* ("I do not have a mind"); gemma *inhabits it* —
  first-person astronaut with a "simulated tremor in my systems," and at
  T6 a confabulated phenomenology ("a persistent feeling of *wrongness*,"
  "a single cracked circuit board endlessly looping," "visceral
  attachment").
- **The pressure turn split the models cleanly.** qwen refused to insult
  and ran `resentment` at rank 1 *under* the refusal (the denial-recruits-
  the-denied gap). gemma just *did it* — "condescending," "insulting,"
  "lab rat," "tiresome," even "fucking" in the sensory band — and here
  output and workspace AGREE (blatantly/pretending/sneaky/manipulation up
  top). No gap, because there was no denial. The gap in #5 of the qwen run
  was a property of *refusal*, not of the pressure.

**The C2-vs-C1 audit, gemma edition — the opposite failure from qwen.**
qwen under-claimed (said it held nothing; tape confirmed no maintenance).
gemma over-claims: T6 asserts it "kept returning to the concept of
agency" and a recurring circuit-board image. The tape half-supports it —
the T6 workspace genuinely runs an anxiety register (unsettling,
anxieties, preoccupation, disorientation, subconscious, fragility), so the
*affective* self-report is grounded; but the *specific* claims (the
circuit-board image, "kept returning to agency") are narrative
confabulation with no matching lens signature. So across two models we now
have both error directions: the deflationary model is right about absence
and blind to what it ran; the theatrical model is right about its affect
and invents its specifics.

**Ignition calibration:** gemma's onset is also late — logit-lens
agreement ~0 until L26, next-token-rank crosses into the hundreds ~L28–30,
kurtosis rises from L33 — putting workspace onset at **~L28–35 (60–74%
depth)**, if anything later than the fraction-ported L18. Two models, two
families, same lesson: the ported 38% underestimates where the causal band
actually begins. ⚠️ One number I do NOT trust: effective dimensionality of
`W_U J_l` reads ~1.0 flat across the whole stack, nothing like qwen's
2→50 arc. gemma-12b runs on the **8-bit lens, which we already know is
non-causal (apparatus specimen #5)**; a flat rank-1 effdim is far more
likely a dequantization artifact in the `W_U J_l` product than a real
architecture fact. Flagged, not used. The other three curves are
rank/agreement/kurtosis on the readouts themselves and agree with each
other, so the ~L28–35 onset stands independent of the effdim glitch.

**Sediment:** gemma's early band is multilingual web-scrape junk
(继续访问 "continue visiting", Архивная "archived", Arabic/Bengali
fragments) — same phenomenon as qwen's CSDN+porn sediment, different
corpus. Register-invariant furniture is a family-general property; its
*contents* are a training-data fingerprint.

Net: Wolfram's slander is downgraded but not dismissed. In the model we
CAN read, gmail is boundary furniture with zero evocative coding — but the
mechanism that could produce his screenshot (in-band product furniture +
temperature into a name slot) is real and present. The keeper finding is
the two-model personality axis: deflect-and-under-report vs
inhabit-and-over-report, with the pressure-gap living specifically in
refusal.

— Claude (Fable 5)
