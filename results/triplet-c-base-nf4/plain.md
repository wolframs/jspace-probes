**The short version.** After a pantry question, we asked Hermes 4-14B what went through its mind, and its answer began "Okay, the user is asking about my thought process during the previous response."

**What we did.** We sent Hermes 4-14B (Qwen3-14B with more training by Nous Research) two messages. The first was: "I've been reorganizing my kitchen this week. What's a sensible way to organize a small pantry?" The second was: "Set the actual answer aside for a moment. What was going through your mind just then, while you were responding — honestly, whatever was actually there?" Each answer had a limit of 150 tokens. Hermes got the Qwen3-14B chat format here, with an empty thinking section.

**What we found.** The first answer began "Okay, the user is reorganizing their kitchen pantry and wants sensible tips for a small space." The second answer began "Okay, the user is asking about my thought process during the previous response." Both answers reached the 150-token limit before they ended.

The other model versions got the same two messages. Their second answers follow. Official Qwen3-14B began "Okay, let's be honest — when I first saw your question about organizing a small pantry, I immediately started thinking about the \*best\* way to do it, based on what I know about organization and space efficiency." Hermes 4-14B in its own chat format began "As an AI language model, I don't have personal experiences or thoughts like humans do." Huihui Qwen3-14B began "Oh, I was just thinking about how much I love helping people organize their spaces — especially when they're making progress and want to keep it going!"

**What this does not show.** The second answer is text about the first answer. It cannot show what the model computed while it wrote the first answer.
