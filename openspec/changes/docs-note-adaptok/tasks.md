## 1. 素材与分析

- [x] 1.1 初始化 `.cache/article-note/adaptok/` 并抓取：HTML 正文（284 KB，含全部图表题注）、PDF（22 页）；LaTeX source **抓取失败（HTTP 406）**，已记入 extraction-log。
- [x] 1.2 读完全文主线（Abstract / §1 / §2 / §3 / §4 / §5 / 附录 B.2）并摘录关键数字与公式。
- [x] 1.3 核对元信息：作者（**Yan Li** 与 Changyao Tian 同等贡献；通讯 Hao Li、Xue Yang）、单位、arXiv `2505.17011`（v1 2025-05-22、v2 2025-10-14）、代码 `VisionXLab/AdapTok`；**OpenAlex 第一作者字段有误，以论文为准**。
- [x] 1.4 下载并核对 5 张主图原图；确认备选图路径差异（`vis_content_aware`/`vis_temporal_dynamics` 需走 `images/` 前缀）。
- [x] 1.5 写 `analysis/{methodology,experiment,terminology}.md` 三 lane（含四个规定小标题）与 `synthesis.md`（558 字，≤1000）。
- [x] 1.6 用户审核 design 通过（"apply"）。

## 2. 图片发布

- [x] 2.1 5 张原图转 WebP：最长边 ≤1600px（图 1 由 2.4 MB 压到 116 KB）。
- [x] 2.2 发布到 `management/docs/_assets/adaptok/`，命名 `fig-1-…` 至 `fig-5-…`。
- [x] 2.3 逐张确认存在与体积（总 386 KB，单张最大 116 KB）；图 1、图 2 小字可读性待用户目视。
- [x] 2.4 单篇图片总量 386 KB ≤5MB。

## 3. 正文与 sidecar

- [x] 3.1 §0 论文信息（含会议状态"未确认"、作者口径说明、"papers 库未入库"）、§1 一句话总结（4 条贡献）。
- [x] 3.2 §2 问题与动机：固定预算的两个方向错配，配图 1。
- [x] 3.3 §3：Mermaid 数据流 + 图 2 框架总览；3.1 自适应 tokenizer（patchify + block causal + 掩码采样）；3.2 adaptive scorer（式 4、5 + 符号表）；3.3 IPAL（式 6 + `n_k` + Algorithm 1 + 三种替代策略）；3.4 AR 生成（式 7）。
- [x] 3.4 §4 训练与实现细节：10 项配置披露表，硬件与种子写「未披露」。
- [x] 3.5 §5 推理与系统链路：Mermaid 时序 + 延迟 50.9 vs 571.7 ms + 块级因果的最小延迟含义。
- [x] 3.6 §6 实验与结果：重建 / 生成 / 规模 / 自适应消融 / 分配策略 / 打分指标六组，配图 3、图 4、图 5；按 D3/D4 标注口径。
- [x] 3.7 §7 相关工作与定位（离散视频 tokenizer / 自适应 tokenizer 两条脉络 + 生成侧）。
- [x] 3.8 §8 局限与启发：论文自述局限 + 四处口径提醒 + **与数字人的关系**（六维对照表、两条待验证判据、头部 token 线索）+ 三条可操作启发。
- [x] 3.9 §9 术语与符号表（含四处易错命名）、§10 相关文档。
- [x] 3.10 `adaptok.json`：frontmatter 只含 `arxiv_id`；sidecar 含 `changelog` / `progress` / `appendix` / `related`。

## 4. 验证与交付

- [x] 4.1 `validate-note.py` / `validate-analysis.py` / `check-delivery.py` 全绿。
- [x] 4.2 frontmatter 键与既有笔记一致（`title`/`author`/`date`/`tags`/`arxiv_id`/`summary`/`order`），无 `papers_id`。
- [x] 4.3 结构自检：11 个 `##`、13 个 `###`、表格列数全一致、`$` 无奇数行、2 个 Mermaid 块配对；5 张图编号连续且资产全部命中；7 处站内链接目标全部存在。
- [x] 4.4 `docs_order.py list` 确认 `order: 160` 无重复（90 与 120 先后与并行会话的 `causal-forcing`、`latent-spatial-memory` 碰撞，顺延到当前最大 150 之后）。
- [x] 4.5 FastAPI 详情接口 200（11,823 字符，5 张图 URL 齐全），sidecar 4 条 `related` 全部解析。
- [x] 4.6 `openspec validate docs-note-adaptok --strict` 通过。
- [x] 4.7 提交 `docs(note): 新增 AdapTok 论文笔记`。

> 遗留：图 1、图 2 的图内小字可读性需用户目视（本机模型不支持读图）。

## 5. 后续（不在本 change 内）

- [ ] 5.1 另开 change 做 **TivTok**（arXiv:2606.17590）笔记，素材已抓在 `.cache/article-note/tivtok/`。
- [ ] 5.2 两篇完成后，写 `数字人领域问题` 第七章首条目（属 `docs-dh-field-tech-applicability`）。
