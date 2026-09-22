# Proposal: sync-projflow-round3（pick 上游文档图片能力 + 文档根目录约定 + 排序常量收敛）

## Why

上游 ProjFlow 新增了两条 `[shared]` 文档基础设施改动，本仓库尚未同步：

1. `e505269` **wiki 文档图片支持** — 本仓库 `server/main.py` 未挂载任何静态资源目录，Markdown 里写图片必然 404；`MarkdownRenderer` 也没有图片语义包装与样式。这挡住了所有需要配图的文档（论文精读笔记的架构图/实验曲线、架构文档的模块图）。刚接入的 `article-note` skill 也因此只能把图停在 `.cache/` 里。
2. `4a3b964` **文档根目录唯一** — 上游明确「说明性文档统一置于 `management/docs/`，仓库根目录不设 `docs/`」，并写入 spec 防止回潮。本仓库刚因照抄上游过期的 `AGENTS.md` 目录树而误建过根目录 `docs/`（已在 `d99af94` 删除），需要把这条约束固化成 spec。
3. `644fed0` **文档页文内锚点接管 + 文档列表排序链** — 其中「文内锚点接管」本仓库已具备；但排序链上游已把文件夹优先级**泛化到 `server/config.py`**（默认空，下游按需覆盖），而本仓库仍把领域目录名硬编码在 `server/routers/management.py` 内。同一逻辑、常量位置不同 = 长期分叉，需要收敛。

## What Changes

**从上游 pick（`e505269`）**：
- `server/main.py`：把 `management/docs/_assets/` 挂载为只读静态目录到 `/api/management/docs-assets/`；目录不存在时自动创建，不导致启动失败。
- `server/routers/management.py`：`get_docs()` 扫描时跳过我下划线前缀目录（`_assets/` 等），资产目录内的 `.md` 也不入库。
- `web/src/components/common/MarkdownRenderer.vue`：覆写 markdown-it 的 image 规则，输出 `<img loading="lazy">`；「整段仅一张带 alt 的图」包装为 `<figure>` + `<figcaption>`（alt 兼作图题）。
- `web/src/styles/index.scss`：`.markdown-body` 下新增 `figure` / `img` / `figcaption` 样式（自适应宽度、居中、圆角、图题弱色小字）。
- `management/docs/_assets/.gitkeep`：建立资产目录约定。

**从上游 pick（`4a3b964`）**：
- 把「仓库文档根目录唯一」写入 spec（`AGENTS.md` 的对应说明已由 `d99af94` 落地，本变更只补 spec 约束）。

**从上游 pick（`644fed0`）—— 仅收敛，不重复实现**：
- **文内锚点接管**：本仓库已具备且与上游落地内容一致，本变更只做核对，不重复改动。
- **文档列表排序链**：本仓库实现与上游等价，但文件夹优先级常量硬编码在 router；收敛为 `server/config.py` 的 `DOCS_FOLDER_ORDER`（值仍为本仓库领域顺序），使 `management.py` 与上游逐字对齐。

**联动**：
- `.agents/skills/article-note/SKILL.md`：图片端点就绪后，移除「未就绪时只登记 raw、不写 docs-assets 链接」的临时限制，恢复标准发布流程。

**登记**：
- 上游同步记录改写到本次 change（`docs/external-sources.md` 已按 `d99af94` 删除，不再单设登记表）。

## Capabilities

### New Capabilities

- `doc-image-assets`: wiki 文档图片的存储约定、静态服务端点、Markdown 引用方式与 figure 渲染规范。
- `repo-docs-structure`: 仓库说明性文档的根目录唯一性约束（统一置于 `management/docs/`，根目录不设 `docs/`）。

### Modified Capabilities

（无）

## Impact

- 后端：`server/main.py`（新增静态挂载）、`server/routers/management.py`（文档扫描跳过资产目录；排序常量改为从 config 导入）、`server/config.py`（新增 `DOCS_FOLDER_ORDER`）。
- 前端：`web/src/components/common/MarkdownRenderer.vue`、`web/src/styles/index.scss`。
- 数据/目录：新增 `management/docs/_assets/`（内容随笔记入库）。
- Skill：`.agents/skills/article-note/SKILL.md`（前置条件解除）。
- 不影响：既有文档（原本无图）、其它路由与页面、端口与业务数据。
- 依赖方向：`article-note` 的图片发布依赖本能力。
- 归属：`server/`、`web/src/` 属共享脚手架层 → 实施提交加 `[shared]` 前缀。
