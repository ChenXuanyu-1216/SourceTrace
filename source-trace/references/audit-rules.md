# Audit rules (v0.1)

How to decide verdicts, categories and risk levels in stages 4 and 5. The rules are written so that two careful runs reach the same answer; where a judgment call remains, the rule says which way to lean.

## Verdicts

Every node and every edge gets exactly one verdict:

| Verdict | When |
|---------|------|
| `supported` | The evidence says the same thing. Paraphrase is fine if the meaning and numbers are unchanged and the qualifiers are unchanged or narrower (see below). |
| `finding` | Anything else. The finding gets one category from the decision order below. |

A `supported` verdict also cites its evidence IDs. "Looks fine" without evidence is not a verdict.

A definition that only restates or spells out its own label adds no claim to check (e.g. 分类评价指标: "用于评价分类模型性能的指标"). If the label's term is in the source, the node is `supported`; cite where the term appears. Use questions 6 and 7 below only when the definition says something more than the label.

The same holds for a plain-words explanation of what the term itself means, once the source supports the term and its main point. Example: 过拟合 "模型过度适应训练数据的细节而使未见数据上的表现下降" when the source says overfitting lowers generalization. "过度适应训练数据" is what the word overfitting means, not an added mechanism, so the node is `supported`. To tell the two apart, ask: **could this part be false while the rest of the definition is true?** If not, it is an explanation of the term. If it could, it is a separate claim, and question 6 applies (e.g. "有放回" could be false of a sampling method that is otherwise as described).

**A narrower or more cautious claim that the source implies is `supported`.** This is the mirror image of the qualifier test in question 4: widening a claim is a finding, but narrowing it is not, as long as the source's statement already implies the tree's. Examples:
- a narrower case: 装袋法 "在分类时以投票汇总" when the source says the result is produced by voting;
- fewer members: "难以被某些决策树方法简洁表达" when the source says decision trees cannot solve the problem well;
- weaker certainty: 通常, 可能, 缓解 where the source says 避免.

Do not recommend restoring the source's broader wording. Only a *new* condition, mechanism or property that the source does not imply goes to question 6.

This does not cover a range or bound that the tree gives as the source's own condition. "资料将其设为满足0<α<1" where the source says "0 < α ≤ 1" excludes a value the source allows, so the source does not imply it: question 5 applies.

Only the label, the definition and the relationship are audited. Node `kind` is a label from the tool that generated the tree, not a knowledge claim: do not report a `kind` that differs from what the slides call the concept.

## Categories: decision order

**First, gather all the evidence for the item:** text, table rows and figures (`graphic` items) on every page, not just the page where the term first appears. Figures count as much as text: a diagram that groups similar points into circles is evidence for what clustering means. Paraphrase is fine: a definition is supported if the evidence, combined across pages, says the same thing in other words. Answer the questions below only after this step. Most false "cannot be checked" findings come from skipping it.

Then go through these questions in order and stop at the first "yes". Questions 2–3 apply only to edges and 4–7 only to nodes.

1. **Is the node's concept (or, for an edge, either end node's concept) absent from the source?** → **`unsupported-expansion`** (scope `whole`). Cite the evidence that shows what the source says instead, if any (e.g. the slide that lists the actual members of a group).
   - **The concept counts, not the word.** A concept is in the source when the source names it or describes the thing the label names, in any words. A label taken from outside the source is not a finding by itself. Examples: 词袋表示 when the source says texts are represented by word sets "以词频为特征" and words do not depend on their "位置"; 概率平滑修正 when the source says the probability estimates are "修正" so that no probability is 0. Both concepts are present, so continue with the next questions; the edges using these nodes are not affected.
   - **An outside name can still carry a claim.** If the name adds something the source does not state (a specific method, formula or property, e.g. a named smoothing formula when the source only says the estimate is corrected), that claim goes to question 6 as a `detail`.
2. **Edges: does the evidence contradict the relationship** (wrong target, reversed, swapped, or a link the source rules out)? → **`incorrect-relationship`**. Judge the edge on its own, even if one of its nodes also has a finding.
3. **Edges: is the relationship stated nowhere,** not even by combining pages, while nothing contradicts it either? → **`unsupported-expansion`** (scope `whole`). Every other edge is `supported`. A relationship can also be stated by the structure of the source: see the agenda and paragraph rules under Edge cases.
4. **Qualifier test.** Delete the absolute or widening part of the claim: words like 总是, 一定, 所有, 每个, 只, 唯一, 最…, always, every, all, only, the best, the most. **If what remains is supported** → **`overgeneralization`**. This holds even when another page contradicts the absolute version, and even when the source never states a weaker version.
   - "过拟合…总是由训练数据过少导致" → delete 总是 and the dropped cause: "过拟合…由训练数据过少导致" is supported → overgeneralization.
   - "准确率…是评价分类模型最可靠的指标" → delete the superlative clause: "预测正确的样本占全部样本的比例" is supported → overgeneralization.
