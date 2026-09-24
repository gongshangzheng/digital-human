# Tasks: docs-note-gen-acceleration（生成侧加速十篇）

> 分批实施（D4）：第一批「注意力/内核 + 缓存」→ 第二批「自回归并行」→ 第三批「端到端系统 + 仓库类」。每批完成即校验并提交。

## 1. 素材与分析

- [x] 1.1 抓取八篇论文素材（HTML 全部成功；PDF：fpsattention / inferix / nar 有，其余缺 → 页码类引用改为「章节 + 图/表号」）
- [x] 1.2 核实十篇标识：8 篇 arXiv（2506.04648 / 2508.10774 / 2606.09828 / 2412.04062 / 2503.10696 / 2605.09430 / 2512.16093 / 2511.20714）+ 2 篇无同行评议论文（worldattention、dax）
- [x] 1.2b 范围变更：`fpsattention` 已由另一会话完成并归档（`2026-09-24-docs-note-fpsattention`）→ 移出本 change；**本 change 实际覆盖 9 篇**
- [x] 1.3 第一批分析（blade / latent-spatial-memory）：methodology + experiment + terminology + image-collection + synthesis，过 `validate-analysis.py`
- [x] 1.4 第二批分析（zipar / nar / flashar）
- [x] 1.5 第三批论文分析（turbodiffusion / inferix）；仓库类来源已由联网调研确认为官方仓库（无同行评议论文）

## 2. 图片发布

- [x] 2.1 第一批：从 HTML 下载采用图 → WebP → publish 到 `_assets/<slug>/`（blade 2 张 / LSM 3 张）
- [x] 2.2 第二批：zipar 3 张 / nar 3 张 / flashar 1 张（Figure 1、3 被 arXiv 406 限流，正文如实说明）
- [x] 2.3 第三批：inferix 发布 2 张（范式对比 / 引擎框架）；turbodiffusion 不发布原图（图均为无图题定性帧对比）

## 3. 写作

- [x] 3.1 第一批两篇正文 + sidecar（blade 304 行 / latent-spatial-memory 377 行，均双校验通过）
- [x] 3.2 第二批三篇（zipar 323 行 / nar 345 行 / flashar 444 行，均双校验通过）
- [~] 3.3 第三批：turbodiffusion（402 行）、inferix（353 行）已完成；worldattention、dax 待写（仓库类，按 D2 骨架）

## 4. 回补与收口

- [ ] 4.1 十篇齐备后，一次性把《数字人加速》「生成侧加速」四方向里的工作名替换为文档链接（= `docs-intern-acceleration` 3.1）
- [x] 4.2 更新 `论文笔记/README.md` 九行状态（blade / latent-spatial-memory 已标完成；fpsattention 由另一会话完成）
- [ ] 4.3 同步伞 change `internship-work-review-docs` 2.14 与 `docs-intern-acceleration` 3.1 状态

## 5. 校验与提交

- [ ] 5.1 每批 `validate-note.py` + 浏览器抽查（公式 / 图 / 链接 / Mermaid）
- [ ] 5.2 `openspec validate docs-note-gen-acceleration --strict`
- [ ] 5.3 分批聚焦提交（每批一个提交，不夹带他人工作）
