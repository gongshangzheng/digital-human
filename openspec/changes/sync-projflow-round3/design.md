## Context

- 上游 ProjFlow 三条 `[shared]` 改动尚未进入本仓库：`e505269` 文档图片支持、`4a3b964` 文档根目录唯一、`644fed0` 文档页文内锚点接管 + 文档列表排序链。
- 本仓库与上游共享层存在**已分叉的定制**，不能直接 cherry-pick：
  - `server/main.py`：路由注册与其余内容与上游一致，仅 import 行不同（上游多 `StaticFiles` 与 `MANAGEMENT_DIR`），平台名/端口不同（本仓库 8812）。
  - `web/src/components/common/MarkdownRenderer.vue`：**文内锚点接管**本仓库已有，且与上游 `644fed0` 落地内容一致；`[[proj#task]]` / `[[slug]]` 链接改写本就双方共有。剩余唯一差异是上游 `e505269` 的 image / figure 规则。
  - `server/routers/management.py` 的 `get_docs()`：本仓库把文件夹优先级硬编码为 router 内的 `_DOCS_FOLDER_ORDER = ['实习复盘', '论文笔记', 'knowledge']`；上游 `644fed0` 已把同一机制泛化到 `server/config.py` 的 `DOCS_FOLDER_ORDER`（默认空）。**同一逻辑、常量位置不同 = 分叉**，本变更需收敛。
- 本仓库文档目录已重构为 `management/docs/{knowledge,论文笔记,实习复盘}`，`docs/external-sources.md` 已删除（`d99af94`）。
- `article-note` skill 已接入（`7a60519`），其「图片端点未就绪」的前置限制依赖本变更解除。

## Goals / Non-Goals

**Goals：**

- 在三个共享层文件（`server/main.py`、`server/routers/management.py`、`web/src/components/common/MarkdownRenderer.vue` + `index.scss`）上落地与上游等价的图片能力，且不破坏本仓库定制。
- 把「仓库文档根目录唯一」固化为 spec，防止再次照抄上游过期目录树而回潮。
- 把文档列表的文件夹优先级常量从 router 收敛到 `server/config.py`，使 `management.py` 与上游 `644fed0` 逐字对齐。
- 解除 `article-note` 的图片发布前置限制。

**Non-Goals：**

- 不引入上游 `documentation` skill（本仓库未采用该 skill，图片写作规范留在 `article-note` 与 spec 中）。
- 不改动 `docs-page-content` 既有 sidecar / TOC / 排序需求（收敛只挪常量位置，不改排序行为，故不动 spec）。
- 不补写历史文档的配图；本变更只提供能力。
- 不做图片压缩工具链（沿用 `article-note` 的 `figures.py`）。

## Decisions

### D1：逐文件对照移植，不用 cherry-pick

上游 `e505269` 触碰的四个代码文件中，`MarkdownRenderer.vue` 与 `management.py` 已与上游分叉，`server/main.py` 的 import/注册块不同。cherry-pick 必冲突，改为按上游 diff 逐段合入。

- 备选：`git cherry-pick e505269` — 冲突点正好落在我们的定制块附近，手工合并反而更慢且易丢定制，不采用。

### D2：`figure` 包装只在「整段单图」时生效

沿用上游实现：`paragraph_open` 时检查该段 inline 子节点，忽略空白文本后**恰好一个 image 且 alt 非空**才包 `<figure>`，否则走默认渲染。

- 理由：避免把「文字 + 行内小图」的段落误包成图块；无 alt 的图退化为裸 `<img>`。
- 备选：对所有 image 无条件包 figure —— 会产生空 `figcaption`，且打断行内图文混排，不采用。

### D3：资产目录以 `_` 前缀排除扫描，而不是维护排除列表

`get_docs()` 改为 `dirs[:] = [d for d in dirs if not d.startswith('_')]`。

- 理由：下划线前缀是通用约定，未来新增 `_drafts/` 等资产/草稿目录无需改代码。
- 风险：以下划线开头的**正文**目录会被静默跳过。当前 3 个内容目录（`knowledge/`、`论文笔记/`、`实习复盘/`）都不带下划线，无影响；在 spec 中记录该约定。

