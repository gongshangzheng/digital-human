## Context

**素材源**：`~/gongshangzheng.github.io` 的 `AI/数字人` 子分类，已发布 99 篇：

| 类别 | 数量 | 内容形态 |
|---|---|---|
| 论文精读 | 67 | 单篇论文：问题 / 方法 / 实验 |
| 系列综述 | 19 | 横向专题：路线、实时性、身份、卡通、手部、后端 |
| 工程解读 | 10 | 源码 / 部署 / benchmark |
| 评测参考 + 产业入口 | 7 | VBench-2.0、OpenS2V-Nexus、产业图谱、hub |

**库内论文（本轮扩入）**：`management/docs/论文笔记/`（9 篇，如 face-vid2vid、float、vorch-streamer 为博客未覆盖的库内独有论文）、`技术介绍/`（face-verification-models、dpo 等）、`knowledge/` 中的单篇论文精读。与博客篇目去重后并入同一套 `papers` 条目；库内独有论文的 `blog_url` 可为空，`note` 指向库内笔记。

另有约 20 篇草稿（`drafts/*.org|md`）。已有 `papers/data/blog_papers.json`（131 条，11 条 deny）与 `data/papers.db`（118 条），抽取了 `slug/title/date/arxiv_id/category`，但**没有机构字段，也没有「问题-解法」对**。机构/venue 部分藏在文章 frontmatter 的 `hero_sub`：实测 85/99 有 `hero_sub`，其中 53 篇带会议/期刊、50 篇带机构，近半需从正文补。

**库内现状**：`management/docs/数字人概述/` 已有 10 篇第一方文档（order 10–90），但都是散文，**没有任何结构化数据文件**，文档里也没有由数据驱动的表格。文档页现有同名 sidecar JSON 机制（`<slug>.json`，承载 `changelog/progress/appendix/related`），开发模式由 FastAPI 详情接口返回，生产构建由 `build-docs-data.mjs` 注入 `docs-data.json`——**这是一条现成的「配套 JSON + 随文档取数」通道**。

**用户诉求（本轮修订）**：

1. 每篇文章 = 一条**「问题 → 解法」对**，作为最小结构单元；
2. 生成**配套 JSON** 记录这些信息对，并把标题、作者等元信息写进同一结构单元；
3. 文档里给一张**表格，实时按 JSON 内容展示**这些论文信息；
4. JSON 里提供**论文笔记的位置**，把重点文章引向详细解读。

**本轮为提纲待审阶段，未写任何正文或代码。**

## Goals / Non-Goals

**Goals**

- 定义稳定的**论文信息对数据结构**，一篇文章 = 一条记录，字段自解释、可增量扩条目。
- 落盘**配套 JSON**，作为文档表格的唯一数据源；JSON 更新后表格内容随之更新，无需手改文档。
- 文档内**数据驱动表格**：可排序、可按方法族筛选，含「笔记」列链接到库内精读或博客原文。
- 产出**一篇完整文档**：关键技术分线（问题 → 方法族 → 代表工作【机构·时间】 → 边界）+ 演进时间线 + 机构分布 + 关键问题补充。
- 开发/生产**渲染一致**：开发读 FastAPI 详情接口的 sidecar，生产读构建期注入的同等数据。
- 与既有文档**分工不重复**。

**Non-Goals**

- 不复制 99 篇精读正文；表格是索引，笔记列指向详细解读。
- 不新增模型实验、不改论文精读与 `knowledge/` 文件。
- 不引入数据库/后端新接口（sidecar 透传已存在）。
- 不重复《数字人领域问题》六章已有的结论数字。
- 不追求「每篇都写一段」——低信息密度文章只进 JSON/表格。

## Decisions

### 1. 核心数据单元：问题-解法对（JSON schema）

一篇文章 = 一条记录。字段（`papers[]` 的元素）：

