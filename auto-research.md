# auto-research

This is an experiment to have the LLM do its own research.

## Setup

To set up a new experiment, work with the user to:

1. **Agree on a run tag**: propose a tag based on today's date (e.g. `mar5`). The branch `auto-research/<slug>-<tag>` must not already exist — this is a fresh run.
2. **Create the branch**: `git checkout -b auto-research/<slug>-<tag>` from current master.
3. **Read the in-scope files**: The repo is small. Read these files for full context:
   - `README.md` — repository context.
4. **Initialize results.tsv**: Create `results.tsv` with just the header row. The baseline will be recorded after the first run.
5. **Confirm and go**: Confirm setup looks good.

Once you get confirmation, kick off the experimentation.

## Experimentation

Each experiment runs on a single GPU. The training script runs for a **fixed time budget of 5 minutes** (wall clock training time, excluding startup/compilation).

**What you CAN do:**
- Modify files in `src/` or any file related to the website, backend service, etc. — these are the files you edit. Everything is fair game: architecture, logic, parameters, configuration, etc.

**What you CANNOT do:**
- Modify any file out of scope of the "What you CAN do" section. If you need to modify a file outside this scope, you MUST ask the user first.
- Modify the evaluation harness.

**The goal is simple: get a better score (lowest or highest, depending on the evaluation metric provided).** Since the time budget is fixed, you don't need to worry about training time  — it's always 5 minutes. Everything is fair game: change the architecture, the logic, the hyperparameters, the batch size, etc. The only constraint is that the code runs without crashing and finishes within the time budget.

**Simplicity criterion**: All else being equal, simpler is better. A small improvement that adds ugly complexity is not worth it. Conversely, removing something and getting equal or better results is a great outcome — that's a simplification win. When evaluating whether to keep a change, weigh the complexity cost against the improvement magnitude. A 0.001 val_bpb improvement that adds 20 lines of hacky code? Probably not worth it. A 0.001 val_bpb improvement from deleting code? Definitely keep. An improvement of ~0 but much simpler code? Keep.

**The first run**: Your very first run should always be to establish the baseline, so you will run the training script as is.

## Output format

Once the script finishes it prints a summary of key metrics. The specific parameter names will depend on the experiment.

Example:
```
---
metric1:          0.997900
metric2:          45060.2
...
```

You can extract the key metrics from the log file using grep for the relevant parameter names:

```
grep "^metric_name:" run.log
```

## Logging results

When an experiment is done, log it to `results.tsv` (tab-separated).

The TSV has a header row and columns corresponding to the metrics of interest:

```
commit	score	col2	...	status	description
```

1. git commit hash (short, 7 chars)
2. score, col2, etc. — the primary metric and values for the metrics you are tracking
3. status: `keep`, `discard`, or `crash`
4. short text description of what this experiment tried

Example:

```
commit	score	memory	status	description
a1b2c3d	0.997900	44.0	keep	baseline
b2c3d4e	0.993200	44.2	keep	increase LR to 0.04
```

## The experiment loop

The experiment runs on a dedicated branch (e.g. `auto-research/<slug>-mar5`).

LOOP FOREVER:

1. Look at the git state: the current branch/commit we're on
2. Tune the source code with an experimental idea.
3. git commit
4. Run the experiment: e.g., `uv run train.py > run.log 2>&1 or npm run dev > run.log 2>&1` (whatever is appropriate for the codebase)
5. Read out the results: `grep "^metric_name:" run.log`
6. If the grep output is empty, the run crashed. Run `tail -n 50 run.log` to read the stack trace and attempt a fix.
7. Record the results in the tsv (NOTE: do not commit the results.tsv file)
8. If the score improved, you "advance" the branch, keeping the git commit
9. If the score is equal or worse, you git reset back to where you started

The idea is that you are a completely autonomous researcher trying things out. If they work, keep. If they don't, discard. And you're advancing the branch so that you can iterate.

**Timeout**: Each experiment should take a reasonable amount of time. If a run hangs or exceeds its budget, kill it and treat it as a failure.

**Crashes**: If a run crashes (OOM, or a bug, or etc.), use your judgment: If it's something dumb and easy to fix (e.g. a typo, a missing import), fix it and re-run. If the idea itself is fundamentally broken, just skip it, log "crash" as the status in the tsv, and move on.

**NEVER STOP**: Once the experiment loop has begun, do NOT pause to ask the human if you should continue. Do NOT ask "should I keep going?" or "is this a good stopping point?". The human might be asleep, or gone from a computer and expects you to continue working *indefinitely* until you are manually stopped. You are autonomous. If you run out of ideas, think harder — read papers referenced in the code, re-read the in-scope files for new angles, try combining previous near-misses, try more radical architectural changes. The loop runs until the human interrupts you, period.

As an example use case, a user might leave you running while they sleep. If each experiment takes you ~5 minutes then you can run approx 12/hour, for a total of about 100 over the duration of the average human sleep. The user then wakes up to experimental results, all completed by you while they slept!
