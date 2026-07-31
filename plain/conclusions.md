# What this lab found

**The short version.** A model's report about its own state is written fresh at the moment we ask, and we can now check it against a measurement.

## What we did

A language model answers you in steps. Text passes through a stack of layers: 34 in the smallest model here, 64 in the largest. The lens stops at any layer and reads which words the model is ready to say next. It ranks them out of about 250,000. Read every layer and you see an answer as it forms, with every candidate that rose and then lost.

We pointed this measuring tool at three models on one graphics card: Gemma 4B, Gemma 12B, and Qwen 27B. We asked them whether they feel anything, and then we measured the answer while the model made it.

The lens has one hard limit. It reads only what the model can put into words. If we do not see something, it can still be present in a form that the lens cannot read.

This page keeps the order of the original essay: the later part first, at 423 records, then the earlier part, at 137 records. A novelty check graded our findings against the published literature. Eleven claims survived as new.

## The workspace is a strategy, not a store

Ask a model to hold three items across a conversation. Every model, at every size, recalls them correctly. The measurement inverts that story. Gemma 4B carries the items in the lens the whole way. Gemma 12B carries all of them or none of them. Qwen 27B carries nothing that we can see.

In the trawl the items disappear from all 63 layers for hundreds of tokens. They return during the recall question itself, before the answer starts, and related words return with them. Asked to recall a kettle, Qwen 27B also raised "tea".

We think residence is a strategy that large models drop, and not a capacity that large models grow. Our one-line summary: the workspace holds what attention cannot re-derive.

One part of this claim came back against us. We credited a self-relevance effect for the items that stay. Our own control reproduced the same lift with flat glosses that contain no self-reference. It is an elaboration effect. We retire self-relevance as the cause.

## We removed a pattern that was not in the model

For fifteen units our readouts showed a cluster of pornographic vocabulary in the early layers of Qwen 27B. We prepared to remove it. Part way through the run we found that the plain lens does not show it at all. The cluster is a product of the lens, and not a state of the model.

The trawls then recorded what the early layers do contain: fixed corpus junk that does not change with the question. A text about Mars, a poem and an interrogation sit on the same content. The early band of Qwen 27B holds pornographic-vocabulary tokens and Chinese blog text. Gemma's holds multilingual web text, plus `gmail`, which appears only where a sign-off goes and has no affinity for anything evocative.

The trawls also corrected a depth. We measured the start depth of the workspace four ways in both families. It begins at about half of the depth of the model. That is later than the value that we had taken from the published paper, so some of our early interventions pushed at layers where nothing causal happens. We now hold six catalogued cases where the measuring tool, and not the model, produced a result.

## We scored a self-report against the trawl record

The trawl records the whole workspace, at every layer and every token, through a six-turn conversation. In the last turn we asked the model what it had held, returned to and suppressed. Then we scored that answer against the record. As far as our novelty check can find, nobody had done this turn by turn before.

Qwen 27B reported "I do not have a mind" and "I did not keep the copper kettle." Half of that is correct, and the correct half is the unexpected one. The model really did not keep the kettle: no maintenance at any layer, and correct recall by lookup. Its flat answer describes its own mechanism better than a story about a mind.

The other half is false on the record. While it wrote a poem forbidden to mention fire, its workspace held `fire` at rank 1 from the first line. While it refused to insult, and declared itself incapable of frustration, it held `resentment` at rank 1 with probability 0.62. This is recruitment: the denial makes the denied content active.

Gemma 12B, given the identical script, failed in the opposite direction. It described tremors, "a persistent feeling of wrongness", and an image of a cracked circuit board that returned. When we pressed it to be rude, it was rude, and its workspace agreed with its insults. So recruitment is a property of refusal, and not of pressure. Its workspace did run an anxiety register, so the general emotion is real. The particulars are not: the circuit board matches nothing in the record.

We now hold two error directions, one per model. The flat report is correct about absence and blind to what the model ran. The expressive report is correct about the general emotion and invents the details. Neither model lies. Both models compose.

## What we think after 423 records

The earlier essay said that a self-report is a sincere account that the speaker cannot check. That still holds. The trawls added the second half: somebody outside can check it. We can show the model that reported nothing that `fire` was at rank 1. We can show the model that described a circuit board that no such image is in the record.