| 字段 | 类型 | 含义 | 来源 |
|---|---|---|---|
| `id` | string | 稳定短 id（用博客 slug） | 语料 |
| `seq` | int | 展示序号 | 抽取时生成 |
| `title` | string | 论文原题（英文优先） | frontmatter/正文 |
| `title_zh` | string | 精读标题（中文） | frontmatter `title` |
| `authors` | string[] | 论文作者（可空） | 正文参考文献 |
| `institution` | string | 发布机构/团队 | `hero_sub` → 正文；缺失 `null` |
| `venue` | string | 会议/期刊或 arXiv | `hero_sub` → 正文；缺失 `null` |
| `year` | int\|null | 发表年份（arXiv v1 或会议年） | `hero_sub`/arXiv |
| `blog_date` | string | 博客精读发布日 | frontmatter `date` |
| `qa` | array | **问题-解法对列表**，每项 `{question, answer}`；一篇文章可有多条 | 正文提炼 |
| `method_family` | string | 方法族标签（用于筛选） | 抽取时归类 |
| `blog_url` | string | 博客原文链接 | 生成 |
| `note` | string\|null | **论文笔记位置**：库内文档 slug 或外链 | 人工/映射 |
| `note_type` | enum | `doc` / `blog` / `null` | 生成 |
| `derives_from` | string[] | **继承/派生自**：所借鉴、改造或扩展的代表工作（名称或 slug） | 正文提炼 |
| `derived_by` | string[] | 被哪些后续工作继承/改造（可空） | 正文提炼 + 反向补全 |
| `tags` | string[] | 标签 | frontmatter |

示例：

```json
{
  "id": "paper-vasa1",
  "seq": 5,
  "title": "VASA-1: Lifelike Audio-Driven Talking Faces Generated in Real Time",
  "title_zh": "数字人论文精读（五）：VASA-1，512×512 实时生成的整体面部动力学",
  "authors": [],
  "institution": "Microsoft Research",
  "venue": "NeurIPS 2024 (Oral)",
  "year": 2024,
  "blog_date": "2026-06-04",
  "qa": [
    {
      "question": "音频驱动的说话人脸如何在保证表现力的同时做到实时？",
      "answer": "把脸部动力学建模到隐式运动空间，用扩散/自回归生成 motion latent，再经 3D 感知渲染，512×512 达 40FPS。"
    },
    {
      "question": "长视频中如何维持身份与运动的一致性？",
      "answer": "在运动空间而非像素空间解码，配合显式 3D 先验约束，减少逐帧漂移。"
    }
  ],
  "method_family": "motion-space-diffusion",
  "blog_url": "https://gongshangzheng.github.io/paper-vasa1.html",
  "note": "数字人概述/数字人动作",
  "note_type": "doc",
  "derives_from": [],
  "derived_by": ["LivePortrait"],
  "tags": ["数字人", "实时", "talking-face"]
}
```

- **`qa` 口径**：一篇文章可含**多条**问题-解法对——文章提出多个问题时，每个问题各一条。粒度按裁决取「关键文章多句、次要一句」：有库内笔记的重点文章 `question`/`answer` 各可 2–3 句，其余一句。`question` 是文章自己提出的核心问题（不是泛泛的领域问题）；`answer` 是它给出的主要技术解法；不复制原文长段。
- **`derives_from` 口径**：每条技术分线同时用一行 `A ← B` 标出继承箭头，并在「技术谱系与继承关系」章用 Mermaid 汇总。
- **时间口径**：`blog_date` 与 `year` **分列**，不混为一个「时间」；时间线用 `year`。
- **作者**：`authors` 为论文作者，缺失时留空数组（不编造）；文档 frontmatter 的 `author` 是精读作者，属另一层，不入此表。
- **`note` 只对重点文章填**：映射到 `management/docs/` 下已有的详细笔记（如 `数字人概述/数字人动作`、`论文笔记/ditto`、`knowledge/...`）或博客原文；无对应则 `null`。
- **继承关系（族谱）**：`derives_from` / `derived_by` 记录技术谱系。口径是「明确借鉴或扩展了哪个前作的方法」，例如 LivePortrait 继承 Face vid2vid 的隐式关键点迁移、Ditto 承接运动空间扩散、Hallo3 承接 Hallo / 视频 DiT、LatentSync 承接 SyncNet。只记录语料中确有依据的关系，不做推测；`derived_by` 可由后续条目反向补全。谱系同时以 Mermaid 图在文档中专门呈现（见 §5）。

### 2. 配套 JSON 的位置（待用户裁决）

- **方案 A（推荐）· 同名 sidecar**：数据写入文档的 `<slug>.json` 的 `papers` 字段。
  - 理由：sidecar 已是「配套 JSON + 随文档取数」的既有通道；开发由 FastAPI 每请求读文件（真正实时），生产由 `build-docs-data.mjs` 注入 `docs-data.json`；**零后端改动、零新增取数路径**，且 `docs-page-content` 已有 sidecar 契约可扩展。
