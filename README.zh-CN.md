# SourceTrace

[![tests](https://github.com/ChenXuanyu-1216/SourceTrace/actions/workflows/tests.yml/badge.svg)](https://github.com/ChenXuanyu-1216/SourceTrace/actions/workflows/tests.yml)

[English](README.md) | **简体中文** | [日本語](README.ja.md) | [한국어](README.ko.md) | [Italiano](README.it.md) | [العربية](README.ar.md)

> 本文由 AI 译自 [README.md](README.md)。两者不一致时，以英文版为准。

一个 Agent Skill：对照课件，审核 AI 生成的知识树。

AI 工具几秒钟就能把课件变成知识树，但其中的定义可能有错，关系可能是编出来的，重要内容也可能漏掉。SourceTrace 对照原始图片检查每个节点和每条边，每个结论都有证据：**为什么**有问题，在课件的**哪里**（页码和原文），以及依据的是**什么**（证据编号）。

它可以在支持 Agent Skills 的工具中使用，例如 Claude Code 或 Codex，能处理中文或英文的课件和网页截图。

## 输出

提供课件图片（PNG/JPG）和知识树（JSON）。它会在知识树旁边的 `sourcetrace-output/` 文件夹里写入三个文件：

| 文件 | 内容 |
|------|------|
| `report.md` | 审核报告：概要、问题、来源提示（折叠）、遗漏、结构问题、已确认内容 |
| `audit.json` | 同一结果的机器可读版本：每个节点和每条边都有结论 |
| `evidence-index.json` | 从课件中提取的全部内容，每条都有编号、页码和原文引用 |

下面是在 8 页中文课件上运行得到的两条问题，文字有删节，省略了修改建议一栏（[完整报告](tests/smoke/model-eval-e2e/report.md)）：

| 编号 | 对象 | 类别 | 风险 | 问题 | 证据 |
|---|---|---|---|---|---|
| F-002 | N005 数据集划分比例 | 概念错误 | 高 | 比例数字错误：树中写"8 : 1 : 1"，课件写"7 : 2 : 1"。 | EV-013 第 2 页 "本课程推荐的划分比例：训练集 : 验证集 : 测试集 = 7 : 2 : 1。" |
| F-004 | E010 过拟合 —related-to→ 高偏差 | 关系错误 | 高 | 关系对调：第 4 页图示为"过拟合 → 高方差"，树中却把过拟合连到高偏差。 | EV-020 第 4 页 "Diagram: 过拟合 → 高方差（对训练数据过于敏感）" |

每个问题归入六个类别之一（概念错误、关系错误、无依据扩展、过度概括、无法核验、遗漏），并给出风险等级，每条问题都附有修改建议。如果一个定义除了一处添加的细节以外都有资料支持，就不算错误，而是作为低风险的*来源提示*，单独放在一个折叠的部分里。

## 快速开始

1. 安装唯一的依赖：

   ```bash
   pip install jsonschema
   ```

2. 把 `source-trace/` 文件夹复制到所用工具的 skills 文件夹：

   | 工具 | Skills 文件夹 |
   |------|---------------|
   | Claude Code（个人） | `~/.claude/skills/source-trace/` |
   | Claude Code（单个项目） | `<project>/.claude/skills/source-trace/` |
   | Codex | `~/.codex/skills/source-trace/`（请查阅你所用 Codex 版本的文档） |

3. 用自己的话提出请求，并给出课件图片和知识树：

   > 这是我的课件截图（slides/ 文件夹）和 AI 生成的知识树 tree.json，帮我对照课件检查一下。

   > Check knowledge-tree.json against my lecture slides in images/.

知识树必须符合 [`knowledge-tree.schema.json`](source-trace/schemas/knowledge-tree.schema.json)（节点有 `id`、`label`、`definition`、`kind`；边有 `id`、`source`、`target`、`relation`）。如果你的知识树用的是别的格式，技能会先转换，并告诉你是怎样对应的。PPT 或 PDF 课件需要先导出为图片。

## 隐私

SourceTrace 在你的 AI agent 里运行，所以 agent 会读取你的课件图片和知识树。这些内容会发送给 agent 所用的 AI 模型，适用该服务商的条款。技能自带的脚本在本地运行，不向任何地方发送数据。

- **只审核你有权分享给 AI 服务商的课件。** 课件通常属于授课教师，可能需要征得其同意。
- **像对待课件本身一样对待输出文件。** `evidence-index.json` 和 `report.md` 包含课件的原文引用。
- **未经许可，不要提交或公开他人的课件或审核结果。**

## 效果如何

**合成课件。** 在两个埋有错误的测试集上（4 页英文课件、8 页中文课件），普通 AI 助手和 SourceTrace 都找到了全部埋入的错误。SourceTrace 补上了普通模型缺少的部分：

- 每个结论背后都有证据编号、页码和原文，
- 每个节点和每条边都有结论，
- 类别和风险等级固定，
- 机器可读的 `audit.json`，
- 没有偏离主题的"遗漏"条目，
- 中文测试集上的四次运行结果完全相同。

代价是 token 用量多约 30%，耗时约为 3 倍。

**真实内容。** 使用中文维基百科条目（CC BY-SA 4.0），知识树由其他 AI 工具生成，所以其中的错误是真实的。前两个条目的知识树来自 OpenAI Codex，项目负责人审核了每一份报告，每次审核后都修订了规则：

| 运行 | 审核的条目 | 对 | 部分对 | 错 |
|-----|--------------|---------|----------------|-------|
| 机器学习，第 1 次（v0.1.0 规则） | 13 | 6 | 4 | 3 |
| 机器学习，第 2 次（第一次修订） | 18 | 14 | 1 | 3 |
| 决策树学习，第 1 次（第二次修订） | 11 个问题 + 77 个已确认条目 | 85 | 1 | 2 |

v0.3.0 中（详见 [CHANGELOG.md](CHANGELOG.md)）：

- **又测试了两个条目**，使用第五次规则修订。朴素贝叶斯分类器（知识树来自 ChatGPT）：两次重跑在全部 87 项上与答案一致。感知器（知识树来自 Codex）：两次运行都找到了知识树里的两处真实错误，没有把正确的条目判为问题，但漏掉了资料本身的四处问题，这些问题需要简短推导才能看出。这两个测试集的答案是项目负责人认可的 AI 审核；朴素贝叶斯分类器的答案出自生成知识树的那个对话。
- **规模测试**（32 页合成课件、169 项的知识树）、**降质图片**（扫描、拍照和部分遮挡的版本），以及 **Codex 的两次运行**。

第六次规则修订运行过一次，由 Codex 在感知器上运行：条目判断不变，并找到了四处来源问题中的两处。它还没有在与这次修订无关的条目上测试过，所有审核都由同一个人完成或认可。详情和局限：[docs/evaluation.md](docs/evaluation.md) 以及各测试集的 `RESULTS.md`。

## 工作原理

SourceTrace 分六个阶段运行：资料读取 → 证据提取 → 知识映射 → 双向审核 → 冲突检测 → 审核报告。需要判断的部分由 agent 完成：阅读课件、把论断与证据对应、给出结论。凡是能检查或计算的，都由三个脚本完成：

| 脚本 | 阶段 | 作用 |
|--------|-------|------|
| `validate_input.py` | 1 | 检查知识树和图片；给页面编号；对结构问题发出警告，例如知识树不连通 |
| `validate_evidence.py` | 2 | 检查证据索引：编号唯一，页码和来源一致 |
| `build_report.py` | 6 | 对照知识树和证据检查 agent 写的 `audit.json`，补上概要和问题编号，并生成 `report.md` |

关于结论、类别、风险和遗漏的规则见 [`references/audit-rules.md`](source-trace/references/audit-rules.md)。规则背后的设计决定见 [docs/requirements.md](docs/requirements.md)。

也可以自己运行这些脚本：

```bash
python source-trace/scripts/validate_input.py --tree tests/fixtures/ml-basics/knowledge-tree.json --images tests/fixtures/ml-basics/images
python source-trace/scripts/validate_evidence.py --index tests/fixtures/ml-basics/evidence-index.example.json
python source-trace/scripts/build_report.py --tree <tree.json> --index <output>/evidence-index.json --audit <output>/audit.json
```

两个校验脚本支持 `--json`，输出机器可读的结果。`validate_input.py` 写出的图片路径是相对于输出文件夹的（知识树旁边的 `sourcetrace-output/`，或用 `--out` 指定的文件夹）。三个脚本成功时退出码为 0，输入无效时为 1，用法错误时为 2。

## 开发

```bash
pip install -r requirements.txt
python -m pytest
```

119 个测试，约 2 秒。它们覆盖三个脚本（有效输入、每一种错误和警告代码、输出可重复、中英文报告），也检查已保存的技能运行结果是否仍符合答案。它们不运行技能本身，因为那需要 agent；新的运行结果用 `tools/compare_runs.py` 评分。

```
source-trace/          技能本身（安装的就是这个文件夹）
├── SKILL.md           说明和触发描述
├── schemas/           JSON Schema：知识树、证据条目、证据索引、审核结果
├── references/        提取规则和审核规则，需要时加载
└── scripts/           上面的三个脚本
docs/                  需求和评估
tests/fixtures/        测试集：带答案的合成课件；维基百科截图（CC BY-SA），附审核运行和审核意见
tests/baseline/        普通 AI 的运行结果，用于对比
tests/smoke/           技能的端到端运行
tests/consistency/     技能的重复运行
tests/test_*.py        pytest 测试
tools/                 make_fixture_slides.py、compare_runs.py、degrade_images.py
```

## 现状和下一步

v0.3.0。见 [CHANGELOG.md](CHANGELOG.md)。

测试数据原则：SourceTrace 只在开放许可、项目负责人自己编写或合成的材料上测试。不使用第三方课件，也不使用私人数据。

下一步：

1. **为第六次修订找一个新条目：** 与任何规则都无关，最好是英文或其他领域，答案来自与生成知识树不同的模型。
2. **独立审核：** 由项目负责人以外的人审核，或由与运行 agent 不同的模型给出答案。
3. **真实图片：** 开放许可或项目负责人自己编写的课件的照片或扫描件。
4. **任务模式：** 一种严格溯源模式，以及一种允许简短、加标注的资料外解释的审阅模式。

## 参与贡献

欢迎报告错误、指出错误的结论或贡献新的测试集。请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)（英文），尤其是隐私部分：不要附上你无权分享的课件或审核结果。

## 许可证

代码和文档采用 [MIT 许可证](LICENSE)。`tests/fixtures/wiki-*/` 中的维基百科测试集按其来源的要求采用 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)；每个这样的文件夹都有自己的 `LICENSE.md` 和 `ATTRIBUTION.md`。
