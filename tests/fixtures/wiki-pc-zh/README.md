# wiki-pc-zh test set

The fourth real-content test set: 6 screenshots of the Chinese Wikipedia article 感知器 (perceptron, revision 88067151). Licensed under CC BY-SA 4.0, unlike the rest of the repository. See [LICENSE.md](LICENSE.md) and [ATTRIBUTION.md](ATTRIBUTION.md).

It checks the fifth rule revision and the report notes on supported items (commits `80616a0` and `1dbd02b`) on an article that played no part in any rule. It is used the same way as [wiki-nb-zh](../wiki-nb-zh/):

1. **Knowledge tree:** generated from `images/` by OpenAI Codex (GPT-6.1 Sol) in a new conversation, with [PROMPT.md](PROMPT.md). The output is saved here as `knowledge-tree.json`, unedited, so its mistakes are real and not planted. See [TREE-SOURCE.md](TREE-SOURCE.md).
2. **Audit:** two fresh Claude agents ran SourceTrace on `images/` and `knowledge-tree.json`: [audit-run-1](audit-run-1/) and [audit-run-2](audit-run-2/).
3. **Answer key:** [REVIEW.md](REVIEW.md), a review by Codex in a separate session, accepted by the project owner. Results: [RESULTS.md](RESULTS.md).

## What this set adds

- **Figures as evidence:** a neuron diagram captioned 神经细胞结构示意图 on page 1, and a diagram of the perceptron's structure (inputs a1…an, weights w1…wn, bias b, SUM, f, output t) on page 4, which the text refers to as "如右图示".
- **Formulas:** the output function, the structure t = f(Σ wᵢxᵢ + b), the sign function, the criterion function E(w) and the weight update rule.
- **A history section** with dates and people (1943, 1949, 1957, 1958, 1960, 1962, 1969, 1987, 1998) and a limitation (XOR, linear inseparability).
- **Possible inconsistencies in the source:** the definition section outputs 0 or 1, while the structure section uses a sign function with +1 and −1. A tree may follow either one.
- **Non-knowledge on the page:** a site banner, a revision notice, a disambiguation note and a machine-learning navigation sidebar on pages 1–3.
