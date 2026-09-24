## 1. 设计审核与口径确认

- [x] 1.1 ✅ 用户逐题裁决完成（见 design `## Resolved Decisions`）：JSON 位置 A、落点 A、标题 D、语料含库内论文、Q/A 粒度 C（一篇文章可多条 qa）、问题补充写进本文档、提交抽取脚本、表格交互 A。
- [x] 1.2 ✅ 已核对与既有文档分工：本文只做「问题-解法-机构-谱系」横向层，不重述定义与实测数字。
- [x] 1.3 ✅ 确认 `papers` 字段口径与「未标注/未建」标记方式。

## 2. 语料检索与结构化抽取（lane 1）

- [x] 2.1 ✅ 扫博客 `AI/数字人` 得 100 条页面（去重后并入 99）。
- [x] 2.2 ✅ 合并 `blog_papers.json` 与 `papers.db`（arXiv 编号 / category / 作者）。
- [x] 2.3 ✅ 解析 frontmatter `hero_sub` 得 venue / 机构 / 年份。
- [x] 2.4 ✅ 不纳入草稿（裁决：99 已发布 + 库内论文），故无 `[draft]` 条目。
- [x] 2.5 ✅ 骨架落盘 `.cache/docs-dh-key-technology-map/skeleton.json`（106 条）。

## 3. 问题-解法对与元信息补全（lane 2/3）

- [x] 3.1 ✅ 6 批并行抽取 `question`/`answer`/`method_family`，共 157 组问题-解法对，106/106 有 qa。
- [x] 3.2 ✅ 对缺失项跑单独 lane 补机构/venue/年份（补 24 条机构）。
- [x] 3.3 ✅ 作者从 `papers.db` 补 63 条 + 正文补 11 条 = 74/106；其余为综述/工程类，无网络未能核对。
- [x] 3.4 ✅ `note`/`note_type` 映射 12 篇库内笔记；其余留空。
- [x] 3.5 ✅ 未获取项清单写入附录：机构缺 36、venue 缺 30、年份缺 32、作者缺 32。
- [x] 3.6 ✅ `scripts/collect_dh_paper_units.py` 已提交，支持增量合并。

## 4. 配套 JSON 落盘

- [x] 4.1 ✅ 写入 `management/docs/数字人概述/数字人关键技术地图.json` 的 `papers` 字段。
- [x] 4.2 ✅ 不采用独立资产方案（裁决 A）。
- [x] 4.3 ✅ JSON 合法、`id` 唯一、字段完整。

## 5. 前端渲染实现

- [x] 5.1 ✅ 新增 `web/src/components/common/PaperTable.vue`：列 = # / 论文 / 机构 / 发表 / 方法族 / 问题 / 解法 / 继承自 / 笔记；支持排序、方法族筛选、分页；`ellipsis` 提供全文 tooltip。
- [x] 5.2 ✅ `note_type==='doc'` 走站内 `/management/docs/<note>`；`blog` 新窗口外链；缺失显示「未建」。
- [x] 5.3 ✅ `DocPage.vue` 按 `<!-- papers-table -->` 切分 `bodyContent`，标记处挂载 `PaperTable`，其余交 `MarkdownRenderer`。
- [x] 5.4 ✅ TOC 由完整 `content` 提取、不受切分影响；`extractToc` 与滚动记忆逻辑未改动。
- [x] 5.5 ✅ 开发模式（FastAPI 详情接口返回 106 条 sidecar）与生产构建（`docs-data.json` 含 106 条）均验证。

## 6. 文档写作

- [x] 6.1 ✅ 「这份地图回答什么」+「语料与方法」。
- [x] 6.2 ✅ 「关键任务与问题空间」。
- [x] 6.3 ✅ 13 条技术分线（问题 → 方法族 → 代表工作表【机构·venue/时间】 → 边界）。
- [x] 6.4 ✅ 「演进时间线（2020—2026）」Mermaid + 「机构与团队分布」表。
- [x] 6.5 ✅ 「关键问题补充」15 条候选，含证据与「还缺什么」。
- [x] 6.6 ✅ 「论文信息对总表」只放占位标记。
- [x] 6.7 ✅ 附录：抽取方法与未获取项。

## 7. 规格与落位

- [x] 7.1 ✅ `docs-page-content` delta 完成，`openspec validate --strict` 通过。
- [x] 7.2 ✅ `order: 15`（占用 10 与 20 之间空位），既有 order 未改。
- [x] 7.3 ✅ frontmatter 合法（title/author/date/tags/summary/order）。
- [x] 7.4 ✅ 问题补充未回流（裁决：全部写进本文档），未改《数字人领域问题》。

## 8. 验证与交付

- [x] 8.1 ✅ 标题层级 `##`/`###`；表格列数与分隔行一致。
- [x] 8.2 ✅ 6 处站内 `[[...]]` 链接目标均存在（脚本校验通过）。
- [x] 8.3 ✅ Mermaid 图节点无单 `$`；无 KaTeX 公式。
- [x] 8.4 ✅ 缺失项标「未标注」，未编造。
- [x] 8.5 ✅ `docs_order.py list` 无缺失/重复（15 → 20 → …）。
- [x] 8.6 ✅ `npm run build` 通过；`build-docs-data.mjs` 含新文档与 106 条 sidecar。
- [x] 8.7 ✅ `openspec validate docs-dh-key-technology-map --strict` 通过；FastAPI 详情接口可取文档与 106 条 papers。
- [x] 8.8 ✅ 提交 `docs(dh-key-tech): ...`，仅含本文档、sidecar、PaperTable 组件、DocPage 改动、采集脚本与 OpenSpec change。
