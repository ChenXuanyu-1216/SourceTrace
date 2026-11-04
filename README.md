# SourceTrace

An Agent Skill that audits an AI-generated knowledge tree against the slides it was built from.

AI tools can turn lecture slides into a knowledge tree in seconds, but a definition may be wrong, a relationship may be invented, and important material may be missing. SourceTrace checks every node and edge against the source images and backs each verdict with evidence: **why** it is a problem, **where** it is in the slides (page and quote), and **what** it rests on (evidence IDs).

It works with tools that support Agent Skills, such as Claude Code or Codex, and handles slides in Chinese or English.

## What you get

Give it the slide images (PNG/JPG) and the knowledge tree (JSON). It writes three files to `sourcetrace-output/` next to the tree:

| File | Content |
|------|---------|
| `report.md` | The audit report: summary, findings, omissions, structure problems, confirmed items |
| `audit.json` | The same result in machine-readable form: a verdict for every node and edge |
| `evidence-index.json` | Everything extracted from the slides, each item with an ID, page and verbatim quote |

Two findings from a run on 8 Chinese slides, with the text shortened and the recommendation column left out ([full report](tests/smoke/model-eval-e2e/report.md)):

| 编号 | 对象 | 类别 | 风险 | 问题 | 证据 |
|---|---|---|---|---|---|
| F-002 | N005 数据集划分比例 | 概念错误 | 高 | 比例数字错误：树中写"8 : 1 : 1"，课件写"7 : 2 : 1"。 | EV-013 第 2 页 "本课程推荐的划分比例：训练集 : 验证集 : 测试集 = 7 : 2 : 1。" |
| F-004 | E010 过拟合 —related-to→ 高偏差 | 关系错误 | 高 | 关系对调：第 4 页图示为"过拟合 → 高方差"，树中却把过拟合连到高偏差。 | EV-020 第 4 页 "Diagram: 过拟合 → 高方差（对训练数据过于敏感）" |

Each problem gets one of six categories (conceptual error, incorrect relationship, unsupported expansion, overgeneralization, ambiguous, omission) and a risk level, and every finding includes a recommended fix.

## Quick start

1. Install the one dependency:

   ```bash
   pip install jsonschema
   ```

2. Copy the `source-trace/` folder into your tool's skills folder:

   | Tool | Skills folder |
   |------|---------------|
   | Claude Code (personal) | `~/.claude/skills/source-trace/` |
   | Claude Code (one project) | `<project>/.claude/skills/source-trace/` |
   | Codex | `~/.codex/skills/source-trace/` (check your Codex version's documentation) |

3. Ask in your own words, giving the slide images and the tree:

   > 这是我的课件截图（slides/ 文件夹）和 AI 生成的知识树 tree.json，帮我对照课件检查一下。

   > Check knowledge-tree.json against my lecture slides in images/.

The tree must follow [`knowledge-tree.schema.json`](source-trace/schemas/knowledge-tree.schema.json) (nodes with `id`, `label`, `definition`, `kind`; edges with `id`, `source`, `target`, `relation`). If yours uses another format, the skill converts it first and tells you what it mapped. PPT or PDF slides need to be exported to images.

## Privacy

SourceTrace runs inside your AI agent, so the agent reads your slide images and knowledge tree. They are sent to whichever AI model your agent uses, under that provider's terms. The skill's own scripts run locally and send nothing anywhere.

- **Only audit slides you are allowed to share** with your AI provider. Course slides usually belong to the instructor, so you may need their permission.
- **Treat the outputs like the slides themselves.** `evidence-index.json` and `report.md` contain verbatim quotes from them.
- **Don't commit or publish someone else's slides or audit results** without permission.

## How well it works

On two test sets (4 English slides, 8 Chinese slides), a plain AI assistant and SourceTrace both found every planted error. SourceTrace adds what the plain model lacks:

- evidence IDs, pages and quotes behind every verdict,
- a verdict for every node and edge,
- fixed categories and risk levels,
- a machine-readable `audit.json`,
- no off-target "missing" items,
- the same result in all four runs on the Chinese set.

It costs about 30% more tokens and 3× the time. Both test sets are synthetic. The next tests use openly licensed material and larger, lower-quality decks (see [Status and next steps](#status-and-next-steps)). Details: [docs/evaluation.md](docs/evaluation.md).

## How it works

SourceTrace runs six stages: source ingestion → evidence extraction → knowledge mapping → bidirectional audit → conflict detection → audit report. The agent does the parts that need judgment: reading the slides, matching claims to evidence, and choosing verdicts. Three scripts do everything that can be checked or computed:

| Script | Stage | Does |
|--------|-------|------|
| `validate_input.py` | 1 | Checks the tree and the images; numbers the pages; warns about structure problems such as a disconnected tree |
| `validate_evidence.py` | 2 | Checks the evidence index: unique IDs, matching pages and sources |
| `build_report.py` | 6 | Checks the agent's `audit.json` against the tree and the evidence, adds the summary and finding IDs, and generates `report.md` |

The rules for verdicts, categories, risk and omissions are in [`references/audit-rules.md`](source-trace/references/audit-rules.md). The design decisions behind them are in [docs/requirements.md](docs/requirements.md).

You can also run the scripts yourself:

```bash
python source-trace/scripts/validate_input.py --tree tests/fixtures/ml-basics/knowledge-tree.json --images tests/fixtures/ml-basics/images
python source-trace/scripts/validate_evidence.py --index tests/fixtures/ml-basics/evidence-index.example.json
python source-trace/scripts/build_report.py --tree <tree.json> --index <output>/evidence-index.json --audit <output>/audit.json
```

The two validators accept `--json` for machine-readable output. All three scripts exit with 0 on success, 1 on invalid input, and 2 on a usage error.

## Development

```bash
pip install -r requirements.txt
python -m pytest
```

77 tests, about 2 seconds. They cover the three scripts (valid input, every error and warning code, repeatable output, Chinese and English reports). They also check that the saved skill runs still meet the answer keys. They do not run the skill itself, which needs an agent; use `tools/compare_runs.py` to grade new runs.

```
source-trace/          the skill (this folder is what gets installed)
├── SKILL.md           instructions and trigger description
├── schemas/           JSON Schemas: knowledge tree, evidence item, evidence index, audit
├── references/        extraction and audit rules, loaded when needed
└── scripts/           the three scripts above
docs/                  requirements and evaluation
tests/fixtures/        test sets: slide images, knowledge trees, answer keys
tests/baseline/        plain-AI runs, for comparison
tests/smoke/           end-to-end runs of the skill
tests/consistency/     repeated runs of the skill
tests/test_*.py        the pytest suite
tools/                 make_fixture_slides.py, compare_runs.py
```

## Status and next steps

v0.1.0. See [CHANGELOG.md](CHANGELOG.md).

Test data policy: SourceTrace is tested only on material that is openly licensed, written by the project owner, or synthetic. No third-party course material and no private data are used.

Next:

1. **Openly licensed real content:** the Chinese Wikipedia article 机器学习, captured as [tests/fixtures/wiki-ml-zh](tests/fixtures/wiki-ml-zh/) (CC BY-SA 4.0 in its own folder), with the knowledge tree generated by a different AI tool and the report reviewed by the project owner as an independent answer key.
2. **Larger decks and trees:** a synthetic deck of 30+ slides and a tree with 100+ nodes.
3. **Lower-quality images:** scan- and photo-like versions of the test slides (blur, noise, rotation, compression), generated by a script.
4. **Codex** and other Agent Skills tools.

## License

[MIT](LICENSE)
