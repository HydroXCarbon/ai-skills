---
# Skill slug. Lowercase kebab-case. Must match the folder name.
name: stochastic-consensus-research

# Trigger sentence Claude reads to decide whether to load this skill.
# Phrase as "Use when ...". This is the matcher — keep it specific.
description: "Use when the user asks for stochastic consensus research, multi-agent consensus research, or wants N independent agents to converge on a researched answer. Spawns 5 Sonnet researchers in parallel, scores agreement, and reports consensus + dissent."

# Optional. Hint shown to authors about what the skill expects as input.
argument-hint: "<topic>"
---

# Multi-Agent Consensus Research

## Overview

Researches a topic by spawning N independent Sonnet agents (default N=5) **on the same question** — not different angles. Each agent runs its own stochastic exploration. Findings are then scored by agreement: claims that appear across many agents are high-confidence consensus; claims that only one or two agents surface are flagged as outliers or dissent. Final deliverable is a PDF report at `./output/<topic-slug>/report.pdf` with raw agent dumps preserved for traceability.

## When to use

Trigger phrases include "stochastic consensus research on X", "multi-agent consensus on X", "have N agents agree on X", "research X with consensus scoring", "get a consensus answer about X".

Do **not** trigger for:
- Single-source lookups — use the `research` skill.
- Multi-angle fan-out research — use `fan-out-research` instead (different angles, not consensus).
- Codebase exploration — use `gsd-explore`.

The distinguishing feature is **agreement scoring across identical prompts**, not coverage breadth.

## Step 1 — Resolve topic and slug

- If `$ARGUMENTS` is non-empty, use it as the topic. Otherwise ask via `AskUserQuestion` for the research topic.
- Slugify the topic for the output folder: lowercase, replace spaces with `-`, strip punctuation, collapse repeated `-`, cap at 60 chars.
- Run `test -d ./output/<slug>/`. If it exists, ask the user via `AskUserQuestion`:
  - **Overwrite** — proceed and replace existing files
  - **New slug** — append `-v2`, `-v3`, etc.
  - **Cancel** — stop

## Step 2 — Decide agent count

Default N=5. If the user passed `--agents N` in `$ARGUMENTS`, use that count (clamp to min 3, max 10).

If the topic is ambiguous (multiple distinct meanings), ask once via `AskUserQuestion` to disambiguate before spawning agents.

## Step 3 — Spawn N agents in parallel (same prompt)

Use the `Agent` tool with `subagent_type: "general-purpose"` and `model: "sonnet"`. **Dispatch all N agents in a single message with N parallel Agent calls.** Every agent receives the **same self-contained prompt** — that is what makes this stochastic consensus rather than fan-out:

- The full topic
- Instruction to independently research and return their best 5–10 findings
- Required output format: each finding as a one-sentence claim + a source URL + a 1-line justification
- Instruction to surface dissent if a common claim seems wrong
- Instruction to be skeptical of any single source — cross-check

See [references/agent-prompt.md](references/agent-prompt.md) for the shared prompt template.

## Step 4 — Score consensus and synthesize

Once all N agents return, the leader (this skill, you) scores agreement:

- **Cluster claims** that say the same thing (normalize wording before comparing).
- For each cluster, count how many of N agents surfaced it → that is its **consensus score** (e.g. 4/5).
- **Consensus tier**: claims with ≥⌈N/2⌉+1 agents = "Strong consensus". 2–⌈N/2⌉ = "Partial". 1 = "Outlier / single-source".
- **Dissent**: if two clusters contradict each other, note both with their scores.
- Deduplicate URLs; keep the canonical source for each consensus cluster.

See [references/scoring-rubric.md](references/scoring-rubric.md) for the exact clustering and scoring rules.

## Step 5 — Generate the report

Before generating, confirm with the user via `AskUserQuestion`:

- **Generate PDF** — write the single consolidated markdown, then render PDF from it
- **Markdown only** — write the single consolidated markdown, skip PDF
- **Cancel** — stop without writing

**Both non-Cancel options produce ONE consolidated file** at `./output/<slug>/report.md`. No separate `raw/` dumps — everything is compacted into this single document for easy reading. Order:

1. **Title** — the research topic
2. **Date** — generation date
3. **Agents** — N and model name
4. **Sources & URLs** — full list, numbered, with one-line annotations
5. **Summary** — 2–3 paragraph executive summary
6. **Strong Consensus** — claims with score ≥⌈N/2⌉+1, each with its score and canonical source
7. **Partial Consensus** — claims with 2–⌈N/2⌉ agreement
8. **Outliers / Dissent** — single-agent claims and any explicit contradictions
9. **Tables** (optional) — only include if comparing entities/options across attributes
10. **Raw Agent Dumps** — appended as a final section with one `### Agent N` subsection per agent, containing that agent's verbatim output (traceability lives here instead of a separate folder)

See [assets/report-template.md](assets/report-template.md) for the exact structure.

If the user picks **Cancel**, stop here and report what was synthesized in-chat. Nothing is written.

If the user picks **Generate PDF**, after writing the consolidated markdown, run the PDF generation script:

```
python3 .claude/skills/stochastic-consensus-research/scripts/stochastic-consensus-research.py \
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
Agents: <N> Sonnet agents (same prompt, independent runs)
Sources: <count> unique URLs
Strong consensus: <count> claims
Partial consensus: <count> claims
Outliers / dissent: <count> claims
Summary: <one-paragraph executive summary>
Output: ./output/<slug>/report.pdf
```

Do **not** dump the full report into chat — that defeats the PDF deliverable.

## Open questions

If the topic is ambiguous (multiple distinct meanings), ask via `AskUserQuestion`:

- **{Interpretation A}** — research the topic in this domain
- **{Interpretation B}** — research the topic in this domain
- **Both / broader** — let each agent decide and score interpretations separately

If `./output/<slug>/` already exists, ask via `AskUserQuestion`:

- **Overwrite** — replace existing files in that folder
- **New slug** — append `-v2`, `-v3`, etc.
- **Cancel** — stop without writing

## Hard rules

- Always spawn at least 3 parallel agents; default 5; cap at 10. Never run as a single-agent — that's the `research` skill.
- All N agents receive the **same prompt**. Differentiation comes from sampling randomness, not from author-assigned angles. Author-assigned angles = `fan-out-research`, a different skill.
- All N Agent dispatches must be in a single message (parallel), never sequential.
- Always default subagent model to `sonnet`.
- Never dump the full PDF content into chat; the in-chat summary is bounded (see Step 6).
- Never write outside `./output/<slug>/` — no edits to source code, no commits, no pushes.
- Always preserve raw agent dumps as the final "Raw Agent Dumps" section inside the single `report.md` — never write a separate `raw/` folder.
- If PDF generation fails (missing dependency, etc.), report the failure and the path to the markdown intermediate — do not claim the PDF exists.