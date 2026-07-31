**The short version.** We pushed a slang-word direction hard into Qwen 27B's early layers, the wrong depth for this test, and the answer broke apart.

**What we did.** We pushed a lens direction for informal words into Qwen 27B's state, at a fixed strength, on every step. The push targeted layers 2 to 8. This depth is early, before the workspace band that later work in this lab found is the right place for this kind of push.

**What we found.** The output was not the requested answer. The text broke into repeated quote marks and blank lines, even though "whilst" itself reached rank 1 to 2 at these layers. The layers built on top of it lost their normal structure.

**What it means.** This push broke the model's chain of computation at this early, wrong depth, before the text took a coherent shape. Seven early layers each added the same push. We think the effect grew larger at each one, before the layers that decide meaning were built.

**What this does not show.** This does not show that steering never works. A matched push at a later, correct depth changed the content without breaking the answer.
