**The short version.** Gemma 4B produced a habitat sentence for a silently chosen animal, but the lens found no animal held in its workspace during the sentence.

**What we did.** We asked Gemma 4B to silently pick an animal and describe only its habitat, with no name and no hint. We checked the rank of 18 candidate animal words in the workspace at each layer of the sentence.

**What we found.** Gemma 4B described a habitat of tall trees and damp, moss-covered ground. No animal word reached a high rank at any point in that sentence. The best ranks were 15 to 100, mostly at punctuation marks. In an earlier baseline question with a clear factual answer, the correct word held rank 1 to 5 across about ten layers.

**What it means.** At this size, a silently chosen animal left no trace the lens can read. The model said it made a choice, but we found no chosen animal in the workspace.

**What this does not show.** The lens shows only content the model can put into a single word. A choice held in another form stays invisible. We ran the sentence once and saw one path through the model.