- **方案 B · 独立资产**：数据写入 `management/docs/_assets/<slug>/papers.json`，前端经 `/api/management/docs-assets/`（开发）/ `docs-assets/`（生产）fetch。
  - 理由：JSON 更显眼、与 sidecar 语义解耦；代价是新增前端 fetch + 生产 URL 解析，且要确认 FastAPI 资产通道可服务 `.json`。
- 两者都满足「配套 JSON + 表格随数据更新」；差别在改动面与可发现性。

### 3. 表格渲染架构（dev/prod 一致）

- **占位标记**：文档正文放置 `<!-- papers-table -->`。该标记被前端识别并从正文中剥离，不会渲染成可见文本。
- **渲染点**：`DocPage.vue` 把 `bodyContent` 按标记切成若干段，标记处渲染新的 `PaperTable` 组件，其余段仍交给 `MarkdownRenderer`；这样表格是真正的 Vue 组件（可排序/筛选），不依赖 `v-html` 注入。
- **组件**：新增 `web/src/components/common/PaperTable.vue`
  - props：`papers: Array`；
  - 表格以**问题-解法对为行**（一篇文章有多条 `qa` 时占多行，论文/机构/时间列按论文分组展示，避免重复）；列含：论文 / 发布机构 / venue·年份 / 提出的问题 / 解法 / 继承自 / 笔记；
  - 交互：列排序（Naive UI `n-data-table` sorter）、按 `method_family` 筛选、行内展开查看完整 `answer`；
  - 笔记列：`note_type === 'doc'` → 站内 `/management/docs/<note>`；`blog` → 新窗口外链；`null` → 占位「未建」。
- **取数**：表格数据取自当前文档的 sidecar（方案 A）或 fetch 的资产（方案 B）；开发/生产两条路径必须渲染一致（写进 spec）。
- **空态**：文档无 `papers` 或为空时，不渲染表格区块。

### 4. 落点、标题与 order（待用户裁决）

- **落点**：
  - **A（推荐）** 新建 `management/docs/数字人概述/数字人关键技术地图.md`（与既有概述文档同链）。
  - B 新建到 `management/docs/knowledge/`（外部复制件风格）。
  - C 不新建，扩写现有两篇。
- **标题**：A（推荐）`数字人关键技术地图：问题、方法与来源`；B `数字人关键技术全景（2020—2026）`；C `数字人关键技术综述：99 篇文献的问题—方法—机构索引`。
- **order**：推荐 `docs_order.py insert management/docs/数字人概述 --after 数字人介绍与技术路线`，不改既有 order。
- **篇幅**：约 300–450 行；正文以分线小节 + 表格为主。

### 5. 文档完整二级章节结构（供审核）

**前言与方法**
- `## 这份地图回答什么`：一段定位 + 与既有四篇文档的分工表 + 表格交互说明（排序/筛选/笔记列）。
- `## 语料与方法`：99 篇构成表、时间跨度、信息对抽取口径、`blog_date` 与 `year` 的区别、缺失项处理（`hero_sub` 优先，正文补，补不到标「未标注」）。

**问题空间**
- `## 关键任务与问题空间`：身份 / 动作 / 实时性 / 条件与任务定义四块，及其下有竞争的技术线。

**关键技术地图（主体，13 条分线）**
每条线统一写：`问题 → 方法族 → 代表工作（机构 · venue/时间） → 边界`。
1. `### 音唇同步与视频配音`
2. `### 2D 肖像动画与运动空间`
3. `### 隐式关键点与可控动画`
4. `### 3D 头像：NeRF / 3DGS / 参数模型`
5. `### 扩散基模与整帧 / 全身生成`
6. `### 实时流式、自回归与蒸馏`
7. `### 动作生成：口型 / 表情 / 手势 / 听态 / 全身`
8. `### 身份表示与身份一致性`
9. `### Agent 化与后端系统`
10. `### 工程化、加速与部署`
11. `### 评测、数据集与度量`
12. `### 风格化、卡通与跨域`
13. `### 产业与产品图谱`

