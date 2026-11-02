# SourceTrace

An Agent Skill that audits an AI-generated knowledge tree against its source material. Give it the source images (PNG/JPG, e.g. exported slides) and the knowledge tree (JSON); it extracts evidence, maps every node and edge to that evidence, audits in both directions, and writes:

- `report.md`: a human-readable audit report
- `audit.json`: a machine-readable audit result

It works with any tool that supports Agent Skills, such as Claude Code or Codex.

## Layout

```
docs/requirements.md   scope, workflow and design decisions
source-trace/          the skill itself (this folder is what gets installed)
├── SKILL.md           instructions and trigger description
├── schemas/           JSON Schemas: knowledge tree, evidence item, evidence index
├── references/        detail loaded only when needed
├── scripts/           helper scripts
└── evals/             test cases
tests/fixtures/        test data: source images, knowledge trees, answer keys
  ml-basics/           4 English slides, obvious errors
  model-eval/          8 Chinese slides, subtle errors
tests/baseline/        results of plain Claude without the skill, for comparison
tools/                 development helpers (e.g. make_fixture_slides.py)
```

## Install

```bash
pip install jsonschema
```

Then copy the `source-trace/` folder into your tool's skills folder:

| Tool | Skills folder |
|------|---------------|
| Claude Code (personal) | `~/.claude/skills/source-trace/` |
| Claude Code (one project) | `<project>/.claude/skills/source-trace/` |
| Codex | `~/.codex/skills/source-trace/` |

## Use

Ask in your own words, giving the slide images and the tree, for example:

> 这是我的课件截图（slides/ 文件夹）和 AI 生成的知识树 tree.json，帮我对照课件检查一下。

> Check knowledge-tree.json against my lecture slides in images/.

The skill writes `evidence-index.json`, `audit.json` and `report.md` to `sourcetrace-output/` next to the tree.

## Scripts

The skill runs these itself; you can also run them directly.

```bash
python source-trace/scripts/validate_input.py --tree tests/fixtures/ml-basics/knowledge-tree.json --images tests/fixtures/ml-basics/images
python source-trace/scripts/validate_evidence.py --index tests/fixtures/ml-basics/evidence-index.example.json
```

Add `--json` for machine-readable output. Exit code 0 means valid, 1 invalid, 2 a usage error.

## Status

v0.1 in development. Audit rules (`references/audit-rules.md`) are interim until Day 6; the report format is formalized on Day 7.