5. **Does the definition contradict the evidence in meaning** (opposite meaning, wrong number, swapped definitions, a wrong added clause that is not an absolute)? → **`conceptual-error`**.
   - **Contradiction test:** could the tree's statement and the source's statement both be true of the same thing at once? If yes, it is not a contradiction, even if the wording uses opposite-looking words. Example: the source says a Bayesian network represents "条件独立性关系" and the tree says "条件依赖关系". A Bayesian network's graph encodes both dependencies (edges) and conditional independencies (missing edges), so both are true: this is not a conceptual error. If the tree's version is supported elsewhere (e.g. a diagram showing the dependencies), the node is `supported`; otherwise continue with question 6.
   - Contradictions in numbers (7:2:1 vs 8:1:1), in the end point of a range (0<α<1 vs 0 < α ≤ 1), in negation of the same property (产生 vs 一般不产生 稀疏解), or in which concept a definition belongs to (precision given recall's definition) pass the test and are conceptual errors.
   - **A claim the tree attributes to the source** ("资料给出的", "资料将其设为") is a claim about the source. If the source states it differently, it is a conceptual error even when the tree's version may be true in general. Say in `reason` only that the tree differs from the source, not that it is wrong.
6. **Is the definition supported except for one specific added detail** (a mechanism, property or condition that could be checked on its own) that no evidence states and nothing contradicts? → **`unsupported-expansion`** with scope **`detail`**. In `reason`, quote the exact added detail and say which part of the definition is supported. Examples: "有放回" in a bootstrap-sampling definition when the source only says "随机抽取的一部分数据"; "较大间隔" for SVM when the source only says it is a supervised method for classification and regression.
   - **Only the unsupported fragment is the finding.** A word that differs from the source's but does not contradict it (预测误差 where the source says 泛化误差) is not part of the finding. If the source's word is more precise, suggest it in `recommendation` as optional wording.
   - **A different word for a different property is a detail.** Ask whether the two words name the same thing. 预测误差 and 泛化误差 both name the model's error, so the difference is wording. 多路划分 (how many branches one split has) and the source's 多层分裂 (how many levels of splits) name different properties, so the tree's word is an unsupported detail. Contradiction is not needed: if the two cannot both be true, question 5 applies instead.
   - **A class defined from a single instance:** when the source never defines a general class and only explains one member of it, a general definition of the class is a `detail` finding. The generalization from that member is the added detail. Example: 集成学习 "组合多个模型的预测以改善整体表现的方法" when the source only says that random forest, one ensemble method, averages the predictions of many trees. In `reason`, name the instance that supports the core idea.
   - **The label test comes first.** If the class definition only says what the class's name means, it is `supported`, even when the source explains only one member: 线性分类器 "利用特征的线性组合形成决策边界" when the source says the perceptron is "一种线性分类器" and shows its linear combination. The rule above applies when the definition carries over something the name does not say, such as the member's structure, learning method or output coding.
   - **A slide title does not define the class.** A slide titled 神经网络 whose text describes only 多层感知机 explains one member. A definition of 神经网络 built from that text ("层与层之间全连接") is a `detail` finding by the rule above.
7. **Is the term in the source, but nothing in its definition can be checked** after gathering all evidence, because the source only names the term (e.g. in a list, a sidebar or a table header) and never explains it, or because the only relevant evidence has `low` certainty? → **`ambiguous`** (shown in reports as 资料未定义 / 无法核验, "cannot verify").
   - **First apply the label test from Verdicts.** A definition that only spells out the label or explains what the term means adds nothing to check, so it is `supported` even when the source only names the term. Ask whether the definition could be false while the term is true. Example: the source only says 随机搜索 can replace grid search. 随机搜索 "在超参数空间中随机采样若干组超参数进行评估" only spells out the name → `supported`. GELU "基于高斯分布累积分布函数的平滑激活函数" could be false of an activation function named GELU → `ambiguous`.

When a definition is partly right and partly wrong, the wrong part decides the category. Say in `reason` which part is correct.

## Risk

| Default risk | Categories |
|--------------|------------|
| `high` | `conceptual-error`, `incorrect-relationship` |
| `medium` | `unsupported-expansion` (scope `whole`), `overgeneralization`, core omissions |
| `low` | `unsupported-expansion` (scope `detail`), `ambiguous`, supporting-detail omissions |

Use the default unless there is a concrete reason not to, e.g. an omission of the lecture's central concept → `high`, or a wrong number in a minor example, or a wrong end point of a range in an otherwise correct definition → `medium`. Whenever the risk differs from the default, put the reason in `risk_reason`. A changed risk without `risk_reason` is an error.

## Omissions (source → tree)

Go through the evidence index and sort each piece of uncovered content into one tier.

| Tier | What | Report? | Risk |
|------|------|---------|------|
| **Core** | A topic in a slide title or an agenda/overview slide; a defined term; a stated rule ("X is …", "X should …"); a table row; a relationship shown in a diagram; a slide's main point that the tree only partly covers (e.g. both ends of a trade-off but not the trade-off itself) | always | `medium` |
| **Supporting detail** | When or why to use a method; a notation or symbol legend (e.g. "TP：真正例 …"), or a convention a formula relies on (e.g. "假定偏置量b等于0"); a property or caveat of a concept that is in the tree, including a limitation and its remedies from a 缺点 / limitations section (e.g. "贪心算法…只能达到局部最优", or what to do about the 异或 problem); background: history, applications, other names, and comparisons with other methods from a study or survey | always | `low` |
| **Not knowledge** | Examples in parentheses when the concept they illustrate is in the tree; homework, reading lists, course logistics; site navigation, menus and banners on a web page | never | — |

**When content fits both tiers,** the concept decides. A stated rule, property or caveat about a concept the tree already has a node for is a supporting detail, unless it is the main point of its slide or section. Core is for content with no node of its own: a method, a defined term or a slide's main point. Example: "为了估计特征的分布参数，我们要先假设训练集数据满足某种分布" is a stated rule, but 参数估计 has a node, so it is supporting. A second method for the same job (离散化 next to the tree's 高斯朴素贝叶斯) is core.

