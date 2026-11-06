# Skill feedback (source-trace, img-scan-2 run)

## 1. Script runs

| Script | Runs | Result |
|--------|------|--------|
| `scripts/validate_input.py --json` | 1 | valid; one warning `DISCONNECTED_TREE` (3 parts) |
| `scripts/validate_evidence.py` | 1 | VALID: 8 sources, 39 evidence items (2 graphic, 4 table, 33 text) |
| `scripts/build_report.py` | 1 (plus one `--help` call to see the options) | WRITTEN on the first run: 26 supported, 11 findings, 4 omissions |

No run failed, so nothing had to be changed in response to an error.

## 2. Unclear or guessed points

1. **Swapped edges and `related-to`.** SKILL.md: "If no allowed relation expresses the correct relationship … Do not fall back on `related-to`, which loses the direction." E010/E011 already use `related-to`, and the slide-4 arrows (欠拟合 → 高偏差, 过拟合 → 高方差) carry no label, so no specific relation (`causes`, etc.) is stated by the source. I recommended replacing the edges with the corrected target and kept `related-to`, because choosing `causes` would add a claim the source does not make. The rule reads as if it is only about relationships that need a missing verb; it does not say what to do when the source's own arrow is unlabeled.
2. **A finding's recommendation vs. a separate omission.** audit-rules.md says both "Before reporting, check that the content is not already covered by a finding on an existing node" and "A finding covers only the content it is about." The L2 bullet (EV-025) contains the contradicted part (一般不产生稀疏解) and an extra property the tree lacks (使权重整体变小). I put the extra property into the N012 recommendation (which restores the source sentence) and did not file a separate supporting omission. Same for the test-set caveat on slide 8 (EV-038, cited by the N004 finding) and the accuracy caveat (EV-037, cited by the N017 finding), where the rules give an explicit example, so those were clear.
3. **Slide title + bullet list as evidence for `includes`.** The agenda rule covers "a lecture title followed by a list of topics". It does not say whether a content slide titled 数据集划分 listing 训练集 / 验证集 / 测试集 supports 数据集划分 includes 训练集. I judged it supported, and also cited EV-013 (the 划分比例 bullet naming all three sets), so the verdict does not rest on structure alone.
4. **Notation legend granularity.** evidence-extraction.md has rows for titles, bullets, table rows and diagrams, but not for a legend line above a table ("TP：真正例　FP：假正例 …"). I made it one `text` item with location "Legend line above the table" rather than four items, since no tree item cites a single symbol.
5. **Splitting a bullet with a trade-off.** Slide 4's "模型复杂度增加时，偏差降低、方差升高；需要在两者之间取得平衡" has two clauses joined by "；". I kept it as one item, since both clauses are about the same concept (偏差-方差权衡) and no tree item cites either part separately. The splitting rule supports this, but it took some thought.

Everything else (verdicts, the decision order, risk defaults, the omission tiers) was clear and matched this deck directly; several findings (过拟合 "总是", 准确率 "最可靠", L2 稀疏解, 精确率/召回率 swap, 7:2:1 vs 8:1:1) are the rules' own worked examples.

## 3. Image issues

- All eight images look like scans or photos of printed slides: grayscale, low contrast, speckle noise all over the background, and a slight tilt/skew (the header bars on slides 4 and 8 are visibly rotated; the slide-4 diagram boxes are not quite level).
- Despite this, all text was legible, so every evidence item is `certainty: high`. I re-checked the exact words and numbers that findings depend on: "7 : 2 : 1" (slide 2), "不可用于调参" (slide 2), "通常" (slide 3), "一般不产生稀疏解" (slide 5), the precision/recall "含义" cells (slide 7) and "只能在最终评估时使用一次" (slide 8).
- The "k−1" on slide 6 is rendered with a dash that could be a hyphen or a minus sign; I transcribed it as a minus sign (U+2212). No finding depends on it.
- The slide-4 arrows have no labels, which limited what replacement relation could be recommended for the swapped edges (see point 1 above).
