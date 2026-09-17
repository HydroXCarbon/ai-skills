---
name: management-talk

description: "Use when engineer-to-engineer content needs to be rewritten for engineering-org leadership (VPs, directors, PMs, release managers, execs at a technical company) and shaped for the channel it's going to — JIRA comment, Slack post, async standup line, email, or meeting talking-points. Triggers on requests to write for management / exec / VP / director / PM / release manager, \"executive summary\", \"leadership update\", \"status update\", \"make this less technical / less jargony\", or asking for a Slack / email / standup / meeting version of engineering work."

argument-hint: "[channel] [source: ticket key or pasted text]"
---

# Management Talk

## Overview

Same audience and translation rules as a written status report, but **shaped
for the channel** — JIRA comment, Slack post, async standup, email, or meeting
talking-points. The audience reads code names but not code. The channel decides
length, formatting, and how much structure to leave on the page.

Use this any time engineering content needs to flow up the org, sideways into
product/release, or into a non-engineering meeting — regardless of destination.
Its natural upstream is [`post-mortem`](../post-mortem/SKILL.md): post-mortem
owns the engineering truth, this skill reframes it.

## When to use

Trigger phrases include "write something for management / exec / VP / director
/ PM / release manager", "rewrite this for [non-eng audience]", "make this
non-technical / less techy / less jargony", "send a slack update / standup note
/ email" *about a piece of engineering work*, "executive summary / exec summary
/ leadership update / status update", "talking points for [meeting]" *based on
an engineering update*.

Do **not** trigger for marketing, finance, customer-facing, or true ELI5
audiences — those need a different rewrite. Flag and confirm before producing
one. Do **not** use this to write the engineering record itself; that's
[`post-mortem`](../post-mortem/SKILL.md).

## Arguments

- **channel** — JIRA, Slack, standup, email, or meeting talking-points.
  Decides the shape.
- **source** — a ticket key, pasted technical text, or the current
  conversation.

## Step 1 — Confirm the channel

If the channel isn't stated, ask one short question — *"JIRA, Slack, standup,
or email?"* — and **stop**. Everything downstream depends on it.

## Step 2 — Locate the source material

The input is one of:

1. **A ticket key** (e.g. `JIRA-12345`) → fetch it (for JIRA:
   `GET /rest/api/3/issue/<KEY>?fields=summary,status,priority,assignee,comment`,
   plus any custom fields your instance uses for technical evaluation) —
   usually the cleanest source of current state. Reframe the most recent
   substantive comment; don't dump the full thread.
2. **Pasted technical text** → use directly.
3. **The current conversation** → if engineering content was just produced and
   the user says *"now in slack"* / *"now for the VP"*, reuse what's in
   context.

If the source is ambiguous, ask one question and **stop**.

## Step 3 — Translate for the audience

**Audience:** engineering-savvy non-engineers — VPs, directors, PMs, release
managers, execs at companies that ship technical products. They read
product/framework names and cross-reference ticket keys and PRs. They do not
read code. They want *what's the state, what does it mean for customers, who
owns it, what's next.* They do not want how the bug works at the function
level.

**Keep.** Product names, framework names, team-owned component names, ticket
keys, PR numbers, customer/workload identifiers (`Tada`, `DeepSpeed`,
`PyTorch`, `Llama-2-70B`, `vLLM`, `JIRA-12345`, `PR #5751`). These are the
bridge between engineering and leadership tracking.

**Strip.** Function names, file paths, struct fields, commit SHAs, code
expressions, env var names, line numbers, internal data-structure jargon
(`tadaLaunchPrepare`, `tada/prim.h::syncWaitPeer`, `scratchBuf`, `0e0a6bac`).
None of it is actionable to this audience.

**Translate.** Mechanism into one or two sentences of plain-English
cause-and-effect. Not *"the kernel reads from `scratchBuf == NULL`"* but *"the
GPUs end up reading from an uninitialized buffer and wait forever for a signal
that never arrives."* Translate without lying — a race stays a race; a
regression stays a regression.

**Don't over-strip.** This audience reads concept-level technical vocabulary
fluently — *race condition, synchronization, uninitialized buffer, fast-path,
workaround, registration, queue, driver, kernel* (in the GPU sense). The line
is between *this concept exists and matters here* (keep) and *here's the
function/struct/file/SHA* (strip). Replacing "race" with "timing issue"
patronizes the reader.

