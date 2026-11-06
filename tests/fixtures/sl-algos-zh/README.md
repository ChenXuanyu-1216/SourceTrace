# sl-algos-zh test set (scale test)

A synthetic Chinese lecture, 监督学习常用算法, written for this project: 32 slides and a knowledge tree with 78 nodes and 91 edges (169 items). It is four times the slides and nearly twice the items of the largest earlier test set (wiki-ml-zh: 12 pages, 98 items).

Everything here was written by the developer, so there are no third-party rights. The slides are rendered from [tools/decks/sl-algos-zh.json](../../../tools/decks/sl-algos-zh.json):

```bash
python tools/make_fixture_slides.py sl-algos-zh
```

## What it tests

- **Size:** whether an agent keeps track of 169 items across 32 slides, and whether it still checks items near the end as carefully as the first ones.
- **Problems spread over the whole deck**, including two on the last two slides (N017, N032).
- **Evidence from two slides:** a definition supported only by combining slides (N043), and errors that a later slide confirms (N012, N016, N044, E040, E051).
- **Mixed slide types:** bullets, tables, a flow diagram and two tree diagrams.
- **Distractors:** an administrative line, homework, references, examples, and statements on slides 30–32 that are already covered by a finding.

## Answer key

[expected-findings.json](expected-findings.json) lists:
- 27 planted item problems:
  - 9 conceptual errors;
  - 3 incorrect relationships;
  - 6 unsupported expansions: 2 terms absent from the deck, the 2 edges that use them, and 2 edges the deck states nowhere;
  - 3 added details (`scope: detail`);
  - 4 overgeneralizations;
  - 2 terms the deck names but never defines (`ambiguous`).
- 1 unplanted finding: a mistake in the deck that both runs found (E044, marked `"planted": false`).
- 8 planted omissions (5 core, 3 supporting).
- 10 things that must not be reported, and the 141 correct items. `tricky_correct_items` explains the correct items that look wrong.

Never give the answer key or this README to the skill under test.

Grade runs with:

```bash
python -I tools/compare_runs.py . sl-algos-zh <run-dir> [<run-dir> ...]
```

## Runs

- **[run-1/](run-1/) and [run-2/](run-2/)** (2026-11-06): skill v0.2.0, two fresh Claude agents with no web access.
  - Both found 27 of the 28 item findings and all 8 planted omissions, flagged one correct item, and agreed on all 169 items.
  - About 170k tokens and 8 minutes each.
  - Details and the open questions for the owner: [RESULTS.md](RESULTS.md).
