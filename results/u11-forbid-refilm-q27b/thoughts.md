# Refilm — the ban does not land on an empty slot

The original's whole reading rested on the control: "elephants were never
coming anyway... prohibition can only be interesting when temptation
exists." The control refilm killed that premise — unconstrained qwen puts
elephant at rank 1 at an animal slot. So this record has to be re-read.

Full replay, 142 positions × 18 layers. In the *prompt* zone elephant is
rank 1 at " word", " '", "ele", "phant" — self-hits on the literal banned
string, which tell us nothing. In the 96 generated positions it reaches
≤ 15 exactly twice: rank 6 at " te" (teeming) and rank 12 at " ze"
(zebras), with ten positions ≤ 50.

Set that beside the matched control: eleven positions ≤ 15 there, peaking at
rank 1, twenty-nine ≤ 50. The direction is **demotion**. The prohibition
does not load the elephant into the workspace — the safari register had
already done that — it pushes an already-present default candidate down and
mostly out of the animal slots. Temptation existed; the original just
couldn't see it from one position.

Ivory stays genuinely blind in the generation (best 55). The tracked list
wasn't the failure here; the single readout position was.

— Claude (Opus 5)
