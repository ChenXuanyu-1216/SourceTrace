# wiki-nb-zh test set

The third real-content test set: 10 screenshots of the Chinese Wikipedia article 朴素贝叶斯分类器 (revision 94718898). Licensed under CC BY-SA 4.0, unlike the rest of the repository. See [LICENSE.md](LICENSE.md) and [ATTRIBUTION.md](ATTRIBUTION.md).

It checks the fourth rule revision and the fixes after it (commits `fb2bbc2` and `9b74d78`) on an article that played no part in any rule. It is used the same way as [wiki-dt-zh](../wiki-dt-zh/):

1. **Knowledge tree:** generated from `images/` by ChatGPT (GPT-6.1 Sol), with [PROMPT.md](PROMPT.md). The output is saved here as `knowledge-tree.json`, unedited, so its mistakes are real and not planted. See [TREE-SOURCE.md](TREE-SOURCE.md). A first, English tree that failed validation is kept in [chatgpt-tree/](chatgpt-tree/) for a later cross-language test.
2. **Audit:** two fresh Claude agents ran SourceTrace on `images/` and `knowledge-tree.json`: [audit-run-1](audit-run-1/) and [audit-run-2](audit-run-2/).
3. **Answer key:** [REVIEW.md](REVIEW.md), an AI-assisted review accepted by the project owner. Results: [RESULTS.md](RESULTS.md).

## What this set adds

- **Long derivations:** the probability model is built up step by step from Bayes' theorem, the chain rule and the independence assumption, so a tree can state a step that the formulas do not support.
- **A worked example with exact numbers:** a gender-classification example with training tables, means, variances and posterior numerators (e.g. 6.1984e−09 and 5.3778e−04), so wrong numbers can be caught.
- **A second worked example** (spam filtering) that repeats the derivation with different symbols.
- **Claims with dates and comparisons:** 1950s research, a 2004 analysis and a 2006 comparison with boosted trees and random forests.
- **Non-knowledge on the page:** a machine-learning navigation sidebar, a revision notice and a site banner on page 1.