### D4：`repo-docs-structure` 单独立 capability，而不是塞进 `docs-page-content`

上游把该约束放在 `documentation` capability；本仓库没有 `documentation`（文档内容契约在 `docs-page-content`、布局在 `docs-page-layout`）。塞进 `docs-page-content` 会把「页面内容渲染」与「仓库目录结构」混为一谈。

- 决策：新建 `repo-docs-structure` capability 承载目录结构约束，后续结构类规则可继续归此。
- 备选：新建空壳 `documentation` 与上游对齐 —— 会与既有 `docs-page-content` 职责重叠，不采用。

### D5：`article-note` 解除限制而非删除说明

`SKILL.md` 的「前置条件」表述改为「文档图片端点就绪（`sync-projflow-round3` 之后）」，恢复标准 `figures.py publish` 流程；保留「端点未就绪时」的降级描述作为历史兜底，避免文档与实际能力再次脱节。

### D6：排序链与上游对齐 —— 领域常量收敛到 `config.py`

本仓库 `management.py` 的 `_doc_sort_key` 与上游 `644fed0` 逻辑等价，但文件夹优先级写死在 router 内。收敛步骤：

1. `server/config.py` 新增 `DOCS_FOLDER_ORDER = ['实习复盘', '论文笔记', 'knowledge']`，并沿用本仓库 config 既有的「下游库可覆盖」注释惯例（同 `OUTPUTS_DIR` / `TRAINING_DIR`）。
2. `server/routers/management.py` 删除本地 `_DOCS_FOLDER_ORDER`，改从 `server.config` 导入 `DOCS_FOLDER_ORDER`，`_doc_sort_key` 引用公开常量。

- 理由：上游是通用脚手架，默认只能为空；本仓库的目录顺序是**领域知识**，应由下游 config 注入。收敛后 `_doc_sort_key` 逻辑与上游一致，残余差异仅两处无害项（`import json` 行位置、一行本地 sidecar 注释），上游后续再改排序链可干净 cherry-pick。
- 备选：保持 router 内硬编码 —— 每次上游改动都要手工合并且长期分叉，不采用。
- 边界：三个内容目录（`实习复盘` / `论文笔记` / `knowledge`）之外新增目录时，改 config 一行即可，无需动 router。

## Risks / Trade-offs

- [`paragraph_open/close` 覆写与其他 markdown-it 插件冲突] 本仓库还用了 `markdown-it-task-checkbox` → 缓解：只在 `loneFigureImage` 命中时改返回；其余路径调用保存的 `defaultParagraphOpen/Close`，并实测任务列表与 Mermaid 仍正常。
- [静态挂载与 `/api` 代理路径重复前缀] Vite 已把 `/api` 代理到 8812 → 缓解：挂载点用 `/api/management/docs-assets`，与其它 `/api/management/*` 路由同前缀，无需改 Vite。
- [资产目录被文档列表扫到] → 缓解：`get_docs()` 排除下划线目录，spec 中有对应 Scenario。
- [`_assets` 目录为空导致 git 不跟踪] → 缓解：放 `.gitkeep`。
- [图片进 app 但体积失控] → 缓解：沿用 `article-note` 的 `figures.py inspect/publish`（≤500KB/图、≤5MB/篇），spec 不强制但 skill 强制。

## Migration Plan

1. 后端：`server/main.py` 加静态挂载；`management.py` 的 `get_docs()` 跳过下划线目录。
2. 前端：`MarkdownRenderer.vue` 加 image 规则与 figure 包装；`index.scss` 加样式。
3. 目录：新增 `management/docs/_assets/.gitkeep`。
4. Skill：`article-note/SKILL.md` 解除前置限制。
5. 排序收敛：`config.py` 新增 `DOCS_FOLDER_ORDER`；`management.py` 改为从 config 导入。
6. 校验：`openspec validate sync-projflow-round3 --strict`；后端启动 + `GET /api/management/docs` 不含资产且目录顺序稳定；前端实测 figure/figcaption 与任务列表。

回滚：删除 `server/`、`web/` 的对应片段与 `_assets/` 即可；无数据迁移，无 schema 变更。
