## Context

排序契约本身已经在 spec 里：`docs-page-content` 规定排序链 `order` → `id` → `date` 降序 → slug、`order` 以 10 为步长、文件夹先后可配置；后端 `server/routers/management.py:_doc_sort_key` 已实现。缺的是**内容侧的强制约定**：`documentation` skill 只把 `order` 写成「可选」，于是 `论文笔记/` 两篇既无 `order` 也无 `id`，实际按 `date` 降序排成 `ditto` → `avatar-forcing`，与 `论文笔记/README.md` 清单里的阅读顺序相反；同时因为 `论文笔记/README.md` 没有 frontmatter，`docs_order.py` 在该目录直接报错退出，工具等于不可用。

## Goals / Non-Goals

**Goals：**

- 让 skill 明确「每个内容文件夹用显式排序键」，并写清缺省回落行为与索引 README 的 frontmatter 要求，使新建文档不再悄悄落到日期排序。
- 让 `论文笔记/` 真正用上 `order`：两篇笔记按阅读顺序编号，README 补最小 frontmatter 使工具可用。

**Non-Goals：**

- 不改后端排序实现、不改前端、不改 `docs-page-content` 既有契约（本次只是让内容满足既有契约）。
- 不重构 `knowledge/` 的 `id` 排序（52 篇保持原样），也不在本 change 内处理 `knowledge/README` 的同类缺口。
- 不新增或删除文档，不改动任何正文内容。

## Decisions

### D1：skill §2 的元数据段落改为强制排序键 + 缺省行为说明

`SKILL.md` §2 第二条由现在的一段话改为：

```markdown
- frontmatter 必填 `title`、`author`、`date`、`tags`、`summary`；排序键按文件夹选择：
  - 正文文档用 `order`（数字，10 为步长，如 `10, 20, 30`）表达阅读顺序；插入新篇优先占用相邻空位，不为插入一篇而重排既有文档。
  - 沿用 `id` 排序的文件夹（如 `knowledge/` 的外部复制件）可继续只写 `id`。
- **每个内容文件夹都必须有显式排序键**：未写 `order` 与 `id` 的文档会落到该目录内的 `date` 降序（越新越靠前），所以新建文档不得依赖日期隐式决定阅读顺序。
- 文件夹索引 `README.md` 也要带最小 frontmatter（`title`/`author`/`date`/`tags`/`summary`）；否则顺序工具在该目录直接报错，且列表标题会退化成裸 slug。
- 排序链为文件夹优先级 → `order` → `id` → `date` 降序 → slug。
```

备选方案是只改 §3 工具说明。否决原因是规则属于元数据约定，写在工具段落里会被读成「用工具时才需要」。

### D2：skill §3 补「新文档必须带 order」与工具的前置条件

在 §3 现有命令示例后追加两点：

- 新建或插入文档时 `order` 是必填项，用 `insert` 占空位（默认 dry-run，确认后 `--apply`）；单篇新建也要写 `order`，不要留空。
- 工具要求目录内所有 `.md` 都有合法 frontmatter；遇到索引 README 未加 frontmatter 时会直接失败，修复方式是先补 frontmatter 再运行工具。

### D3：skill §6 交付检查增加顺序校验

在交付检查列表里加一句：确认目标目录 `order` 无缺失、无重复，且与既定阅读顺序一致（用 `docs_order.py list <目录>` 复看）。

### D4：论文笔记的 order 分配

按阅读顺序（`avatar-forcing` 是体系入口兼对照前置篇，`ditto` 是它的对照篇）：

| 文档 | order |
|---|---|
| `论文笔记/avatar-forcing.md` | 10 |
| `论文笔记/ditto.md` | 20 |

插入点放在 frontmatter 的 `date` 之前或之后不影响解析，实施时统一放在 `summary` 之后。

### D5：论文笔记 README 的最小 frontmatter

`论文笔记/README.md` 现在没有任何 frontmatter，补：

```yaml
---
title: 论文笔记
author: 汤问
date: 2026-09-22
tags: [digital-human, 论文笔记]
summary: 数字人论文/模型统一笔记库：一篇一个论文/模型、夹内平铺，含 10 节统一模板与篇目清单。
---
```

**默认不给 README 写 `order`**，因此它在列表里保持当前位置（排在两篇笔记之后）；要不要让索引排在本目录最前，见「待确认项」。理由是：让索引排最前需要占掉 `order: 10` 并把两篇笔记重编为 20/30，属于改变现有列表顺序，应先明确。

### D6：`article-note` 校验允许 `order`（实施中发现）

给两篇笔记写 `order` 后，`validate-note.py` 报 `ERROR: unsupported frontmatter fields: order`——它的 `ALLOWED_META` 是 `{title, author, date, tags, summary, id, arxiv_id, papers_id}`，没有 `order`。这是两个 skill 的矛盾：`documentation` 现在要求每个内容文件夹用显式排序键，而笔记校验器拒绝这个键。

处理：把 `order` 加入 `ALLOWED_META`。理由：排序键由 `docs-page-content` 契约规定、后端已实现，拒绝它的是校验器的白名单过时；不允许的话，「论文笔记必须用 order」这条规则无法交付。备选方案是让论文笔记改用 `id`，但那会把阅读顺序与知识库的整理编号混为一谈，否决。

## Risks / Trade-offs

- [`validate-note.py` 与排序键的冲突] → D6 直接把 `order` 加入白名单，并保留对其他未知字段的拒绝；若将来 frontmatter 约定扩展，两边需同步（skill §2 与校验器白名单）。
- [给 README 加 frontmatter 会让它更像一篇「文档」出现在列表里] → 但它本来就已经出现在列表里（只是标题退化成 `论文笔记/README`），补 frontmatter 后显示反而更正确；若后续要把它从列表排除，那属于后端行为变更，另开 change。
- [skill 措辞过强会与 `knowledge/` 的 `id` 现状冲突] → D1 明确保留「沿用 `id` 的文件夹可继续只写 `id`」，并要求的是「有显式排序键」而不是「一律用 order」。
- [只改 skill 不改内容，规则仍会被绕过] → 本 change 同时落地 `论文笔记/`，且 §6 交付检查提供可复查的判据。
- [顺序偏好被单方面决定] → 默认方案写入 D4/D5，并在待确认项里列出可替换选项。

## 待确认项

1. **论文笔记的阅读顺序**：默认 `avatar-forcing` 10 → `ditto` 20（AF 是体系入口与 ditto 的对照前置篇）。若你希望按写作时间倒序（ditto 10 → AF 20），改一行即可。
2. **索引 README 是否排最前**：默认不加 `order`（保持在末尾）。若要排最前，需要 README 取 10、两篇笔记改 20/30，会改变当前列表顺序。
3. **`knowledge/README` 的同类缺口**：它同样没有 frontmatter，也会在列表里显示为裸 slug，也会让 `docs_order.py` 在 `knowledge/` 报错。本 change 不处理；需要的话我另开一个小的内容级改动。

## Migration Plan

1. 用户审核本 design（尤其 D1 的措辞与三条待确认项）。
2. apply 阶段：改 `SKILL.md` 三处 → 给两篇笔记写 `order` → 给 README 补 frontmatter → 用 `docs_order.py list management/docs/论文笔记` 复看（应显示 10/20 且无重复）。
3. 校验：`docs_order.py list` 输出符合预期、`GET /api/management/docs` 中 `论文笔记/` 顺序为 avatar-forcing → ditto → README(标题为「论文笔记」)、`openspec validate docs-skill-order-convention --strict` 通过。
