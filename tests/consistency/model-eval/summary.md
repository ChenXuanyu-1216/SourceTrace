# Consistency check: model-eval (2026-11-02)

The SourceTrace skill at commit `bda9912`, run 3 times on the model-eval fixture (8 Chinese slides, 19 nodes, 18 edges). Each run was a fresh agent with its own copy of the skill, no answer key, and the same Chinese request. `report.md` was skipped because the test harness blocks sub-agents from writing it; only `evidence-index.json` and `audit.json` are compared.

Reproduce the numbers:

```bash
python -I tools/compare_runs.py . model-eval tests/consistency/model-eval/run-1 tests/consistency/model-eval/run-2 tests/consistency/model-eval/run-3
```

## Validity

| | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| `evidence-index.json` valid | yes | yes | yes |
| Evidence items (text / table / graphic) | 39 (33 / 4 / 2) | 39 (33 / 4 / 2) | 39 (33 / 4 / 2) |
| Nodes and edges with a verdict | 37 / 37 | 37 / 37 | 37 / 37 |
| Findings without evidence, unknown evidence IDs | none | none | none |
| `summary` adds up | yes | yes | yes |
| `DISCONNECTED_TREE` reported | yes | yes | yes |

All three extractions produced the same number of items of each type.

## Agreement between runs (37 nodes and edges)

| | Agree in all 3 runs |
|---|---|
| Verdict (supported / finding) | **37 / 37** |
| Category | **36 / 37** |
| Risk | **36 / 37** |

The one disagreement is **N017** (准确率 "是评价分类模型最可靠的指标"):

| Run | Category / risk | Reasoning |
|---|---|---|
| 1 | conceptual-error / high | The slides contain no weaker claim ("accuracy is reliable") that was strengthened, so the clause is a wrong addition contradicted by slide 8. |
| 2, 3 | overgeneralization / medium | "最…" is an absolute claim the slides don't make, and slide 8 contradicts it. |

Both readings follow the current `audit-rules.md`, which does not say what to do when an absolute claim has no weaker version in the source. This is the same overlap the smoke test flagged (skill-feedback point 8).

## Omissions (source → tree)

| Omission | Run 1 | Run 2 | Run 3 | Answer key |
|---|---|---|---|---|
| F1 score (slide 7 table) | medium | medium | medium | expected |
| Bias-variance trade-off (slide 4) | medium | medium | medium | acceptable |
| When to use cross-validation (slide 6) | medium | **low** | medium | acceptable |
| TP/FP/FN/TN definitions (slide 7) | — | — | **low** | not listed |
| Homework line (slide 8) | — | — | — | should not report |

The 3 main omissions are the same in every run. The differences are in minor details: whether to report them, and at what risk. Run 2 lowered a risk without a separate reason field, so it is not possible to check whether it followed the "only with a reason" rule.

## Against the answer key

Every run found all 11 planted tree problems with an accepted category, plus the F1 omission. No correct item was flagged and no run reported the homework line.

## Conclusions

1. **The skill is stable on this fixture.** Verdicts agree on 37/37 items, and the evidence extraction is structurally identical across runs.
2. **The remaining variation is in exactly two places,** both rule gaps rather than random noise:
   - an absolute claim with no weaker version in the source (`conceptual-error` vs `overgeneralization`),
   - whether a minor detail (when to use a method, symbol definitions) is a significant omission, and at what risk.
3. **For Day 7:** add a `risk_reason` field so that changes to the default risk can be checked.
4. **Limits:** 3 runs, one model (Claude), one 8-slide fixture written by the developer. This says nothing yet about larger decks, real scans, or Codex.
