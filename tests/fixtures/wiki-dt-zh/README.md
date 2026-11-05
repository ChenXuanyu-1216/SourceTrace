# wiki-dt-zh test set

The second real-content test set: 6 screenshots of the Chinese Wikipedia article 决策树学习 (revision 93550494). Licensed under CC BY-SA 4.0, unlike the rest of the repository. See [LICENSE.md](LICENSE.md) and [ATTRIBUTION.md](ATTRIBUTION.md).

It checks whether the rules revised on [wiki-ml-zh](../wiki-ml-zh/) were tuned only to that one article. It is used the same way:

1. **Knowledge tree:** generated from `images/` by an AI tool other than Claude, with [PROMPT.md](PROMPT.md). The output is saved here as `knowledge-tree.json`, unedited, so its mistakes are real and not planted.
2. **Audit:** SourceTrace runs on `images/` and `knowledge-tree.json`, with rules that this article played no part in.
3. **Answer key:** the project owner reviews the resulting `report.md`.

## Runs

- **[audit-run-1/](audit-run-1/)** (2026-11-05): skill at commit `1956d56`, run by a fresh Claude agent with no web access. The tree is from OpenAI Codex ([TREE-SOURCE.md](TREE-SOURCE.md)).
  - Result: 98 evidence items, 77 supported, 4 findings (all low-risk source notes), 7 omissions.
  - All three scripts passed on the first try.
  - Cost: about 139k tokens and 9 minutes.
  - Review by the project owner: [audit-run-1/REVIEW.md](audit-run-1/REVIEW.md) (pending).

## What this set adds

Compared with `wiki-ml-zh`, this one has:
- formulas (基尼不纯度, 信息熵, 信息增益) and a worked calculation with exact numbers (0.8112781, 0.940286, 0.0481271), so wrong numbers in the tree can be caught;
- a decision-tree figure with its own caption;
- lists of algorithms (ID3, C4.5, CHAID, MARS) and of pros and cons;
- some awkwardly worded source sentences (e.g. "决策树创建的过度复杂会导致无法很好的预测训练集之外的数据"), where a tree's clearer paraphrase has to be judged against unclear wording.
