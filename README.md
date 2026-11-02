# SourceTrace

An Agent Skill for multi-modal knowledge tracing and verification: it breaks content into claims, traces each one back to its source (text, PDF, web, image, audio, video), and reports whether the source supports it.

## Layout

```
source-trace/          the skill itself (this folder is what gets installed)
├── SKILL.md           instructions and trigger description
├── references/        detail loaded only when needed
├── scripts/           helper scripts
└── evals/             test cases
```

## Install

Copy `source-trace/` into your skills folder, for example `~/.claude/skills/source-trace/`.

## Status

Early draft.
