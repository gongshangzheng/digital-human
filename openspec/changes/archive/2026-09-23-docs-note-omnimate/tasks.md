# Tasks: docs-note-omnimate

> 门禁（同 `article-note` 流水线）：素材 → 分析 → 结构审批 → 图片发布/正文/sidecar → 校验。

## 1. 素材与分析

- [x] 1.1 抓取素材到 `.cache/article-note/omnimate/`（**source tarball 成功**：LaTeX 单文件 + 5 张矢量原图；另有 PDF）
- [x] 1.2 从 `Arxiv.tex` 建立图号 ↔ 文件 ↔ 图题映射（含 `trim` 裁切参数），写入 `analysis/image-collection.md`
- [x] 1.3 分析 lane（methodology / experiment / terminology）+ image-collection，并通过 `validate-analysis.py`
- [x] 1.4 用户已审 design 的 10 节结构与图表清单（门禁通过）

## 2. 图片发布

- [x] 2.1 `pdftocairo -png -r 200` 栅格化 5 张矢量图（teaser / method / train_GPC / result / ablation）
- [x] 2.2 内容裁切（A4 整页画布：排除顶/左细边框线后按内容 bbox 裁剪）→ `figures.py convert` + `publish` 到 `management/docs/_assets/omnimate/`
- [x] 2.3 体积校验：5 张共 **610KB**（单图 ≤500KB、单篇 ≤5MB）

## 3. 写作

- [x] 3.1 写 `management/docs/论文笔记/omnimate.md`（486 行；11 节；5 图；8 个块级公式 + 2 张 Mermaid；指标口径未公开已标注）
- [x] 3.2 写 sidecar `management/docs/论文笔记/omnimate.json`（`related` 用 `{slug,title}`；`notes` 记录口径风险与 venue 情况）
- [x] 3.3 链接回补：《数字人领域问题》250 行
- [x] 3.4 更新 `management/docs/论文笔记/README.md` 清单（`omnimate.md` → 已完成）

## 4. 校验与提交

- [x] 4.1 `validate-note.py --note management/docs/论文笔记/omnimate.md` 通过
- [x] 4.2 浏览器抽查：公式渲染、5 张图加载、站内链接、2 张 Mermaid
- [x] 4.3 `openspec validate docs-note-omnimate --strict`
- [x] 4.4 聚焦提交：笔记 + sidecar + `_assets/omnimate/` + 概述链接回补 + README + change 工件

## 备注（写作期发现，已落在正文/sidecar）

- **design 图号顺序修正**：原稿把 method 列为「图 1」会导致正文图号非单调，写作前已改为按论文顺序（Fig 1 teaser → 图 1；Fig 2 method → 图 2；Fig 3 train_GPC → 图 3；Fig 4/5 → 图 4/5）。
- **papers 库事实纠正**：写作者实测 `data/papers.db` 中**存在** `arxiv-2607.23023`（`source=blog`，来自博客精读导入），因此没有按原口径写「未入库」，而是写成「未作为独立 arXiv 条目入本地资料集，papers_id 按命名规范」。
- **Figure 2 图题与图内字母不一致**（图题写 (b) GPC / (c) MRCM，图内为 (b) MRCM / (c) GPC）→ 正文按图内字母引用并登记差异。
- 13 个指标的实现口径与 TTFF 计时口径**均未披露** → 正文标注不可复现验证；AQ/VQ/Sync-D/LSE-C 非第一亦已写明。
