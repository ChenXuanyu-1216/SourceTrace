# Source of knowledge-tree.json

- **Tool:** ChatGPT
- **Model version:** GPT-6
- **Date:** 2026-11-06
- **Prompt:** [PROMPT.md](../PROMPT.md), with the 10 images in `../images/`
- **Edits:** none. The JSON is saved exactly as the project owner pasted it from ChatGPT.
- **Status:** not used for the wiki-nb-zh audit, which uses a second, Chinese tree from ChatGPT (see ../TREE-SOURCE.md). Kept for a later cross-language test (English tree, Chinese source).

## Differences from the prompt

- **Language:** the prompt is in Chinese and asks for the title "朴素贝叶斯分类器". The reply is in English: title, labels and definitions.
- **Relation values:** four edges (E020, E030, E037, E038) use `include`, which is not an allowed value; the prompt lists `includes`. `validate_input.py` rejects the tree for this.
