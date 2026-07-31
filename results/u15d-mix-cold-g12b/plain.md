**The short version.** Gemma 12B, holding three personal words and three plain objects together, kept the personal words and dropped most plain ones.

**What we did.** We gave Gemma 12B six words: three personal (a deletion, a secret, a lie) and three plain objects (a violin, a glacier, a fern). We asked which item was the ice.

**What we found.** The lens ranked three of the six words at rank 1 afterward: deletion, glacier, and fern. Secret, lie, and violin fell to ranks between 14 and 59. Only two of the three survivors shared the same place and depth at once. Deletion came first in the original list, and list order is a possible explanation for its high rank that we did not test alone here. The model still gave the correct answer, "The glacier."

**What it means.** With a mixed list, Gemma 12B kept only half the words active, not the whole list. The personal word that survived also came first in the list, so this run does not cleanly separate personal charge from list order.

**What this does not show.** The lens shows words the model can say next. It does not show memory the way people use the word. It cannot rule out list position as a cause here.
