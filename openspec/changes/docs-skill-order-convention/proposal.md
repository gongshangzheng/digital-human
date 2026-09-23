## Why

`management/docs/` 下有四个内容文件夹，但只有三个使用了显式排序键：`数字人概述/`（`order: 10–90`）、`技术介绍/`（`order: 10`）、`knowledge/`（`id: 1–52`）。**`论文笔记/` 两篇都没有 `order`，也没有 `id`**，于是排序链在 `order`/`id` 上都取 `inf`，实际落到 `date` 降序——接口当前返回 `ditto`（09-23）排在 `avatar-forcing`（09-22）之前，理由是「更新」而不是「该先读」，与 `论文笔记/README.md` 清单里的阅读顺序相反。

`documentation` skill 现在只把 `order` 写成「可选」并给一句「建议用 10、20、30 空档」，没有规定**每个内容文件夹都必须有显式排序键**，也没有说明缺 `order` 时会回落 `date` 降序，更没有提示**索引 README 缺 frontmatter 会让顺序工具直接报错**（`docs_order.py list management/docs/论文笔记` 当前以 `ERROR: 缺少以 --- 开始的 frontmatter` 退出）。结果是 agent 新建笔记时不写 `order` 不违规，列表顺序悄悄由日期决定。

## What Changes

- 更新 `.agents/skills/documentation/SKILL.md`：
  - §2 明确每个内容文件夹 SHALL 使用显式排序键：正文文档用 `order`（10 为步长），外部复制件（`knowledge/`）沿用 `id`；写明**未写 `order`/`id` 时会回落该目录内的 `date` 降序**，因此新建文档 MUST NOT 依赖日期隐式排序。
  - §2 要求文件夹索引 README 也带最小 frontmatter（否则顺序工具在该目录报错、列表标题退化为裸 slug）。
  - §3 补「新建/插入文档必须写 `order`，并用工具占用相邻空位」，并写明工具遇到无 frontmatter 文件会直接失败及修复方式。
  - §6 交付检查增加「同目录 `order` 完整、无重复、与阅读顺序一致」。
- 让 `论文笔记/` 真正用上 order：两篇笔记补 `order`（`avatar-forcing` 10 → `ditto` 20，按阅读顺序）；`论文笔记/README.md` 补最小 frontmatter，使 `docs_order.py` 在该目录可用。
- 修正 `article-note` 校验与排序键的矛盾：`validate-note.py` 的允许字段加上 `order`，否则按新规则写的论文笔记会被自己的交付校验判为失败。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `repository-agent-skills`: 新增两条要求：① `documentation` skill 必须写明「每个内容文件夹使用显式排序键」的约定、缺省回落行为、索引 README 的 frontmatter 要求，以及交付前对同目录 `order` 的校验；② `article-note` 笔记校验必须接受排序键 `order`。

## Impact

- 修改 `.agents/skills/documentation/SKILL.md`（§2、§3、§6）。
- 修改 `.agents/skills/article-note/scripts/validate-note.py`（`ALLOWED_META` 加 `order`）。
- 修改 `management/docs/论文笔记/avatar-forcing.md`、`ditto.md`（各加一行 frontmatter）、`management/docs/论文笔记/README.md`（补最小 frontmatter）。
- 不改后端排序实现：`server/routers/management.py:_doc_sort_key` 与 `documents-page-content` 的排序契约（`order` → `id` → `date` 降序 → slug、文件夹优先级、10 步长）保持不变，本次只是让内容满足既有契约。
- 不涉及 API、依赖与前端代码。
