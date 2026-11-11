# Contributing to SourceTrace

Thank you for helping. The most useful contributions are:

- **A wrong verdict or a rule problem:** an audit that called something wrong when it was right, missed a problem, or picked the wrong category or risk. Every rule in the skill came from a reviewed run like this.
- **A bug in one of the scripts** (`validate_input.py`, `validate_evidence.py`, `build_report.py`).
- **A new test set** that follows the data policy below.

Please open an issue before a large change, so we can agree on it first.

## Privacy and test data: read this first

SourceTrace works on course material, which usually belongs to someone else.

- **Never attach slides, screenshots or audit outputs from material you may not share** in an issue or a pull request. Course slides usually belong to the instructor. `evidence-index.json` and `report.md` contain verbatim quotes from the slides, so treat them like the slides themselves.
- **Show the problem on material that is safe to share:** one of the test sets in `tests/fixtures/`, or a small example you made yourself (a few slides and a short tree are enough).
- **Test data in this repository** is openly licensed, written by the contributor, or synthetic. No third-party course material and no private data.

## Reporting a script bug

Use the "Script bug" issue template. Include the command you ran, its full output, your Python version and operating system, and the smallest input that shows the problem.

## Reporting a wrong verdict or a rule problem

Use the "Wrong verdict or rule problem" issue template. Include:

- the item: node or edge ID, its label or relationship, and its definition;
- what the skill said (verdict, category, risk) and what you expected;
- why, quoting the evidence: the evidence IDs, pages and the source's exact words;
- the skill version or commit, the agent (Claude Code, Codex, …) and the model;
- the part of `skill-feedback.md` or the agent's final message about it, if there is one.

## Development

```bash
pip install -r requirements.txt
python -m pytest
```

The tests take a few seconds and also run on GitHub Actions for every push and pull request. On Windows, run your own Python commands that print Chinese as `python -X utf8 …`.

- **Scripts** (`source-trace/scripts/`): keep to the standard library and `jsonschema`, keep the output deterministic (the tests check that it repeats byte for byte), and add or adjust tests in `tests/` for every change.
- **Rules** (`source-trace/SKILL.md`, `source-trace/references/`): keep each change short and in the existing style. Avoid new categories or schema fields unless one is unavoidable. A rule change should come from a run that shows the problem, and should say which run.
- **Saved runs are never edited or regenerated.** They record what the skill did with the rules of their time. A rule change is checked by new runs.
- **CHANGELOG.md:** add an entry under "Unreleased" for every change that users or test results would notice.

## Adding a test set

Look at an existing set first: [sl-algos-zh](tests/fixtures/sl-algos-zh/) for synthetic slides, [wiki-pc-zh](tests/fixtures/wiki-pc-zh/) for real content. A test set is a folder in `tests/fixtures/` with:

- `images/`: one PNG or JPG per page;
- `knowledge-tree.json`, following [`knowledge-tree.schema.json`](source-trace/schemas/knowledge-tree.schema.json), saved unedited if it came from an AI tool;
- `README.md`: what the set tests and where the tree came from;
- for openly licensed sources, `LICENSE.md` and `ATTRIBUTION.md`: the source, its revision or version, the authors, the license, and what you changed;
- an answer key: `expected-findings.json` for synthetic sets, which `tools/compare_runs.py` grades against, or a `REVIEW.md` for real content.

**Runs** go in their own subfolders (`run-1/`, `audit-run-1/`, `codex-run-1/`), with the agent's outputs and its `skill-feedback.md`, unedited. Each run is a fresh agent in a clean folder that holds only `source-trace/`, the images and the tree, with no web access. Save the prompt you used.

## Pull requests

- Keep each pull request to one change, and say what it changes and why.
- Run `python -m pytest` before opening it.
- Add the CHANGELOG entry.

## License of contributions

By contributing, you agree that your contribution is released under the [MIT License](LICENSE), except for material in `tests/fixtures/wiki-*/`, which is under CC BY-SA 4.0 like the rest of those folders.
