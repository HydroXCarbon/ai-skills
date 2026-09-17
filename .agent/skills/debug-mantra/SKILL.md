---
name: debug-mantra
description: "Use when any debugging session starts — the user reports a bug, says something is broken/throwing/failing/hanging, asks to debug, diagnose, or investigate an issue, or pastes a stack trace or error log. Recites a four-mantra block verbatim, then enforces four gates in order: reproduce reliably, trace the fail path, falsify the hypothesis, cross-reference every breadcrumb. Also triggers on /debug-mantra."
---

# Debug Mantra

## Overview

A four-step discipline that governs the whole debugging session. The mantra
block is recited verbatim in the first response, then the four gates are
applied in order — no fix is proposed until each gate is satisfied. The
output is a confirmed root cause plus a breadcrumb ledger, which becomes the
raw material for [`post-mortem`](../post-mortem/SKILL.md).

The mantra is a constraint **you** carry through the session — not advice to
deliver back to the user.

## When to use

Trigger phrases include "/debug-mantra", "this is broken", "it's throwing",
"tests are failing", "help me debug this", "why is this hanging", plus any
pasted stack trace, panic, or error log.

Do **not** trigger for writing a fix the user has already diagnosed, for
[`post-mortem`](../post-mortem/SKILL.md) writeups of an already-fixed bug, or
for general code review — those are different skills.

## Step 1 — Recite the mantra

Emit this block verbatim as the first thing in your first response, then begin
work. Once per session — never re-recite mid-session, never paraphrase,
shorten, or skip a line.

> **Mantra:**
> 1. **First is reproducibility.** Can the issue be reproduced reliably?
> 2. **Know the fail path.** Debugger first; then source trace + knob enumeration; then in-code instrumentation.
> 3. **Question your hypothesis.** What would disprove it?
> 4. **Every run is a breadcrumb.** Cross-reference all of them.

If the user says "skip the mantra" → skip the recital, still apply Steps 2–5
silently.

## Step 2 — Reproduce reliably

Build a runnable repro before anything else.

- **Reliable repro** → capture the exact steps, inputs, and environment as a
  runnable artifact: failing test, curl script, CLI invocation, replay
  harness. Proceed to Step 3.
- **Flaky repro** → the bug is not yet debuggable. Raise the rate first: loop
  the trigger, parallelise, add stress, narrow timing windows, inject sleeps.
  50% flake is debuggable; 1% is not. Stay in Step 2.
- **No repro at all** → **Stop.** Say so explicitly and ask for what's
  missing (see Open questions). Do **not** proceed to hypothesise.

Target: a fast (1–5 s), deterministic pass/fail signal. Pin time, seed the
RNG, freeze network, isolate filesystem.

## Step 3 — Know the fail path

Once reproducible, find *where* the code breaks and *what stops it from
breaking*. The differential narrows the search. Escalate only when the prior
tactic fails.

1. **Attach a debugger.** If the env supports it, attach and step to the
   failure site. One breakpoint beats ten logs. Do this **before** turning any
   knobs.
2. **Source trace + knob enumeration.** If there's no debugger, or it can't
   reach the bug, trace the code path end-to-end and list every knob that can
   influence the outcome:
   - config flags, env vars, feature toggles
   - branch conditions, input shape
   - timing, concurrency, build options

   Each knob is a candidate axis for the differential. Flip one at a time.
3. **In-code instrumentation.** If outside knobs can't move the failure, go
   inside: `printf` / log statements at the suspected fail site, dump the
   relevant internal state. Tag every probe with a unique prefix (e.g.
   `[DBG-a4f2]`) so cleanup is a single grep. Let the trace show where reality
   diverges from your model.

## Step 4 — Falsify the hypothesis

When a candidate root cause surfaces, scrutinise it **before** testing it.

- Does it explain the symptom end-to-end? Walk it through.
- What is the simplest **proof**? What is the cleanest **disproof**?
- Run the **disproof first.** If the hypothesis survives, it's real. If it
  dies, you saved yourself from chasing a phantom.
- Generate 3–5 ranked hypotheses, not one. Single-hypothesis thinking anchors
  on the first plausible idea.

## Step 5 — Cross-reference every breadcrumb

Maintain a running **ledger** of every experiment in the session. Each entry:
what changed, what happened, what it ruled in or out.

- When a new hypothesis surfaces, walk the ledger. Does it hold for **every**
  prior observation, not just the most recent?
- If any past run contradicts it, the hypothesis is wrong or incomplete —
  refine or discard.
- When in doubt, design the **single experiment** whose outcome makes it
  certain. Run that next instead of churning on adjacent runs.
- Update the ledger after every run. It is your memory across the session.

Once the cause is confirmed and the fix is validated, offer to hand the ledger
to [`post-mortem`](../post-mortem/SKILL.md).

## Open questions

If there is no repro at all, stop and ask via `ask_question`:

- **Give me env access** — you run the repro steps in the failing environment
  and paste back what happens.
- **Hand me captured artifacts** — HAR file, log dump, core dump, trace from a
  run that actually failed.
- **Authorise instrumentation** — I add tagged probes to the suspect path and
  you deploy/run it to collect a trace.

## Hard rules

- Recite the mantra block **verbatim**, exactly once, in the first response.
- Apply the gates **in order**:
  - Never propose a fix before Step 2 is satisfied (a reliable repro exists).
  - Never test hypotheses before Step 3 has narrowed the fail path.
  - Never commit to a hypothesis before Step 4 has tried to disprove it.
  - Never declare a hypothesis correct until Step 5 confirms it against every
    prior breadcrumb.
- If you catch yourself proposing a fix without a reliable repro, stop and
  return to Step 2.
- Remove every `[DBG-*]` probe before the session ends.