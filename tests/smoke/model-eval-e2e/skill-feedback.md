# Skill feedback (source-trace, this run)

## 1. build_report.py runs

I ran `scripts/build_report.py` **once**, and it succeeded on the first try (exit 0, `report.md` in Chinese, "Supported: 26, findings: 11, omissions: 4"). No run failed, so there were no errors to fix.

The other scripts: `validate_input.py` ran once (valid, one `DISCONNECTED_TREE` warning) and `validate_evidence.py` ran once (valid, 39 items).

## 2. Unclear or underspecified places

Most of the skill was clear. The decision order in `audit-rules.md` and its worked examples (总是 and 最可靠) matched two of the findings exactly, and the rule "check that the content is not already covered by a finding" settled three possible omissions without any guessing (EV-017, EV-037, EV-038). I had to make a judgment call in these places:

1. **Definitions that only restate the term (N018 分类评价指标).** Rule 6 in audit-rules.md says: "Is the term in the source but its definition cannot be checked, because the source never defines it (e.g. it appears only as a table header) … → `ambiguous`." The slides never define 分类评价指标. It is only a slide title, with a table of metrics below it. The tree's definition, "用于评价分类模型性能的指标", just expands the term. A literal reading of rule 6 makes this `ambiguous`. The verdict table, which says "Paraphrase is fine", reads as `supported`. I chose **supported** and cited the title and the four table rows. I judged that reporting a tautology would be noise. A sentence covering definitions that only restate the term would help two runs agree here.

2. **Agenda slide as evidence for "X includes Y" edges (E001, E006, E018).** The edges say "模型评估 includes 数据集划分 / 分类评价指标 / k 折交叉验证". The only support is that the lecture "模型评估与泛化" lists these topics under "本讲内容". The rules don't say whether an agenda listing counts as stating an "includes" relationship, or whether the edge is `unsupported-expansion` under question 3. I treated it as **supported** by combining the title and the agenda item. A rule on agenda slides would help.

3. **Paths in `sources`.** evidence-extraction.md says to copy each `path` "exactly as reported (relative to where the script ran, with the platform's separators)". Because the scripts run from the skill folder, the paths came out as `..\\input\\images\\slide-01.png`. That is a Windows-only path that is relative to the skill folder, not to the output folder, so the index is not portable. I followed the instruction literally.

4. **Granularity of the agenda header and the legend line.** The extraction table says "one item per … bullet". The header bullet "本讲内容：" carries no knowledge of its own. I extracted it as its own item (EV-003) and gave each agenda topic its own sub-bullet item. For the symbol legend on slide 7, "TP：真正例 FP：假正例 FN：假反例 TN：真反例", the table has no row for a legend line. I extracted it as one `text` item rather than four, following "split a bullet only if it states two unrelated facts".

5. **Risk for a wrong number (N005, 8:1:1 vs 7:2:1).** audit-rules.md gives "a wrong number in a minor example → `medium`" as an example of lowering the risk. It doesn't say whether a course-recommended split ratio counts as a "minor example". I judged that it does not and kept the default **high**.

6. **Recommendation for an edge that should simply not exist (E016).** The skill says recommendations must stay "within the tree schema", but it doesn't say whether "delete the edge" is the expected recommendation or whether a replacement edge is preferred. I recommended deleting the edge and offered "N014 related-to N003" as an optional replacement.

7. **"Missing pages may be the cause" for unsupported expansions.** SKILL.md says that when the tree covers material not in the images, I should "tell the user that missing pages may be the cause". Here the agenda slide lists all five topics and all eight slides are present, so missing pages are unlikely for Dropout. I mention it only briefly in the final message. The instruction could say this applies only when there is reason to think pages are missing.
