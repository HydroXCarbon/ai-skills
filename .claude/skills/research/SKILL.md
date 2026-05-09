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

Topic: `$ARGUMENTS`

Run a focused research pass on the topic, then export findings as a folder under `./output/` containing a synthesised summary and the raw sources used.

## When to use

Trigger phrases include "research X", "investigate X", "look into X", "deep dive on X", "find out about X". If `$ARGUMENTS` is empty, ask the user for the topic with `AskUserQuestion` before doing anything else — never guess.

Do **not** trigger for plain explanation requests ("explain X", "what is X"), debugging, or codebase questions — those are different skills.

## Steps

1. **Slugify the topic** from `$ARGUMENTS` → lowercase kebab-case (`React Server Components` → `react-server-components`). Strip punctuation; collapse whitespace to single hyphens.

2. **Pick the output directory**:
   - Target: `./output/<slug>/`
   - If it already exists, suffix with `-2`, `-3`, … until you find an unused name.
   - Create it: `mkdir -p ./output/<slug>/sources`

3. **Search** with `WebSearch` for the topic. Pick **5–8 URLs**, biased toward primary sources: official docs, RFCs, project READMEs, vendor engineering blogs, well-known specs. De-prioritise SEO/content-farm pages.

4. **Fetch each URL sequentially** (deterministic numbering matters for citations):
   - `WebFetch` the URL.
   - `Write` it to `./output/<slug>/sources/NN-<domain>.md` (e.g. `01-react.dev.md`). File header:
     ```markdown
     # Source NN
     - URL: <url>
     - Fetched: YYYY-MM-DD
     ---
     <fetched body, lightly trimmed of nav/footer if obvious>
     ```
   - Also call `ctx_fetch_and_index` on the same URL with `source: "research/<slug>"` so the page is indexed for later `ctx_search`. Treat this as fire-and-forget — if it fails, log a one-line note in the summary's "Open questions / gaps" section but keep going.
   - If `WebFetch` itself fails, skip the URL, do not advance the NN counter, and note the skip in the summary.

5. **Write `./output/<slug>/summary.md`** in this exact structure:
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

6. **Print** the absolute path to `summary.md` so the user can open it directly.

## Notes

- One pass per invocation — no automatic refinement loop. If the user wants more depth, they re-invoke with a narrower topic.
- Never overwrite an existing topic folder; always suffix.
- Sources are fetched **once** and saved locally; do not re-fetch the same URL within a single run.
- `ctx_fetch_and_index` is for *future* searchability; its failure must not block local file output.
- The skill writes only inside `./output/`. It does not commit, push, or modify anything else in the working tree.
