# model-eval-scan test set (image quality)

The 8 [model-eval](../model-eval/) slides as a greyscale photocopy scan: a slight tilt, lower contrast, blur, speckles and JPEG artefacts. The tree is the model-eval tree, and the answer key is the model-eval key unchanged, so any difference from the clean runs comes from the images.

One of three image-quality test sets, with [model-eval-photo](../model-eval-photo/) and [model-eval-occluded](../model-eval-occluded/). The images are made from the clean slides by a seeded script, so they are the same every time:

```bash
python tools/degrade_images.py model-eval scan photo occluded
```

Give the skill under test only `images/` and `knowledge-tree.json`, never this README or the answer key. Grade runs with:

```bash
python -I tools/compare_runs.py . model-eval-scan <run-dir> [<run-dir> ...]
```

## Runs

- **[run-1/](run-1/) and [run-2/](run-2/)** (2026-11-06): skill at `fb2bbc2`, two fresh Claude agents with no web access. Results for all three image-quality test sets: [model-eval-occluded/RESULTS.md](../model-eval-occluded/RESULTS.md).
