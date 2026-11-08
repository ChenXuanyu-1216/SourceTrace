# Prompt for generating the knowledge tree

Use an AI tool **other than Claude**, in a **new conversation** that has not seen any other knowledge tree or this project's answer keys. For [wiki-nb-zh](../wiki-nb-zh/TREE-SOURCE.md), the tree used was a translation of an earlier reply in the same conversation, so the two trees were not independent. Upload the 6 images in `images/` in order (`page-01.jpg` to `page-06.jpg`) and send the prompt below. Then:

- Save the reply's JSON **exactly as returned** as `knowledge-tree.json` in this folder. Do not correct mistakes in it: they are what the audit is supposed to find.
- If the reply is not valid JSON (e.g. it has text around the code block), copy only the JSON part and change nothing else.
- If the reply does not follow the prompt (another language, values outside the allowed lists), do not ask the tool to fix it in the same conversation. Record what happened, and start a new conversation if a new tree is needed.
- Record the tool, model version and date in `TREE-SOURCE.md`, e.g. "OpenAI Codex, GPT-x, 2026-11-07".

---

```text
这 6 张图片是一篇关于“感知器”的学习资料截图（按顺序 page-01 到 page-06）。请根据这些资料，为我生成一棵知识树，帮助我复习。

要求：
1. 覆盖资料中的主要知识点和它们之间的关系，大约 20–35 个知识点。
2. 每个知识点写一句简短的定义。
3. 只输出 JSON，不要输出其他文字。格式如下：

{
  "schema_version": "0.1",
  "title": "感知器",
  "nodes": [
    { "id": "N001", "label": "知识点名称", "definition": "一句话定义", "kind": "concept" }
  ],
  "edges": [
    { "id": "E001", "source": "N001", "target": "N002", "relation": "includes" }
  ]
}

规则：
- id：节点用 N001、N002……，边用 E001、E002……，不能重复。
- kind 只能是：concept、method、task、example、fact
- relation 只能是：includes、is-a、part-of、example-of、causes、depends-on、uses、contrasts-with、related-to
- 边的含义是“source relation target”，例如 N001 includes N002 表示“N001 包含 N002”。
- source 和 target 必须是已有节点的 id。
```
