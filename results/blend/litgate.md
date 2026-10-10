# blend-01 literature gate (2026-10-10, complete)

Checked against arXiv abs/HTML pages, ACL Anthology and repo READMEs. "Evenings" = GPU + coding for a first validated readout on the 3090 bench; my estimate, not from the papers.

## 1. Binding IDs
- **How do Language Models Bind Entities in Context?** Jiahai Feng, Jacob Steinhardt. arXiv 2310.17191 (v1 2023-10-26, v2 2024-05-06). ICLR 2024 per the repo README. https://arxiv.org/abs/2310.17191
- Models: LLaMA 13B/30B (default)/65B, Pythia family (repo: 70M–12B), Tulu-13B. No Gemma, no Qwen.
- Method: mean-difference vectors ΔE(k), ΔA(k), averaged over ~500 synthetic contexts (capitals, fruits, shapes, bios, ...), then validated by substituting/adding them (causal mediation). Assumes additivity; position interventions use RoPE.
- Artifacts: https://github.com/jiahai-feng/binding-iclr (TransformerLens; generates data; no precomputed vectors; authors used 4×A100).
- Port: **plausible with work**. Obstacle: only shown in ≥13B LLaMA / "sufficiently large" Pythia; never in a Gemma/Qwen chat model. 2 evenings.

## 2. Ordering ID
- **Representational Analysis of Binding in Language Models.** Qin Dai, Benjamin Heinzerling, Kentaro Inui. EMNLP 2024 main (2024.emnlp-main.967); arXiv 2409.05448 (v3 2024-10-25; v2 withdrawn; v1 title said "Large Language Models"). https://arxiv.org/abs/2409.05448
- Models: Llama2-7B (main, layer 8), Llama3-8B, Float-7B, **Qwen1.5-7B**, Pythia-6.9B (appendix).
- Method: PCA on entity-token activations at one layer; PC1 = "OI-PC" (ICA/PLS as checks). Editing along OI-PC re-binds entity to attribute (logit diff / flip). Data: box-tracking prompts (Kim & Schuster 2023) plus six templated relation sets, 1,000 contexts each.
- Artifacts: https://github.com/cl-tohoku/OI-Subspace
- Port: **straightforward**. Obstacle: none hard; OI may be partly positional, so keep their filler-word controls. 1 evening.

## 3. Variable binding
- **How Do Transformers Learn Variable Binding in Symbolic Programs?** Yiwei Wu, Atticus Geiger, Raphaël Millière. ICML 2025; arXiv 2505.20896. https://arxiv.org/abs/2505.20896
- Model: one GPT-2-like transformer **trained from scratch** (12 layers, d_model 512, 37.8M params). No pretrained LLM.
- Method: interchange interventions on residual stream and head outputs over synthetic dereferencing programs, across training checkpoints.
- Artifacts: https://variablescope.org (interactive); no code repo found.
- Port: **unlikely**. It is a training-dynamics result on a toy model; there is no readout to carry over. Cite as background only.

## 4. Lookbacks
- **Language Models Use Lookbacks to Track Beliefs.** Nikhil Prakash, Natalie Shapira, Arnab Sen Sharma, Christoph Riedl, Yonatan Belinkov, Tamar Rott Shaham, David Bau, Atticus Geiger. arXiv 2505.14685 (v1 2025-05-20, v3 2026-02-24). No venue on the arXiv page. https://arxiv.org/abs/2505.14685
- Models: Llama-3-70B-Instruct (main); appendix: Llama-3.1-405B-Instruct and **Qwen2.5-14B-Instruct**.
- Method: interchange interventions under a causal-abstraction model, with desiderata-based component masking (DCM) to learn the subspaces. Data: CausalToM, templated two-character stories; 80 clean/counterfactual pairs per experiment, only items the model answers correctly.
- Artifacts: https://belief.baulab.info (code + data).
- Port: **plausible with work**. Obstacle: the model must solve CausalToM; main result is 70B, and the sub-70B evidence is one appendix model. 3–5 evenings.

## 5. Rebinding circuit (found)
- **A retrieval conditioned rebinding circuit for dynamic entity tracking in large language models.** Soyoung Oh, Vera Demberg. arXiv 2606.08644 (v1 2026-06-07, v2 2026-09-11). Preprint. https://arxiv.org/abs/2606.08644
- Models: Gemma2-9B, **Gemma3-12B**, Llama3.2-3B, Llama3.1-8B (instruction-tuned).
- Method: five-stage greedy path patching (N=100), pruning heads under 1% contribution, then attention-pattern and Q/K binding-ID interchange interventions. Task: boxes/objects with one swap (after Kim & Schuster), N=300 held out. Circuits: 38/672, 83/768, 42/672, 40/1024 heads.
- Artifacts: https://github.com/sori424/dynamicET (contents not inspected).
- Port: **plausible with work**. Obstacle: discovery ran on one H100 80GB, ~16 h for Gemma-12B; ours is 8-bit on 24GB. Reusing their head list as a readout: 2–3 evenings. Rediscovery: a week or more.

