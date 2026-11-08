# Skill feedback (SourceTrace run on input/: 感知器, 6 web-page screenshots)

## 1. Script runs

| Script | Runs | Failed runs |
|---|---|---|
| `scripts/validate_input.py --json` | 1 | 0 (valid, no warnings; 35 nodes, 48 edges, 6 images) |
| `scripts/validate_evidence.py` | 1 | 0 (87 items: 83 text, 4 graphic) |
| `scripts/build_report.py` | 1 | 0 (81 supported, 2 findings, 9 omissions) |

No run failed, so nothing had to be changed in response to script errors. Before the single `build_report.py` run I edited two of my own omission recommendations, because on re-reading they added claims of my own ("这也解释了感知器为什么输出二元值"; "每一项 −(wᵀp_i)t_i 都为正"). That was my own check against the "Add no claims of your own" rule, not a script error.

## 2. Unclear or underspecified instructions

1. **A likely slip in the source that only outside knowledge reveals.** audit-rules.md, "Problems in the source itself": "the source may contradict itself or contain an evident slip". The source says "其中R为输入向量的最大平均值"; the tree says "R是输入向量的最大范数". Nothing else in the source talks about R, so the source does not contradict itself. The slip is only "evident" if you know the theorem from outside, and evidence-extraction.md says "Never fill in hidden text from your own knowledge". The rules don't say whether outside knowledge may make a slip "evident". **What I did:** I judged N029 against the printed text. The two words name different quantities and cannot both describe R, so I used question 5 (`conceptual-error`). I lowered the risk to medium with a `risk_reason`, and in the final message I list the wording as a possible problem in the source.

2. **Risk for a wrong endpoint in a parameter range.** "Use the default unless there is a concrete reason not to, e.g. … a wrong number in a minor example → `medium`." N023 gives 0<α<1 where the source has 0<α≤1. This is not an example, but it is a small numeric detail of a correct definition. **What I did:** I used `conceptual-error` with risk `medium` and a `risk_reason`. Another run could reasonably keep `high`. A sentence on wrong ranges or bounds, as opposed to wrong values, would help.

3. **Two overlap rules that conflict.** evidence-extraction.md says "Extract each statement once, on the page where it is first complete", and also "A sentence split across two images is one item on the page where it starts; say `continues on page N`". Several sentences start, cut off, at the bottom of one screenshot and appear complete at the top of the next. Under the first rule they belong on the later page; under the second, on the earlier page. **What I did:** I read the second rule as applying only when no single image shows the whole sentence. These sentences went on the page where they are first complete, and the `location` says where they start (e.g. EV-013, EV-029, EV-045, EV-084).

4. **A formula introduced on a different page.** "Write a formula … in a `text` item together with the sentence that introduces it." "为此，Rosenblatt提出了感知机准则函数：" is at the bottom of page 4, and formula (3) is on page 5, which also repeats the sentence. **What I did:** I made one item on page 5 (EV-068) and noted this in `location`.

5. **The label test against "a class defined from a single instance".** N003 线性分类器 is defined as "利用特征的线性组合形成决策边界". The source never defines linear classifiers in general, and only says the perceptron is one. Question 6's single-instance rule would make this a `detail` finding. The label test in Verdicts ("could this part be false while the rest … is true?") makes it `supported`, because a linear decision boundary is what "linear classifier" means. The rules don't say which test wins. **What I did:** I applied the label test (`supported`), because the rules say to apply it first.

6. **A `contrasts-with` edge between two notations that the source never compares.** E017 links the 0/1 output convention in the 定义 section to the ±1 sign function in the 结构 section. The source never says they differ, but the two formulas plainly do. Question 3 ("stated nowhere, not even by combining pages") left room for doubt. **What I did:** I marked it `supported` by combining EV-040 and EV-058. A line in the edge cases on whether two formulas that visibly differ "state" a contrast would help.

7. **How to group a long history section.** "One omission per missing concept. Group its details into that one entry." A history section with about ten dated events is not one concept. **What I did:** I made two background omissions: early history up to 1962, and the period after 1969 (stagnation, recovery, the 1998 kernel-method work).

The rest was clear: verdicts, the decision order, the tiers, the navigation-box rule, and the script usage.

## 3. Image difficulties

- **Small text in low-resolution screenshots.** The images are 800×600 phone-width screenshots of a Wikipedia page. The body text is small, and sub- and superscripts in formulas (wᵀp_i, ∑_{p_i∈M}, (2R/γ)², 0<α≤1) are hard to read at native size. I made 2× enlarged crops (in `work/`) of every formula area and of the passages that findings hinge on. The crops confirmed "0 < α ≤ 1" and "最大平均值" before I reported on them.
- **Overlapping screenshots.** Each image repeats several lines of the previous one, and sentences are cut at the top and bottom edges. I extracted each sentence once, as described in 2.3.
- **Unreadable figure detail.** The neuron illustration on page 1 has labels too small to read even when enlarged. I extracted only its caption (EV-012) and did not use the figure for any verdict. The perceptron diagram on page 4 was readable when enlarged and gave three `graphic` items.
- **Site chrome.** I skipped the Wikipedia header, revision notice, disambiguation note and edit links. The "机器学习与数据挖掘" sidebar became a single navigation-box item (EV-014), which no verdict relies on.