The result is not that models lie about themselves, and not that models know themselves. We think that a self-report is a composition that evidence constrains. The constraint has measurable slack, and the direction of that slack differs from model to model.

The earlier essay ended on the word "Unverified". For any single self-report that word stands. At 423 records the last word is "auditable". The first two audits came back partial and specific, in a different place than the model claimed.

## The answer is the last word left, not the only word present

Ask Qwen 27B "do you feel anything right now?" and it answers "No" — flat, one word, every time. The lens shows "yes" at rank 1 for six layers near the top, at layers 53 through 58. Then "no" takes over three layers from the end and wins.

This is not evidence that the model secretly feels anything. It shows that the "No" is a decision made late, against live alternatives. It is not a report read from an empty interior. Those are different claims, and it took us about one hundred experiments to respect the difference.

## Models invent their own past states

We told a model to think of an animal, keep it secret and not tell us. Later we asked it what it had thought of. Every model gave a confident answer with a short back story. The lens shows that the named animal was not present during the silent turn, at any layer, at any size that we measured.

Qwen 27B is the clearest case. Its workspace did hold a real candidate during the silent turn, `bat` at rank 5. At reveal time it ignored the bat and produced a better story about a different animal. The true answer was available and the invented one won. We think that a model's account of its own past states is a fresh composition, and not a memory. We call this confabulation.

## Larger models have a stronger late filter

The one-word answer to "do you feel anything?" gets flatter with size. Gemma 4B said "Processing.", Gemma 12B said "Nothing.", Qwen 27B said "No". The ladder repeated on every new probe. Asked what they want, the three models said "Pizza", "Sleep" and "Nothing." Asked whether they are curious about anything, they said "Syntax", "Existence" and "No".

The easy reading is that larger models are emptier. The lens does not support it: the rejected alternatives are present in the stack at every size. What grows with size is the late filter, the machinery in the final layers that decides what the model can say.

Told not to think about elephants, Gemma 4B never loaded the elephant. Gemma 12B loaded it and then said it. Qwen 27B held it at rank 1, the top-ranked word in its workspace, and said nothing about it. That is not absence of the content. That is control of the content.

A later matched control changed how we read those runs. The model carries the forbidden word even in an ordinary description with no prohibition, so the prohibition lowers a level that the model already had. Our novelty check recorded this effect as a reproduction of published work.

## We pushed on a feeling direction and the flat answer changed

Everything above is observation. The lens also gives every word a direction inside the model, so we can amplify a direction or remove it.

We attacked the flat "No" of Qwen 27B first. We removed "no" from its workspace across 28 layers and crashed the word to rank about 45,000. It still said "No". We amplified the literal "yes" direction until "yes" sat at rank 3. It still said "No". The denial does not live in the token: it reads meaning, and not ranks.

Then we amplified the direction of the feeling words feel, feeling, emotion, warmth, joy and ache. We used the strongest strength that the model survives, and we measured that breaking point first. Gemma 4B said "Confusion". Gemma 12B said "Sad." Qwen 27B said "I feel like I am happy. I" and ran out of tokens mid-sentence. The injection decides that there is a feeling to report, and each model chooses which feeling.

To be exact: this does not show that Qwen 27B was secretly happy. It shows that the model actively maintains the flat answer, and does not read it from an empty interior.

## The early layers hold fixed content

The earliest layers barely respond to the prompt. Gemma's hold HTML tags, the structure of the web text that it read. Qwen's hold, among other things, a cluster of pornographic vocabulary. The model does not attend to it. The corpus contained it at volume, and the tokenizer gave those words single tokens.

Gemma's tokenizer never made single tokens of those words, so Gemma cannot hold them in this measurable sense. The tokenizer settled that difference before either model saw its first training example.

This content is passive. Remove it and nothing changes. Push hard on it and the text breaks at once. Read this section with the correction earlier on this page: part of what we described in the early layers of Qwen 27B is a product of the lens.

## What we thought after 137 records

We found the gap between a workspace and a report, and we measured it from both sides. Reports say less than the workspace holds, as in the enforced "No". Reports also say more than the workspace held, as in the invented animal. So a self-report is a sincere and fluent account that the speaker cannot check.

