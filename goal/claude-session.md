# Claude Code Session Marker

**Active session name:** `ai`

## How to resume this session

From the project root:

```bash
cd /Users/mutyalaqwipo/qwipo/ai-learning-v1
claude --resume
```

A picker will appear listing recent sessions for this project. Pick the one named **`ai`** and it loads with full conversation history.

## Optional — auto-resume on `claude` in this directory

If you always want this session to come back when you type `claude` from this folder, add an alias to your `~/.zshrc`:

```bash
alias claude-ai='cd /Users/mutyalaqwipo/qwipo/ai-learning-v1 && claude --resume ai'
```

Then `claude-ai` from anywhere drops you straight back into this session.

## What this file is *not*

This file is just a memo for *you* — Claude Code does not read it to actually resume sessions. Resumption is driven by `claude --resume` against `~/.claude/projects/-Users-mutyalaqwipo-qwipo-ai-learning-v1/`. If the session is ever deleted from that directory, this marker won't bring it back.

**Last updated:** 2026-04-29
