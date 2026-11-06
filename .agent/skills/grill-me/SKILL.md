---
name: grill-me
description: "Use when the user wants to stress-test a plan, decision, or idea by being interviewed relentlessly until you reach a shared understanding, or uses any 'grill' trigger phrase."
---

# Grill Me

## Overview

Interview the user relentlessly about a plan, decision, or idea until you
reach a shared understanding. The topic is mapped as a **design tree**: every
decision branches into the decisions that hang off it. The output is a series
of numbered question rounds, each with a recommended answer, ending when every
branch has been visited and nothing is left silently assumed.

## When to use

Trigger phrases include "grill me", "stress-test this plan", "poke holes in
this", "interview me about this idea", "challenge my thinking".

Do **not** trigger for plain brainstorming of a new feature or for one-off
factual questions — those are different tasks.

## Arguments

- **topic** — the plan, decision, or idea to grill. If omitted, infer it from
  the conversation so far.

## Step 1 — Build the design tree

- Identify the decisions the topic hinges on and which depend on which.
- Compute the **frontier**: every decision whose prerequisites are already
  settled — the questions you can ask _now_ without guessing at answers you
  haven't heard yet.
- A question whose answer depends on another question still open in this round
  belongs to a _later_ round, not this one.

## Step 2 — Gather facts without the user

Finding _facts_ is your job, never the user's.

- When a frontier question needs a fact from the environment (filesystem,
  tools, etc.), look it up yourself — delegate to a sub-agent with a fresh
  context window if one is available. Don't ask the user for anything you could
  look up yourself.
- Don't block on it: a running exploration is an unsettled prerequisite, so
  only the questions downstream of it wait for the result. Ask the rest of the
  frontier now.
- The _decisions_ are the user's: put each to them and wait.

## Step 3 — Ask a round

Ask the whole frontier in one round: number each question and give your
recommended answer. Word each question so "yes" accepts your recommended
answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

## Step 4 — Recompute and repeat

Each round the user answers reshapes the tree: settled decisions push the
frontier outward and unblock questions that depended on them. Recompute the
frontier and return to Step 2.

The session is done when the frontier is empty: every branch of the design
tree visited, nothing left silently assumed. Summarize the settled decisions
and ask the user to confirm via `ask_question`:

- **Confirmed — shared understanding reached** — you may now act on the outcome.
- **Not yet — keep grilling** — ask what is still unsettled and return to Step 1.

## Hard rules

- Never act on the outcome until the user confirms a shared understanding.
- Never ask the user for a fact you could look up yourself.
- Never ask a question whose answer depends on another still-open question in
  the same round.