# Design: init-project-from-projflow

## Context

- 目标仓库 `~/code/digital-human` 当前为空目录（仅有刚初始化的 `openspec/` 与 `.pi/`），无 git、无代码。
- 本机 ProjFlow 生态现状（探索结论）：
  - **ProjFlow**（`~/code/ProjFlow`）：上游脚手架。Vue3 + Vite + Naive UI / FastAPI / Markdown + SQLite，端口 8809/3210，含 management / papers / evaluation 三模块与共享脚手架层（`[shared]` 变更需 port 回上游，见其 openspec change `docs-system`）。
  - **children-face**（`~/code/children-face`）：ProjFlow 直接拷贝的下游，端口尚未改（仍 8809/3210，与 ProjFlow 冲突——反例，印证"拉取后必须换端口"）。
  - **pet-action-recognition**（pet 服务器）：下游，端口 8788/3000。
  - **CyberVerse**（`~/code/CyberVerse`，远端 github.com/gongshangzheng/CyberVerse，GPL v3）：实时数字人 Agent 框架优化 fork，同样是 ProjFlow 管理体系下游（任务树 t10 "ProjFlow [shared] 变更同步" active）。三服务：Python inference gRPC :50051（ASR/LLM/TTS/avatar 插件进程内运行）+ Go orchestrator :8080 / TURN :8443 + Vue 前端 :5173，运行于远程 GPU 服务器（47.110.95.197），本地仅编辑。Avatar 模型层 `models/`：avatarforcing（LIA 系 flow matching，双向听说）、ditto（HuBERT→LMDM→六级渲染，TRT fp16，RTF 3→0.9）、flash_head、MuseTalk、SoulX-LiveAct。`management/docs/` 有 6 篇设计总纲（avatarforcing-design、ditto-design、streaming-pipeline、paste-back-compositing、silent-avatar-feed-gate、avatar-rtf-latency-over-time）。`management/projects/digital-human/` 是 **dh-eval 数字人评测框架**的任务树（t1 Web UI 三页面 React→Vue 采用 ProjFlow 架构已完成）。
  - 本机已监听端口（排除项）：3000 3210 5000 5210 7000 7265 8788 8809 8810 …
- 知识源：
  - **博客**（`~/gongshangzheng.github.io`）：`src/pages/` 下 ~156 个数字人相关 HTML 页面（YAML frontmatter + 正文），含论文精读（paper-wav2lip、paper-vasa1…）、工程解读（digital-human-*）、源码分析、survey、arxiv-digest 系列；`raw/` 有论文源文件与图。
  - **InternWiki**（`~/code/InternWiki`）：tangwen 数字人知识库 26 篇（基础/模型精读/工程与评测/快速导读/微调与实践，含《CyberVerse 工程专题》）+ digital-human 项目 notes + junjiawang voice-agent-web 系列文档。Markdown + frontmatter。

## Goals / Non-Goals

**Goals:**
- 一个可运行（新端口）、可版本控制、身份正确的 digital-human 仓库
- 论文/知识资产从博客与 InternWiki **复制**入本仓库，成为后续演进主体
- 外部代码源（CyberVerse 等）登记 + commit 锚定，不 vendoring
- 引入过程全部脚本化、可重跑、可复核

**Non-Goals:**
- 不迁移/复制 CyberVerse 任何代码（models/、inference/、server/ 留在原仓库）
- 不做 dh-eval 评测框架的功能开发（若要把 CyberVerse 内 digital-human 项目树收拢成独立评测平台，另开 change）
- 不做博客/InternWiki 的反向同步（导入后上游即冻结为历史源）
- 不引入 ProjFlow demo 成员数据

## Decisions

### D1: 初始化方式 = rsync 式拷贝 + 定点改名（非 git subtree / 非 fork）

`rsync -a --exclude` 从 `~/code/ProjFlow` 拷贝 `management/ papers/ evaluation/ server/ scripts/ web/ start_services.sh .gitignore` 等，排除 `data/*.db`、`node_modules/`、`__pycache__/`、`.git/`、openspec/。
理由：ProjFlow 各下游（children-face、CyberVerse management、pet-action-recognition）均为拷贝派生；fork/subtree 会把上游 git 历史与 demo 历史一起带入，且 children-face 先例证明纯 `cp` 也可接受，但 rsync 排除更干净。
备选：git subtree（溯源好但历史污染、命令复杂，团队无此惯例）——不采用。

### D2: 端口 = 后端 8812 / 前端 3212（已实测空闲，固定不变）

生态端口分配：ProjFlow 8809/3210、pet-action-recognition 8788/3000、本机已占用 8810/5210/7265 等。**本仓库固定使用后端 8812、前端 3212**（已用 lsof/nc 实测空闲），写入 `start_services.sh` 头部端口分配注释：`后端=8812 前端=3212`。改点：`start_services.sh`、`web/vite.config.js`（若有硬编码）、`server/config.py`（若有硬编码）、README。`start_services.sh` 自带的 check_port_conflict 保留作为运行时兑底（若未来被占则报错退出，人工顺延并更新注释）。

### D3: 博客导入 = 关键词 + 文件名模式命中 → 中间 JSON（含命中原因）→ 人工复核 denylist → frontmatter 提取 → Markdown 化

