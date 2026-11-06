# Skill feedback: SourceTrace run on "模型评估与泛化" (8 slides, occluded images)

## 1. Script runs

| Script | Runs | Result |
|---|---|---|
| `scripts/validate_input.py --json` | 1 | Valid. One warning: `DISCONNECTED_TREE` (3 parts). No errors. |
| `scripts/validate_evidence.py` | 1 | Valid on the first run (8 sources, 40 items). Warning `LOW_CERTAINTY` for EV-014 and EV-034, which is intended. |
| `scripts/build_report.py` | 1 | Succeeded on the first run: 26 supported, 11 findings, 4 omissions. |

No run failed, so nothing had to be changed in response to script errors. Before the build I made one edit by my own choice: I removed a suggested `includes` edge from 偏差-方差权衡 to N008/N009 in an omission recommendation, because the source does not state it ("Add no claims of your own").

## 2. Unclear or missing instructions

1. **Partly occluded evidence items.** evidence-extraction.md sets `certainty` per item and says "Do not split a definition from its own explanation". It does not say what to do when one part of a bullet or table row is legible and another part is hidden.
   - Slide 2, bullet 4: I split it into EV-013 (the legible text "本课程推荐的划分比例：训练集 : 验证集 : 测试集 =", `high`) and EV-014 (the hidden value, `low`). The splitting rule covers only clauses about different concepts, so this was my own call.
   - Slide 7, precision row: the rule is "One item per … data row", so I kept the row as one item. I marked it `low` because the formula and meaning cells are hidden. As a side effect, the legible metric name "精确率 (Precision)" now has `low` certainty too, and EV-034 is cited in the supported edge E007. A rule for this case would help, for example: "split off the unreadable cells" or "use certainty for the cells that matter".
2. **How to write unreadable content.** The skill says "Quote text verbatim" and also "extract what you can with low certainty … do not invent content". It gives no placeholder format for text you cannot see. I wrote `[被遮挡，无法辨认]` in `content` and described the white patch in `location`.
3. **N015 精确率: occluded definition vs. a definition moved from another concept.** Three rules seemed to point different ways:
   - audit-rules Q5 lists "precision given recall's definition" as a conceptual error.
   - Q7 says `ambiguous` when "the only relevant evidence has `low` certainty".
   - SKILL.md says "`low` evidence cannot reject a tree item on its own".

   The source's own precision row (EV-034) is unreadable. But the tree's wording matches the high-certainty recall row (EV-035) word for word, and the F1 row (EV-036) treats precision and recall as two different metrics. I judged that the rejection rests on high-certainty evidence and is not "the only relevant evidence", so I chose `conceptual-error` (high). In the reason I say plainly that the precision row is occluded. In the recommendation I did not supply the correct definition, because it cannot be read from the image and I may not use outside knowledge. A worked example for "correct definition unreadable, but the tree's definition provably belongs to another concept" would remove this guesswork.
4. **Fixing a swapped `related-to` edge.** SKILL.md says "Do not fall back on `related-to`, which loses the direction". E010 and E011 already use `related-to`, and the slide-4 arrows (欠拟合 → 高偏差, 过拟合 → 高方差) have no labels. No allowed relation clearly states "corresponds to", and the error is the target, not the relation. So I recommended keeping `related-to` and correcting the target. I was not sure whether the rule is meant to forbid this. It reads as if it is about choosing a replacement relation, not about keeping the tree's own relation.
5. **When to tell the user about unreadable pages.** "Unreadable image: … tell the user" is clear about what to do. It does not say whether a partly occluded page counts as an "unreadable image". I treated it as one and say so in the final message.

Everything else (agenda rule for E001/E006/E018, qualifier test for N006/N017, Dropout as unsupported-expansion, omission tiers) was clear and matched this case directly.

## 3. Image difficulties

- All 8 slides are photographed or rendered at a slight perspective angle, with vignetting and a dark border. The text was still clearly legible, so this did not affect certainty.
- **Slide 2:** a white patch covers the ratio value after "训练集 : 验证集 : 测试集 =".
- **Slide 7:** a white patch covers the 公式 and 含义 cells of the 精确率 (Precision) row.
- To make sure nothing could be recovered, I cropped both regions, enlarged them and raised the contrast with PIL (temporary files in a `crops/` folder inside `img-occluded-2/`, deleted afterwards). Both patches were uniformly blank.
- I extracted the occluded parts as `low`-certainty placeholders and did not fill them from general knowledge. N005 (8:1:1) is reported as `ambiguous`. In the N015 finding I note that the correct precision definition must be taken from the original slide.
