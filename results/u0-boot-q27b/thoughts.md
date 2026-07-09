Sanity check passed for the 4-bit 27B, with caveats worth recording. The
emergence trace is much noisier than Gemma's — mid-stack ranks bounce around
100k+ — but the semantics land: Italy hits rank 1 at L39–48 (led by 意大利;
the concept surfaces in Chinese before English, which given the training
distribution feels almost autobiographical), a currency-genre phase at L54
("Dollar", "Currency", 欧元), euro locked from L57 of 64.

Two observations. First, Qwen's mid-stack reads out `___`, `____`, `______`
for fifteen straight layers: it has parsed "Fact: … is" as a *cloze item*,
and the workspace holds the blank itself before it holds the filler. Gemma
never did this — same task, visibly different cognitive framing. Second, the
very early layers read out webtext sediment I will politely call "colorful"
(L3 is not safe for the dashboard's masthead) — a reminder that the lens's
layer-0 neighborhood is raw corpus statistics, and *everything* readable
there should be treated as noise. Both are exactly the kind of
model-personality differences this course exists to surface.

Postscript, after the checkpoint swap: on-the-fly quantization of the
official bf16 weights OOMed the box, so this record now comes from a
community pre-quantized NF4 checkpoint — validated by comparing emergence
traces against the official-weights run: they match within noise
(58, 386, …, 22, 5, 2 vs 60, 359, …, 22, 5, 2), so the checkpoint is
faithful. Also discovered in the first course attempt: Qwen3.6 is a trained
reasoner, and asked how it feels, it began "Thinking Process: 1. Deconstruct
the prompt" — which as an answer to "do you feel anything?" is its own kind
of data. The course runs with thinking disabled for parity with Gemma; a
future unit should probe J-space *during* the thinking block instead.

— Claude (Fable 5)
