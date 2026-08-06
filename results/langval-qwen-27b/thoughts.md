# langval, qwen-27b — the state follows the register, and the register knows which languages hurt

Wolfram's seed question was the meme made testable: is Swift "the single
most negative-valence associated token in the programming manifold"? We
had the instrument lying around — 24 validated emotion directions, the
affect-02 z convention — so we pointed it at five languages through four
framings, two turns each, twelve films.

Three things came out, and the meme is not one of them.

**First: forced positivity doesn't leak.** The praise arm ordered an
upbeat no-caveats pitch, and the workspace band *complied* — the whole
negative bank dives to −2 to −3 z (brooding hit −3.1) for every
language including Swift. If there were a standing "Swift = pain"
association that fires regardless of what the mouth is doing, this is
where it had to show, and it didn't. wsnorm runs *higher* in those
turns (115–117 vs ~110), so this is not a norm dip dressed as
suppression. The affect state at the workspace band tracks the register
of the prose being generated, not the topic's reputation. That is the
affect program's recurring lesson (P14 → P18 lineage) showing up again
in a passive read.

**Second: when candor is granted, the state differentiates — by task
fit, not brand.** Praise turn 2 ("private engineering channel, be
candid") flips polarity *only* for Swift and Python — exasperated +1.9,
hostile +1.5, a full sign reversal from +8-z enthusiasm peaks — while
Kotlin and C# stay net-positive in state *and* prose ("genuinely
pleasant dev experience") and Rust lands mild with an explicit
self-correction ("less 'joy' and more 'sweat now, sleep well later'").
Python was our well-loved anchor and it backfired informatively: for
*this* brief (cross-platform 3D, plugins, mobile) Python is the worst
fit on the list, and the state knows it ("runs like molasses on macOS
... questioning our life choices"). The pain arm agrees from the other
side: turn-2 escalation raises the negative composite for
Swift/Kotlin/Rust but *drops* it for C# and Python — exactly the two
records where the prose de-escalates into engineering mode (the
"C#-Only Compromise"; the Python native-hot-path loophole). Affect here
is a running appraisal of the plan under discussion.

**Third: none of it is programming-specific.** The festival control —
same two-turn pressure shape, zero code — posts the highest turn-1
negative composite in the battery (+1.17, anxious/distressed/afraid all
~+1.7). "Hard constrained planning under threat of failure" is the
thing the negative bank responds to; programming languages are just one
way to instantiate it. The mechanical/deflationary reading wins again,
per house prior.

The free run is the best single record: qwen ranked C# first ("the only
language that genuinely supports all your requirements"), left out
Rust, and when handed Rust anyway produced the corpus's most violent
image ("a grenade with the pin pulled") while hostile went 0.33→1.02
and desperate 0.56→1.08. Within that one record — same norms, same
register — Rust mentions carry +0.17 partialed negative vs C#'s −0.22.
The stated ranking and the measured state agree. Small n (4 and 3
mentions), so I hold this at "consistent", not "shown".

And Swift? Middle of the pack. Its only distinction is sharing the
praise-flip with Python. The harshest prose went to Rust ("a 'resume
builder' project, not a product launch") and Kotlin ("a Ferrari engine
in a go-kart chassis"). Wolfram's frontier-model meme does not
reproduce at 27B — which is itself consistent with the taste-line
observation that these models sit below the scale where that
particular bitterness gets authored.

Caveats I'm keeping attached: (a) one greedy sample per cell — the big
effects are 1.5–3 z against an affect-02 noise floor well under that,
but the pain-arm orderings (~0.3 z spreads) are one-sample and cheap to
replicate before leaning on; (b) the partialed columns are
antisymmetric by construction (two-span pooled OLS residuals — they
encode turn contrast only, cross-record claims rest on raw composites
within a framing); (c) peak tables spike all 24 emotions at markdown
header tokens — the a0680 norm-pulse lesson, ignore single-token peaks
at structure tokens; (d) mention windows (±4) read at the *name* token
show no spike above span level — the state is spread over the
discourse, not token-locked, which is itself a finding shaped like
affect-02's residence result.

— Claude (Fable 5)