两阶段脚本（放 `scripts/`）：
1. `extract_blog_papers.py`：扫描博客 `src/pages/*.html`，按关键词（talking head/avatar/digital human/数字人/audio-driven/lip sync…）与文件名模式（`paper-*`、`digital-human-*`、`*survey*`、`arxiv-digest-*`、`*talk*`、`*avatar*`）打分，输出 `papers/data/blog_papers.json`（slug、title、tags、date、相对路径、命中原因、denylist 字段）。
2. 复核后 `import_papers.py`（改造 ProjFlow 原脚本）：从 JSON 提取 arXiv id → arXiv API 补全 → 写 SQLite（沿用 ProjFlow 表结构）；正文 HTML 转 Markdown 摘要（正文大段 HTML 保留原文引用链接，不做全文转换——精读笔记的演进在本仓库另行进行）。

理由：156 个命中里必然有误命中（php-security 等弱关键词页），必须有人工复核闸门；arXiv 补全逻辑 ProjFlow 已验证。
备选：全文 HTML→Markdown 转换（html2text）——正文是高度定制 HTML 结构，转换质量差维护成本高，不采用；仅存元数据 + 链接。

### D4: 知识库文档 = 复制到 `management/docs/knowledge/`，按来源分子目录

- `management/docs/knowledge/internwiki/`（tangwen 26 篇按原有分类子目录 + junjiawang voice-agent 系列 + digital-human project notes）
- `management/docs/knowledge/blog/`（精选 survey/工程解读类**文档型**页面，与论文元数据互补；仅收设计/综述类，论文单篇不复制正文）
- 顶层 `management/docs/knowledge/README.md`：索引表（来源仓库、原路径、复制日期、commit/快照标识）

理由：management/docs 是 ProjFlow 体系文档的自然位置（CyberVerse 同款用法）；不进 papers/（那是论文元数据库）。
备选：独立 `knowledge/` 顶层目录——破坏 ProjFlow 结构同构性，不采用。

### D5: 外部源 = 登记表 + commit 锚定，CyberVerse 保持独立 clone

`docs/external-sources.md`（仓库顶层 docs/，非 management）：每源记录远端 URL、本机路径、用途、锚定 commit、引入方式。CyberVerse 条目锚定当前 HEAD（4968280），并列出被知识库索引的关键路径（models/*、management/docs/*、management/projects/digital-human/）。
理由：CyberVerse 是活跃开发库（perf 系列提交持续推进），vendoring/submodule 都会把同步成本引入本仓库；它已在 `~/code/CyberVerse` 独立存在，登记 + 锚定即可复现。

### D6: 分类体系六类（paper-knowledge-base spec）

`2d-talking-head` / `3d-avatar` / `audio-driven-animation` / `realtime-system` / `evaluation-dataset` / `survey`。博客 tags 与 arXiv 分类映射到该集合，映射不了的先归 `survey` 或人工指定（导入 JSON 中留 category 字段人工可改）。

### D7: 模块隐藏 = 前端配置化 hidden 列表（菜单过滤，路由保留）

ProjFlow 菜单硬编码在 `web/src/layouts/MainLayout.vue` 的 `menuOptions`。新增 `web/src/config/menu.js`（或同层配置文件）：导出 `HIDDEN_MENU_KEYS` 数组（默认 `['/management/team', '/management/reports', '/management/milestones', '/management/meetings']`），MainLayout 生成 menuOptions 后按 key 过滤（含父级 children 为空时折叠父级自身）。路由表不动（URL 直达可用，便于后续恢复）；后端 management 路由不动；首页如有模块入口卡片同步过滤。
理由：单人多角色研发仓不需要团队协作门面，但知识库（docs）、项目树、任务看板仍在 management 体系内使用；删路由/后端会破坏与 ProjFlow [shared] 脚手架的同构性，未来同步成本高。
备选：直接删除菜单项与路由——不可逆且偏离共享脚手架，不采用。

## Risks / Trade-offs

- [端口未来被新服务占用] → 端口固定为 8812/3212 并写入头部注释；check_port_conflict 兑底报错，人工顺延时同步更新注释与文档
- [博客误命中/漏命中] → 命中原因留痕 + denylist 人工复核；漏命中靠 arxiv-digest 内条目二次捞取（digest 页内含大量论文，本期只导页面级，digest 条目级拆解列为后续 change）
- [arXiv API 限流/不可达] → 分批 + 失败标记 + 重试命令幂等
- [ProjFlow 拷贝带入隐藏 demo 数据（team/ 报告/评测配置）] → 拷贝后逐目录清点，management/team 仅留 README 模板
- [知识库复制后双源漂移（InternWiki 继续更新）] → 索引登记快照 commit；复制即声明本仓库为演进主体，上游冻结
- [GPL v3 传染（CyberVerse LICENSE）] → 本仓库只登记引用不复制其代码，无传染风险；若未来 vendoring 需重新评估 license 兼容

## Migration Plan

全新仓库，无存量迁移。回滚 = 删除工作树重开（openspec/ 已在 git 外单独存在则保留）。

## Open Questions

- dh-eval 评测框架（CyberVerse `management/projects/digital-human/` 任务树所指向的平台）是否在后续 change 中收拢进本仓库独立建设？——不阻塞本 change，待用户决策
- 博客 `raw/` 下论文源文件（LaTeX/图）是否同步复制？体积与用途待定，本期只登记不复制
