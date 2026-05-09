---
description: Draft a Conventional Commits message with emoji prefix for staged changes, then offer to commit.
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git commit:*), AskUserQuestion
argument-hint: "[optional type hint, e.g. fix or docs]"
---

Draft a commit message for the **currently staged** changes using Conventional Commits with an emoji prefix, then offer to commit.

User hint (optional, may be empty): `$ARGUMENTS`

## Step 1 — Inspect state

Run these in parallel (single message, multiple Bash calls):

- `git status` (do NOT use `-uall`)
- `git diff --cached`
- `git diff` (unstaged — only to detect divergence)
- `git log -n 5 --oneline` (to mirror this repo's existing style if any)

## Step 2 — Decide source

- **Staged diff non-empty** → proceed using staged changes.
- **Staged empty, unstaged non-empty** → tell the user nothing is staged and suggest `git add <files>`. **Stop.** Do not pass `-a`.
- **Both empty** → tell the user there is nothing to commit. **Stop.**

## Step 3 — Pick type + emoji

Choose one row based on the dominant nature of the staged diff:

| Type | Emoji | When |
| --- | --- | --- |
| feat | ✨ | new user-facing capability |
| fix | 🐛 | bug fix |
| docs | 📝 | docs / README / comments only |
| style | 🎨 | formatting / whitespace, no logic change |
| refactor | ♻️ | code restructure, no behavior change |
| perf | ⚡ | performance improvement |
| test | ✅ | tests added or fixed |
| build | 📦 | build system / deps / packaging |
| ci | 👷 | CI/CD config |
| chore | 🔧 | misc maintenance, no src/test change |
| revert | ⏪ | reverts a prior commit |

If `$ARGUMENTS` names a type, bias toward it — but override when the diff clearly says otherwise (e.g. user passed `fix` but the diff is docs-only → emit `📝 docs:` and note the override).

## Step 4 — Write the message

- **Subject:** `<emoji> <type>: <imperative subject>`
  - ≤72 chars total
  - imperative mood ("add", not "added"/"adds")
  - no trailing period
  - lowercase first word after the colon unless it's a proper noun
- **Body** (optional, blank line after subject):
  - Only when the *why* isn't obvious from the diff
  - Wrap at ~72 chars
  - Focus on motivation, not a restatement of the diff

Do **not** add a `Co-Authored-By` footer — the user owns this message.

## Step 5 — Print the draft

Output the full message inside a fenced block so the user can copy it verbatim:

```
<emoji> <type>: <subject>

<optional body>
```

## Step 6 — Offer to commit

Use `AskUserQuestion` with three options:

1. **Commit staged changes with this message** (Recommended)
2. **Skip — I'll commit manually**
3. **Edit and retry** — redraft once with the user's feedback (max one retry per invocation)

## Step 7 — Act on the choice

- **Commit chosen** → run, using a heredoc to preserve formatting:
  ```bash
  git commit -m "$(cat <<'EOF'
  <emoji> <type>: <subject>

  <optional body>
  EOF
  )"
  ```
  Then run `git status` and report success with the new commit's short hash (`git log -1 --pretty=%h%x20%s`).
- **Skip chosen** → do nothing. Confirm the message was not committed.
- **Edit chosen** → ask the user what to change, redraft once, return to Step 5. Do not loop further.

## Hard rules

- Never use `--amend`, `--no-verify`, `--no-gpg-sign`, or `-a` on `git commit`.
- Never run `git add`. Only commit what is already staged.
- If a pre-commit hook fails: report the failure verbatim and stop. Do not retry with `--amend` or any flag that bypasses hooks.
- Never `git push`.