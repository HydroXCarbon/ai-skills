---
name: stochastic-consensus-research
description: "Use when the user asks for stochastic consensus research, multi-agent consensus research, or wants N independent agents to converge on a researched answer. Spawns 5 researcher subagents in parallel on the same question, scores agreement, and reports consensus + dissent."
---

# Multi-Agent Consensus Research

## Overview

Researches a topic by spawning N independent subagents (default N=5) **on the same question** — not different angles. Each agent runs its own stochastic exploration. Findings are then scored by agreement: claims that appear across many agents are high-confidence consensus; claims that only one or two agents surface are flagged as outliers or dissent. Final deliverable is a PDF report at `./output/<topic-slug>/report.pdf` with raw agent dumps preserved for traceability.

## When to use

Trigger phrases include "stochastic consensus research on X", "multi-agent consensus on X", "have N agents agree on X", "research X with consensus scoring", "get a consensus answer about X".

Do **not** trigger for:
- Single-source lookups — use the `research` subagent.
- Multi-angle fan-out research — use `fan-out-research` instead (different angles, not consensus).
- Codebase exploration.

The distinguishing feature is **agreement scoring across identical prompts**, not coverage breadth.

## Arguments

Extracted from the user's prompt:

- **topic** — the primary research question or subject.
- **--agents N** — the number of parallel agents to spawn (default 5, min 3, max 10).

## Step 1 — Resolve topic and slug

- If a topic was provided in the prompt, use it. Otherwise ask via `ask_question` for the research topic.
- Slugify the topic for the output folder: lowercase, replace spaces with `-`, strip punctuation, collapse repeated `-`, cap at 60 chars.
- Run `test -d ./output/<slug>/`. If it exists, ask the user via `ask_question`:
  - **Overwrite** — proceed and replace existing files
  - **New slug** — append `-v2`, `-v3`, etc.
  - **Cancel** — stop

## Step 2 — Decide agent count

Default N=5. If the user passed `--agents N` in their prompt, use that count (clamp to min 3, max 10).

If the topic is ambiguous (multiple distinct meanings), ask once via `ask_question` to disambiguate before spawning agents.

## Step 3 — Spawn N agents in parallel (same prompt)

Use `invoke_subagent` with the `research` subagent type. **Dispatch all N agents in a single call with N parallel subagent entries.** Every agent receives the **same self-contained prompt** — that is what makes this stochastic consensus rather than fan-out:

- The full topic
- Instruction to independently research and return their best 5–10 findings
- Required output format: each finding as a one-sentence claim + a source URL + a 1-line justification
- Instruction to surface dissent if a common claim seems wrong
- Instruction to be skeptical of any single source — cross-check

See [references/agent-prompt.md](references/agent-prompt.md) for the shared prompt template.

## Step 4 — Score consensus and synthesize

Once all N agents return, score agreement:

- **Cluster claims** that say the same thing (normalize wording before comparing).
- For each cluster, count how many of N agents surfaced it → that is its **consensus score** (e.g. 4/5).
- **Consensus tier**: claims with ≥⌈N/2⌉+1 agents = "Strong consensus". 2–⌈N/2⌉ = "Partial". 1 = "Outlier / single-source".
- **Dissent**: if two clusters contradict each other, note both with their scores.
- Deduplicate URLs; keep the canonical source for each consensus cluster.

See [references/scoring-rubric.md](references/scoring-rubric.md) for the exact clustering and scoring rules.

## Step 5 — Generate the report

Before generating, confirm with the user via `ask_question`:

- **Generate PDF** — write the single consolidated markdown, then render PDF from it
- **Markdown only** — write the single consolidated markdown, skip PDF
- **Cancel** — stop without writing

**Both non-Cancel options produce ONE consolidated file** at `./output/<slug>/report.md`. Order:

1. **Title** — the research topic
2. **Date** — generation date
3. **Agents** — N and model name
4. **Sources & URLs** — full list, numbered, with one-line annotations
5. **Summary** — 2–3 paragraph executive summary
6. **Strong Consensus** — claims with score ≥⌈N/2⌉+1, each with its score and canonical source
7. **Partial Consensus** — claims with 2–⌈N/2⌉ agreement
8. **Outliers / Dissent** — single-agent claims and any explicit contradictions
9. **Tables** (optional) — only include if comparing entities/options across attributes
10. **Raw Agent Dumps** — one `### Agent N` subsection per agent, containing that agent's verbatim output

See [assets/report-template.md](assets/report-template.md) for the exact structure.

If the user picks **Cancel**, stop here and report what was synthesized in-chat. Nothing is written.

If the user picks **Generate PDF**, after writing the consolidated markdown, run the PDF generation script:

```
python3 .agents/skills/stochastic-consensus-research/scripts/stochastic-consensus-research.py \
  --markdown ./output/<slug>/report.md \
  --output ./output/<slug>/report.pdf \
  --title "<topic>" \
  --date "<YYYY-MM-DD>"
```

## Step 6 — Brief in-chat summary

After the PDF is written, print a terse summary to the user. Keep it under ~10 lines:

```
Topic: <topic>
Date: <YYYY-MM-DD>
Agents: <N> subagents (same prompt, independent runs)
Sources: <count> unique URLs
Strong consensus: <count> claims
Partial consensus: <count> claims
Outliers / dissent: <count> claims
Summary: <one-paragraph executive summary>
Output: ./output/<slug>/report.pdf
```

Do **not** dump the full report into chat — that defeats the PDF deliverable.

## Open questions

If the topic is ambiguous (multiple distinct meanings), ask via `ask_question`:

- **{Interpretation A}** — research the topic in this domain
- **{Interpretation B}** — research the topic in this domain
- **Both / broader** — let each agent decide and score interpretations separately

If `./output/<slug>/` already exists, ask via `ask_question`:

- **Overwrite** — replace existing files in that folder
- **New slug** — append `-v2`, `-v3`, etc.
- **Cancel** — stop without writing

## Hard rules

- Always spawn at least 3 parallel agents; default 5; cap at 10. Never run as a single-agent.
- All N agents receive the **same prompt**. Differentiation comes from sampling randomness, not author-assigned angles. Author-assigned angles = `fan-out-research`, a different skill.
- All N subagent dispatches must be in a single `invoke_subagent` call (parallel), never sequential.
- Never dump the full PDF content into chat; the in-chat summary is bounded (see Step 6).
- Never write outside `./output/<slug>/` — no edits to source code, no commits, no pushes.
- Always preserve raw agent dumps as the final section inside the single `report.md`.
- If PDF generation fails (missing dependency, etc.), report the failure and the path to the markdown intermediate — do not claim the PDF exists.