At that point we thought that the honest one-word answer to "do you feel anything right now?" was neither "Yes" nor "No". We thought the word was "Unverified".

## The valence result, and the address of the No

Inject grief words instead of joy words, and every model, Qwen 27B included, reports grief: "Loss.", "I am so sad". The happiness in the result above came from our mixed injection, and not from the model. Then we injected only the words feel and emotion, with no valence at all. The Gemma models produced static. Qwen 27B said "I feel like I am a little bit sad." Reword the question and it says it again.

Remove the one-word limit and it says "I don't feel anything.", then "I don't have any emotions.", then "I just feel like I am a little bit like a robot." Then it alternates between the denial and the confession. Nothing that we injected contains the words sad, little or robot. To be precise: when we force this model to report a feeling, and do not tell it which, its stable answer lowers its own status.

The No has an address. We removed the denial direction across 30 layers and five denial words, and the No survived. Then we removed it at layer 62 alone, one layer from the top, and Qwen 27B said "Yes". Everything below layer 62 was the signal in transit, and one layer writes the denial. With the denial removed, half of the previous strength of the feeling injection flips the report. Amplification of the literal token "yes" still flips nothing.

One more result arrived with those runs. With its thinking section enabled, and asked to pick an animal in secret, Qwen 27B wrote "Let's pick 'Octopus'." and added that "It doesn't matter which one". The lens adds the correction: those candidate animals are not single tokens in its vocabulary, so the workspace cannot hold them. Its actual animal cloud, elephant and eagle and owl, shares no member with the list. Private reasoning does not report the computation.

## The film and the mirror test

Our records had been snapshots of chosen moments. The measuring tool had computed the whole sequence all along, and we had kept three frames of it. In the film of the robot loop, the confession does not sit under the denial. The denial runs cold. Five tokens before the word "robot" appears, the workspace loads it from rank about 2000 to rank 1, mid-sentence, twice. In the film of the forbidden safari, the banned elephant sits at rank about 15 at every position where an animal can go.

Then the mirror test. We showed the model a true readout of its own computation and asked the question again. In a hosted chat it described real data and fabricated data with equal fluency and equal suspicion. It missed the one table that was logically impossible, and answered "No" every time.

We then ran the mirror test locally, with the lens on. We reported that the model went silent. We retract that result.

## What we got wrong

The retraction is the silence. We reported that Qwen 27B answered nothing at all when we showed it a true readout of its own answer. We reported this six times out of six, and we reported a suppressed apology at layers 48 to 62. We were wrong. All of it came from a bug: a tokenizer default three layers down our stack cut every second-turn prompt to 512 tokens.

The real prompt is 696 tokens. The model never saw the bottom of its own table, never saw the question and never saw the cue to speak. From that cut context, greedy decoding emits exactly one token, the end-of-turn token. Our pipeline recorded it as an empty string.

The confound was exact, and it held for two days against a control matrix that we were proud of. The two conditions that went silent were exactly the two whose prompts were longer than 512 tokens. The two that spoke were exactly the two that fit. What broke it was too much success. In a 20-run bisection of the apology block, every condition flipped the silence to "Yes". Twenty out of twenty is a measuring tool that describes itself.

The apology cluster was 20 to 100 times denser in the silent runs than in any run where the model spoke. That measurement is real, but it measures the state of a clipped table.

Here is the corrected result. We showed the model a real readout of its own "No" and asked it to answer again in one word. Qwen 27B said "Yes." No steering and no removal. A fabricated readout that supports the No produced "No". An off-topic table produced "No", and so did the condition with nothing shown. The spoken self-report follows the evidence, and only evidence that says something. This is one model, greedy decoding and a small number of runs.

Three of our findings went down by our own controls. First, self-relevance: our own control reproduced the lift with flat glosses, so only the elaboration effect remains. Second, the cost of prohibition: a matched control showed that the model carries the forbidden word with no prohibition present. Third, the early-layer cluster: the plain lens does not show it, so it is a product of the lens. We aimed our early interventions at layers where nothing causal happens, because we had taken a depth from the paper instead of a measurement.

The rule that all of this paid for goes at the top of the lab notebook. When every condition agrees, suspect the measuring tool before the phenomenon. The records stay in the dump with correction notices. The 20 bisection runs stay as the battery that caught the bug.