**Bias toward** active voice, concrete subjects, short paragraphs. *"We found
the bug. Alex wrote the fix. PR is up for review."* beats *"The root cause has
been identified and a fix has been authored and submitted for review."*

**Avoid:**

- Hedging that isn't really hedging (*"we believe", "appears to", "may have"*).
  State it or don't.
- Re-stating the obvious for thoroughness (*"This bug is in Tada, which is used
  for GPU communication, which is important for distributed training,
  which…"*).
- Telling leadership how to do their job (*"you should prioritize", "this needs
  to land before X"*). Give them the facts; they decide.
- Engineering-process minutiae: bisect runs, debug iterations, debugger
  sessions. They care that you found it, not how. Exception: when the process
  *is* the story (*"we burned three weeks before realising the bisect was
  misleading"*) — one sentence as a learning, not a play-by-play.

## Step 4 — Shape it for the channel

Same content, different shell. Pick the one that matches where it's going.

### JIRA comment / written status report

Full structured block. Bolded section labels. Easy to scan from the ticket
page. Use as many building blocks as fit, ordered by what matters most for
*this* item:

- **Status / TL;DR.** One bolded line. Reader can stop here and have the right
  answer. *"Fixed pending merge."* / *"Root cause unknown — investigating."* /
  *"Blocked on vendor."* / *"Customer-visible regression in 7.2; rollback in
  flight."*
- **Impact.** Who's affected, how badly, what they see. Customer / workload /
  product terms, not test-suite terms. *"Llama-2-70B fine-tuning hangs on every
  eval step"* > *"the test fails."*
- **What broke.** Short paragraph. Plain-English mechanism, one level of why,
  no code identifiers.
- **Why now / how it slipped through.** Optional. Include when leadership will
  ask anyway: latent regression, CI gap, prior incomplete fix, change that
  landed during a freeze.
- **Owner.** Person + team + their PR/branch/ticket. One link, not five.
- **Next steps.** Concrete, near-term, ordered. *"Code review → merge →
  backport to 7.2."*
- **Workaround / mitigation.** If customers are hitting it now, what can they
  do today? One sentence.
- **Risk.** Optional, real risks only — *"fix touches the hot path; perf
  regression possible until benchmarked."* Don't manufacture risk to look
  thorough.

### Slack — channel post or DM

Single message, no walls of text. Heavy bolded section labels read as "I
escaped from JIRA" — don't.

- One **bolded TL;DR** as the first line.
- 2–4 short bullets underneath: impact, owner + link, next step. Drop blocks
  that don't apply.
- One link, embedded inline (`JIRA-12345` / `PR #5751`). Not a link wall.
- No greeting, no signoff. The channel is the context.
- If it's a **thread reply**, lose the TL;DR — just lead with the answer.

Length target: under ~80 words for a top-level post, under ~40 for a thread
reply.

### Async standup note

The audience scans 10 of these in 30 seconds. Front-load the verb.

- 1–3 lines, max. No bullets, no bolded labels — the format **is** the
  sentence.
- Pattern: *"\<state\> \<thing\>. \<owner if not me\>. \<next\>."*
- *"Fixed Tada hang affecting dumbModel runs (JIRA-12345). PR #5751 in review.
  Backport to v7.2 next."*
- *"Still chasing the LLM-7B eval-step hang. Reproducer is reliable now;
  bisecting. No ETA yet."*

### Email — internal exec / cross-team

Subject line is half the value.

- **Subject:** the TL;DR as a noun phrase. *"Tada hang in dumbModel: fix in
  review (JIRA-12345)."*
- **Greeting:** match the recipient register (*Hi Sam,* / *Hi all,*).
- **Body:** the JIRA-comment shape, but as flowing paragraphs separated by
  blank lines rather than bolded labels. Two or three paragraphs is plenty.
- **Sign off** with the next decision point that needs the recipient's
  attention, if any. Otherwise a plain *"— [Name]"*.

### Meeting talking-points

You're going to *say* this, not show it.

- Bullet list, max one short clause per bullet.
- Order is the order you'll speak in.
- Include the numbers and keys you want to say out loud, in the bullet itself,
  so you don't fumble.
- Skip prose. *"dumbModel LLM-7B fine-tuning was hanging."* / *"Root cause:
  skipped sync in Tada fast-path."* / *"Alex's fix in review, PR #5751."* /
  *"Backport to v7.2 once it lands."*

## Step 5 — Deliver

1. Produce the draft as a single chat block, formatted as the channel would
   render it.
2. Ask where it goes. Default is print-only — the user copies it.
3. **Ticket back-post:** only if the user explicitly says so. Show the exact
   payload, wait for an explicit *"post it"* / *"go ahead"* / *"yes"*, then
   send it (for JIRA: `POST /rest/api/3/issue/<KEY>/comment`).
4. **Never post to Slack, email, or any non-ticket channel from this skill.**
   Hand the draft to the user; they post it.
5. **One iteration is normal, three is a smell.** On a third revision, ask what
   framing or audience assumption you're missing instead of tweaking blindly.

## Worked example — same bug, three channels

**Source (engineering record):**

> **Mechanism:** the single-stream fast-path in `tadaLaunchPrepare` /
> `tadaLaunchKernel` / `tadaLaunchFinish` (gated on
> `scheduler->numStreams == 1 && !plan->persistent`) skipped the cross-stream
> event between `launchStream` and `handle->shared->deviceStream`. dumbModel
> hits this gate exactly. Kernel launched before deviceStream's IPC publish /
> scratch-buffer writes (the ones that populate `scratchBuf`) were visible to
> launchStream → `scratchBuf == NULL` in the kernel → stray pointer dereference
> → ring ready-flag read from garbage → thread spins forever.

### As a JIRA comment

> **Status: Fixed pending merge.** Bug found, fix validated, PR up for review.
>
> **Impact:** LLM-7B fine-tuning on 8 GPUs would hang every time it tried to
> evaluate the model — blocking the entire workload. Affects customers using
> dumbModel (a popular framework for training large models that don't fit on a
> single GPU), which means most large-model fine-tuning runs on the platform
> were exposed.
>
> **What broke:** Our GPU communication library (Tada) skipped an internal
> synchronization step under a specific configuration that dumbModel happens to
> trigger. The GPUs ended up reading from an uninitialized buffer and got stuck
> waiting for a signal that would never arrive. The unsafe shortcut had been in
> the code for months but wasn't reached by any real workload until now.
>
> **A previous fix attempt** added a defensive check that hid the symptom in
> some paths but left the underlying race in place. This new fix removes the
> unsafe shortcut entirely and tightens the safety check on the device side.
>
> **Owner:** Alex (Tada team). PR org/platform#5751.
>
> **Next steps:** code review → merge. Customers hitting this today can disable
> IPC registration as a temporary workaround.

### As a Slack post

> **Tada hang affecting dumbModel LLM-7B fine-tuning is fixed pending merge.**
> (JIRA-12345)
>
> - Skipped synchronization in the comms fast-path → GPUs read uninitialized
>   memory → hang. Latent for months; dumbModel was the first workload to hit
>   it.
> - Owner: Alex, PR #5751 in review.
> - Workaround until merge: disable IPC registration.

### As a standup note

> Fixed Tada hang on dumbModel LLM-7B (JIRA-12345). Alex's PR #5751 in review.
> Workaround posted in the ticket; backport to v7.2 next.

What changed between channels: same diagnosis, same owner, same next step. JIRA
gets every block. Slack drops "why now" and the previous fix attempt — too much
for the channel. Standup keeps state + key + owner + next. None of them mention
`scratchBuf` or `tadaLaunchPrepare`.

## Open questions

If the channel isn't stated, ask via `AskUserQuestion`:

- **JIRA comment** — full structured block on the ticket.
- **Slack** — one short message, TL;DR plus 2–4 bullets.
- **Standup** — 1–3 front-loaded lines.
- **Email / talking-points** — subject-led paragraphs, or spoken bullets.

If the source names no owner, ask who owns it. Don't guess.

## Hard rules

- **Never invent facts** to make the rewrite cleaner. If the engineering source
  says "root cause unknown", the rewrite says "root cause unknown" — never
  promote a speculation to a finding for narrative tidiness.
- **Never strip a ticket key, PR number, or customer/workload name** while
  de-jargoning. They're the cross-reference bridge; losing them breaks
  tracking.
- **Never invent owners.** If the source doesn't name one, ask — don't infer
  from `git blame` or recent commits.
- **Get sign-off before posting to a ticket.** Print-only needs no approval.
- **Never post to Slack, email, or any non-ticket channel from this skill.**
  Hand the draft to the user; they post it.
- **Stay out of advocacy.** This produces a status update, not a
  recommendation. If the user wants a recommendation memo, confirm before
  reframing.