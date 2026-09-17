---
name: post-mortem
description: "Use when a debug session has landed a validated fix and the bug needs its canonical engineering record — root cause, mechanism, fix, validation, and how it slipped through. Engineer audience; code identifiers are first-class. Triggers on /post-mortem, \"write the post-mortem / postmortem / RCA / root cause analysis\", \"document this fix\", \"write up the root cause\", \"close out this bug with a writeup\"."
---

# Post-mortem

## Overview

The canonical engineering record of a bug fix. Written **after** debugging
lands a real fix, **for** other engineers — and for future-you, who will have
forgotten everything in six months. Code identifiers are welcome here; this is
the artifact that lets the next person recover the mental model fast.

For the up-the-org version of the same content, hand the finished post-mortem
to [`management-talk`](../management-talk/SKILL.md). They compose: post-mortem
owns the engineering truth, management-talk reframes it for leadership.

## When to use

Trigger phrases include "/post-mortem", "write the post-mortem / postmortem /
RCA / root-cause analysis", "document this fix", "write up the root cause",
"close out this bug with a writeup". After a
[`debug-mantra`](../debug-mantra/SKILL.md) session clearly lands a fix,
proactively offer to draft one.

Do **not** trigger for:

- **A bug that isn't fixed, or a fix that isn't validated.** A post-mortem of
  a hypothesis is misleading. Refuse and say what's missing.
- **A customer-visible outage or incident.** Those need a separate incident
  report (timeline, blast radius, paging history, comms). This skill is
  bug-fix scope. Flag and confirm before producing one.
- **A trivial fix** (typo, obvious one-liner). The PR description is the
  record. Don't manufacture ceremony.

## Arguments

- **ticket key** — JIRA (or equivalent) key for the source ticket, extracted
  from the user's prompt. Used as the default destination and cross-reference.
- **destination** — where the writeup goes, if not the source ticket. If absent,
  ask.

## Step 1 — Confirm the four required inputs

Before writing a single line, confirm all four. If any are missing, list what's
missing and **stop**.

- [ ] **Reliable repro** exists — not "happens sometimes", but a deterministic
      or high-rate-flake repro the next person can run.
- [ ] **Root cause is known** — the mechanism is identified, not a hypothesis.
- [ ] **Fix is identified** — PR / commit / branch pointer.
- [ ] **Fix is validated** — the original repro now passes; the customer
      workload or failing test now succeeds.

These map directly onto [`debug-mantra`](../debug-mantra/SKILL.md) Steps 2–5.
If you came in via that skill, its breadcrumb ledger is your raw material —
pull from it.

## Step 2 — Confirm the destination

Default: a comment on the source ticket. Other valid destinations: PR
description, `docs/postmortems/<ticket>.md`, internal wiki page. The shape is
the same — only the wrapping changes.

## Step 3 — Draft the record

Use these blocks in this order. **Summary, Root cause, Fix, and Validation are
mandatory.** The rest are conditional but usually present. Produce the draft as
a single chat block.

### 1. Summary *(mandatory)*

One paragraph. What broke, in user/workload terms. What fixed it, in one
sentence. Ticket key, PR number, owner. A reader who stops here should have the
right answer.

### 2. Symptom

What was actually observed — test output, error message, log line, perf number,
customer report. Concrete identifiers; don't paraphrase the failure mode.

### 3. Root cause *(mandatory)*

The actual bug mechanism. **Code identifiers welcome and expected** — function
names, file paths, struct fields, branch conditions, commit SHAs of the
offending change. Walk the cause chain end-to-end. This is the most expensive
section and the reason the post-mortem exists at all.

### 4. Why it produced the symptom

Link root cause to symptom. Often non-obvious — the bug is in
`tadaLaunchPrepare` but the visible failure is a customer training run hanging
hours later. Walk the chain so a reader who only knows the symptom can connect
it back without re-deriving it.

### 5. Fix *(mandatory)*

What changed, and **why this change addresses the root cause** rather than
hiding the symptom. Link the PR / commit. If a previous attempt papered over
the symptom, name it and explain what was wrong with it — that history is part
of the cause.

### 6. How it was found

Short. The debugging path:

- What repro made it deterministic.
- What tools cracked it (debugger, source tracing, knob enumeration, in-code
  instrumentation — the `debug-mantra` Step 3 cascade).
- Hypotheses tried and rejected, one line each for why.
- The single experiment that confirmed the cause.

