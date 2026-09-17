# Debug Mantra — what it is, for non-engineers

**TL;DR — it's a checklist that stops an engineer (or Claude) from guessing at a bug.** It forces four things to happen in order before anyone proposes a fix: make the bug happen on demand, find where it actually breaks, try to prove the theory wrong, and check the theory against everything seen so far. Nothing gets called "fixed" until all four are satisfied.

## Why this exists

The expensive failure mode in debugging isn't a hard bug. It's a plausible-sounding fix that ships, doesn't work, and burns another cycle — or worse, hides the symptom while leaving the real problem in place. That happens when someone latches onto the first believable explanation and starts changing code.

This skill removes that option. It's a set of gates, not advice.

## The four gates

**1. Can we make it happen on demand?**

If the bug can't be triggered reliably, it can't be debugged — so the first job isn't fixing anything, it's building a repeatable way to trigger it. A bug that fails 50% of the time is workable. One that fails 1% of the time isn't, and the work becomes "make it fail more often" before anything else.

**2. Where does it actually break?**

Not where the error message appears — where the logic goes wrong. Those are often far apart: the visible symptom can be hours and many steps downstream of the actual cause. The skill works through progressively more invasive tools until the real location is pinned down.

**3. What would prove this theory wrong?**

Once there's a candidate explanation, the skill requires trying to *disprove* it before trying to confirm it, and requires three to five competing theories rather than one. Confirming a theory you already believe is easy and tells you almost nothing. Failing to kill it is what makes it credible.

**4. Does the theory explain *everything* we've seen?**

Every experiment gets logged — what changed, what happened, what it ruled out. A new theory has to hold up against the whole log, not just the most recent test. If any earlier result contradicts it, the theory is wrong or incomplete, and it goes back for revision.

## What this looks like from your side

- **"I can't work on this yet" is a valid, expected answer.** If a bug can't be reproduced, the skill explicitly stops and asks for what's missing — access to the failing environment, captured logs from a real failure, or permission to add diagnostic instrumentation. That's not stalling. Guessing without a reproducible case is how you get fixes that don't fix anything.
- **Fewer "fixed it — actually, not fixed" reversals.** The cost is front-loaded into gates 1 and 2, which look slow from outside. The saving is on the back end: no re-opened tickets, no second and third attempt at the same bug.
- **A confirmed cause, not a suspected one.** When work does come back as done, the mechanism is identified and tested against every observation — not "we think it was probably a timing issue."
- **The written record is nearly free.** The experiment log from gate 4 is exactly the raw material a root-cause writeup needs, so the post-mortem doesn't require reconstructing the investigation from memory weeks later.

## What it doesn't do

It doesn't make bugs easier or faster to find, and it doesn't estimate. A hard bug is still hard — this changes the *order* of the work and what counts as finished, not the total difficulty. It also only covers investigation. It says nothing about whether a bug is worth fixing, how to prioritize it, or when it ships; those stay product calls.

## Where it sits

Three skills cover one bug's life, and they hand off in sequence:

| Skill | Runs when | Audience |
|---|---|---|
| **debug-mantra** | During the investigation | The engineer, as a working constraint |
| **post-mortem** | After the fix is validated | Other engineers, and future-you in six months |
| **management-talk** | When it needs to go up or across the org | Leadership, PMs, release managers — this document is its output |

You'll rarely see debug-mantra directly. You'll see its effect: a clearer "not yet reproducible" signal early, and a confirmed diagnosis rather than a hopeful one later.