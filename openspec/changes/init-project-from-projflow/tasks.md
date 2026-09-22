# Tasks: init-project-from-projflow

## 1. 脚手架拷贝与改名（project-scaffold）

- [x] 1.1 rsync 拷贝 ProjFlow 的 `management/ papers/ evaluation/ server/ scripts/ web/ start_services.sh .gitignore AGENTS.md`，排除 `.git/ data/*.db node_modules/ __pycache__/ openspec/`
- [ ] 1.2 端口改为 8812/3212：`start_services.sh`（含头部注释 `端口分配：后端=8812 前端=3212`）、`web/vite.config.js`、`server/config.py`、前端 API base、README 中所有出现处
- [ ] 1.3 身份改名：README 标题/描述改为 digital-human（数字人研发管理平台），全局搜索清除 ProjFlow demo 字样（保留架构性引用如"基于 ProjFlow 脚手架"）
- [ ] 1.4 清理 demo 数据：`management/team|daily|weekly|monthly`、`evaluation/models|datasets|results` 中的 ProjFlow 示例内容清空（保留 template 与 README）
- [x] 1.5 新增 `web/src/config/menu.js` hidden 列表（默认隐藏团队成员/报告/里程碑/会议纪要），MainLayout 菜单按其过滤，首页模块入口同步过滤；验证隐藏模块 URL 直达可用、从列表移除后菜单恢复
- [x] 1.6 `git init` + 首个 `.gitignore` 校验（覆盖 db/node_modules/__pycache__）+ 首次提交

## 2. 外部源溯源（external-code-sources）

> 修订（2026-09-22）：原设计在仓库根目录建 `docs/external-sources.md` 独立登记表；后确认与上游 ProjFlow 废弃根目录 `docs/` 的既定约定冲突（`83c78fb`），且信息与知识库索引重复。改为溯源信息并入 `management/docs/knowledge/README.md`，删除该文件与根目录 `docs/`。

- [x] 2.1 建立外部源溯源：四源（CyberVerse、ProjFlow、博客、InternWiki）的来源、引入方式与快照/锚定 commit —— 记录位置由 `docs/external-sources.md` 改为知识库索引 `management/docs/knowledge/README.md`
- [x] 2.2 CyberVerse 的 `management/docs/` 6 篇设计文档与 `management/projects/digital-human/tasks.json` 的 commit 锚定
- [x] 2.3 把 CyberVerse 锚定 commit（`4968280`）与关键索引路径（`models/*`、`management/docs/*`、`management/projects/digital-human/`）并入 `management/docs/knowledge/README.md` 的来源表
- [x] 2.4 删除 `docs/external-sources.md` 与仓库根目录 `docs/`（`git rm` + 确认 `test ! -d docs`）
- [x] 2.5 更新引用：`README.md`（第 12、26 行）、`AGENTS.md`（第 7、134 行）、`management/docs/knowledge/README.md`（第 3 行）
- [x] 2.6 删除 `AGENTS.md` 目录树中过时的根目录 `docs/` 条目（与上游 `[shared]` change `fix-agents-docs-tree` 同款修订）
- [x] 2.7 删除废弃 change `openspec/changes/docs-external-sources-slim`（登记表既已移除，瘦身提案作废）

## 3. 博客论文资产导入（paper-knowledge-base）

- [x] 3.1 编写 `scripts/extract_blog_papers.py`：扫描博客 `src/pages/*.html`，关键词 + 文件名模式打分，输出 `papers/data/blog_papers.json`（slug/title/tags/date/路径/命中原因/category 待填）
- [x] 3.2 人工复核 JSON：denylist 排除误命中（如 php-security），为每条填六类分类（2d-talking-head / 3d-avatar / audio-driven-animation / realtime-system / evaluation-dataset / survey）
- [x] 3.3 改造 `scripts/import_papers.py`：读取复核后 JSON，提取 arXiv id，调 arXiv API 分批补全（失败标记可重试），写 SQLite（沿用 ProjFlow papers 表结构与 API）
- [x] 3.4 验证：`bash start_services.sh` 后前端论文页可见导入条目，分类筛选、收藏、笔记功能可用

## 4. InternWiki 知识库复制（paper-knowledge-base）

- [x] 4.1 复制 tangwen 数字人文档 26 篇（基础/模型精读/工程与评测/快速导读/微调与实践）到 `management/docs/knowledge/internwiki/`，保留原分类子目录
- [x] 4.2 复制 junjiawang voice-agent-web 系列与 tangwen digital-human 项目 notes（README/tasks.json/3dgs-methods-research/hardware-assessment）
- [x] 4.3 精选博客文档型页面（survey/工程解读，与论文元数据互补）复制到 `management/docs/knowledge/blog/`
- [x] 4.4 编写 `management/docs/knowledge/README.md` 索引：每条登记来源仓库、原路径、复制日期、来源 commit

## 5. 验证与收尾（project-scaffold）

- [x] 5.1 一键启动验证：`bash start_services.sh`，确认 8812/3212 正常、与 ProjFlow/pet-action-recognition 并存无冲突、`/api/health` 正常
- [x] 5.2 规范检查：`npm run check`（web/ 内若有）、Python 语法检查 server/ scripts/
- [x] 5.3 最终提交并运行 `openspec validate init-project-from-projflow` 通过