This section is for the next debugger — make it learnable.

### 7. Why it slipped through

What allowed this bug to reach the branch / release / customer. Pick the real
reason:

- CI gap — no test exercises this path or configuration.
- Latent code — correct when written, broken by a later change elsewhere.
- Workload gap — no real workload reached this path until now.
- Incomplete prior fix — a defensive check hid the symptom; root cause
  untouched.
- Review miss — the change was reviewable; the implication wasn't.

If the honest answer is "no good reason — we should have caught this", say so.
**Blameless:** describe the gap, not the person.

### 8. Validation *(mandatory)*

How we know the fix works. Concrete:

- Original failing test now passes (test name, link).
- Customer workload now completes (workload identifier, run link).
- Perf regression resolved (number before, number after).
- Stress / soak / fuzz run clean (duration, scale).
- Other affected configurations also tested.

If you validated one configuration only, say so explicitly — *"validated on
Llama-2-70B / 8 GPUs / DeepSpeed; not retested on other workloads."* Never
imply broader coverage than you have.

### 9. Action items / follow-ups

Concrete next steps that aren't in the fix PR itself. Each item: what + owner +
tracking artifact.

- Regression test added at \<seam\>. (Owner, test name.)
- Refactor to prevent the class of bug. (Owner, ticket.)
- CI gap closed: \<new check\>. (Owner, PR.)
- Doc / runbook updated. (Owner, link.)
- Related ticket filed for \<adjacent issue\>. (Owner, key.)

If there are none, write *"None — the fix is sufficient and no class-of-bug
follow-up is warranted."* Don't manufacture action items to look thorough.

## Step 4 — Sign-off before posting

Print-only output needs no approval. To post back to a ticket, show the exact
payload, wait for an explicit *"post it"* / *"go ahead"* / *"yes"*, then send
it (for JIRA: `POST /rest/api/3/issue/<KEY>/comment` with the ADF payload).

## Step 5 — Offer the handoff

Ask once: *"Want a leadership-flavored version? I can hand this to
`management-talk`."* Don't do it automatically.

## Tone

Engineer-to-engineer. Different from
[`management-talk`](../management-talk/SKILL.md):

- **Code identifiers are first-class.** `tadaLaunchPrepare`,
  `tada/prim.h::syncWaitPeer`, `scratchBuf`, commit SHAs, line numbers — keep
  them. The whole point is that future engineers can grep their way back to
  the change.
- **Mechanism over narrative.** Walk the actual cause chain. Don't soften it
  into "a synchronization issue" — say which function skipped which event
  under which gate.
- **Active voice, concrete subjects, short paragraphs.**
- **No hedging.** "We believe" / "appears to" / "may have" — drop. State it or
  don't write it.
- **Blameless.** Describe the bug, the gap, and the fix. Never "X should have
  caught this." The CI gap is the failure mode, not the person.
- **No advocacy.** A post-mortem records what happened and what's next. If you
  want to argue for a refactor, that's a separate proposal — link it from the
  action items.

## Worked example — Tada hang in dumbModel (JIRA-12345)