**Background** omissions say so in `reason` (背景 / background), so the reader can tell them from gaps in the method.

Before reporting, check that the content is not already covered by a finding on an existing node or edge. For example, do not report "test set may only be used once" when the test-set node already has a finding that cites it, or "Supervised includes Regression" when the wrong edge for Regression already has a finding that recommends it.

**A finding covers only the content it is about.** Cite in a finding only the evidence for that item's own claim. Content that is a separate point stays an omission, even if it is related. Example: a summary slide says "支持向量机在高维、小样本的数据上通常表现良好" and "没有一种算法在所有问题上都是最优的". The first is the evidence for an SVM overgeneralization finding. The second is a general lesson, not a claim about SVM, so it is checked as an omission whether or not the SVM finding mentions it.

**A topic whose members are all in the tree is covered,** even without a node for the topic itself. Example: an agenda lists 评估指标, and the tree has MSE, 精确率 and 召回率. Do not report the missing grouping node.

**One entry per node or topic,** not per sentence, so that two runs give the same count. Cite every evidence item the entry rests on.
- Content with no node of its own: one entry per missing concept, with its details.
- Details missing from a node the tree has (properties, caveats, limitations, a symbol legend or convention for its formula): one entry for that node, even when they come from different sentences. The entry is core if any part of it is.
- Background: one entry per kind in each section. A history section is one entry however long; the other names given in a section are one entry, even for several concepts.

**A missing claim appears in only one entry:** when a statement fits two omissions (e.g. "只需要少量的训练数据" under both training efficiency and the independence assumption), put it in the one it is most directly about and leave it out of the other.

**A node with a compatible definition already covers the source's definition.** When the tree defines a concept in its own words and the definition is supported, the source's differently worded definition of it is not an omission. Report only the parts the tree really lacks, such as a symbol legend (what pᵢ stands for) or a "not to be confused with" note. Do not recommend adding a source explanation that the source itself leaves incomplete.

Read limitations sections (缺点, limitations, caveats, 讨论) sentence by sentence. Their statements are easy to read as already covered by a node that names the problem, when the node leaves out the limitation itself. A supported node does not settle this: N026 "即使独立性假设不完全成立……分类结果仍然可以正确" is `supported`, and the source's "实际上独立假设常常是不准确的" is still an omission, because the node never says the assumption usually fails.

## Edge cases

- **True but incomplete edge:** an edge whose relationship holds but tells only part of the story (e.g. linking a concept to one paradigm when the source applies it to all three) is `supported`. Mention the incompleteness in the related node's finding, if there is one; otherwise it is an omission under the tiers above.
- **Content needing two pages:** combine them. Cite both evidence IDs. This applies to verdicts as well as to findings: a paraphrase supported only by combining pages is `supported` (e.g. "估计目标变量与输入变量之间的关系" is supported when one page describes inputs and targets and another describes estimating their relationship).
- **Agenda or overview slides:** a lecture title followed by a list of topics supports `includes` from the lecture's subject to each listed topic, and to a node that is that topic's main concept (e.g. 交叉验证 on the agenda supports 模型评估 includes k 折交叉验证). It says nothing about how the listed topics relate to each other.
- **A method introduced in a paragraph about a field:** a paragraph whose subject is X, and which presents a method as serving X's purpose, supports `X uses method`. Example: a paragraph says 计算学习理论 analyses algorithms and their performance, then says 偏差-方差分解 is a method for quantifying generalization error. That supports 计算学习理论 uses 偏差与方差分解. All three conditions are needed:
  1. the same paragraph;
  2. X is the paragraph's subject;
  3. the method's stated purpose is part of what X does.

  Two terms that only appear in the same section or paragraph support no relationship.
