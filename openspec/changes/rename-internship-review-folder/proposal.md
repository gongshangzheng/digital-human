# Proposal: rename-internship-review-folder（`实习复盘/` 更名为 `数字人概述/`）

## Why

`management/docs/实习复盘/` 这个目录名把内容定位绑在了「实习」这一临时身份上，而里面的 8 篇（技术路线、身份、动作、框架、工程设计、加速、行业全景、总结）是**数字人方向的长期概述性文档**，不是一次实习的记录。目录名与内容定位不一致，也影响知识库与论文笔记的引用语义。

## What Changes

- **重命名目录**：`management/docs/实习复盘/` → `management/docs/数字人概述/`（`git mv`，文件名不变）。
- **更新服务端排序配置**：`server/config.py` 的 `DOCS_FOLDER_ORDER` 首项由 `实习复盘` 改为 `数字人概述`（顺序位置不变：仍排第一）。
- **更新全部在用的引用**（`[[实习复盘/...]]` → `[[数字人概述/...]]`）：
  - 该目录内 6 篇文档的交叉链接
  - `management/docs/论文笔记/{README.md,avatar-forcing.md,avatar-forcing.json}`
  - `.agents/skills/article-note/{phases/4-change.md,references/sidecar-guide.md}`（把命名空间示例改成新名）
- **更新主 specs 中已过时的示例与默认值**：`docs-page-content`（中文路径示例、默认文件夹顺序）、`docs-page-layout`（子目录折叠示例）。
- **不改写历史**：`openspec/changes/archive/**` 与已完成 change 的记录保持原样（它们记录当时的事实，重写等于篡改历史）。经核对，**活跃 change 里没有未完成任务引用该路径**，因此重命名不会打断在途工作。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `docs-page-content`: 两处 MODIFIED —— ①「中文（Unicode）文件名文档可访问」的示例路径 `实习复盘/数字人介绍与技术路线` 改为 `数字人概述/...`；②「文件夹在列表中的先后可配置」的默认顺序与示例由 `实习复盘 → 论文笔记 → knowledge` 改为 `数字人概述 → 论文笔记 → knowledge`。
- `docs-page-layout`: 一处 MODIFIED —— 「左侧文档列表支持子目录折叠」的示例分组名改为 `数字人概述/`。

## Impact

- 目录：`management/docs/数字人概述/`（8 篇，内容不变，仅改链接与目录名）
- 配置：`server/config.py`（`DOCS_FOLDER_ORDER` 首项）
- 文档：`management/docs/论文笔记/` 3 个文件；`.agents/skills/article-note/` 2 个文件
- 规范：`openspec/specs/docs-page-content/spec.md`、`openspec/specs/docs-page-layout/spec.md`
- 运行时影响：文档列表的文件夹分组与顺序（名字变化，位置不变）；旧链接 `/management/docs/实习复盘/...` 会 404（无重定向，属预期）
- 不涉及后端其它逻辑、前端代码、API 结构与业务数据
