# wiki-ml-zh test set

Real content that the developer did not write: 12 screenshots of the Chinese Wikipedia article 机器学习 (revision 94516905). Licensed under CC BY-SA 4.0, unlike the rest of the repository. See [LICENSE.md](LICENSE.md) and [ATTRIBUTION.md](ATTRIBUTION.md).

How this test set is meant to be used:

1. **Knowledge tree:** generated from `images/` by an AI tool other than Claude, with [PROMPT.md](PROMPT.md). The output is saved here as `knowledge-tree.json`, unedited, so its mistakes are real and not planted.
2. **Audit:** SourceTrace runs on `images/` and `knowledge-tree.json`.
3. **Answer key:** the project owner reviews the resulting `report.md` and records which findings are right or wrong and what was missed. This makes the answer key independent of the developer who wrote the rules.

Compared with the synthetic test sets, this one adds:
- web-page screenshots instead of slides;
- text cut across page boundaries;
- figures with captions in a sidebar;
- Wikipedia maintenance boxes and navigation, which are not knowledge;
- English terms in parentheses inside Chinese text.
