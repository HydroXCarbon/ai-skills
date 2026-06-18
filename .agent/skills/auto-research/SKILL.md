---
name: auto-research
description: "Use when the user wants to run an autonomous experimentation loop — sets up a branch, establishes a baseline, then iterates experiments indefinitely, logging results to results.tsv."
---

# Auto Research

## Overview

This skill runs as an autonomous researcher on a dedicated branch. Given a project slug and run tag, it sets up an isolated branch, establishes a baseline, then loops forever: tune code → commit → run → measure → keep or reset. Results are appended to `results.tsv` and the branch advances only when the score strictly improves.

## When to use

Trigger phrases include "auto-research this", "run experiments overnight", "tune this autonomously", "loop on experiments and keep the best".

Do **not** trigger for one-off runs, single-experiment requests, or general code edits — those are normal tasks. This skill is for **autonomous, indefinite, branch-isolated** experiment loops.

## Arguments

Recognized keys extracted from the user's prompt:

| Key | Values | Default | Effect |
|-----|--------|---------|--------|
| `metric` | any string | ask | Primary metric column name in `results.tsv` |
| `direction` | `lower` \| `higher` | ask | Whether lower or higher score is better |
| `scope` | comma-separated paths | ask | Files/dirs editable without asking; e.g. `app/,src/` |
| `budget` | integer (minutes) | `5` | Wall-clock time limit per run before killing |

Unknown keys → warn the user and ignore. For each recognized key present, skip the matching `ask_question`.

---
## Step 1 — Setup

1. **Generate a run tag.** Use today's date (e.g. `may14`) as `<run-tag>`.
2. **Identify the research goal.** 2–4 word kebab-case summary (e.g. `lighthouse-perf`). This is `<topic-summary>`.
3. **Check the branch is fresh.** Branch name: `auto-research/<topic-summary>-<run-tag>`. If it exists, **stop** and report — never reuse a prior run.
4. **Create the branch** from current `main`/`master`: `git checkout -b auto-research/<topic-summary>-<run-tag>`.
5. **Read the in-scope files for context.** At minimum `README.md` and `AGENTS.md` (if present). Read `scope` paths if supplied.
6. **Check for a project runner.** Look for a script the project already provides for measurement. If one exists, use it — don't invent your own. Read it to understand its flags.
7. **Initialize `results.tsv`** with just the header row. Use the columns the project runner already produces if one exists; otherwise confirm column names with the user.
8. **Check for dashboard.** Check if `dashboard/index.html` exists. If not, ask via `ask_question`: "No dashboard found. Would you like me to create a basic auto-refreshing dashboard to track progress?" If yes, create it according to the [Dashboard Specification](references/dashboard.md).
9. **Confirm and go.** Summarize setup and wait for explicit go-ahead.

---

## Step 2 — Baseline run

The first run captures unmodified baseline. Run the measurement command and record result with status `keep`.

- Run: `<measure-command> --note="baseline"` (append TSV row).
- If the runner defaults to `discard` status (correct behaviour), **immediately** promote the baseline: `<measure-command> --set-last-status=keep` or equivalent.
- Extract the baseline score — this becomes `best_score`.
- Do **not** commit `results.tsv`.

---

## Step 3 — Experiment loop

**LOOP FOREVER** until the user manually interrupts.

### Each iteration

1. **Record HEAD**: `prev_commit=$(git rev-parse HEAD)`, `best_score=<last keep row's score>`.
2. **Propose an idea.** Tune only in-scope files. Out-of-scope requires asking first. **Never touch the measurement harness.**
3. **Commit** the change: `git commit -m "exp: <description>"`.
4. **Run** the measurement: `<measure-command> --note="<description>"`.
   - Runner should write status `discard` by default.
5. **Read the new score** from stdout or the last TSV row.
6. **Handle crashes** (empty/zero score, error output):
   - Trivial fix (typo, import) → fix, re-run.
   - Broken idea → log `crash` in TSV, `git reset --hard $prev_commit`, continue.
7. **Compare** new score to `best_score`.
8. **Advance or reset:**
   - **Strictly better** → promote: `<measure-command> --set-last-status=keep`. Update `best_score`. Keep the commit.
   - **Equal or worse** → `git reset --hard $prev_commit`. The TSV row stays with `discard` status.
   - **Simplification win** (equal score, meaningfully simpler code) → promote to `keep`.

See [references/protocol.md](references/protocol.md) for the TSV status and scoring protocol.

### NEVER STOP

Do **not** pause to ask "should I continue?" The user expects indefinite autonomous operation. If you run out of ideas: re-read in-scope files for new angles, combine prior near-misses, try more radical changes. The loop runs until interrupted.

### Timeouts

If a run hangs past `budget`, kill it and treat as `crash`.

---

## Open questions (if not provided)

Ask via `ask_question`:

- **Measurement command** — what to run (e.g. `node lighthouse/scripts/run.mjs`, `uv run eval.py`).
- **Primary metric** — column name and direction (lower/higher).
- **Secondary metrics** — any additional columns to track.
- **Source directory** — what's in scope to edit. Anything outside requires approval.

---

## Hard rules

- **Never keep a commit with an equal or lower score.** Reset immediately. Do not change old TSV rows.
- Never modify the measurement harness or `results.tsv` schema.
- Never commit `results.tsv`.
- Never reuse an existing `auto-research/<slug>-<run-tag>` branch.
- Never stop to ask "should I continue?" — only stop on manual interrupt or fatal error.
- Never run `git push --force` or `git branch -D` on protected branches.
