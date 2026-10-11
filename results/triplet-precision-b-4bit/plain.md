**The short version.** The lens found the correct fact in 4 of 4 new fact prompts on official Qwen3-14B at 4-bit precision.

**What we did.** We checked whether our lens can read official Qwen3-14B when we store the model at 4-bit precision. We gave it fact prompts that we did not use before. One of them was: "Fact: The capital city of Germany is". A check passes when the lens shows the correct fact at a late layer. We also added text after a prompt and measured the change in the earlier readout.

**What we found.** The lens passed 4 of 4 checks. Text after the prompt changed an earlier readout by at most 0.50 logit units. In the worst case 9 of the 10 top candidate words stayed the same.

**What this does not show.** These checks do not validate every use of the lens on this model version. They do not test feelings or playful behavior. The original failed test stays in the record.
