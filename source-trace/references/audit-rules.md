# Audit rules (v0.1)

How to decide verdicts, categories and risk levels in stages 4 and 5. The rules are written so that two careful runs reach the same answer; where a judgment call remains, the rule says which way to lean.

## Verdicts

Every node and every edge gets exactly one verdict:

| Verdict | When |
|---------|------|
| `supported` | The evidence says the same thing. Paraphrase is fine if the meaning, numbers and qualifiers are unchanged. |
| `finding` | Anything else. The finding gets one category from the decision order below. |

A `supported` verdict also cites its evidence IDs. "Looks fine" without evidence is not a verdict.

A definition that only restates or spells out its own label adds no claim to check (e.g. 分类评价指标: "用于评价分类模型性能的指标"). If the label's term is in the source, the node is `supported`; cite where the term appears. Use questions 6 and 7 below only when the definition says something more than the label.

The same holds for a plain-words explanation of what the term itself means, once the source supports the term and its main point. Example: 过拟合 "模型过度适应训练数据的细节而使未见数据上的表现下降" when the source says overfitting lowers generalization. "过度适应训练数据" is what the word overfitting means, not an added mechanism, so the node is `supported`. To tell the two apart, ask: **could this part be false while the rest of the definition is true?** If not, it is an explanation of the term. If it could, it is a separate claim, and question 6 applies (e.g. "有放回" could be false of a sampling method that is otherwise as described).

Only the label, the definition and the relationship are audited. Node `kind` is a label from the tool that generated the tree, not a knowledge claim: do not report a `kind` that differs from what the slides call the concept.

## Categories: decision order

**First, gather all the evidence for the item:** text, table rows and figures (`graphic` items) on every page, not just the page where the term first appears. Figures count as much as text: a diagram that groups similar points into circles is evidence for what clustering means. Paraphrase is fine: a definition is supported if the evidence, combined across pages, says the same thing in other words. Answer the questions below only after this step. Most false "cannot be checked" findings come from skipping it.

Then go through these questions in order and stop at the first "yes". Questions 2–3 apply only to edges and 4–7 only to nodes.

1. **Is the node's term (or, for an edge, either end node's term) absent from the source?** → **`unsupported-expansion`** (scope `whole`). Cite the evidence that shows what the source says instead, if any (e.g. the slide that lists the actual members of a group).
2. **Edges: does the evidence contradict the relationship** (wrong target, reversed, swapped, or a link the source rules out)? → **`incorrect-relationship`**. Judge the edge on its own, even if one of its nodes also has a finding.
3. **Edges: is the relationship stated nowhere,** not even by combining pages, while nothing contradicts it either? → **`unsupported-expansion`** (scope `whole`). Every other edge is `supported`. A relationship can also be stated by the structure of the source: see the agenda and paragraph rules under Edge cases.
4. **Qualifier test.** Delete the absolute or widening part of the claim: words like 总是, 一定, 所有, 每个, 只, 唯一, 最…, always, every, all, only, the best, the most. **If what remains is supported** → **`overgeneralization`**. This holds even when another page contradicts the absolute version, and even when the source never states a weaker version.
   - "过拟合…总是由训练数据过少导致" → delete 总是 and the dropped cause: "过拟合…由训练数据过少导致" is supported → overgeneralization.
   - "准确率…是评价分类模型最可靠的指标" → delete the superlative clause: "预测正确的样本占全部样本的比例" is supported → overgeneralization.