> **Summary.** Tada's single-stream fast-path skipped a required cross-stream
> synchronization, causing kernels to launch before scratch-buffer writes were
> visible. Triggered reliably by dumbModel on LLM-7B fine-tuning, hanging the
> workload at every eval step. Fixed by removing the unsafe fast-path and
> tightening a device-side check. JIRA-12345, PR org/platform#5751, owner Alex
> (Tada team).
>
> **Symptom.** 8-GPU LLM-7B fine-tuning under dumbModel hung indefinitely at
> the first eval step. No error, no timeout — busy-spin in
> `tadaKernel_AllReduce_f32_RING`. Reproduced on every run.
>
> **Root cause.** The single-stream fast-path in `tadaLaunchPrepare` /
> `tadaLaunchKernel` / `tadaLaunchFinish` (gated on
> `scheduler->numStreams == 1 && !plan->persistent`) skipped the cross-stream
> event between `launchStream` and `handle->shared->deviceStream`. dumbModel
> hits this gate exactly. The kernel was launched before the IPC publish /
> scratch-buffer writes on `deviceStream` (which populate `scratchBuf`) were
> visible to `launchStream`. In the kernel: `scratchBuf == NULL` → stray
> pointer dereference → ring ready-flag read from garbage memory → thread
> spins forever waiting for a ready signal that will never arrive.
>
> **Why it produced the symptom.** The hang lives in the all-reduce ring
> waitloop, the last visible thing in the call stack — but the actual bug is
> at launch-prep, several frames earlier. The skipped sync is silent until a
> workload triggers the exact gate (single-stream, non-persistent), and
> dumbModel's reduce-scatter pattern hits it at every eval step.
>
> **Fix.** PR #5751 removes the single-stream fast-path entirely (the saving
> was negligible vs. the safety it bypassed) and adds a device-side null check
> on `scratchBuf` before dereference, so the same class of bug fails loudly
> instead of silently spinning. A previous attempt (PR #5612) added a
> host-side defensive check after IPC publish that hid the symptom in some
> paths but left the underlying race in place — that change is also reverted.
>
> **How it was found.** Reproducer narrowed from "8-GPU LLM-7B hangs
> sometimes" to a deterministic 30s repro by pinning to a single eval step on
> a 2-GPU subset. Initial hypothesis: kernel launch ordering on
> `launchStream`. Disproved by the debugger — the kernel was correctly
> enqueued. Second hypothesis: scratch-buffer init race. Confirmed by adding
> `[DBG-7af3]` instrumentation in `tadaLaunchPrepare` printing `scratchBuf`
> and a `deviceStream` event-record timestamp; the launch happened before the
> publish completed. Single experiment that nailed it: forcing
> `numStreams = 2` made the bug disappear, isolating the gate.
>
> **Why it slipped through.** Latent code path. The single-stream fast-path
> was added in March under the assumption that dumbModel paths always took the
> multi-stream route. That assumption was true at the time. A May change to
> dumbModel's launcher began collapsing eval steps to a single stream — at
> which point the gate flipped. Tada's CI did not exercise the single-stream +
> IPC + scratch-buffer combination; the customer workload was the first to hit
> it.
>
> **Validation.** Original LLM-7B / 8-GPU / dumbModel workload now completes a
> full eval pass cleanly (3 consecutive 2-hour runs). `tada-tests`
> `all_reduce_perf` regression suite green. Soak run: 6 hours on 8 GPUs, no
> hang. Not retested on other model sizes or non-dumbModel workloads — both go
> through the multi-stream path and were never affected.
>
> **Action items.**
> - Regression test added: `tests/single_stream_ipc_publish_test.cpp`
>   exercising the previously-uncovered gate. (Alex, merged in PR #5751.)
> - CI gap: add a single-stream + IPC matrix entry to nightly. (Alex,
>   JIRA-12346.)
> - Doc update: Tada launch-fast-path invariants documented in
>   `docs/launch_synchronization.md`. (Alex, PR #5752.)
> - Related: audit other `numStreams == 1` fast-paths for the same class of
>   bug. (Filed as JIRA-12347.)

What this does that a leadership version can't: names every code identifier,
walks the cause chain so the reader can grep their way to the offending lines,
names the prior fix attempt and what was wrong with it, documents the exact
experiment that nailed the cause, states validation coverage honestly, and
gives every action item an owner and a tracking artifact.

## Open questions

If a required input from Step 1 is missing, ask via `ask_question` rather
than drafting around the gap:

- **Point me at the repro** — the command, test, or workload that fails
  deterministically.
- **Point me at the fix** — PR, commit SHA, or branch.
- **Tell me what validated it** — which run, test, or workload confirms it.
- **Draft anyway, marked incomplete** — only if the user explicitly accepts a
  record with named gaps.

If the destination is unclear, ask: ticket comment, PR description,
`docs/postmortems/<ticket>.md`, or print-only.

## Hard rules

- **Refuse to draft without all four required inputs.** A post-mortem of a
  hypothesis is worse than no post-mortem.
- **Never invent root cause, owner, validation runs, or action items.** If a
  section's facts aren't there, ask. Don't fill the gap with plausible prose.
- **Never strip code identifiers** from the engineering record. They are the
  index. The leadership reframe is `management-talk`'s job.
- **Blameless.** Describe gaps and bugs, never people.
- **State validation coverage honestly.** If you tested one config, say so.
  Implying broader coverage is the failure mode that breeds repeat
  regressions.
- **Get sign-off before posting to a ticket.** Print-only needs no approval.
  Never post to a non-ticket destination from this skill.
- **One iteration is normal, three is a smell.** On a third revision, ask
  which specific section is wrong instead of tweaking blindly.