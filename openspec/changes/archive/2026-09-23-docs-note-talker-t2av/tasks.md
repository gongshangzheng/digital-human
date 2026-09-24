# Tasks: docs-note-talker-t2av

> 门禁（同 `article-note` 流水线）：素材 → 分析 → 结构审批 → 图片发布/正文/sidecar → 校验。

## 1. 素材与分析

- [x] 1.1 抓取素材到 `.cache/article-note/talker-t2av/`（HTML + PDF 成功；source tarball 406 失败，已记入 extraction-log）
- [x] 1.2 盘点图源：HTML 仅 1 张正文图（`fig1.png` 939×720），其余为 6 张表；PDF p4 缩略图过小不采用 → 写入 `analysis/image-collection.md`（「1 图 + 2 Mermaid」替代方案）
- [x] 1.3 分析 lane（methodology / experiment / terminology）+ image-collection，并通过 `validate-analysis.py`
- [x] 1.4 用户已审 design 的 10 节结构与图表清单（门禁通过）

## 2. 图片发布

- [x] 2.1 `figures.py convert` + `publish` → `_assets/talker-t2av/fig-1-overview.webp`（939×720 / 41KB）
- [x] 2.2 未将低分辨率缩略图入库；`_assets` 内无超限文件

## 3. 写作

- [x] 3.1 写 `management/docs/论文笔记/talker-t2av.md`（492 行；11 节；1 原图 + **2 张 Mermaid**；5 个块级公式 + 143 个行内式；Table 1–6 关键数值照录；UTMOS/SyncNet 加事实核对注；正文写明配图受论文限制）
- [x] 3.2 写 sidecar `management/docs/论文笔记/talker-t2av.json`（`related` 用 `{slug,title}`；`notes` 记录仅 1 图、上游固定 `6712f62`、UTMOS 与 SyncNet 口径疑点）
- [x] 3.3 链接回补：`knowledge/Talker-T2AV 模型精读.md`、`knowledge/Talker-T2AV 接入与验证.md` 各加一处论文层前向链接
- [x] 3.4 更新 `management/docs/论文笔记/README.md` 清单（`talker-t2av.md` → 已完成）

## 4. 校验与提交

- [x] 4.1 `validate-note.py --note management/docs/论文笔记/talker-t2av.md` 通过
- [x] 4.2 浏览器抽查：公式渲染、图 1 加载、2 张 Mermaid 渲染、站内链接
- [x] 4.3 `openspec validate docs-note-talker-t2av --strict`
- [x] 4.4 聚焦提交：笔记 + sidecar + `_assets/talker-t2av/` + knowledge 前向链接 + README + change 工件

## 备注（写作期发现，已落在正文/sidecar）

- **配图受论文限制**：论文只有 1 张正文图（Figure 1），无法满足「≥3 张原图」，改用 2 张 Mermaid 补结构、由 Table 1–6 承载证据；正文已写明这一点，未用低分辨率缩略图凑图。
- **数字张力**：英文 UTMOS 3.458 略低于 UniAVGen 3.459，与「naturalness 显著更好」措辞有张力 → 照录 + 加注。
- **SyncNet C/D 量级可疑**（0.66–6.33 / 8.44–13.91，与常见 0–1 不同量纲，论文未说明变体与后处理）→ 只在论文协议内比较，不做跨来源横比。
- Table 3 加粗标注不一致、MoVA↔MOVA 拼写不一致 → 正文按事实处理并登记。
- 视频侧表示即 **LIA-X** 40 维 motion code → 与 `[[论文笔记/lia-x]]` 互链，避免重复解释。