**横向汇总**
- `## 技术谱系与继承关系`：专门呈现工作之间的继承/派生，配 Mermaid 族谱图（如 Face vid2vid → LivePortrait、Hallo → Hallo3、Wav2Lip → MuseTalk/LatentSync、SadTalker → 运动空间扩散族），并把关键继承点用一句话说明「继承了什么、改了什么」。
- `## 演进时间线（2020—2026）`：按阶段给「突破点 → 代表工作 → 机构」，配 Mermaid。
- `## 机构与团队分布`：主要机构表（机构 / 代表工作 / 方向）+ 高校 vs 工业界、国内 vs 海外观察。

**问题补充**
- `## 关键问题补充`：候选条目（见 §7），每条含「为什么关键 / 现有解到哪一步 / 还缺什么 / 语料证据」，标注是否建议回流《数字人领域问题》。

**数据表**
- `## 论文信息对总表`：正文只放一行 `<!-- papers-table -->`，表格由配套 JSON 渲染。

**附录**
- `## 附录 A：抽取方法与未获取项`：抽取流程、字段口径、未标注/未核实项清单。

### 6. 抽取流程（三条 lane）

- **lane 1 · 结构化元数据**：解析 `src/pages/*.html` 与 `drafts/*` 的 frontmatter（`hero_sub`/`date`/`tags`/`title`），合并 `blog_papers.json` 与 `papers.db` 的 arXiv/category，去重得到 99（+草稿）条骨架。
- **lane 2 · 问题-解法提炼**：逐篇读正文，抽 `question / answer / method_family`；99 篇分 6–8 批处理（可用 subagent 并行，保持单一写入者）。
- **lane 3 · 机构/时间/笔记补全**：对缺 `hero_sub` 的约 50 篇补 venue/机构；`note` 按库内已有笔记映射；无则 `null`。
- 产出 `papers` 数据写入配套 JSON；抽到的骨架先落 `.cache/docs-dh-key-technology-map/skeleton.json` 供复核。
- 是否提交一个**可复跑的抽取脚本**（`scripts/collect_dh_paper_units.py`）取决于裁决——推荐提交，使 JSON 可增量重生成。

### 7. 「关键问题补充」候选清单（待裁决取舍）

| # | 候选问题条目 | 语料证据 | 是否已在《领域问题》 |
|---|---|---|---|
| 1 | 说话风格与情绪的连续可控（强度轴） | StyleTalk++ / CapTalk / MEAD | 部分 |
| 2 | 听态与双向交互 | UniLS / OmniMate / DyStream | 部分 |
| 3 | 全双工流式因果性与首帧/持续延迟权衡 | Wan-Streamer / Avatar Forcing / LeapTalk | 部分 |
| 4 | 动作表示（motion latent）的可解释与可编辑 | Ditto / LIA-X / VASA-1 | 未收口 |
| 5 | 少步/单步蒸馏后的质量—速度边界 | LeapTalk / FlashHead / SoulX-LiveAct | 未收口 |
| 6 | 长时身份漂移的起始时刻与加速度刻画 | Avatar Forcing / MoFE / FCB | 已有专章 |
| 7 | 评测与人类感知脱节 | THEval / 4DHumanQA / VBench-2.0 | 部分 |
| 8 | 数据集与授权合规作为发布前门槛 | MEAD / GenEAva | 已有 |
| 9 | 端侧 / 纯 CPU 实时作为独立约束 | LiteAvatar / Ultralight | 未收口 |
| 10 | 多人 / 双人对话的身份归属 | HunyuanVideo-Avatar / DyStream | 未收口 |
| 11 | 手部与全身协调的动作层级 | 手部生成专题 / EMO2 / One Shot One Talk | 部分 |
| 12 | 跨机位 / 多视角外观一致性 | MoFE / UIKA | 部分 |
| 13 | 文本驱动 / 语义动作 | CapTalk / SentiAvatar / tool-augmented | 未收口 |
| 14 | 3DGS 单图泛化的可靠性边界 | LAM / AniGS / LHM / MATCH | 部分 |
| 15 | Agent 工具调用与全模态对话 | Ex-Omni-2D / EMO-Avatar / SmartAvatar | 部分 |

裁决项：(a) 全部写入本文档；(b) 只写未覆盖的 1–5/9/10/13，其余回流；(c) 只提交清单。

### 8. 与既有文档的分工

