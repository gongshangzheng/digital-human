# Tasks: docs-note-lia-x

> 门禁（同 `article-note` 流水线）：素材 → 分析 → 结构审批 → 图片发布/正文/sidecar → 校验。**用户明确确认结构前不得写入 `management/docs/论文笔记/`。**

## 1. 素材与分析

- [x] 1.1 抓取素材到 `.cache/article-note/lia-x/`（HTML + PDF 成功；source tarball 406 失败，已记入 extraction-log）
- [x] 1.2 下载候选原图（10 张；`3d1.png` 406 待补）并建立 `analysis/image-collection.md` 候选表与替代方案
- [x] 1.3 分析 lane（methodology / experiment / terminology）+ synthesis，并通过 `validate-analysis.py`
- [x] 1.4 **用户审 design 的 10 节结构与图表清单（门禁，已通过）**

## 2. 图片发布

- [x] 2.1 从 PDF 补齐 Figure 4(a)（`pdfimages` 取 p5-001，与已下载 Pitch/Roll 像素比对确认）
- [x] 2.2 拼接 Figure 4 三面板为单张图（Pillow，白底留白，1581×968）
- [x] 2.3 `figures.py convert` + `publish` 发布采用图到 `management/docs/_assets/lia-x/`，命名 `fig-<编号>-<语义>.webp`
- [x] 2.4 校验体积：单图 ≤500KB、单篇 ≤5MB（实际 5 张共 443KB）

## 3. 写作

- [x] 3.1 写 `management/docs/论文笔记/lia-x.md`（10 节骨架；图题 + 解读；公式 3 个 + 符号表；Table 1 的 FID 冲突加事实核对注；未披露项写"未披露"）
- [x] 3.2 写 sidecar `management/docs/论文笔记/lia-x.json`（`related` 用 `{slug,title}` 对象）
- [x] 3.3 链接回补：《数字人身份》86、《数字人加速》83（仅链接替换）
- [x] 3.4 更新 `management/docs/论文笔记/README.md` 清单状态（`lia-x.md` → 已完成）

## 4. 校验与提交

- [x] 4.1 `validate-note.py --note management/docs/论文笔记/lia-x.md` 通过
- [x] 4.2 浏览器抽查：公式渲染（156 个 KaTeX、0 错误）、图片加载（5 张 decode 成功，含拼接图 1581×968）、站内链接（9 个）、Mermaid 1 张
- [x] 4.3 `openspec validate docs-note-lia-x --strict`
- [x] 4.4 聚焦提交：笔记 + sidecar + `_assets/lia-x/` + 概述链接回补 + README
