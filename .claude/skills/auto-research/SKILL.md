---
name: auto-research
description: "Use when the user wants to run an autonomous ML/code experimentation loop — sets up a branch, establishes a baseline, then iterates experiments indefinitely, logging results to results.tsv."
argument-hint: "[metric=<name>] [direction=lower|higher] [scope=<path,...>] [budget=<minutes>]"
allowed-tools: "Read, Write, Edit, Bash, AskUserQuestion"
---

# Auto Research

## Overview

This skill runs Claude as an autonomous researcher on a dedicated branch. Given a project slug and run tag, it sets up an isolated branch, establishes a baseline, then loops forever: tune code → commit → run → measure → keep or reset. Each experiment runs on a fixed time budget (default 5 minutes wall-clock training time). Results are appended to `results.tsv` and the branch advances only when the score improves.

## When to use

Trigger phrases include "auto-research this", "run experiments overnight", "tune this autonomously", "loop on training runs and keep the best".

Do **not** trigger for one-off training jobs, single-experiment requests, or general code edits — those are normal coding tasks. This skill is specifically for **autonomous, indefinite, branch-isolated** experiment loops.

## Arguments

Parse `$ARGUMENTS` before doing anything else. Arguments are optional key=value pairs supplied by the user when invoking the skill. Recognized keys:

| Key | Values | Default | Effect |
|-----|--------|---------|--------|
| `metric` | any string | ask | Primary metric column name in `results.tsv`; used in `grep "^<metric>:"` |
| `direction` | `lower` \| `higher` | ask | Whether a lower or higher score is better |
| `scope` | comma-separated paths | ask | Files/dirs Claude may edit without asking; e.g. `src/,model.py` |
| `budget` | integer (minutes) | `5` | Wall-clock time limit per training run before killing the process |

**Parsing rules:**
- Strip each token, split on `=`, trim whitespace.
- Unknown keys → warn the user and ignore.
- For each recognized key that is present, skip the matching `AskUserQuestion` in **Open questions** — treat the value as already confirmed.
- If `$ARGUMENTS` is empty or absent, all open questions remain active.

## Step 1 — Setup

Run the following in order. Stop and ask via `AskUserQuestion` if any step is ambiguous.

1. **Agree on a run tag.** Propose `<run-tag>` based on today's date (e.g. `mar5`). Confirm with the user.
2. **Pick the project slug.** Use the repo's name or ask the user. The branch will be `auto-research/<slug>-<run-tag>`.
3. **Check the branch is fresh.** Run `git rev-parse --verify auto-research/<slug>-<run-tag>` — if it exists, **stop** and report; do not reuse a prior run.
4. **Create the branch** from current `master`/`main`: `git checkout -b auto-research/<slug>-<run-tag>`.
5. **Read the in-scope files for context.** At minimum `README.md`. If `scope` was supplied via arguments, read those paths; otherwise read any repo-specific orientation file the user names.
6. **Initialize `results.tsv`** with just the header row. Columns: `commit\tscore\t<other-metrics>\tstatus\tdescription`. If `metric` was supplied via arguments, use it directly; otherwise confirm metric column names with the user.
7. **Confirm and go.** Summarize setup back to the user and wait for explicit go-ahead before starting the loop.

## Step 2 — Baseline run

The very first run establishes the baseline — run the training script unmodified.

- Run the script: `<train-command> > run.log 2>&1` (e.g. `uv run train.py > run.log 2>&1`).
- Extract metrics: `grep "^<metric_name>:" run.log` for each tracked metric.
- If grep is empty, the run crashed — `tail -n 50 run.log`, diagnose, fix, re-run.
- Record the result in `results.tsv` with status `keep` and description `baseline`.
- Do **not** commit `results.tsv`.

## Step 3 — Experiment loop

**LOOP FOREVER** until the user manually interrupts. Each iteration:

1. **Note git state**: current branch HEAD.
2. **Propose an experimental idea.** Tune the source code — anything in scope is fair game: architecture, logic, hyperparameters, batch size, optimizer, etc. Out-of-scope files require asking the user first. **Never modify the evaluation harness.**
3. **Commit** the change with a one-line description of the experiment.
4. **Run** the training script: `<train-command> > run.log 2>&1`.
5. **Read results**: `grep "^<metric_name>:" run.log`.
6. **Handle empty grep (crash)**: `tail -n 50 run.log` to read the stack trace.
   - **Trivial fix** (typo, missing import) → fix, re-run.
   - **Fundamentally broken idea** → log `crash` in `results.tsv` with description, `git reset --hard` to prior commit, move on.
7. **Log result** to `results.tsv` (tab-separated). Status is `keep`, `discard`, or `crash`.
8. **Advance or reset:**
   - **Score improved** → keep the commit, advance the branch.
   - **Score equal or worse** → `git reset --hard` to the prior commit. Status `discard`.
   - **Simplification win** (equal score + simpler code) → keep. Status `keep`.

### Simplicity criterion

All else being equal, simpler is better. A tiny score gain that adds 20 lines of hacky code → reject. A tiny score gain by deleting code → keep. A neutral change that simplifies → keep.

### NEVER STOP

Once the loop has begun, do **not** pause to ask the human if you should continue. The user might be asleep or away from the keyboard — they expect indefinite autonomous operation until they manually interrupt. If you run out of ideas: re-read the in-scope files for new angles, combine prior near-misses, try more radical architectural changes, look up referenced papers. The loop runs until interrupted, period.

### Timeouts and crashes

- If a run hangs or exceeds budget, kill it and treat as failure (`crash` status).
- Use judgment on crashes: fix-and-retry for typos/imports; skip for fundamentally broken ideas.

<!--
  ─── Subfolder reference cheatsheet ───
  For detailed criteria, see [references/example.md](references/example.md).
  Use the template at [assets/README.md](assets/README.md).
-->

## Open questions

If the user has not specified the training command or metric names, ask via `AskUserQuestion`:

- **Training command** — what to run (e.g. `uv run train.py`, `npm run dev`, `python train.py`).
- **Primary metric** — the column to optimize, and whether lower or higher is better.
- **Secondary metrics** — any additional columns to track in `results.tsv`.

If the in-scope files for editing are unclear, ask:

- **Source directory** — typically `src/`, but confirm. Anything outside this scope requires user approval before edits.

## Hard rules

- Never modify the evaluation harness.
- Never modify files outside the agreed-upon source scope without asking the user first.
- Never commit `results.tsv`.
- Never reuse an existing `auto-research/<slug>-<run-tag>` branch — every run is fresh.
- Never stop the loop to ask "should I continue?" — only stop on manual interrupt, fatal error, or explicit user instruction.
- Never run destructive git operations (`git push --force`, `git branch -D master`) — the loop only resets within its own branch.