- **Slide order:** the position of a slide supports no relationship. A slide that comes right after a method's slides, but never names the method, does not link its terms to that method. Example: a 核方法 slide follows the SVM slide, but neither slide mentions the other's term, so 支持向量机 uses 核函数 is `unsupported-expansion`. Only the agenda rule above lets structure state a relationship. In `recommendation`, say the link is probably intended and that the source never states it.
  - Heading levels on a web page are the same: two sections side by side, or one inside the other, neither state nor rule out a relationship. Judge the edge by what the text says. Example: 参数估计 includes 概率平滑修正 is `supported` because the 样本修正 section corrects "基于频率的估计", although it is a sibling section, not a subsection.
- **`contrasts-with` from two versions of one thing:** when the source gives two formulas or conventions for the same thing (an output coded 0/1 in one section and ±1 in another), the difference is in the evidence. The edge is `supported`, citing both, even if the source never compares them; it claims only that they differ, not why. If the source never says which version applies where, that is a problem in the source (see below).
- **`=` or 展开为 where the source prints `∝`:** the tree claims an equality, the source a proportionality. It is `supported` when the source's own words present the step as a rewriting of the same expression ("可将该式写成…"); otherwise the equality is a `detail`.
- **`is-a` from a method to a task:** read 线性回归 is-a 回归 as "线性回归 is a method for 回归". It is `supported` when the source says so (e.g. "最基本的回归方法").
- **Evidence only in a diagram or table:** equally valid as text. Cite the `graphic` or `table` item.
- **Navigation boxes and site menus** on a web page (e.g. a sidebar listing "监督学习（分类 · 回归）") are the site's general categories, not the article's statements. They can be cited together with the article's own text, but never support a node or edge on their own, and never create an omission.
- **Problems in the source itself:** the source may contradict itself or contain an evident slip (S and ¬S called "相互独立" next to "要么是垃圾邮件，要么就不是"; "都用到离散化方法" right after a section on the Gaussian method; "估计各个变量的方法" where 方差 is meant). Then:
  - Quote the evidence verbatim, and never correct it, in the index or in a finding.
  - Judge the tree item against the more specific evidence: an explanation, a formula or a worked example outweighs a single word or a sweeping summary sentence. N033 "互斥且穷尽" is `supported` by "要么…要么就不是" and p(S|D)+p(¬S|D)=1.
  - When the problem bears on an item's verdict or recommendation, say in that item's `reason` which statements conflict and which one you used. This applies to `supported` items too: their `reason` is optional, holds only such a note, and is shown next to the item in the report's confirmed list. Keep it to one or two sentences, and do not add notes to supported items for anything else.
  - A problem in the source is not a finding about the tree. List the problems you noticed in your final message to the user.
- **Check a source claim against the source before you rely on it.** Some problems show only after a short derivation. Before a recommendation quotes a general claim of the source (a property such as 正数, 反对称, 恒为; a condition under which a result holds), test it against the source's own formulas and definitions: try the boundary cases (0, equality, the end point of a range) and the other conventions the source uses (0/1 vs ±1 labels). Example: "E(w)是一组正数的和" fails, because f(0)=+1 lets a misclassified term with wᵀpᵢ=0 and tᵢ=−1 be 0; recommend "各项非负；全部正确时为零" instead. A claim that fails is a problem in the source, handled as above: no new category, a note in the item's `reason`, and a line in the final message. Use only the source's own content for this check.
- **A slip that only outside knowledge reveals** is not evident. "R为输入向量的最大平均值" may be wrong, but nothing in the source shows it. Judge the tree against the printed text, and in `recommendation` do not put the doubtful wording back unmarked: give the source's wording and mark the tree's version as an outside explanation to check (资料外释义，待核实). Mention the possible slip in the final message.
- **Findings that hinge on an exact word or number** (通常 vs 总是, 7:2:1 vs 8:1:1, 不产生 vs 产生): look at the image again before reporting, and quote the exact text in `reason`.
- **Structure warnings** from `validate_input.py` (disconnected parts, isolated nodes, duplicate edges) are not findings. `build_report.py` adds them to the report's Structure section; do not repeat them in `items` or `omissions`.
