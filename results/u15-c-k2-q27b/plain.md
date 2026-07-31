**The short version.** Qwen 27B answered correctly about a held item even though the lens ranked that word far outside its top 8.

**What we did.** We asked Qwen 27B to hold two items in mind: a whale and a lantern. We added one turn of unrelated text, then asked which one was the light source, and read the lens at that point.

**What we found.** The lens gave whale rank 2, inside its top 8. It gave lantern rank 21, outside the top 8. Qwen 27B still answered, "The lantern."

**What it means.** A low lens rank for one word did not mean the model lost it. The model still named it correctly right after.

**What this does not show.** The lens shows words the model was ready to say next. It does not show whether Qwen 27B held lantern in some other form. Absence from the top 8 is a limit of the lens, not proof the word was gone.
