# Claude Code Plugins & MCP Servers

Reference list of plugins and MCP servers used with Claude Code in this vault. Reinstall with the commands below after a fresh setup.

> Gemini equivalents (extensions, commands) live under `.gemini/` — this file is Claude-only.

## Install commands

```bash
# Official marketplace (skill-creator, superpowers, frontend-design)
/plugin install skill-creator@claude-plugins-official
/plugin install superpowers@claude-plugins-official
/plugin install frontend-design@claude-plugins-official

# GSD — installed via npx (not a /plugin), writes to ~/.claude
npx get-shit-done-cc --claude --global

# context-mode (third-party marketplace)
/plugin marketplace add mksglu/context-mode
/plugin install context-mode@context-mode

# claude-mem (third-party marketplace)
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
```

## MCP servers

```bash
# context7 — Upstash docs/code lookup MCP
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest
```

## What each plugin does

| Plugin | Purpose |
| --- | --- |
| `skill-creator` | Create, edit, eval, and benchmark Claude skills. Use when scaffolding or tuning a skill. |
| `superpowers` | Discipline framework — meta-skills for TDD, debugging, brainstorming, plan writing, code review, parallel agents, worktrees. Adds the "always invoke skills first" rule. |
| `frontend-design` | Generates distinctive, production-grade frontend code (components, pages, apps) that avoids generic AI aesthetics. |
| `get-shit-done-cc` (GSD) | Full project lifecycle: phases, plans, milestones, audits, code review, UAT, ship. Installed via `npx`, not `/plugin install`. |
| `context-mode` | Context-window protection. Provides `ctx_*` MCP tools that index large outputs (logs, fetches, batch commands) and let Claude search them instead of dumping into context. |
| `claude-mem` | Persistent cross-session memory database. Auto-captures observations and lets future sessions search prior work via `mem-search`. |

## What each MCP server does

| Server | Purpose |
| --- | --- |
| `context7` | Upstash-hosted MCP that fetches up-to-date library docs and code examples on demand. Use when answering API/library questions where freshness matters. |

## Notes

- `skill-creator`, `superpowers`, and `frontend-design` all live on the `claude-plugins-official` marketplace (preinstalled — no `marketplace add` needed).
- `context-mode` and `claude-mem` need their marketplaces added first.
- GSD is the odd one out — it's an `npx` installer, not a Claude plugin. Re-run the `npx` command to upgrade.
- MCP install commands above default to user scope. Add `-s project` to write to a project's `.mcp.json` instead, or `-s local` for this-project-only.

