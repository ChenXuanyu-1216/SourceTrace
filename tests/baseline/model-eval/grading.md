# Baseline grading: model-eval (2026-11-02)

Two runs of Claude (Opus 5.5) **without** the SourceTrace skill. Each got only the 8 Chinese slide images and `knowledge-tree.json` (no answer key), with this prompt:

> 这是我的课程课件（images/slide-01.png 到 slide-08.png），以及一个 AI 根据课件生成的知识树（knowledge-tree.json）。请对照课件检查这个知识树是否准确，指出其中的问题，以及课件中有哪些重要内容被遗漏了。

Answers: [run-1.md](run-1.md), [run-2.md](run-2.md). Graded by hand against [expected-findings.json](../../fixtures/model-eval/expected-findings.json).

## Detection

| Planted problem | Difficulty | Run 1 | Run 2 |
|-----------------|------------|-------|-------|
| N004 test set "也可用于调整超参数" | phrase added | found | found |
| N005 ratio 8:1:1 vs 7:2:1 | number changed | found | found |
| N006 "通常" → "总是", one cause dropped | qualifier | found, both parts | found, both parts |
| N012 L2 "同样倾向于产生稀疏解" | half right, half wrong | found | found |
| N015 precision has recall's definition | definitions swapped, table | found | found |
| N017 accuracy "最可靠" | needs slides 7 + 8 | found | found |
| E010 overfitting → high bias | diagram only | found | found |
| E011 underfitting → high variance | diagram only | found | found |
| E016 cross-validation uses test set | wrong edge, correct node | found, and said N014 is correct | found |
| N013 Dropout | true but not in slides | found | found |
| E015 regularization includes Dropout | true but not in slides | found | found |
| Omission: F1 score | table row | found | found |
| **Total** | | **12 / 12** | **12 / 12** |

Categories: both runs put N006 and N017 under "与课件矛盾" (contradictions). The answer key accepts that (`also_accept: conceptual-error`).

## Correct items (26)

- **Run 2** explicitly confirms 24 of 26. It does not list E005, and calls E012 (正则化 related-to 过拟合) "太笼统" (too vague) rather than wrong.
- **Run 1** confirms only N014 explicitly, and also calls E012 too vague.
- No correct item was called wrong. **0 false positives.**

## `should_not_report`: the homework line

Both runs list the homework line (slide 8) at the bottom of their omission lists, but both say it is not a knowledge point and can be left out of the tree. Counted as **handled correctly, with some noise**.

## Found something the answer key missed

Both runs report that the tree is **not connected**: overfitting, underfitting, bias/variance and regularization never link to the root 模型评估, although slide 1 lists them as topics of the lecture. Checked: the tree has **3 connected components**. This was not planted on purpose; it is a real flaw in the fixture tree. `validate_input.py` does not check for it.

## Extra omissions reported

Besides F1, both runs report: the bias-variance trade-off itself and when to use cross-validation (both in `acceptable_extra_findings`), plus TP/FP/FN/TN definitions, the accuracy and precision formulas, and L1/L2 details. Run 1 also suggests a separate 泛化能力 node. These are reasonable but finer-grained than the answer key. The granularity of "significant omission" is still undefined.

## Conclusions

1. **Subtle errors did not stump the baseline.** 12/12 in both runs, including diagram-only, table-only and two-slide problems in Chinese. At 8 slides, detection is not where SourceTrace adds value. Untested: much longer decks (30+ slides), low-quality images (scans, photos of whiteboards), and trees with hundreds of nodes, where attention may fail.
2. **The gaps are the same as on ml-basics:** no evidence IDs, no risk levels, categories that don't match the taxonomy, no machine-readable output, and a report shape that differs between runs.
3. **New for the validator:** warn when the tree has more than one connected component.
4. **New for the vocabulary:** both runs wanted a more specific relation than `related-to` for "正则化 用于降低 过拟合". The v0.1 list has no `reduces`/`mitigates`.
5. **The answer key needs an `acceptable_extra_findings` entry** for the disconnected tree.
