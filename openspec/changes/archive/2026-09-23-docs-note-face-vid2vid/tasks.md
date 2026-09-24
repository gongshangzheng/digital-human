# Tasks: docs-note-face-vid2vid

> 门禁（同 `article-note` 流水线）：素材 → 分析 → 结构审批 → 图片发布/正文/sidecar → 校验。

## 1. 素材与分析

- [x] 1.1 抓取素材到 `.cache/article-note/face-vid2vid/`（HTML + PDF 成功；source tarball 406 失败，已记入 extraction-log）
- [x] 1.2 下载候选原图 8 张，并建立 `analysis/image-collection.md`（图号↔文件名映射与采用建议）
- [x] 1.3 分析 lane（methodology / experiment / terminology）+ synthesis，并通过 `validate-analysis.py`
- [x] 1.4 用 `pdftotext -layout` 逐图核对 PDF 编号（LaTeXML anchor 有 +1 偏移），锁定 6 张采用图的编号
- [x] 1.5 用户已审 design 的 10 节结构与图表清单（门禁通过）

## 2. 图片发布

- [x] 2.1 `figures.py convert` 把采用图（论文 Figure 2/3/4/10/6/14）转 WebP（大图降采样）
- [x] 2.2 `figures.py publish` 发布到 `management/docs/_assets/face-vid2vid/`（命名 `fig-<编号>-<语义>.webp`）
- [x] 2.3 体积校验：6 张共 **391KB**（单图 ≤500KB、单篇 ≤5MB）

## 3. 写作

- [x] 3.1 写 `management/docs/论文笔记/face-vid2vid.md`（397 行；11 节；6 图；4 个块级公式 + 1 张 Mermaid；`Nan` 与正面化 Angle 落后均加事实核对注）
- [x] 3.2 写 sidecar `management/docs/论文笔记/face-vid2vid.json`（`related` 用 `{slug,title}`；`notes` 记明未入本地 papers 库、图号采用 PDF 编号）
- [x] 3.3 链接回补：`liveportrait.md` 首现处（第 28 行）改为 `[[论文笔记/face-vid2vid|Face Vid2vid]]`
- [x] 3.4 更新 `management/docs/论文笔记/README.md` 清单（新增 `face-vid2vid.md` 行，状态=已完成）

## 4. 校验与提交

- [x] 4.1 `validate-note.py --note management/docs/论文笔记/face-vid2vid.md` 通过
- [x] 4.2 浏览器抽查：KaTeX 188 个 / 0 错误、6 张图全部 decode、与 liveportrait 的双向互链生效
- [x] 4.3 `openspec validate docs-note-face-vid2vid --strict`
- [x] 4.4 聚焦提交：笔记 + sidecar + `_assets/face-vid2vid/` + `liveportrait.md` 链接回补 + README + change 工件

## 备注（写作文本的诚实项，已落在正文里）

- 「不估计 Jacobian」（假设头部近刚体 $J_s=R_s$）是与 FOMM 的关键机制差异，已在正文写明。
- free-view 的两条边界（非 3D 重建、无角度量化指标）已写给；`liveportrait.md` 另新增「2D 与 3D 的区别」小节并回链本篇。
- Table 3 正面化 Angle 落后 pSp（90.9 vs 99.8）与 Table 1 的 `Nan` 均照录并加注，不做解释性发挥。