## 6. Belief-state geometry
- **Transformers Represent Belief State Geometry in their Residual Stream.** Adam S. Shai, Sarah E. Marzen, Lucas Teixeira, Alexander Gietelink Oldenziel, Paul M. Riechers. NeurIPS 2024; arXiv 2405.15943. https://arxiv.org/abs/2405.15943. Toy only: 4 layers, d_model 64, context 10, trained on Mess3 / RRXOR HMMs. Affine regression from residual activations to exact belief states. No code URL in the paper.
- Follow-up in pretrained LLMs: **Large Language Models Develop Belief State Geometry In-Context.** Daniel Balcells, Andrew Jun Lee, Chirag Rastogi, Paul M. Riechers, Adam Shai, Xavier Poncini. arXiv 2609.17376 (2026-09-15, 87 pp). https://arxiv.org/abs/2609.17376
- Models (from the alphaXiv overview; arXiv HTML 404, PDF too large to fetch): Qwen3.5-9B (main) and 4B, Llama 3.1-8B, 3.2-3B, Gemma 4-E4B, E2B.
- Method: prompt with raw HMM token streams (40 HMMs, 20,000-token sequences), fit per-layer affine probes to the exact Bayesian belief state; held-out R² 0.83–0.99; patching/steering in the probe subspace.
- Artifacts: no code link found.
- Port: **straightforward for HMM prompts, unlikely for natural text**. Obstacle: needs ground-truth hidden states, which exist only for synthetic processes, so it cannot be read on the same tokens as the other lenses. 2 evenings.

## 7. Reward subsystem
- **Sparse Reward Subsystem in Large Language Models.** Guowei Xu, Mert Yuksekgonul, James Zou. arXiv 2602.00986 (v1 2026-02-01, v2 2026-05-11). Preprint. https://arxiv.org/abs/2602.00986
- Models: Qwen-2.5 SimpleRL-Zoo 1.5B/7B/14B, Qwen2.5-7B-PPO-Zero, Llama-3.1-8B-Instruct, **Gemma-3-4B-it**, Phi-3.5-mini.
- Method: two-layer MLP value probe on hidden states at each generation step, trained by TD error against binary final correctness; "value neurons" = hidden dimensions ranked by L1 norm of probe input weights. "Dopamine neurons" = top 50 dimensions per layer by peak-minus-trough of smoothed activation on positive- vs negative-surprise samples. Data: GSM8K, MATH500, Minerva Math, ARC, MMLU-STEM.
- Artifacts: no code found.
- Port: **plausible with work**. Obstacle: hundreds of long sampled reasoning traces with graded answers (generation up to 16k tokens); dopamine neurons shown on the 14B RL-tuned Qwen only. 3–4 evenings on Gemma-3-4B.

## 8. Anthropic (exist)
- Emotion Concepts and their Function in a Large Language Model, 2026-04-02. https://transformer-circuits.pub/2026/emotions/index.html, arXiv 2604.07729.
- Verbalizable Representations Form a Global Workspace in Language Models, 2026-07-06. https://transformer-circuits.pub/2026/workspace/index.html, arXiv 2607.15495.

## (a) Corrections to the handoff
- 5 is Oh & Demberg, 2606.08644. Claim matches.
- 6: first author is Shai, not Riechers (Riechers is last). The LLM follow-up exists and includes Qwen and Gemma.
- 3 is a from-scratch toy model, not an LLM result.
- 4: 70B main model; Qwen2.5-14B in an appendix.
- 2: EMNLP 2024. 7: Xu, Yuksekgonul, Zou; "neurons" are hidden-state dimensions, so 4-/8-bit weights are no obstacle.

## (b) Not verified
- Model list and details of 2609.17376 beyond the abstract (secondary source).
- Contents of the dynamicET and belief.baulab.info code.
- Peer-review venue for items 4, 5, 7 (none stated on arXiv).
- Seen in search only, unread: "Mixing Mechanisms: How Language Models Retrieve Bound Entities In-Context" (arXiv 2510.06182); Dai et al. "Cell-Based Representation of Relational Binding" (ACL 2026, arXiv 2604.19052); Piotrowski et al. 2502.01954.

## (c) Cheapest two to port first
1. Ordering-ID PC (item 2): PCA, public code, already shown on a 7B Qwen. The same box prompts feed item 1's mean-difference vectors and item 5's task.
2. Value probe (item 7) on Gemma-3-4B, the only non-binding readout already shown on a bench model that works on ordinary text. Item 6's probes are cheaper but only read HMM prompts.
