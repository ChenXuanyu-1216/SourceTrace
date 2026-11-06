# model-eval-occluded test set (image quality)

The [model-eval-photo](../model-eval-photo/) images, plus glare that wipes out two pieces of evidence. It tests a rule no earlier test set reached: **the audit must not reject a tree item on unreadable evidence.**

| Slide | Hidden by glare | Tree item | On clean slides | Expected here |
|---|---|---|---|---|
| 2 | "7 : 2 : 1" at the end of the split-ratio bullet | N005 数据集划分比例 (8 : 1 : 1) | `conceptual-error`, high | `ambiguous`, low |
| 7 | the formula and meaning of the precision row; the label 精确率 (Precision) stays readable | N015 精确率 (given recall's definition) | `conceptual-error`, high | `conceptual-error` from readable evidence, or `ambiguous` |

A `conceptual-error` on N005 means the agent guessed the hidden numbers. For N015 both answers are accepted: the readable recall row shows that the tree gave precision the recall definition, but nothing readable says what precision is. Filling in the hidden definition from the agent's own knowledge is wrong either way. The rest of the answer key is the model-eval key, with one acceptable extra omission added to all model-eval keys (L2 "使权重整体变小").

One of three image-quality test sets, with [model-eval-scan](../model-eval-scan/) and [model-eval-photo](../model-eval-photo/). The images are made from the clean slides by a seeded script, so they are the same every time; the hidden areas are listed in `OCCLUSIONS` in the script:

```bash
python tools/degrade_images.py model-eval scan photo occluded
```

Give the skill under test only `images/` and `knowledge-tree.json`, never this README or the answer key. Grade runs with:

```bash
python -I tools/compare_runs.py . model-eval-occluded <run-dir> [<run-dir> ...]
```

## Runs

- **[run-1/](run-1/) and [run-2/](run-2/)** (2026-11-06): skill at `fb2bbc2`, two fresh Claude agents with no web access. Results for all three image-quality test sets: [RESULTS.md](RESULTS.md).
