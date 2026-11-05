# Skill feedback: dt-audit-1 (决策树学习, 6 pages, 35 nodes, 46 edges)

## 1. Script runs

| Script | Runs | Result |
|---|---|---|
| `validate_input.py --json` | 1 | valid, no errors, no warnings |
| `validate_evidence.py` | 1 | VALID: 6 sources, 98 evidence items (6 graphic, 92 text) |
| `build_report.py` | 1 | written: supported 77, findings 4, omissions 7 |

No run failed, so nothing had to be changed in response to a script error.

Side note on `build_report.py` output (not an error):
- The evidence column truncates long quotes. For F-003 (CHAID) the quote is cut at “在生成树的过程中…”, right before “多层分裂”, which is the word the finding is about. The reason column still quotes it, but a reader checking the evidence column does not see the key word. audit-rules.md says findings that hinge on an exact word should quote the exact text; the truncation works against that.
- In the summary's “最重要的问题” list, omissions show as “F-005 —：…”. The dash with a full-width colon looks like a formatting slip.
- With no main findings, the top-problems list is filled with omissions, including two low-risk supporting ones (F-006, F-007). That is defensible, but it makes low-risk items look like the headline.

## 2. Unclear or missing instructions

1. **Overlapping screenshots.** The pages are scrolling captures of a web page, so content repeats across pages (the end of page 1 shows again on page 2, the Bagging bullet on pages 2 and 3, the Gini formula on pages 3 and 4, the advantages list on pages 5 and 6). evidence-extraction.md says “One item per checkable statement” and “IDs are never reused”, but does not say whether repeated content should get one item or one per page. I extracted each statement once, on the page where it first appears in full, and noted the repeat in `location`.

2. **Website chrome.** “Skip page numbers, logos and decoration” and “Also extract non-knowledge text such as homework or reading notes” do not say how to treat page furniture: a site banner, a revision notice, hatnotes, a navigation sidebar. I skipped the Telegram banner and the revision notice as decoration. I extracted the two hatnotes and the “机器学习与数据挖掘” sidebar list as text items, and did not use the sidebar in the audit.

3. **Reading order in two-column layouts.** “by page, then top to bottom, left to right” is ambiguous when a right-column figure sits beside left-column text. I numbered the left column first, then the right-column figure and caption.

4. **Displayed formulas.** The extraction table has rows for titles, bullets, tables and diagrams, but none for equations. I used `type: text` and transcribed the formulas in Unicode (Σ, subscripts, log₂).

5. **Narrowing qualifiers and hedges.** audit-rules.md says “Paraphrase is fine if the meaning, numbers and qualifiers are unchanged”, and question 4 covers only absolute or widening words. It does not cover a qualifier that narrows or hedges a claim. The tree has several: “在分类时” (Bagging voting), “某些决策树方法” (XOR), “通常” (data preparation, heuristic search), “可能存在” (IG bias), “缓解” where the source says “避免”. Read strictly, each changed qualifier blocks `supported`, which would add five or six near-noise findings. My rule: hedges that only weaken certainty (通常, 可能, 缓解) are `supported`, because the source entails them. Restrictions that move the claim to a narrower subject or condition than the source, and imply a contrast the source does not make (“在分类时”, “某些决策树方法”), are `unsupported-expansion` scope `detail` under question 6. Please state this explicitly.

6. **A different word that is a different concept.** Question 6 says “A word that differs from the source's but does not contradict it (预测误差 where the source says 泛化误差) is not part of the finding.” The source says CHAID uses “多层分裂” and the tree says “多路划分”. These do not contradict each other, but they are not synonyms: multi-level and multi-way are different properties. I reported it as a `detail` finding (F-003). Some guidance is needed on when a differing word is a synonym (ignore it) and when it is a separate unsupported property.

7. **Omission tiers overlap.** Core includes “a defined term; a stated rule”. Supporting includes “a property or caveat of a concept that is in the tree”. Many items are both: the source's own definition of Gini impurity when the node exists with a different, compatible definition; the TDITD stopping condition; “CART 最先由 Breiman 等提出”. I chose `supporting` whenever the concept itself is already a node. Core lists “a relationship shown in a diagram” but not a relationship stated in text (“ID3, C4.5 和 C5.0 决策树的生成使用信息增益”). I put the missing C4.5/C5.0 → 信息增益 link under core as “a stated rule”.

8. **Comparisons that are not in parentheses.** The not-knowledge tier mentions “Examples in parentheses”. The advantages section has comparisons written as full sentences (“其他技术往往需要数据归一化”, “关联规则只能处理类别型的而神经网络只能处理数值型的数据”, “神经网络是黑箱模型”). I treated them as illustrative comparisons and did not report them as omissions. That was a guess.

9. **The explanation-of-term test still leaves judgment calls.** I applied “could this part be false while the rest of the definition is true?” and accepted these as explanations of the term: 信息熵 “衡量…不确定性”, 剪枝 “删减树的部分结构来控制复杂度”, 主元分析/旋转森林 “变换（输入）特征”, 节点纯度 “类别越集中则纯度越高”. Another careful run could plausibly mark 主元分析 “变换输入特征” as a `detail` finding, because the source never explains PCA.

10. **Diagram-based edges.** E032 (泰坦尼克号生存预测 example-of 分类树) is not stated in words. I called it supported by combining the figure, whose leaves are the class labels died/survived, with “分类树 的输出是样本的类标”. The rules allow combining pages but give no example of inferring the type of a figure from its content. I would have liked one.

Everything else (stage order, file locations, schema fields, risk defaults, report generation) was clear.
