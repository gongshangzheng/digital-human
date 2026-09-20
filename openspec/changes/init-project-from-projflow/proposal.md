# Proposal: init-project-from-projflow（初始化 digital-human 仓库）

## Why

数字人方向（钉钉会议面试官数字人）的调研、笔记、评测与工程实践分散在四个信息源：ProjFlow（通用项目管理脚手架）、博客 gongshangzheng.github.io（~150 篇数字人相关页面）、InternWiki（tangwen 数字人知识库 26 篇 + junjiawang 语音 Agent 文档）、CyberVerse（实时数字人 Agent 框架优化 fork，含 Avatar Forcing 与 Ditto 等模型插件，已 clone 至 `~/code/CyberVerse`，远端 github.com/gongshangzheng/CyberVerse）。需要初始化一个统一仓库收拢这些资产，作为后续数字人研发的单一事实来源。

## What Changes

- **从 ProjFlow 拷贝共享脚手架**：`management/`（团队/日报/周报/文档）、`papers/`（论文搜集）、`evaluation/`（评测体系）、`server/`（FastAPI 8809）、`web/`（Vue3 3210）、`scripts/`、`start_services.sh`，改名为 digital-human 身份（README、端口沿用 8809/3210 避免与 pet/children-face 冲突需在 design 确认）
- **git init + 首次提交**：当前目录无版本控制
- **导入博客论文资产**：从 `~/gongshangzheng.github.io/src/pages/` 筛选数字人相关页面（论文精读 paper-*、工程解读 digital-human-*、源码分析、survey、arxiv-digest），提取元数据（title/tags/日期）转 Markdown 存入 `papers/data/`，经 `scripts/import_papers.py` 走 arXiv API 补全元数据入 SQLite
- **复制 InternWiki 数字人文档**：tangwen 的基础/模型精读/工程与评测/快速导读/微调与实践共 26 篇 + junjiawang 的 voice-agent-web 数字人相关文档，存入 `management/docs/digital-human/`（或知识库目录，design 定）
- **登记外部代码源**：以登记表方式锚定 CyberVerse（`~/code/CyberVerse` 独立 clone，记录远端 URL 与 commit），其 `models/`（avatarforcing / ditto / flash_head / MuseTalk / SoulX-LiveAct）、`management/docs/`（avatarforcing-design、ditto-design、streaming-pipeline、rtf 基准）与 `management/projects/digital-human/` 作为重要参考源纳入知识库索引；不在本仓库内重复 vendoring 代码
- **清理 ProjFlow 残留 demo 数据**：management/ 中与数字人无关的示例内容不引入
- **隐藏协作类管理模块**：团队成员、报告（日报/周报/月报）、里程碑、会议纪要等在前端菜单中隐藏（配置化 hidden 列表，路由保留，可随时恢复）；项目树、任务看板、文档保持可见

## Capabilities

### New Capabilities
- `project-scaffold`: 仓库目录结构、服务启动（FastAPI + Vue3）、git 版本控制与 README，从 ProjFlow 脚手架派生
- `paper-knowledge-base`: 数字人论文/笔记库——从博客与 InternWiki 导入的元数据驱动的论文库，含分类、检索、笔记
- `external-code-sources`: 外部代码源（CyberVerse / Avatar Forcing / Ditto）的登记、引入与版本记录规范

### Modified Capabilities
（无——全新仓库，无既有 spec）

## Impact
- 新建仓库全部内容；不修改任何上游仓库（ProjFlow / 博客 / InternWiki 均只读）
- 依赖本地工具：python3 + uvicorn、node/npx vite、sqlite3
- 博客导入为**复制**而非引用，后续以本仓库为论文笔记的演进主体
- CyberVerse 已在 `~/code/CyberVerse` 独立 clone，本 change 只做登记与索引，不复制其代码——不阻塞任何任务