5. **Does the definition contradict the evidence in meaning** (opposite meaning, wrong number, swapped definitions, a wrong added clause that is not an absolute)? → **`conceptual-error`**.
   - **Contradiction test:** could the tree's statement and the source's statement both be true of the same thing at once? If yes, it is not a contradiction, even if the wording uses opposite-looking words. Example: the source says a Bayesian network represents "条件独立性关系" and the tree says "条件依赖关系". A Bayesian network's graph encodes both dependencies (edges) and conditional independencies (missing edges), so both are true: this is not a conceptual error. If the tree's version is supported elsewhere (e.g. a diagram showing the dependencies), the node is `supported`; otherwise continue with question 6.
   - Contradictions in numbers (7:2:1 vs 8:1:1), in negation of the same property (产生 vs 一般不产生 稀疏解), or in which concept a definition belongs to (precision given recall's definition) pass the test and are conceptual errors.
6. **Is the definition supported except for one specific added detail** (a mechanism, property or condition that could be checked on its own) that no evidence states and nothing contradicts? → **`unsupported-expansion`** with scope **`detail`**. In `reason`, quote the exact added detail and say which part of the definition is supported. Examples: "有放回" in a bootstrap-sampling definition when the source only says "随机抽取的一部分数据"; "较大间隔" for SVM when the source only says it is a supervised method for classification and regression.
   - **Only the unsupported fragment is the finding.** A word that differs from the source's but does not contradict it (预测误差 where the source says 泛化误差) is not part of the finding. If the source's word is more precise, suggest it in `recommendation` as optional wording.
   - **A class defined from a single instance:** when the source never defines a general class and only explains one member of it, a general definition of the class is a `detail` finding. The generalization from that member is the added detail. Example: 集成学习 "组合多个模型的预测以改善整体表现的方法" when the source only says that random forest, one ensemble method, averages the predictions of many trees. In `reason`, name the instance that supports the core idea.
7. **Is the term in the source, but nothing in its definition can be checked** after gathering all evidence, because the source only names the term (e.g. in a list, a sidebar or a table header) and never explains it, or because the only relevant evidence has `low` certainty? → **`ambiguous`** (shown in reports as 资料未定义 / 无法核验, "cannot verify").

When a definition is partly right and partly wrong, the wrong part decides the category. Say in `reason` which part is correct.

## Risk

| Default risk | Categories |
|--------------|------------|
| `high` | `conceptual-error`, `incorrect-relationship` |
| `medium` | `unsupported-expansion` (scope `whole`), `overgeneralization`, core omissions |
| `low` | `unsupported-expansion` (scope `detail`), `ambiguous`, supporting-detail omissions |

Use the default unless there is a concrete reason not to, e.g. an omission of the lecture's central concept → `high`, or a wrong number in a minor example → `medium`. Whenever the risk differs from the default, put the reason in `risk_reason`. A changed risk without `risk_reason` is an error.

## Omissions (source → tree)

Go through the evidence index and sort each piece of uncovered content into one tier.

| Tier | What | Report? | Risk |
|------|------|---------|------|
| **Core** | A topic in a slide title or an agenda/overview slide; a defined term; a stated rule ("X is …", "X should …"); a table row; a relationship shown in a diagram; a slide's main point that the tree only partly covers (e.g. both ends of a trade-off but not the trade-off itself) | always | `medium` |
| **Supporting detail** | When or why to use a method; a notation or symbol legend (e.g. "TP：真正例 …"); a property or caveat of a concept that is in the tree | always | `low` |
| **Not knowledge** | Examples in parentheses when the concept they illustrate is in the tree; homework, reading lists, course logistics | never | — |

Before reporting, check that the content is not already covered by a finding on an existing node or edge. For example, do not report "test set may only be used once" when the test-set node already has a finding that cites it, or "Supervised includes Regression" when the wrong edge for Regression already has a finding that recommends it.

One omission per missing concept. Group its details into that one entry, and cite every evidence item it rests on.

## Edge cases

- **True but incomplete edge:** an edge whose relationship holds but tells only part of the story (e.g. linking a concept to one paradigm when the source applies it to all three) is `supported`. Mention the incompleteness in the related node's finding, if there is one; otherwise it is an omission under the tiers above.
- **Content needing two pages:** combine them. Cite both evidence IDs. This applies to verdicts as well as to findings: a paraphrase supported only by combining pages is `supported` (e.g. "估计目标变量与输入变量之间的关系" is supported when one page describes inputs and targets and another describes estimating their relationship).
- **Agenda or overview slides:** a lecture title followed by a list of topics supports `includes` from the lecture's subject to each listed topic, and to a node that is that topic's main concept (e.g. 交叉验证 on the agenda supports 模型评估 includes k 折交叉验证). It says nothing about how the listed topics relate to each other.
- **A method introduced in a paragraph about a field:** a paragraph whose subject is X, and which presents a method as serving X's purpose, supports `X uses method`. Example: a paragraph says 计算学习理论 analyses algorithms and their performance, then says 偏差-方差分解 is a method for quantifying generalization error. That supports 计算学习理论 uses 偏差与方差分解. All three conditions are needed:
  1. the same paragraph;
  2. X is the paragraph's subject;
  3. the method's stated purpose is part of what X does.

  Two terms that only appear in the same section or paragraph support no relationship.
- **Evidence only in a diagram or table:** equally valid as text. Cite the `graphic` or `table` item.
- **Findings that hinge on an exact word or number** (通常 vs 总是, 7:2:1 vs 8:1:1, 不产生 vs 产生): look at the image again before reporting, and quote the exact text in `reason`.
- **Structure warnings** from `validate_input.py` (disconnected parts, isolated nodes, duplicate edges) are not findings. `build_report.py` adds them to the report's Structure section; do not repeat them in `items` or `omissions`.
