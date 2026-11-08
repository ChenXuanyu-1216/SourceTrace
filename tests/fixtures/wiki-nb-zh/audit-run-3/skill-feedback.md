# Skill feedback (SourceTrace, run nb5-1)

## 1. Script runs

| Script | Runs | Failed runs |
|--------|------|-------------|
| `validate_input.py` | 1 | 0 (valid, no warnings) |
| `validate_evidence.py` | 1 | 0 (valid; one expected `LOW_CERTAINTY` warning for EV-101, the cut-off end of the evidence formula on page 7) |
| `build_report.py` | 2 | 0 |

The second `build_report.py` run was not caused by an error. After reading the first report I reworded one omission's recommendation (F-014): it had joined "compute the actual probability from the log ratio" and "convert to an S-curve" into one claim, which the source states as two separate sentences. That would have added a claim of my own, so I split it and rebuilt.

My own helper scripts (`work/make_index.py`, `work/make_audit.py`) generate the two JSON files; they ran without errors.

## 2. Unclear or underspecified instructions

- **Overlapping screenshots vs. "first complete".** evidence-extraction.md says: "Extract each statement once, on the page where it is first complete" and "A sentence split across two images is one item on the page where it starts; say `continues on page N`". These two rules point in different directions when a sentence starts at the very bottom of one image and is fully repeated at the top of the next. Example: the note "注意，这里的值大于1也是允许的…" starts with one character ("注") at the bottom of page 7 and appears in full on page 8. I followed the "page where it starts" rule for sentences that were truly split (EV-011, EV-105) and the "first complete" rule for formulas whose introducing sentence was visible but whose formula was cut (EV-037, EV-120, EV-128). A sentence that is fully repeated on the next image, but only begins on the earlier one, could use a tie-break rule.
- **Formulas with `∝` where the math is `=`.** evidence-extraction.md says "`=` and `∝` are different claims". The source writes the chain-rule expansion with `∝` on every line, while its text says "可将该式写成条件概率的形式". The tree (N012) says "展开为 p(C) × ∏…" without an explicit `=` sign. The rules do not say whether a tree's equality claim is supported by a source `∝` when the source's wording says "写成". I judged N012 `supported` from the wording ("写成"), and did not count `∝` as a source slip, since an equality is also a proportionality.
- **Supported items cannot carry a note.** audit-rules.md says that when a source problem "bears on an item's verdict … say in that item's `reason` which statements conflict and which one you used". For N033 (S and ¬S called "相互独立" next to "要么…要么就不是") the verdict is `supported`, and SKILL.md's examples give supported items no `reason`. I left out `reason` on supported items, mentioned the conflict in the final message, and noted the discretization slip in the `reason` of the omission it bears on (F-002).
- **Grouping supporting omissions.** "One omission per missing concept" is clear for a missing method, but less clear for several missing properties of one existing node (N025 lacks training time, the curse-of-dimensionality point, and the parameter-count formula). I made one entry per property (F-004, F-010, F-011), since each could be added independently. Another run could reasonably merge them, which would change the counts.
- **Section structure on a web page.** The "A method introduced in a paragraph about a field" rule and the slide-order rule cover paragraphs and slides, but not wiki section nesting. For E030 (参数估计 includes 概率平滑修正) the 样本修正 section is a sibling of 参数估计, not a subsection. I judged the edge `supported` from the content (the section is about correcting "基于频率的估计" / "概率估计"), not from its position.

Everything else was clear enough to apply without guessing.

## 3. Image difficulties

- **Low resolution (800×600)** with small text and formula subscripts. I made 2× enlarged crops of the dense paragraphs and formulas (pages 1, 2, 4, 5, 7, 8, 10) in `work/` and read the exponents and subscripts from those, e.g. `e^(−(v−μ_c)^2/(2σ_c^2))` and `3.5033e^−02`.
- **Overlapping screenshots:** each page repeats a few lines of the one before. I extracted each statement once, using the rules above, and noted in `location` where text is repeated.
- **Cut-off formula:** the `evidence = …` formula on page 7 runs past the right edge ("p(weight|f") and is not repeated on page 8. I split it into a readable `high` item (EV-100) and an unreadable `low` item (EV-101, ［无法辨认］). No tree item depends on the hidden part.
- **Split table:** the female row of the mean/variance table is cut off at the bottom of page 6. I extracted it from page 7, where it is complete.
- **Site chrome:** I skipped the Wikipedia header, the Telegram banner and the revision notice. I extracted the "机器学习与数据挖掘" sidebar as one navigation-box item (EV-012) and cited it only together with article text.
