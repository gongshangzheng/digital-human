## 1. 素材与分析

- [x] 1.1 初始化 `.cache/article-note/tivtok/` 并抓取：HTML 正文（259 KB，含全部题注）、PDF、5 张原图。
- [x] 1.2 读完全文主线（Abstract / §1 / §2 / §3.1–3.5 / §4.1–4.6 / §5 Discussion / §6 Conclusion）并摘录关键数字与公式。
- [x] 1.3 核对元信息：作者 Weiliang Chen、Yuanhui Huang、Xuebo Wang、Yueqi Duan（清华）；arXiv `2606.17590`（v1 2026-06-16）；**未声明 venue、未见代码链接**。
- [x] 1.4 下载 5 张主图（teaser / pipeline03 / token / tivratio / recon）；备选 `more-vis.png` 未用。
- [x] 1.5 写 `analysis/{methodology,experiment,terminology}.md` 三 lane（含四个规定小标题）与 `synthesis.md`（661 字，≤1000）。
- [x] 1.6 用户审核 design 通过（"开始"）。

## 2. 图片发布

- [x] 2.1 5 张原图转 WebP：最长边 ≤1600px（图 1 由 2.4 MB 压到 143 KB、图 3 由 2.1 MB 压到 100 KB）。
- [x] 2.2 发布到 `management/docs/_assets/tivtok/`，命名 `fig-1-…` 至 `fig-5-…`。
- [x] 2.3 逐张确认存在与体积（总 409 KB，单张最大 143 KB）；图 1、图 3 小字可读性待用户目视。
- [x] 2.4 单篇图片总量 409 KB ≤5MB。

## 3. 正文与 sidecar

- [x] 3.1 §0 论文信息（含"未声明 venue / 无代码"、"papers 库未入库"）、§1 一句话总结（4 条贡献）。
- [x] 3.2 §2 问题与动机：持久内容重复编码 + 信息论论证（式 2），配图 1。
- [x] 3.3 §3：Mermaid 数据流 + 图 2；3.1 前置 holistic tokenizer；3.2 TIV/TV 分解；3.3 SIF（式 3、4 + 复杂度对比 + **为什么不用因果掩码**）；3.4 IB（式 5）；3.5 跨块复用（式 6、7 + 第二张 Mermaid）。
- [x] 3.4 §4 训练与实现细节：10 项配置披露表（含式 8 的损失与自适应权重），硬件与种子写「未披露」。
- [x] 3.5 §5 推理与系统链路：Mermaid 时序 + 三个复杂度读数 + 长视频延迟表 + **显式写"编码非因果"**。
- [x] 3.6 §6 实验与结果：重建 → **TIV 到底学了什么（图 3）** → 长视频（图 4）→ 生成 → TIV 容量与 TIV:TV 分配（图 5）；按 D4/D5 标注二手数字与分辨率口径。
  - 实施时调整：把「TIV 到底学了什么」从 §6 末移到重建表之后，使图号按出现顺序连续（校验器要求），叙事也更顺（先看清 TIV 是什么，再看代价与旋钮）。
- [x] 3.7 §7 相关工作与定位（图像→视频 tokenizer、分解式 tokenizer；与人为定义分解的根本差别）。
- [x] 3.8 §8 局限与启发：论文自述局限 + 四处口径提醒 + **与数字人的关系**（六维对照、与 AdapTok/Face Vid2vid 的互补、三条待验证判据）+ 四条可操作启发。
- [x] 3.9 §9 术语与符号表（含四处易错命名）、§10 相关文档。
- [x] 3.10 `tivtok.json`：frontmatter 只含 `arxiv_id`；sidecar 含 `changelog` / `progress` / `appendix` / `related`。

## 4. 验证与交付

- [x] 4.1 `validate-note.py` / `validate-analysis.py` / `check-delivery.py` 全绿。
- [x] 4.2 frontmatter 键与既有笔记一致（无 `papers_id`）。
- [x] 4.3 结构自检：11 个 `##`、14 个 `###`、表格列数全一致、`$` 无奇数行、3 个 Mermaid 块配对；5 张图编号连续（1–5）且资产全部命中；5 处站内链接目标全部存在。
- [x] 4.4 `docs_order.py list` 确认 `order: 200` 无重复（180 先被并行会话的 `worldattention` 占用，190 亦被占用，顺延至 200）。
- [x] 4.5 FastAPI 详情接口 200（15,496 字符，5 张图 URL 齐全），sidecar 4 条 `related` 全部解析。
- [x] 4.6 `openspec validate docs-note-tivtok --strict` 通过。
- [x] 4.7 提交 `docs(note): 新增 TivTok 论文笔记`。

> 过程记录（两处修正）：① sidecar 的 `desc` 里嵌了未转义的双引号导致 JSON 非法，已改用 `「」`；② 初稿把图 3 放在 §6 末尾导致图号顺序为 1,2,4,5,3，校验器拦下，已将该小节前移。

> 遗留：图 1、图 3 的图内小字可读性需用户目视（本机模型不支持读图）。

## 5. 后续（不在本 change 内）

- [x] 5.1 AdapTok 与 TivTok 两篇素材均已就绪。
- [ ] 5.2 写 `数字人领域问题` 第七章首条目（属 `docs-dh-field-tech-applicability`），含 TIV 身份纯度判据。
