# Synthesizer guidance (leader, Step 4)

The leader (the main model running this skill) is the synthesizer. Use
this checklist when fanning back in.

## Inputs

- N researcher responses, each with `Key findings`, `Sources`, and
  `Confidence notes` sections (see `researcher-prompt.md`).

## Output

A single markdown file at `./output/<slug>/report.md` that follows
`assets/report-template.md`. The leader writes this file, then runs the
PDF script.

## Synthesis rules

1. **Deduplicate findings across researchers.** If two researchers
   surfaced the same fact, merge into one finding. Keep all sources.
2. **Flag genuine disagreements.** If two researchers contradict each
   other, do not pick a winner — surface the disagreement in
   `Key Findings` and let the reader judge. Note both sources.
3. **Rank findings by importance, not by who reported them.** The top
   5–10 findings across all angles go in the consolidated `Key
   Findings` section.
4. **Deduplicate sources.** Same URL from multiple researchers → one
   entry in `Sources & URLs`.
5. **Acknowledge gaps honestly.** If an angle came back thin or a
   researcher flagged low confidence, say so in `Summary`. Do not pad.
6. **Include a comparison table only when warranted.** If the topic
   compares 3+ entities/options across 3+ attributes, build a table.
   Otherwise, skip — a forced table degrades the report.
7. **Date the report.** Use today's date in ISO format (YYYY-MM-DD).

## Quality checklist before generating the PDF

- [ ] Title is the user's actual topic, not a slugified version.
- [ ] Date is set.
- [ ] Sources & URLs section has ≥ N×3 unique URLs (≈ 15 for default N=5).
- [ ] Summary is 2–3 paragraphs, no bullets.
- [ ] Key Findings has 5–10 entries.
- [ ] Table section is either present-and-useful or absent (no empty
      `| - | - |` skeletons).
- [ ] No researcher names like "Researcher 3 said …" leak through —
      the user doesn't care which agent found what.

## After writing report.md

Run the PDF script (see Step 5 of SKILL.md). Then write the brief
in-chat summary (Step 6) — do not dump the full report into chat.