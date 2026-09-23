# Tasks: docs-note-float

> 门禁（同 `article-note` 流水线）：素材 → 分析 → 结构审批 → 图片发布/正文/sidecar → 校验。

## 1. 素材与分析

- [x] 1.1 抓取素材到 `.cache/article-note/float/`（**source tarball 成功**：LaTeX 源码 + 32 张矢量原图；另有 PDF）
- [x] 1.2 从 LaTeX figure 环境建立「图号 ↔ 文件名 ↔ 图题」映射，并写入 `analysis/image-collection.md`
- [x] 1.3 分析 lane（methodology / experiment / terminology）+ synthesis，并通过 `validate-analysis.py`
- [x] 1.4 用户已审 design 的 10 节结构与图表清单（门禁通过）
- [x] 1.5 用 `pdftotext -layout` 核对论文图号（overview=Fig2、comp-lp=Fig3、vector-field=Fig4、efficiency=Fig9、emotion=Fig8、failure=Fig16）

## 2. 图片发布

- [x] 2.1 `pdftocairo -png -r 200` 栅格化 6 张矢量图（overview / vector-field-block / comp-lp / efficiency / emotion-redirection / failure-case）
- [x] 2.2 `figures.py convert` + `publish` 发布到 `management/docs/_assets/float/`（命名 `fig-<编号>-<语义>.webp`）
- [x] 2.3 体积校验：6 张共 **390KB**（单图 ≤500KB、单篇 ≤5MB）

## 3. 写作

- [x] 3.1 写 `management/docs/论文笔记/float.md`（424 行；11 节；6 图；5 个块级公式 + 1 张 Mermaid；Table 1 带 $^{\dagger}$ 脚注说明）
- [x] 3.2 写 sidecar `management/docs/论文笔记/float.json`（`related` 用 `{slug,title}`；`notes` 记明未入本地 papers 库）
- [x] 3.3 链接回补：《数字人动作》42/63、《数字人身份》88、《数字人介绍与技术路线》91
- [x] 3.4 更新 `management/docs/论文笔记/README.md` 清单（新增 `float.md` 行，状态=已完成）

## 4. 校验与提交

- [x] 4.1 `validate-note.py --note management/docs/论文笔记/float.md` 通过
- [x] 4.2 浏览器抽查：KaTeX 221 个 / 0 错误、6 张图全部 decode、站内链接 9 个、Mermaid 1 张
- [x] 4.3 `openspec validate docs-note-float --strict`
- [ ] 4.4 聚焦提交：笔记 + sidecar + `_assets/float/` + 概述链接回补 + README + change 工件

## 备注（写作文本的诚实项，已落在正文里）

- 图 3 落位由「3 方法精析」调整为「6 实验与结果（消融）」，已同步更新 design 图清单。
- 论文符号 $w_r$ 与 $w_{r\to S}$ 是否同量未披露 → 正文按 $w_{r\to S}$ 理解并注明；$\mathbf{c}_t$ 维度论文自相矛盾；Table 2 的 `21/528` 疑为排版笔误，原样照录。
- FLOAT/Hallo/EchoMimic 的评测分辨率未明示，已在 Table 1 引用处注明。
