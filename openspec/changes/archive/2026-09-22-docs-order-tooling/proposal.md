# Proposal: docs-order-tooling（`order` 改为 10 步长 + 插入/重排脚本）

## Why

`数字人概述/`（原 `实习复盘/`）8 篇用 `order: 1…8` 连续编号。每插一篇新文档，**后面所有文档都要改一遍**：本次 `docs-dh-field-problems` 想把新篇放在《数字人介绍与技术路线》之后，就得动 7 个文件的 `order`。两个具体问题：

1. **编号不携带信息，却成了最容易冲突的地方**：每次章序改动都要改多个文件，diff 里混着「内容新增」与「编号调整」两类改动，复核时不好分辨
2. **没有工具，只能手算**：手写 `order` 需要先看目录、想好插到哪、再决定要不要动别人——没有一处能一眼看出「当前有哪些空位」

两件事一起做：**约定 10 步长**（相邻两篇之间永远留 9 个空位，插入时通常不用动别人）+ **一个脚本**（看空位、按位置插入、必要时把后续文档整体位移、以及整目录重排）。

## What Changes

### 1. 取值约定：`order` 以 10 为步长

- `management/docs/数字人概述/` 现有 8 篇改为 `10, 20, 30, 40, 50, 60, 70, 80`（阅读顺序不变，只是编号放大）
- 约定写入 `docs-page-content` 的「用 `order` 字段显式表达阅读顺序」：**步长 10、相邻留插入空间、插入时不重排既有文档**，示例由 `order: 1/2` 改为 `order: 10/20`，并补一条「在两篇之间插入新文档」的 scenario

### 2. 新增脚本 `scripts/docs_order.py`

三个子命令，**默认 dry-run**（加 `--apply` 才写盘）：

```bash
# 1. 看当前顺序与可用空位
python3 scripts/docs_order.py list management/docs/数字人概述

# 2. 按位置插入（自动找中间值；没有空位时把后续文档整体位移）
python3 scripts/docs_order.py insert management/docs/数字人概述 \
    --title "数字人领域问题" --after 数字人介绍与技术路线 --create --apply

# 3. 整目录规范化回 10 步长
python3 scripts/docs_order.py renumber management/docs/数字人概述 --apply
```

- **只改 frontmatter 的 `order`**，不碰正文与其余字段的原始写法
- `insert` 默认策略：**先找空位**（前后两篇之间若还有整数，取中点，不动任何人）；无空位时**把插入点之后的文档整体位移**为 10 步长
- `--shift` 可强制走位移路径；`renumber` 用于空位被用尽后一次性整理
- 排序基准与后端一致（`order → id → date 降序 → slug`），脚本里注明与 `server/routers/management.py:_doc_sort_key` 同源

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `docs-page-content`: 一处 MODIFIED —— 「用 `order` 字段显式表达阅读顺序」增加「步长 10、留插入空间、插入不重排既有文档」的取值约定与对应 scenario。排序**行为**不变（`order` 越小越靠前；未写 `order` 仍回退 `id`；非数字仍被忽略）。

## Impact

- **文档**：`management/docs/数字人概述/` 8 篇 frontmatter `order`（仅编号）
- **代码**：新增 `scripts/docs_order.py`（stdlib only，Python 3.9 兼容；不引第三方依赖）
- **规范**：`openspec/specs/docs-page-content/spec.md`（归档时同步）
- **不改**：`server/` 排序逻辑、`web/`、其它目录（全仓仅本目录用 `order`）
- **后续收益**：`docs-dh-field-problems` 用 `order: 20` 插入，**零改动其它文件**
- 与 `rename-internship-review-folder` 无耦合（只动 frontmatter，不动目录名），顺序可互换
