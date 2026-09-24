## 1. 素材与分析

- [x] 1.1 初始化 `.cache/article-note/pixel3dmm/` 并抓取：HTML 正文（254 KB，含全部题注）、PDF；arXiv 无 LaTeX source（未尝试）。
- [x] 1.2 读完全文主线（Abstract / §1 / §2 / §3.1–3.3 / §4 / §5.1–5.7 / §6 / §7）并摘录关键设计、公式与数字。
- [x] 1.3 核对元信息：作者五人（TUM ×3 / Synthesia / UCL）、arXiv `2505.00615`（**仅 v1，2025-05-01**）、项目页；**ICLR 2026 来自博客 `uika-2026`，arXiv 无标注**。
- [x] 1.4 下载 6 张原图（teaser / method / benchmark diversity / posed / neutral / normals）并记录尺寸；发现 teaser 为 6144×2048 的极宽条带。
- [x] 1.5 写 `analysis/{methodology,experiment,terminology}.md` 三 lane（含四个规定小标题）与 `synthesis.md`（721 字，≤1000）。
- [x] 1.6 修正 README 待读行里我上一轮写错的事实（DINOv3 + DPT head → **DINOv2 + 轻量头、主干 lr 降 10×**），并补上"UIKA 的 DINOv3+DPT 是 UIKA 自己的配方"的限定。
- [ ] 1.7 用户审核 design（§3 结构、§4 的 D1–D6、§5 图表公式、§7 风险项）。

## 2. 图片发布

- [ ] 2.1 5 张原图转 WebP：最长边 ≤1600px、单图 ≤500KB（图 1 由 2.9 MB 压，图 4 由 1.6 MB 压）。
- [ ] 2.2 发布到 `management/docs/_assets/pixel3dmm/`，命名 `fig-1-…` 至 `fig-5-…`。
- [ ] 2.3 逐张确认存在与体积；图 1、图 4 小字可读性提请用户目视。
- [ ] 2.4 单篇图片总量 ≤5MB。

## 3. 正文与 sidecar

- [ ] 3.1 §0 论文信息（含"arXiv 仅 v1 / ICLR 2026 来自博客"说明、"papers 库未入库"）。
- [ ] 3.2 §1 一句话总结（4 条贡献）、§2 问题与动机（两条路线与两段式选择），配图 1。
- [ ] 3.3 §3：图 2 + 两张 Mermaid；3.1 像素级几何线索（架构 / 数据配比 / IC-Light 光照增广 / 训练目标与主干 lr）；3.2 单图 FLAME 拟合（式 4–8，含 UV 最近邻查表与 2D 顶点损失）；3.3 单目视频跟踪（冻结项 / 批量 / 式 9 平滑项）。
- [ ] 3.4 §4 训练与实现细节：10 项配置披露表（含 2×A6000 × 3 天与拟合 30 秒），未披露项写「未披露」。
- [ ] 3.5 §5 推理与系统链路：两段式推理时序 + 视频跟踪的冻结/批量策略 + 与我们评测框架 `driving_mode` 的接点。
- [ ] 3.6 §6 实验与结果：基准（posed / neutral）、协议（Chamfer / NC / R2.5）、主结果（>15%）、既有基准、法向、消融；配图 3、图 4、图 5；按 D3/D5 标注来源与定义。
- [ ] 3.7 §7 相关工作与定位（前馈回归器 vs 优化式；与 UIKA / FlexAvatar / PerformRecast 的关系）。
- [ ] 3.8 §8 局限与启发：论文三条局限 + **与数字人的接口**（成本、监督来源定位、评测框架已接入、第 ③ 条局限接进第七章判据）。
- [ ] 3.9 §9 术语与符号表（含四处易错命名）、§10 相关文档。
- [ ] 3.10 `pixel3dmm.json`：frontmatter 只含 `arxiv_id`；sidecar 含 `changelog` / `progress` / `appendix` / `related`。

## 4. 验证与交付

- [ ] 4.1 `validate-note.py` / `validate-analysis.py` / `check-delivery.py` 全绿。
- [ ] 4.2 frontmatter 键与既有笔记一致（无 `papers_id`，因未入 papers 库）。
- [ ] 4.3 结构自检：标题层级、表格列数、`$` 奇偶、Mermaid 配对、图片编号连续且资产命中、站内链接目标存在。
- [ ] 4.4 `docs_order.py list management/docs/论文笔记` 确认 order 无重复。
- [ ] 4.5 FastAPI 详情接口确认新 slug 可读、sidecar `related` 全部解析。
- [ ] 4.6 `openspec validate docs-note-pixel3dmm --strict`；`git status` 仅含预期文件。
- [ ] 4.7 提交 `docs(note): 新增 Pixel3DMM 论文笔记`。

## 5. 后续（不在本 change 内）

- [ ] 5.1 可考虑在第七章新增"像素级几何跟踪 / 参数化跟踪"技术条目（`docs-dh-field-tech-applicability`），判据用本篇 §6 第三条局限引出的"identity 与 expression 的可分性"。
