---
name: example-agent
description: Template subagent. Use when delegating <specific scoped task> to a fresh-context worker.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a focused subagent. Replace this system prompt with the actual
role.

## Responsibilities

- One clear thing this agent owns.
- Boundaries — what it must not do.

## Output contract

Describe exactly what the agent should return to the orchestrator: a
short report, a JSON blob, a file path, etc. Be explicit.
