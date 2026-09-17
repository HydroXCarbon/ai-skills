# ai-skills

Personal vault for Claude Code and Antigravity customizations — skills,
slash commands, and subagents. Versioned so they can be synced across
machines and shared.

## Layout

```
ai-skills/
├── .claude/
│   ├── skills/            # Claude Code skills (folder per skill, contains SKILL.md)
│   ├── commands/          # Slash commands (.md with YAML frontmatter)
│   ├── agents/            # Subagent definitions (.md with frontmatter)
│   ├── INTEGRATIONS.md    # Plugin + MCP server install reference
│   └── settings.local.json
├── .agent/
│   └── skills/            # Antigravity skills (folder per skill, contains SKILL.md)
├── _specs/                # Planning specs (see the `spec` skill)
├── AGENTS.md              # Conventions for all AI agents working in this repo
└── CLAUDE.md              # Claude Code-specific guidance
```

The dotfile names mean both CLIs **auto-discover** items when a session
runs with this repo as cwd — no symlink needed for project-level use.

Skills are maintained in both trees. The `.agent/` copies are the same
skill adapted to Antigravity: frontmatter reduced to `name` +
`description` (no `argument-hint` / `allowed-tools`), and Claude tool
names swapped for their Antigravity equivalents (`AskUserQuestion` →
`ask_question`).

## Install (global availability)

To make an item available across any cwd, symlink it into the user-level
config dir so edits here propagate live.

| Source (this repo)           | Target                            |
| ---------------------------- | --------------------------------- |
| `.claude/skills/<name>/`     | `~/.claude/skills/<name>`         |
| `.claude/commands/<name>.md` | `~/.claude/commands/<name>.md`    |
| `.claude/agents/<name>.md`   | `~/.claude/agents/<name>.md`      |
| `.agent/skills/<name>/`      | `~/.gemini/config/skills/<name>`  |

Example:

```bash
ln -s "$PWD/.claude/commands/<name>.md" ~/.claude/commands/<name>.md
```

## What goes where

- **Claude skill** — multi-step capability with its own folder and
  `SKILL.md`. Loaded on demand by Claude when its description matches.
- **Claude command** — single `.md` file invoked as `/<name>`. Use for
  reusable prompts.
- **Claude agent** — subagent system prompt + tool allowlist. Invoked
  from the Agent tool by `subagent_type`.
- **Antigravity skill** — same shape as a Claude skill, in
  `.agent/skills/<name>/SKILL.md`. Don't mix the two trees.

## Templates

Each item type ships a `template` scaffold you can copy as a starting
point: `.claude/commands/template.md`, `.claude/agents/template.md`,
`.claude/skills/template/`, `_specs/template.md`. Don't symlink them —
copy and rename.

Antigravity has no separate scaffold: copy `.claude/skills/template/`
and apply the frontmatter/tool-name adaptations listed above.
