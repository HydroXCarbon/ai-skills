---
name: research
description: Research a topic by searching the web and fetching primary sources, then export a structured summary plus raw sources to ./output/<topic-slug>/. Use when the user asks to research, investigate, look into, deep-dive, or find out about a topic.
argument-hint: "<topic to research>"
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
  - Write
  - Edit
  - AskUserQuestion
  - Bash(mkdir:*)
  - mcp__plugin_context-mode_context-mode__ctx_fetch_and_index
  - mcp__plugin_context-mode_context-mode__ctx_search
---

# Research

## Overview

Run a focused research pass on a topic supplied by the user, then export findings as a folder under `./output/<slug>/` containing a synthesised summary and the raw sources used. One pass per invocation — no automatic refinement loop.

## When to use

Trigger phrases include "research X", "investigate X", "look into X", "deep dive on X", "find out about X".

Do **not** trigger for plain explanation requests ("explain X", "what is X"), debugging, or codebase questions — those are different skills.

## Step 1 — Slugify the topic

Topic source: `$ARGUMENTS`.

Slugify → lowercase kebab-case (`React Server Components` → `react-server-components`). Strip punctuation; collapse whitespace to single hyphens.

## Step 2 — Pick the output directory

- Target: `./output/<slug>/`
- If it already exists, suffix with `-2`, `-3`, … until you find an unused name.
- Create it: `mkdir -p ./output/<slug>/sources`

## Step 3 — Search and select sources

`WebSearch` for the topic. Pick **5–8 URLs**, biased toward primary sources: official docs, RFCs, project READMEs, vendor engineering blogs, well-known specs. De-prioritise SEO/content-farm pages.

## Step 4 — Fetch and store sources

Fetch each URL sequentially (deterministic numbering matters for citations):

- `WebFetch` the URL.
- `Write` it to `./output/<slug>/sources/NN-<domain>.md` (e.g. `01-react.dev.md`). File header:
  ```markdown
  # Source NN
  - URL: <url>
  - Fetched: YYYY-MM-DD
  ---
  <fetched body, lightly trimmed of nav/footer if obvious>
  ```
- Also call `ctx_fetch_and_index` on the same URL with `source: "research/<slug>"` so the page is indexed for later `ctx_search`. Treat as fire-and-forget — if it fails, log a one-line note in the summary's "Open questions / gaps" section but keep going.
- If `WebFetch` itself fails, skip the URL, do not advance the NN counter, and note the skip in the summary.

## Step 5 — Write the summary

Write `./output/<slug>/summary.md` in this exact structure:

```markdown
# <Topic>

- Date: YYYY-MM-DD
- Sources: N

## TL;DR
<2–4 sentences>

## Key findings
- Finding one. [1]
- Finding two, contrasted with finding three. [2][3]
- …

## Open questions / gaps
- What the sources didn't cover, or where they disagreed.

## Sources
1. <URL> — one-line takeaway
2. <URL> — one-line takeaway
…
```

Every `[N]` citation in **Key findings** must match a numbered entry in **Sources**. Don't invent claims that aren't grounded in a source.

## Step 6 — Print the result

Print the absolute path to `summary.md` so the user can open it directly.

## Open questions

If `$ARGUMENTS` is empty, ask the user for the topic via `AskUserQuestion` before doing anything else — never guess.

## Hard rules

- One pass per invocation. If the user wants more depth, they re-invoke with a narrower topic.
- Never overwrite an existing topic folder; always suffix with `-2`, `-3`, …
- Sources are fetched **once** and saved locally; do not re-fetch the same URL within a single run.
- `ctx_fetch_and_index` is for *future* searchability; its failure must not block local file output.
- The skill writes only inside `./output/`. It does not commit, push, or modify anything else in the working tree.
