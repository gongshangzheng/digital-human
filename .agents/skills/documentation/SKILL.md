---
name: documentation
description: |
  Digital Human 项目唯一的文档写作 skill：为说明性 Markdown 文档提供 OpenSpec 审核门禁，以及文档落点、frontmatter、sidecar、链接、图片、LaTeX、Mermaid 与写作格式约定。
  适用于新建或结构化修改 management/docs/ 下的文档、论文笔记、技术介绍和项目说明。
---

# 文档写作指南

本 skill 同时定义文档正文的流程门禁和内容规范。它取代旧的 `doc-writing` skill；不要在项目或全局目录创建重叠的文档写作入口。

## 1. OpenSpec 门禁

先判断改动是否为结构级变更：新增文档、重组章节、大段增删、跨文档职责调整均为结构级；错字、一个事实值、短段论证、格式或坏链接修复为内容级。

结构级变更必须按以下顺序执行：

1. 先探索现有文档、代码和可靠素材，确定落点与职责边界。
2. 创建 `openspec/changes/docs-<slug>/` change，并在 `design.md` 写明目标读者、完整二级章节结构、每节论点与结论、关联文档、待调研知识点和待决项。
3. 用户明确审核 design 后，再整理素材；素材口径由用户确认后才写正文。
4. 实施时按 tasks 勾选，验证 OpenSpec、链接、图片、Mermaid、sidecar 与 Git diff。

内容级修改可以直接完成，但不得凭记忆修改：先通读目标文件并核对实际路径。不得编造领域背景、引文、实验结果或未披露配置；正文只说明当前状态，演进历史写进 sidecar `changelog`。

## 2. 文档位置与元数据

- 说明性 Markdown 统一放在 `management/docs/`，可用现有主题子目录，如 `数字人概述/`、`技术介绍/`、`论文笔记/`、`knowledge/`；仓库根目录不设 `docs/`。
- frontmatter 必填 `title`、`author`、`date`、`tags`、`summary`；排序键按文件夹选择：
  - 正文文档用 `order`（数字，10 为步长，如 `10, 20, 30`）表达阅读顺序；插入新篇优先占用相邻空位，不为插入一篇而重排既有文档。
  - 沿用 `id` 排序的文件夹（如 `knowledge/` 的外部复制件）可继续只写 `id`。
- **每个内容文件夹都必须有显式排序键**：未写 `order` 与 `id` 的文档会落到该目录内的 `date` 降序（越新越靠前），所以新建文档不得依赖日期隐式决定阅读顺序。
- 文件夹索引 `README.md` 也要带最小 frontmatter（`title`/`author`/`date`/`tags`/`summary`）；否则顺序工具在该目录直接报错，且列表标题会退化成裸 slug。
- 排序链为文件夹优先级 → `order` → `id` → `date` 降序 → slug。
- 可选同名 sidecar `<slug>.json` 承载 `changelog`、`progress`、`related`、`appendix`；`related` 项必须是含 `slug` 和 `title` 的对象，不能是字符串。

```yaml
---
title: 文档标题
author: 作者
date: 2026-09-22
tags: [digital-human]
summary: 一句话概括本文档内容
order: 10
---
```

## 3. 文档顺序工具

`./scripts/docs_order.py` 是本 skill 随附的、只依赖 Python 标准库的 frontmatter `order` 维护工具；从仓库根目录使用完整路径：

```bash
# 查看当前阅读顺序、整数空位与重复值（只读）
python3 .agents/skills/documentation/scripts/docs_order.py list management/docs/数字人概述

# 预览插入：默认消耗已有整数空位，且绝不写盘
python3 .agents/skills/documentation/scripts/docs_order.py insert management/docs/数字人概述 \
  --title "新文档" --after 数字人领域问题 --create

# 确认上述预览后才写入
python3 .agents/skills/documentation/scripts/docs_order.py insert management/docs/数字人概述 \
  --title "新文档" --after 数字人领域问题 --create --apply

# 明确需要 10、20、30 连续顺序时：新篇取插入点 order，后缀顺延；前缀不变
python3 .agents/skills/documentation/scripts/docs_order.py insert management/docs/数字人概述 \
  --title "新文档" --after 数字人介绍与技术路线 --create --shift --apply

# 明确要求规范化整个目录时，按当前阅读顺序重编为 10、20、30…
python3 .agents/skills/documentation/scripts/docs_order.py renumber management/docs/数字人概述 --apply
```

所有改写命令默认 dry-run，只有显式传入 `--apply` 才写盘。正常插入优先占用相邻文档间的整数空位，不改既有文档；`--shift` 才重排插入点及其后的后缀。工具拒绝重复的数值 `order`、多个 `order:` 行及不合法 frontmatter，除非用户明确使用 `--force`；写入后会做结构校验和单文件回滚保护。

新建或插入文档时 `order` 是**必填项**：用 `insert` 占用相邻空位（默认 dry-run，确认后加 `--apply`），单篇新建也要写 `order`，不要留空。工具要求目录内所有 `.md` 都有合法 frontmatter；若索引 `README.md` 未加 frontmatter，工具会以缺 frontmatter 的错误直接失败，先补 frontmatter 再运行。

## 4. Markdown 内容约定

- 最高正文标题使用 `##`，其下使用 `###`，不跳级；标题应是具体主题，不用“概述”“现行做法”等无信息桶标题包裹。
- 内部文档链接使用 `[[数字人概述/数字人身份|数字人身份]]`；跨文档 slug 必须相对 `management/docs/`，不得链接相对 `.md` 文件。仅链接已存在的文档。
- 文内小节使用 `[标题](#slug)`；锚点来自实际标题，不凭记忆构造。
- 图片放在 `management/docs/_assets/<slug>/`，使用绝对 `/api/management/docs-assets/<slug>/<file>` URL。独立图片用 `![图 N · 说明](...)`，图号连续且正文必须解读该图。
- 原始 HTML 不会被 Markdown 渲染器执行；不要用原始 `<img>` 代替 Markdown 图片。

## 5. 公式与 Mermaid

正文支持 KaTeX：行内公式写 `$...$`，块级公式写 `$$...$$`。每个公式后必须给符号表和中文解释，必要时可附代码块保留原始 TeX。

```markdown
质能关系 $E = mc^2$ 成立。

$$
\mathcal{L}_{total} = \mathcal{L}_{rec} + \lambda \mathcal{L}_{per}
$$
```

- 不使用 `\(...\)`、`\[...\]` 或 `\begin{equation}`；分别改为 `$...$` 或 `$$...$$`。
- 公式定界符内首尾不能留空白；金额如 `$5 到 $10` 保持普通文本。
- Mermaid 节点内只能用 `$$...$$`：`A["输入 $$x_t$$"] --> B["损失 $$\mathcal{L}$$"]`；单 `$` 是 Mermaid 的已知不渲染边界。
- 流程、架构、时序等结构关系优先 Mermaid，不使用 ASCII 图。完整语法与图内公式例子见 `references/mermaid-cheatsheet.md`。

## 6. 交付检查

交付前检查：章节与已审 design 一致；事实可追溯且未编造；链接目标存在；图片 URL 与资产存在；sidecar JSON 合法；同目录 `order` 无缺失、无重复且与既定阅读顺序一致（用 `docs_order.py list <目录>` 复看）；Mermaid 可渲染；公式语法使用受支持定界符；OpenSpec 严格验证通过。论文笔记还须执行 `.agents/skills/article-note/scripts/validate-note.py`。
