# wiki-ml-zh test set

Real content that the developer did not write: 12 screenshots of the Chinese Wikipedia article 机器学习 (revision 94516905). Licensed under CC BY-SA 4.0, unlike the rest of the repository. See [LICENSE.md](LICENSE.md) and [ATTRIBUTION.md](ATTRIBUTION.md).

How this test set is meant to be used:

1. **Knowledge tree:** generated from `images/` by an AI tool other than Claude, with [PROMPT.md](PROMPT.md). The output is saved here as `knowledge-tree.json`, unedited, so its mistakes are real and not planted.
2. **Audit:** SourceTrace runs on `images/` and `knowledge-tree.json`.
3. **Answer key:** the project owner reviews the resulting `report.md` and records which findings are right or wrong and what was missed. This makes the answer key independent of the developer who wrote the rules.

## Runs

- **[audit-run-1/](audit-run-1/)** (2026-11-04): skill at commit `e392abc`, run by a fresh Claude agent with no web access.
  - Result: 221 evidence items, 83 supported, 15 findings, 25 omissions.
  - All three scripts passed on the first try.
  - Cost: about 203k tokens and 14 minutes.
  - Review by the project owner: [audit-run-1/REVIEW.md](audit-run-1/REVIEW.md). Of 13 findings judged, 6 were correct, 4 partly correct and 3 wrong. This led to the rule changes in commit `89d1e55`.
- **[audit-run-2/](audit-run-2/)** (2026-11-04): skill at commit `89d1e55`, same setup as run 1.
  - Result: 231 evidence items, 82 supported, 16 findings, 25 omissions.
  - All three scripts passed on the first try.
  - Cost: about 159k tokens and 11 minutes.
  - 10 of the 13 reviewed findings now match the owner's review. Comparison and the owner's review of the 8 changed items (4 correct, 1 partly correct, 3 wrong): [audit-run-2/COMPARISON.md](audit-run-2/COMPARISON.md). This led to the second rule revision.
  - The saved `report.md` is as the skill produced it at `89d1e55`. Later versions of `build_report.py` render the same `audit.json` with the `detail` findings in a separate source-notes section and different finding IDs, so the IDs in the review refer to this saved report.

## What this set adds

Compared with the synthetic test sets, this one adds:
- web-page screenshots instead of slides;
- text cut across page boundaries;
- figures with captions in a sidebar;
- Wikipedia maintenance boxes and navigation, which are not knowledge;
- English terms in parentheses inside Chinese text.
