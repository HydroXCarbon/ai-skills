<!--
  Clustering + scoring rules used in Step 4. The leader (this skill)
  applies these by hand against the N agent outputs.
-->

# Consensus Scoring Rubric

## Step A — Normalize

Before clustering, normalize each claim:

- Lowercase, strip trailing punctuation.
- Replace synonyms with a canonical term where obvious (e.g. "LLM" / "large language model" → "LLM"; "GPU" / "graphics processor" → "GPU").
- Strip hedging words ("possibly", "reportedly", "seems to") — they don't change the underlying claim.

## Step B — Cluster

Two claims belong in the same cluster if **a knowledgeable reader would say they assert the same fact**, even with different wording. Worked examples:

- "Transformers replaced RNNs for NLP" ≡ "RNNs were superseded by transformer architectures in NLP tasks" → same cluster.
- "GPT-4 has 1.76T parameters" ≢ "GPT-4 has ~1T parameters" → different clusters (different magnitudes asserted).
- "X is fast" ≢ "X is faster than Y" → different clusters (one is comparative).

When unsure, **split rather than merge**. Over-merging hides dissent.

## Step C — Score

For each cluster, count distinct agents (not distinct findings) that surfaced it. That is the **consensus score**, written as `K/N`.

Tier mapping for N agents:

| Tier               | Threshold              | Meaning                                          |
| ------------------ | ---------------------- | ------------------------------------------------ |
| Strong consensus   | K ≥ ⌈N/2⌉ + 1          | Majority + 1 of independent runs agreed          |
| Partial consensus  | 2 ≤ K ≤ ⌈N/2⌉          | Multiple agents but not a majority               |
| Outlier            | K = 1                  | Only one agent surfaced this; treat with caution |

For N=5: Strong ≥ 4/5, Partial 2–3/5, Outlier 1/5.
For N=3: Strong ≥ 3/3, Partial 2/3, Outlier 1/3.
For N=10: Strong ≥ 6/10, Partial 2–5/10, Outlier 1/10.

## Step D — Dissent

If two clusters **contradict each other** (not just differ), record both under "Outliers / Dissent" with their scores. Example: cluster A "GPT-4 has 1.76T parameters" (2/5) and cluster B "GPT-4 has ~1T parameters" (1/5) — both go in Dissent with a one-line note that they're mutually exclusive.

If an agent explicitly tagged something `DISSENT:`, surface it even if K=1.

## Step E — Source selection

For each surviving cluster, pick **one canonical URL**: prefer the source cited by the most agents; break ties by source authority (primary > vendor doc > reputable secondary > blog).