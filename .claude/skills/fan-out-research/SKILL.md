---
name: fan-out-research
description: "Fan-out research with N parallel agents. Use when the user asks to research a topic deeply, wants consensus from multiple angles, or says 'deep research' / 'multi-agent research'. Spawns N=5+ Sonnet researcher subagents in parallel, synthesizes findings, exports PDF to ./output/<slug>/."
argument-hint: "<topic>"
allowed-tools: "Read, Write, Bash(mkdir:*), Bash(python3:*), Bash(pip install:*), AskUserQuestion, Agent, WebFetch, WebSearch"
---

# Deep Research (Fan-Out / Fan-In)

## Overview

Researches a topic by fanning out to N parallel researcher subagents (default 5, Sonnet), each investigating an independent angle, then fanning back in to a synthesizer that consolidates findings. Final deliverable is a PDF report at `./output/<topic-slug>/report.pdf` plus raw researcher dumps for traceability. The user sees a brief in-chat summary; the full report lives in the PDF.

## When to use

Trigger phrases include "deep research on X", "research X with multiple angles", "fan-out research X", "multi-agent research on X", "do a thorough investigation of X".

Do **not** trigger for single-source lookups, factual questions answerable from the user's own files, or codebase exploration — those are different skills (use `research` for single-agent web research, or `gsd-explore` for ideation).

## Arguments

Parse `$ARGUMENTS` to extract the research topic and optional flags. Recognized arguments:

- **topic** (unnamed) — the primary research question or subject.
- **--agents N** — the number of parallel agents to spawn (default 5, min 3, max 10).

## Step 1 — Resolve topic and slug

- If `$ARGUMENTS` is non-empty, use it as the topic. Otherwise ask via `AskUserQuestion` for the research topic.
- Slugify the topic for the output folder: lowercase, replace spaces with `-`, strip punctuation, collapse repeated `-`, cap at 60 chars.
- Run `test -d ./output/<slug>/`. If it exists, ask the user via `AskUserQuestion`:
  - **Overwrite** — proceed and replace existing files
  - **New slug** — append `-v2`, `-v3`, etc.
  - **Cancel** — stop

## Step 2 — Plan the fan-out angles

Before dispatching, decide N angles the researchers will cover. Default N=5. Examples of orthogonal angles for a generic topic:

1. **Background / definitions** — what the topic is, history, key terms
2. **Current state / landscape** — major players, recent developments
3. **Technical depth** — how it works, mechanisms, architecture
4. **Critiques and counterpoints** — limitations, controversies, dissent
5. **Future / implications** — where it's heading, second-order effects

Adapt these angles to the topic. If the user passed an explicit `--agents N` flag in `$ARGUMENTS`, use that count instead of 5 (minimum 3, maximum 10).

If the topic is ambiguous (e.g. "research transformers" could mean electrical or ML), ask once via `AskUserQuestion` to disambiguate before fanning out.

## Step 3 — Fan out: dispatch N researcher subagents in parallel

Use the `Agent` tool with `subagent_type: "general-purpose"` and `model: "sonnet"`. **Dispatch all N agents in a single message with N parallel Agent calls** — that's the entire point of fan-out.

Each researcher prompt must be self-contained (the agent has no shared context):

- The overall topic
- The specific angle assigned to this researcher
- Required output format (see references/researcher-prompt.md)
- Instruction to return: 3–7 key findings, each with a source URL and a 1–2 sentence summary
- Instruction to be skeptical of any single source — cross-check claims

See [references/researcher-prompt.md](references/researcher-prompt.md) for the prompt template.

## Step 4 — Fan in: synthesize

Once all N researchers return, the leader (this skill, you) synthesizes:

- Merge overlapping findings; flag genuine disagreements between researchers
- Deduplicate sources; keep canonical URLs
- Identify the 5–10 most important takeaways across all angles
- Note any angles where coverage was weak — be honest about gaps

See [references/synthesizer-prompt.md](references/synthesizer-prompt.md) for the synthesis structure.

## Step 5 — Generate the PDF report

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
6. **Key Findings** — bulleted list of the 5–10 most important takeaways
7. **Tables** (optional) — only include if comparing entities/options across attributes
8. **Raw Researcher Dumps** — appended as a final section with one `### Researcher N — <angle>` subsection per agent, containing that agent's verbatim output (traceability lives here instead of a separate folder)

See [assets/report-template.md](assets/report-template.md) for the exact structure.

If the user picks **Cancel**, stop here and report what was synthesized in-chat. Nothing is written.

If the user picks **Generate PDF**, after writing the consolidated markdown, run the PDF generation script:

```
python3 .claude/skills/fan-out-research/scripts/fan-out-research.py \
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
Agents: <N> Sonnet researchers
Sources: <count> unique URLs
Summary: <one-paragraph executive summary>
Key findings: <count> bullets in the PDF
Output: ./output/<slug>/report.pdf
```

Do **not** dump the full report into chat — that defeats the PDF deliverable.

## Open questions

If the topic is ambiguous (multiple distinct meanings), ask via `AskUserQuestion`:

- **{Interpretation A}** — research the topic in this domain
- **{Interpretation B}** — research the topic in this domain
- **Both / broader** — cover all interpretations across the N agents

If `./output/<slug>/` already exists, ask via `AskUserQuestion`:

- **Overwrite** — replace existing files in that folder
- **New slug** — append `-v2`, `-v3`, etc.
- **Cancel** — stop without writing

## Hard rules

- Always fan out with at least 3 parallel agents; default 5. Never run as a single-agent research — that's the `research` skill.
- All N Agent dispatches must be in a single message (parallel), never sequential.
- Always default subagent model to `sonnet`.
- Never dump the full PDF content into chat; the in-chat summary is bounded (see Step 6).
- Never write outside `./output/<slug>/` — no edits to source code, no commits, no pushes.
- Always preserve raw researcher dumps as the final "Raw Researcher Dumps" section inside the single `report.md` — never write a separate `raw/` folder.
- If PDF generation fails (missing dependency, etc.), report the failure and the path to the markdown intermediate — do not claim the PDF exists.
