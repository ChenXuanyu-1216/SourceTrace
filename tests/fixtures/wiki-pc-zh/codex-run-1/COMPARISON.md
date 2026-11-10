# codex-run-1: the sixth rule revision, run by OpenAI Codex

The first run of the sixth rule revision (commit `ae1084e`), on the same inputs as the two Claude runs of the fifth revision.

| | |
|---|---|
| Agent | OpenAI Codex (GPT-6.1 Sol, reasoning effort high), run by the project owner on 2026-11-10 |
| Skill | commit `7a41a51`: the sixth rule revision, which no run had used before |
| Inputs | `images/` and `knowledge-tree.json` of this test set, in a clean folder outside the repository (`D:/sourcetrace-codex-pc-1`), so earlier runs, reviews and the answer key were not visible |
| Prompt | [RUN-PROMPT.md](RUN-PROMPT.md); the final message is saved as [final-message.md](final-message.md) |
| Cost | 16 minutes 35 seconds (token count not recorded); the Claude runs took 9 minutes each |

**Read this with two caveats.**
- **Rules and agent changed together.** Several examples in the sixth revision come from this article ("E(w)是一组正数的和", "最大平均值", 0<α<1, b = 0, N003, E017). The run shows that the new rules are followed, not that they generalize. And the agent changed from Claude to Codex along with the rules, so the two effects can't be separated.
- **Same model as the key.** The answer key (REVIEW.md) was written by the same model at the same effort (GPT-6.1 Sol, high), in a separate session, and it is also the model that made the tree. Agreement with the key is therefore not independent of the model.

## Did Codex follow the skill?

Yes, without help.

- **Scripts:** each of the three ran once and passed. `validate_evidence.py` warned about one `low` item (EV-013, the unreadable labels in the neuron figure), as expected.
- **Images:** it read the six images with its own image tool, made 2× copies of every page, and re-read the α interval and the R sentence from separate crops before reporting on them.
- **Working files** are in `work/` (not copied here): page and item batches, a coverage check and the crops.
- **Evidence:** 83 items (75 text, 8 graphic), each statement placed on the first page that shows all of it. It moved two items from page 5 to page 4 to follow that rule.

## Items: the same as both Claude runs

Codex gave the same verdict, category and risk as both Claude runs on all 83 items. The review upheld those on every item, so this is 83/83 against the key.

- **N023** (0<α<1 vs "0 < α ≤ 1"): `conceptual-error`, medium, as before.
- **N029** (R as "最大范数" vs "最大平均值"): same category and risk, but the part the review marked as "partly correct" is fixed. The `reason` says only that the tree differs from the source, and the recommendation no longer puts the doubtful source word back: "原文作'输入向量的最大平均值'（疑似笔误）；'最大范数'为资料外释义，待核实".
- **Notes on supported items:** N014 (反对称 fails at 0, since f(0)=+1) and N020 (the "正数之和" sentence fails at the boundary). Both follow the review. E017 has no note.

## Problems in the source: 2 of 4

| Problem in the review (section 四) | Claude runs | Codex |
|---|---|---|
| "E(w)是一组正数的和" fails at the boundary (f(0)=+1) | missed, and copied into a recommendation | **found:** N020 note, F-013 and the final message; F-013 recommends "各误分类项非负，所有输入都正确分类时E(w)=0" |
| "反对称的符号函数" is not antisymmetric at 0 | missed | **found:** N014 note and the final message |
| 0/1 labels make the margin condition yᵢ(w·xᵢ+b) > γ impossible | missed | missed |
| The bound (2R/γ)² has no scale constraint | missed | missed |
| "最大平均值" as a possible slip (not provable from the source) | in the final message | in the final message, as a possible slip |

Both problems it found are zero-boundary checks of the kind the new rule spells out. The two it missed need combining sections (the labels) or a scaling argument (the bound), which the rule mentions only as "other conventions".

## Omissions: 14 (4 core, 10 supporting)

Compared with the review's 10 groups and the one omission both Claude runs missed:

| Review group | Codex | Comment |
|---|---|---|
| Least squares and gradient descent (core) | F-003, F-004, core | Found; one entry per method |
| Neuron structure and "两种状态" | F-007 | Structure found; the two states not mentioned |
| Abilities and limitations (supporting) | F-005 **core**, F-010 | Content found; the general limitation is reported as core, while the rules call a limitation of a concept the tree has supporting |
| History, both halves (background) | F-009, plus F-006 **core** | The whole history section is one entry, as the new rule says. The 1998 kernel method is a separate core entry (the review: history, supporting); multilayer perceptrons and backpropagation are not named |
| Other names (background) | F-012 | Both concepts' aliases in one entry, as the new rule says |
| Criterion function properties | F-013 | Found, with the non-negative wording the review asks for (the Claude runs copied "正数") |
| "独立的应用于每个神经元" and the symbol legend | F-014 | Independence found; the legend for x(j), w(j), f(x) is missing |
| Novikoff (1962) | F-016 | Found |
| Other descriptions of the bias | F-011 | "虽然不是定向的" found; the recommendation reads it as "固定权重向量w时不改变其方向", an interpretation the review advised against making binding |
| **b = 0 in the learning section** (both Claude runs missed it) | F-015 | **Found**, with the augmented-weight context the review asks for |
| Not in the review | F-008 | English names (Perceptron, Multilayer Perceptron), a separate background entry because they are in another section; not judged |

**Two tier differences:** F-005 (the general limitation of the single-layer perceptron) and F-006 (the kernel method from the history section) are core here and supporting in the review. Both hinge on rules that point two ways: a limitation of a concept with a node is supporting "unless it is the main point of its section", and a method with no node of its own is core, but history is background.

**The owner's decision (2026-11-10):** both are supporting, as in the review. F-005 is a limitation of a concept the tree has, and F-006's method is named only in the history section. Both count as correct omissions with the wrong tier. After this run, a rule line was added: a method named only in a history passage is background.

## What Codex raised in its feedback

1. Whether to extract an illustration inside a navigation box at all.
2. A node label that repeats a wrong source adjective (N014 "反对称符号函数") while its definition repeats the formula correctly.
3. The significance of the general single-layer limitation (see the tier questions above).

The overlap tie-break, the omission grouping, N029's attribution and the zero-boundary checks were clear to it.
