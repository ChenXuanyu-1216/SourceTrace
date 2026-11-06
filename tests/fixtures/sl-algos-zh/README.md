# sl-algos-zh test set (scale test)

A synthetic Chinese lecture, 监督学习常用算法, written for this project: 32 slides and a knowledge tree with 78 nodes and 91 edges (169 items). Compared with wiki-ml-zh (12 pages, 98 items), it has about 2.7 times as many pages and 72% more items.

The lecture was created for this project. The saved audit outputs were produced by the agents described below.

## Running the fixture

Give a fresh agent only the SourceTrace skill, [images/](images/) and [knowledge-tree.json](knowledge-tree.json), in an isolated folder with no web access. Ask it to audit the tree against the slide images. Keep this README, the answer key, `RESULTS.md`, the saved runs and the deck-generation source outside that folder so they cannot reveal expected findings.

The slide images are already included. To regenerate them, run this command from the repository root. It requires Pillow (`python -m pip install pillow`) and the Windows fonts Arial and Microsoft YaHei, and writes to this fixture's `images/` directory.

```bash
python tools/make_fixture_slides.py sl-algos-zh
```

The source is [tools/decks/sl-algos-zh.json](../../../tools/decks/sl-algos-zh.json).

## What it tests

- **Size:** whether an agent keeps track of 169 items across 32 slides, and whether it still checks items near the end as carefully as the first ones.
- **Problems spread over the whole deck**, including two on the last two slides (N017, N032).
- **Evidence from two slides:** a definition supported only by combining slides (N043), and errors that a later slide confirms (N012, N016, N044, E040, E051).
- **Mixed slide types:** bullets, tables, a flow diagram and two tree diagrams.
- **Distractors:** an administrative line, homework, references, examples, and statements on slides 30–32 that are already covered by a finding.

## Answer key

[expected-findings.json](expected-findings.json) lists 28 expected item findings and 8 planted omissions:

- 26 planted item problems:
  - 9 conceptual errors;
  - 3 incorrect relationships;
  - 6 unsupported expansions: 2 terms absent from the deck, the 2 edges that use them, and 2 edges the deck states nowhere;
  - 3 added details (`scope: detail`);
  - 4 overgeneralizations;
  - 1 term the deck names but never defines (`ambiguous`).
- 2 unplanted findings, marked `"planted": false` and added after the first runs:
  - E044: the tree links SVM to kernel functions, but the deck never explicitly states that relationship;
  - N048: the tree defines 神经网络 from the slide's description of 多层感知机 (a source note).
- 8 planted omissions (5 core, 3 supporting).
- 141 correct items; `tricky_correct_items` explains those that look wrong. N078 随机搜索 was planted as `ambiguous` and is now correct.
- 4 acceptable extra omissions: real gaps in the tree that were not planted, which runs may report or leave out.
- 10 omission candidates that must not be reported, such as administrative text or content already covered by a finding.

The owner revised the key once after the first two runs (E044, N048, N078 and the acceptable extra omissions). See [RESULTS.md](RESULTS.md#owners-decisions).

After the audit, grade runs from the repository root. Each run directory must contain `audit.json` and `evidence-index.json`, either directly or under `input/sourcetrace-output/`. For the two saved runs:

```bash
python -I tools/compare_runs.py . sl-algos-zh tests/fixtures/sl-algos-zh/run-1 tests/fixtures/sl-algos-zh/run-2
```

Replace the final paths to compare new runs. The script checks evidence validity, item coverage, agreement and findings against the key. Omissions are matched by substrings in cited evidence or reasons. Omissions that match an acceptable extra are counted as accepted; any others need manual review. Its `expected items` count includes the two unplanted findings.

## Runs

- **[run-1/](run-1/) and [run-2/](run-2/)** (2026-11-06): skill v0.2.0, two fresh Claude agents with no web access.
  - Against the key used at the time, both matched 27 of 28 expected item findings and all 8 planted omissions. Both missed N078 and flagged N048, which that key marked correct.
  - Against the revised key, both match 28 of 28 and flag no correct items. The revision accepted the runs' reading of N078 and N048.
  - Their verdict, category and risk agreed on all 169 items. This agreement does not resolve the disagreements with the key.
  - Run 1 reported 12 omissions; run 2 reported 11. Neither reported a should-not-report omission candidate.
  - Reported cost was about 174k tokens and 8 minutes for run 1, and 162k tokens and 7 minutes for run 2.
  - Details and the open questions for the owner: [RESULTS.md](RESULTS.md).
