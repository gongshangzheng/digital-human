# Design: docs-list-ordering

## Context

- 现状排序链：`date` 降序 → `id` 升序（`server/routers/management.py` 的 `get_docs`）
- 断裂点：两篇同 `date`、都无 `id` → 落到 `os.walk` 顺序（APFS 无序，结果不确定）
- 文件夹顺序：前端 `DocPage.vue` 的 `docTree` 按"首次出现顺序"建树，因此由文档排序间接决定
- 约束：知识库 22 篇外部复制件已占用 `id: 1..22`，不得改动其 frontmatter（上游冻结）

## Goals / Non-Goals

**Goals：** 用 `order` 表达阅读顺序；文件夹先后可控；任何情况下顺序确定；未写新字段时与现状兼容。
**Non-Goals：** 不做拖拽排序 UI；不做用户自定义排序偏好；不改动知识库 frontmatter；不引入数据库存储顺序。

## Decisions

- **D1 `order` 与 `id` 解耦**：`order` = 阅读顺序（随便写、可留空档），`id` = 文档编号（登记表编号，可能有重复语义）。排序优先级 `order` > `id` > `date` > slug。
- **D2 文件夹优先级放服务端常量**：`management.py` 维护 `_DOCS_FOLDER_ORDER = ['实习复盘', '论文笔记', 'knowledge']`。理由：前端不需要感知，API 顺序即渲染顺序；改顺序只动一处。未列出的文件夹排其后。
- **D3 最后一级用 slug 字典序兜底**：彻底避免落到文件系统顺序，保证多次请求一致、换机器一致。
- **D4 前端不改**：树按列表顺序构建，服务端排序即最终顺序。
- **D5 `[shared]` 回灌候选**：排序逻辑属脚手架共享层，改动后按 upstream-sync 规则回灌 ProjFlow。

## Risks / Trade-offs

- [文件夹优先级写成常量不够灵活] → 先满足当前需求（3 个文件夹）；需要时再升级为配置文件
- [有人仍用 `id` 表达顺序] → 兼容：未写 `order` 时 `id` 仍是主键，行为不变
- [知识库顺序被意外改变] → 知识库文档都没有 `order`，测试用例显式覆盖"知识库顺序不变"

## Migration Plan

1. 改 `get_docs` 排序 + 加文件夹常量 → 接口验证顺序确定
2. 给 `实习复盘/` 现有文档补 `order`（入门篇 1、CyberVerse 2，后续按登记表顺延）
3. 验证：列表接口顺序、前端树顺序、knowledge 顺序未变
4. 回滚：去掉 `order` 即回到 `id` 排序

## Open Questions

- 论文笔记 5 篇与后续复盘的 `order` 具体取值（随各篇 change 落地时分配，本文只定机制）
