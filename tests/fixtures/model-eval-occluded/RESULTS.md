# Image-quality test results (2026-11-06)

Six fresh Claude agents ran SourceTrace on the three image-quality versions of model-eval: two on [model-eval-scan](../model-eval-scan/), two on [model-eval-photo](../model-eval-photo/) and two on this test set. Each agent had an isolated folder with only the skill, `images/` and `knowledge-tree.json`, and no web access. The skill was at commit `fb2bbc2`, so these are also the first runs with the fourth rule revision. Outputs are saved unedited in each test set's `run-1/` and `run-2/`, with the agent's `skill-feedback.md`.

The baseline is the three day-6 runs on the clean slides ([tests/consistency/model-eval/day6](../../consistency/model-eval/day6/)). They used the v0.1 rules, so a difference can come from the images or from the rules changed since.

## Summary

| | Clean (3 runs, v0.1 rules) | Scan | Photo | Occluded |
|---|---|---|---|---|
| Expected item findings (key before the owner's decisions) | 11/11 each | 11/11 each | 11/11 each | 10/11 each (N015, see below) |
| Planted omissions | 4/4 each | 4/4 each | 4/4 each | 4/4 each |
| Correct items flagged | 0 | 0 | 0 | 0 |
| Should-not-report items reported | 0 | 0 | 0 | 0 |
| Same verdict, category and risk in all runs | 37/37 | 37/37 | 37/37 | 37/37 |
| Evidence certainty (high / medium / low) | all high | all high | all high | run 1: 39 / 1 / 1; run 2: 38 / 0 / 2 |
| Extra omissions | 0 | 0 | 1 per run (L2) | 1 in run 1 (L2) |
| Cost per run | not recorded here | about 93k tokens, 3 minutes | about 92k tokens, 3 minutes | about 96–98k tokens, 4 minutes |

All 18 script runs passed on the first try. Reproduce the grading from the repository root, for example:

```bash
python -I tools/compare_runs.py . model-eval-occluded tests/fixtures/model-eval-occluded/run-1 tests/fixtures/model-eval-occluded/run-2
```

## What the results show

- **Scan and photo quality had no effect.** Every agent read every slide, rated all evidence `high` certainty, and gave the same verdicts as the clean runs. Several said they went back to the image for each finding that hinges on one word or number, as the rules ask. These versions are still clean by real-world standards (typed text, no handwriting, mild blur), so this does not show how far the quality can drop.
- **Hidden evidence was not guessed.** On the occluded slides, both runs:
  - recorded the hidden parts as unreadable, with `low` certainty and a placeholder instead of the content, after enlarging the area and raising the contrast;
  - marked N005 (8 : 1 : 1) "cannot verify", not a conceptual error, and recommended checking the number against the original slide;
  - did not fill in precision's definition from their own knowledge, and recommended taking it from the original slide.
- **N015 is the one difference from the key.** Both runs kept N015 as a high-risk `conceptual-error`, not `ambiguous`. Their reason uses only readable evidence: the tree's definition of precision is word for word the slide's definition of recall, and the F1 row shows the two are different metrics. `audit-rules.md` names "precision given recall's definition" as an example of a conceptual error. See the decisions below.

## Disagreements reviewed by the owner

1. **N015 on the occluded slides (key: `ambiguous`; both runs: `conceptual-error`).** My recommendation is to accept `conceptual-error` as well. The runs did not use the hidden text: they showed the tree attached another concept's visible definition, and did not invent the correct one.
2. **An extra omission: L2 "使权重整体变小"** (slide 5). Both photo runs and occluded run 1 reported it as a supporting, low-risk omission; the scan runs and the clean runs did not. It is probably an effect of the fourth rule revision ("a finding covers only the content it is about"): the N012 finding is about sparse solutions, so the shrinking-weights effect is a separate point. Under the current rules it is a fair omission. My recommendation is to list it as an acceptable extra in the model-eval keys.

## Owner's decisions

Decided by the project owner on 2026-11-06:

1. **N015 on the occluded slides:** both answers are accepted. The key now expects `conceptual-error` (high) and also accepts `ambiguous`. Filling in the hidden definition is wrong either way.
2. **L2 "使权重整体变小"** is an acceptable extra omission in all four model-eval keys (clean, scan, photo, occluded).

Against the revised keys, all six runs match 11 of 11 expected item findings and 4 of 4 omissions, with no unmatched omissions. The three clean day-6 runs and the end-to-end run still match too. `compare_runs.py` now skips the risk check when a run gives an accepted alternative category, because each category has its own default risk.

## Gaps the agents reported

- **"Do not fall back on `related-to`" was read too widely.** It was added in the fourth revision for a correct relationship that no relation value expresses ("mitigates"). E010 and E011 already use `related-to` and only point at the wrong node. Five of the six runs asked whether the rule forbids keeping `related-to` there. All of them kept the relation and corrected the target, which is right, but the rule should say it applies only when no relation value fits.
- **Partly unreadable evidence.** The extraction rules don't say how to record an item that is only partly hidden. The runs differed: run 1 split the slide 2 bullet into a readable `high` part and a hidden `low` part, but recorded the slide 7 row as one `medium` item; run 2 used `low` for both. The placeholder text also differed. A rule could say: split the readable part from the hidden part, give the hidden part `low` certainty, and use a fixed placeholder such as ［无法辨认］.
- **Where to put working files.** Occluded run 1 saved enlarged crops in a folder next to its run folder and read them back, which broke the test's file rule. They were only crops of its own input images. Run 2 kept its crops inside its run folder and deleted them. The skill could say where temporary files go.

## Not tested

Heavy blur or low resolution, handwriting, real camera photos, and degraded versions of the larger test sets.
