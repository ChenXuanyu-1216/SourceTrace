# SourceTrace

An Agent Skill that audits an AI-generated knowledge tree against its source material. Give it the source images (PNG/JPG, e.g. exported slides) and the knowledge tree (JSON); it extracts evidence, maps every node and edge to that evidence, audits in both directions, and writes:

- `report.md`: a human-readable audit report
- `audit.json`: a machine-readable audit result

It works with any tool that supports Agent Skills, such as Claude Code or Codex.

## Layout

```
docs/requirements.md   scope, pipeline and open questions
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

## Validate inputs

```bash
pip install -r requirements.txt
python source-trace/scripts/validate_input.py --tree tests/fixtures/ml-basics/knowledge-tree.json --images tests/fixtures/ml-basics/images
```

Add `--json` for machine-readable output. Exit code 0 means valid, 1 invalid, 2 a usage error.

## Install

Copy `source-trace/` into your skills folder, for example `~/.claude/skills/source-trace/`.

## Status

Early draft.
