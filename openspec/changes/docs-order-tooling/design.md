# Design: docs-order-tooling

## Context

- `order` 是 `docs-page-content` 规范里有明确语义的字段：**数字、越小越靠前、优先于 `id`、未写则回退 `id`**；排序链最终落到 slug 字典序（不得落到文件系统顺序）。
- 后端唯一实现：`server/routers/management.py` 的 `_doc_sort_key` = `文件夹优先级 → order → id → date 降序 → slug`；`order` 经 `_doc_number` 归一（非数字按 `inf` 排最后）。
- 全仓只有 `management/docs/实习复盘/`（即将改名 `数字人概述/`）8 篇写 `order`，值为连续 1–8。前端不显示 `order`，只影响列表顺序。
- 现有脚本风格见 `scripts/import_papers.py`：`argparse` + `pathlib` + 模块 docstring 写用法。

## Goals / Non-Goals

**Goals**

- 插入一篇新文档时**默认不需要改动其它文件**。
- 需要重排时有一条命令，且**执行前能看到将发生的全部改动**。
- 编号本身不再是最脆弱的一处：脚本能一眼看出空位与重复。

**Non-Goals**

- 不改后端排序逻辑（行为不变，只改取值）。
- 不引入「自动按文件名/日期推导顺序」——顺序是人工判断，脚本只负责把它写对。
- 不做跨目录的全局编号（`order` 只在同一目录内比较；不同目录由 `DOCS_FOLDER_ORDER` 决定先后）。
- 不改正文；不改其他 frontmatter 字段的写法。

## Decisions

### D1：步长取 10，不取 100

10 步长在「相邻最多插 9 篇」的量级上够用，且 order 值与「第几篇」的对应仍可心算（10、20、30…）。100 步长会让 `order: 700` 这种值与直觉脱节，收益却只在极端插入密度下才体现。

- 备选：不编号、改用显式列表文件 —— 引入新事实来源，双写不一致风险更大，不采用。

### D2：脚本做**行级 frontmatter 编辑**，不做 YAML round-trip

PyYAML 把 frontmatter 解析后再 `dump`，会重排字段顺序、改引号风格、把行内数组 `[a, b]` 拆成多行、丢掉注释——一次改 `order` 就把整块 frontmatter 的写法全改掉，diff 不可读。

因此：**正则定位 `order:` 那一行改值**；字段不存在时插到 `title:` 之后（否则追加到 frontmatter 末尾）。其余字节一律不动。

- 写盘前后仅做内置的 frontmatter 结构与 `order` 字段校验：首尾分隔符完整、`order` 行唯一且值为数字；不引入 PyYAML 做完整 YAML 语义解析。`order` 行有奇异写法时按行内 `#` 注释保留后半段。
- 备选：`ruamel.yaml` 保序 dump —— 需要新依赖，收益与 D2 相同，不采用。

### D3：默认 dry-run，`--apply` 才写盘

frontmatter 是手写资产，且 `renumber` 可能一次改十几行。默认只打印计划（文件 + 原值 → 新值 + 是否新建），`--apply` 才落盘。这样「看一眼再决定」是默认路径，而不是需要额外的 `--dry-run` 参数。

- 与 `scripts/import_papers.py` 的直接写盘风格不同：那个脚本写的是可重跑的 SQLite；这里写的是手写文件。

### D4：插入优先找空位，无空位才位移

`insert` 的目标 order 按下面顺序确定：

1. `--order N` 显式指定 → 直接用
2. 解析 `--after <slug>` / `--before <slug>` / `--index N` 得到**插入位置**
3. 若插入位置前后两篇的 order 之间存在整数空位 → **取中点**（例：10 与 30 之间取 20；10 与 20 之间没有整数，取不到）
4. 无空位 → **位移**：把插入点及其后的文档整体重排为 `10, 20, 30 …`（这就是「位移后续所有文档」）
5. `--shift` 强制走第 4 步（即使有空位也重排，用于把编号整理成规整的 10 步长）

`insert` 的位置参数三个都缺省时，追加到目录末尾。

### D5：排序基准与后端同源

脚本内部实现同一套 key（`order → id → date 降序 → slug`），并在注释里指向 `server/routers/management.py:_doc_sort_key`。**不 import 后端模块**（避免为了改 frontmatter 拉起 FastAPI 依赖），但要求两处口径一致；改动后端排序链时必须同步。

- 已知代价：一次轻微的重复实现。判据是「脚本算出的顺序 == 页面看到的顺序」，作为一条验收项。

### D6：重复 `order` 报告而非静默处理

目录内出现重复 order 时（手工编辑很容易撞），`list` 与 `insert`/`renumber` 都要在输出中标红/标出并**以非零码退出**（`--apply` 时拒绝写入，除非显式 `--force`），因为「顺序看似对但实际由 slug 决定」是最难排查的一类问题。

### D7：`--create` 只生成最小 frontmatter

文件不存在且传了 `--create` 时，按同目录既有格式生成：

```yaml
---
title: <title>
author: 汤问
date: <today>
tags: []
order: <n>
summary:
---

# <title>
```

正文只留一个标题与占位注释，不编造内容。`author` 可用 `--author` 覆盖。

## Risks / Trade-offs

| 风险 | 缓解 |
|---|---|
| 改错值导致顺序变化 | 默认 dry-run；`renumber` 的输出是「原值 → 新值」全量清单；改完用 `list` 与后端 `/api/management/docs` 双向核对 |
| 行级编辑写坏 frontmatter | 只改 `order:` 一行；写完立即以内置规则校验 frontmatter 分隔符、唯一 `order:` 行及数值格式（失败则回滚该文件并报错） |
| 与后端排序链漂移 | D5 的注释指引 + 一条验收项（脚本顺序 == API 顺序） |
| 位移把人工安排的语义编号抹掉 | 位移只发生在「无空位」或显式 `--shift` 时，且 dry-run 会完整列出 |
| 脚本变成又一处需要维护的代码 | 规模控制在单文件、stdlib、三个子命令；不做成通用工具 |

## Migration Plan

1. 落规范 delta（本 change 已含）
2. 实现 `scripts/docs_order.py`
3. 对 `数字人概述/` 跑 `renumber --apply`：`1–8 → 10–80`（一次到位）
4. 验证：`list` 输出、重复检测、`insert --create` 的 dry-run/apply 各跑一遍（用临时目录，不污染真目录）
5. 与后端对上：`GET /api/management/docs` 中该分组顺序不变

回滚：`renumber --step 1 --start 1 --apply` 可回到连续编号（脚本自身就能回滚）。

## Open Questions

- 是否需要 `swap`/`move`（把已有文档在目录内挪位）？当前用「`renumber` + 改 `order`」两步可覆盖，暂不单独做。
