## 1. 素材与冲突核对

- [x] 1.1 定位现有章节与条目（并行会话已写入 `## 七、技术适用性` 与 1D tokenizer 条目，并新增 `## 八、工程问题模型化`）。
- [x] 1.2 通读该条目，逐条比对两篇笔记，列出六处需要修正/补写的事实。
- [x] 1.3 更新 proposal 与 design 的实施修正节，把本 change 的职责从"新建章节"改为"修正已有条目"。

## 2. 正文修正

- [x] 2.1 技术表 AdapTok 行：补"分配依据是重建质量（感知损失）"与"因果粒度是块（每块 4 帧）"。
- [x] 2.2 接口表「因果性」行：改为 ✅ AdapTok（块级）/ ❌ TivTok（非因果），并写明 TivTok 为何不用因果掩码。
- [x] 2.3 接口表「时序性」行：补 TivTok 的 TIV/TV 分工是对"身份 vs 运动"的正面回应（架构涌现）。
- [x] 2.4 可检验判据：新增第 6 条「因果化改造的代价」。
- [x] 2.5 「已知证据与代价」：改为两篇笔记已完成可引用，并单列 §4.5 那条**定性**证据及其性质。
- [x] 2.6 预判：补 AdapTok 分配依据与身份的错位（按运动分配 ≠ 保身份）。

## 3. 验证与交付

- [x] 3.1 章节结构未变（`## 七`/`## 八` 原样），表格列数与分隔行一致，无新增标题层级问题。
- [x] 3.2 新增链接目标存在（`论文笔记/adaptok`、`论文笔记/tivtok`、`论文笔记/face-vid2vid`）。
- [x] 3.3 `openspec validate docs-dh-field-tech-applicability --strict` 通过。
- [x] 3.4 FastAPI 详情接口确认文档可读。
- [x] 3.5 提交 `docs(field-problems): 用两篇笔记修正第七章 1D 分词器条目`。

## 4. 长期演进（本 change 不归档）

- [x] 4.1 design 记录"不归档"与长期演进约定。
- [ ] 4.2 后续每条新技术仍按同一流程：先在本 change 的 design 追加条目规格与引用白名单，再追加 tasks，用户确认后才写正文。
- [ ] 4.3 每轮补充完成后**不跑** `openspec-archive-change`。

## 5. 待读登记与登记口径修复（2026-09-24）

- [x] 5.1 `论文笔记/README.md` 追加 `pixel3dmm.md`（arXiv:2505.00615，ICLR 2026）待读行，并写登记说明（它是 tracking / 显式监督信号来源；我们评测框架已有 `driving_mode: pixel3dmm`；未入 papers 库；博客引文纠错记录）。
- [x] 5.2 修复 `papers_id` 登记不一致（11 篇）：`performrecast` 在 papers 库中但缺字段 → 补 `papers_id: arxiv-2603.19731`；`blade`/`face-vid2vid`/`flashar`/`float`/`inferix`/`latent-spatial-memory`/`nar`/`talker-t2av`/`turbodiffusion`/`zipar` 十篇写了 `papers_id` 但既不在 `papers.db` 也不在 `blog_papers.json` → 删除悬空字段。复核后全库一致。
- [x] 5.3 `论文笔记/README.md` 命名规范写死口径：`papers_id` **仅当该论文确实在 papers 库中时才写**（库只从 `blog_papers.json` 导入）。
- [x] 5.4 修复博客仓库 `src/pages/paper-performrecast.html` 与 `public/paper-performrecast.html` 中 `arXiv:2505.00615` 的错误标题（编号对、标题错）。
