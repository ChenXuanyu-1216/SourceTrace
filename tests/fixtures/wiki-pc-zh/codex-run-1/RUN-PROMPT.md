# Prompt for codex-run-1

Codex was started in `D:/sourcetrace-codex-pc-1`, which held only `source-trace/` (the skill at commit `7a41a51`, with the sixth rule revision from `ae1084e`) and `input/` (`images/` and `knowledge-tree.json` of this test set). It was given this prompt:

```text
Use the SourceTrace skill in source-trace/ (read source-trace/SKILL.md first). Audit the knowledge tree input/knowledge-tree.json against the 6 page images in input/images/ (screenshots of a Chinese Wikipedia article). Write the outputs to the default output folder, input/sourcetrace-output/. Do not use the web, and do not read any files outside this folder. Work page by page and node by node, writing results to the files as you go.

When you are done, also write two files in the output folder:

skill-feedback.md:
1. How many times you ran each script, and for any failed run, which errors it reported and what you changed.
2. Any place where SKILL.md or its reference files were unclear, contradictory, missing something you needed, or made you guess. Quote the instruction and say what you did. If everything was clear, say so.
3. How you read the images: which tool you used, what was hard to read (small text, formulas, overlapping screenshots), and what you did about it.

final-message.md: the final message to the user that SKILL.md asks for, exactly as you send it.

Then send me that final message.
```

The earlier Claude runs' prompt was not saved in the repository. Items 1 and 2 above repeat its wording; the opening, item 3 and `final-message.md` are new. The final message is saved because it is where SKILL.md asks for problems in the source itself, which this run is meant to check.
