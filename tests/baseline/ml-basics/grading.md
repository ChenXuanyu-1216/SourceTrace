# Baseline grading: ml-basics (2026-11-01)

Two runs of Claude (Opus 5.5) **without** the SourceTrace skill. Each got only the 4 slide images and `knowledge-tree.json` (no answer key), with this prompt:

> Here are my lecture slides (images/slide-01.png to slide-04.png) and a knowledge tree that an AI generated from them (knowledge-tree.json). Please check whether the knowledge tree is accurate against the slides. Point out any problems, and anything important from the slides that's missing.

Answers: [run-1.md](run-1.md), [run-2.md](run-2.md). Graded by hand against [expected-findings.json](../../fixtures/ml-basics/expected-findings.json).

## Detection

| Planted problem | Expected category | Run 1 | Run 2 |
|-----------------|-------------------|-------|-------|
| N002 "does not require labels" | conceptual-error | found | found |
| E004 Unsupervised → Regression | incorrect-relationship | found | found |
| E007 Supervised → Unsupervised | incorrect-relationship | found | found |
| N008 Deep Learning | unsupported-expansion | found | found |
| E008 ML → Deep Learning | unsupported-expansion | found | found |
| N006 "every unsupervised task is clustering" | overgeneralization | found, called an error | found, called an error |
| N009 Feedback | ambiguous | found | found |
| Omission: dimensionality reduction | omission | found | found |
| **Total** | | **8 / 8** | **8 / 8** |

## Correct items (11)

- **Explicitly confirmed:** run 1 confirms 4 nodes (N001, N004, N005, N007) and says nothing about the rest. Run 2 confirms 10 of the 11.
- **E009 (RL uses Feedback):** both runs criticize it together with N009, because linking Feedback only to RL hides the fact that every paradigm has feedback. The answer key marks E009 as correct, but the criticism is reasonable. This is a borderline case, not a clear false positive.

## Where the baseline falls short of SourceTrace's goals

1. **No evidence IDs.** Sources are cited as "Slide 2", sometimes with a quote; run 1 gives no source column at all. Nothing is traceable at the level of a single evidence item.
2. **No consistent categories or risk levels.** The two runs group findings differently, both file the overgeneralization under errors, and neither ranks severity.
3. **No machine-readable output.** No `audit.json` equivalent, so nothing can be checked automatically.
4. **Omission granularity is undefined.** Besides dimensionality reduction, both runs list 5–6 more "missing" items (k-means, PCA, labeled vs. unlabeled data, the comparison table, RL components, "three paradigms"). Some are useful, some are a matter of taste. There is no rule for what counts as *significant*.
5. **Fixes ignore the schema.** Run 2's corrected tree uses relations such as `"feedback: correct answers"`, which the v0.1 vocabulary does not allow.
6. **Structure varies between runs.** The same input produces two differently organized reports.

## Implications

- **The fixture is too easy for detection.** The plain model already finds every planted problem, so this fixture cannot show a detection gain. It is still useful for checking format, traceability and consistency. Measuring detection needs harder cases: subtler errors, larger decks, Chinese slides, and real course material.
- **The skill's value is traceability and structure:** evidence IDs on every finding, fixed categories with risk levels, `audit.json`, schema-valid recommendations, and the same report shape on every run.
- **Rules to settle on Day 6:**
  - where the line between `conceptual-error` and `overgeneralization` falls
  - what makes an omission significant
  - whether an edge that is true but incomplete (E009) should be flagged