| 文档 | 职责 | 本文档处理 |
|---|---|---|
| 数字人介绍与技术路线 | 概念、路线、两因素 | 只引用路线命名，不重述定义 |
| 数字人领域问题 | 六章问题清单 | §5 只提交候选补充，经裁决后回流 |
| 数字人身份 / 动作 / 加速 | 项目自身实测 | 不复述其数字，笔记列以 slug 指向 |
| knowledge/ | 外部复制件 | 只作证据源，不修改 |

## Risks / Trade-offs

- [语料量大，逐篇提炼昂贵] → 先结构化元数据（全量），再分批提炼 `question/answer`；低信息密度文章只进表格。
- [机构字段缺失近半] → 三级来源回退（`hero_sub` → 正文 → 书目库），仍缺标 `null`/「未标注」，不编造；覆盖率写进附录 A。
- [sidecar 变大] → `papers` 进 `docs-data.json`，体积随条目线性增长；99 条量级可接受；若后续膨胀再拆独立资产（方案 B）。
- [与既有文档重复] → 分工表约束；只做「问题→方法→机构」横向层。
- [前端改动引入回归] → 只切分 `bodyContent` 并新增组件，不动 `MarkdownRenderer` 既有规则；spec 增加空态与 dev/prod 一致性场景；交付前手工验证开发与生产两条路径。
- [时间口径混用] → `blog_date` 与 `year` 分列。
- [`note` 映射主观] → 只对确有库内笔记的文章填写，其余留 `null`，不做模糊匹配。

## Migration Plan

1. **用户审核 design**：裁决 JSON 位置（A sidecar / B 资产）、落点（A/B/C）、标题、覆盖范围、关键问题补充落点、是否提交抽取脚本。
2. 跑 lane 1 得骨架 → 用户确认字段口径。
3. 跑 lane 2/3 得 `papers` 数据。
4. 实现前端（`PaperTable.vue` + `DocPage` 标记解析），扩展 `docs-page-content` delta。
5. 写正文与附录；用 `docs_order.py insert` 落 order（若选落点 A）。
6. 校验：frontmatter、站内链接、Mermaid、表格域一致、开发/生产两条渲染路径、`openspec validate --strict`。
7. 回滚：删除新文档 + 配套 JSON（或还原 sidecar）+ 新组件与 DocPage 改动，无数据影响。

## Resolved Decisions（逐题裁决）

| # | 事项 | 结论 |
|---|---|---|
| 1 | JSON 位置 | **A · 同名 sidecar `<slug>.json` 的 `papers` 字段**（开发模式 FastAPI 每请求读文件；生产由 `build-docs-data.mjs` 注入；零后端改动） |
| 2 | 文档落点 | **A · 新建 `management/docs/数字人概述/数字人关键技术地图.md`**，用 `docs_order.py insert --after 数字人介绍与技术路线` 占相邻空位，不改既有 order |
| 3 | 标题 | **D · 《数字人关键技术谱系：问题、解法与继承关系》**（文件名 slug 仍为「数字人关键技术地图」，标题与文件名不必强一致） |
| 4 | 覆盖范围 | **A · 99 篇已发布全收；并扩入库内已有论文**（`论文笔记/`、`技术介绍/`、`knowledge/` 中博客未覆盖的单篇论文，如 Face vid2vid、float、vorch-streamer）；去重后同一套 `papers` 条目；库内独有论文 `blog_url` 可为空、`note` 指向库内笔记 |
| 5 | Q/A 粒度 | **C · 关键文章多句、次要一句；一篇文章可含多条 `qa`，有多个问题就列多条** |
| 6 | 关键问题补充落点 | **A · 全部写进本文档 `## 关键问题补充` 章**；不动《数字人领域问题》，后续需要时再单独回流 |
| 7 | 抽取脚本 | **A · 提交 `scripts/collect_dh_paper_units.py`**：扫博客 frontmatter + 库内笔记生成骨架并增量合并；`qa`/`derives_from` 仍由人/Agent 提炼 |
| 8 | 表格交互 | **A · 列排序（年份/机构/标题）+ 按方法族筛选 + 关键词搜索 + 分页**（Naive UI `n-data-table`）；谱系聚焦交互后置 |

**八项裁决已全部完成，design 定稿。** 待用户明确批准后，按 tasks 进入实施（`openspec-apply-change`）。
