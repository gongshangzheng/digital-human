## Context

- **素材**（`.cache/article-note/lia-x/`，已通过 `validate-analysis.py`）：主源 HTML（arXiv LaTeXML）+ PDF（12 页，页码权威）；10 张原图（`3d1.png` 下载遇 406，需从 PDF 补）；`analysis/` 含 methodology / experiment / terminology / image-collection 四份；`synthesis.md` 为事实位置索引。
- **论文元信息**：arXiv `2508.09959v1`（2025-08-13）；作者 Yaohui Wang、Di Yang、Xinyuan Chen、François Brémond、Yu Qiao、Antitza Dantcheva；单位 Shanghai Artificial Intelligence Laboratory、Inria / Université Côte d'Azur（PDF 首页与 `analysis/terminology.md`）；项目页 `wyhsirius.github.io/LIA-X-project/`；论文未给出代码仓库（正文写"未见代码仓库"）。venue 以 PDF 为准，未见会议标注 → 不声明会议。
- **我方状态**：**未接入**；仅在《数字人加速》里作为 T2AV 瓶颈与 decoder 蒸馏候选被点名（口径为二手整理：512²、bf16、batch=1 约 333ms/帧）。
- 用户已明确要求：完整结构 + 配图（不走"摘要档"）。

## Goals / Non-Goals

**Goals:**
- 按 10 节骨架成文，采用 5 张论文原图并逐图配中文图题与解读
- 讲清「运动迁移 = latent 空间线性导航 + Sparse Motion Dictionary → edit-warp-render」这条核心机制与其可解释性主张
- 关键结论附来源锚点（§/Eq./Fig./Table/页），数字标来源档；未披露项写"未披露"

**Non-Goals:**
- 不写我们的接入/实测结论（未接入）；不把论文的定性证据写成定量结论
- 不补齐论文未披露的超参（λ₁/λ₂、字典规模 M、优化器、步数等）
- 不改其它笔记与概述正文（仅链接替换）

## 结构契约（10 节，含事实锚点）

| 节 | 标题 | 写什么（锚点） |
|---|---|---|
| 0 | 论文信息 | 表格：标题 / 作者 / 单位 / venue（不声明会议）/ arXiv / 项目页 / 代码仓库（未见）/ papers 库条目 `arxiv-2508.09959` |
| 1 | 一句话总结 | 把运动迁移写成 latent 空间 motion code 的**线性导航** `z_{s→d} = z_{s→r} + w_{r→d}`，`w_{r→d} = Σ aᵢdᵢ`；用 **Sparse Motion Dictionary** 得到可解释运动因子，从而把 warp-render 升级为 **edit-warp-render**；最大约 1B 参数、8×A100（Abstract；Sec. 1 p.1；Eq. 1–3、Eq. 9；Sec. 5 p.5） |
| 2 | 问题与动机 | warp-render 类方法不可编辑；source 与 driving 首帧在姿态/表情上存在差异导致 misalignment；需要可解释、可控的运动因子来在动画前校正源图（Sec. 1；Sec. 4.3） |
| 3 | 方法精析 | 架构：编码器 E + 生成器 G（光流 G_f + 渲染 G_r），自监督训练；线性导航（Eq. 1–3）；稀疏惩罚 `λ₂·S(A_{r→d})`（Eq. 9，L1 实现）；编辑操作与范围（Eq. 10–11，`aᵢ ∈ [-0.5, 0.5]`）；稀疏化 → 语义可解释（嘴/眉/眼/pout/smile/yaw-pitch-roll）（Sec. 3–4.3） |
| 4 | 训练与实现细节 | 数据：4 个公开数据集 + 1 个内部数据集，约 0.5M talking-head 序列 / 约 94M 帧 / 55K 身份；StyleGAN-T 风格 residual block；scaling = 通道数 + 深度 + 字典规模；最大约 1B；8×A100 + gradient accumulation；**未披露**：优化器、学习率、训练步数、batch size、λ₁/λ₂、字典规模 M、三档结构差异 |
| 5 | 推理与系统链路 | edit → warp → render 流程（Mermaid）；编辑在推理前作用于源图，可与动画解耦；与我们链路：T2AV 瓶颈 333ms/帧（二手整理）→ decoder 蒸馏候选（链《数字人加速》83） |
| 6 | 实验与结果 | **自重现**（Table 1，p.8）：256²/512² 下多数指标最优；**但 VoxCelebHQ FID 10.74 高于 DaGAN 9.13**，论文"所有指标最优"的表述与表格原值不一致（照录 + 事实核对注）；**跨重现**（Table 2，p.8）无 GT，用 ID Similarity（↓）与 Image Quality（↑），LIA-X 两项最优（0.206 / 58.74）；**规模消融**（Table 3/4，p.8–9）：0.05B→0.3B 提升明显、0.3B→0.9B 有限（Large LPIPS 0.115 略差于 Middle 0.113），作者把"提升有限"归因于数据规模不足，属假设非对照实验 |
| 7 | 相关工作与定位 | warp/关键点线（FOMM、DaGAN、TPS、MCNet）与自身的 LIA 前身；可解释/解耦表示（稀疏字典 vs 稠密字典）；与扩散类方法的差别（效率与可编辑性 vs 生成质量） |
| 8 | 局限与启发 | 论文局限：稀疏性与语义可控**只有定性证据**（Fig. 3/4/6），无 disentanglement 定量指标；关键超参未披露；规模收益有限归因属假设；「论文局限 vs 我们结论」对照表（我方写"未接入；仅作为加速候选被点名"）+ 可操作启发（latent 线性导航 + 稀疏字典作为可控接口的思路；decoder 蒸馏的价值判断） |
| 9 | 术语与符号表 | motion code / motion dictionary / Sparse Motion Dictionary / edit-warp-render / ToFlow / warp-render；符号 `E`、`G_f`、`G_r`、`A_{r→d}`、`dᵢ`、`aᵢ`、`z_{s→d}`、`S(·)`、`λ₁`、`λ₂` |
| 10 | 相关文档 | `[[论文笔记/liveportrait]]`、`[[数字人概述/数字人身份]]`、`[[数字人概述/数字人加速]]`、knowledge《音画同步专题》等、papers 库条目、项目页 |

## 图表与公式清单

| 图号 | 论文来源 | 落位 | 解读要点 |
|---|---|---|---|
| 图 1 | Figure 2（`general.png`） | 3 方法精析 | 架构：E + G(G_f, G_r)，自监督 + 稀疏约束得可解释字典 |
| 图 2 | Figure 3（`sparsity_new.png`） | 3 方法精析 | 无稀疏约束时几乎激活全部运动向量 |
| 图 3 | Figure 4 三面板（`3d1/2/3.png`，需拼接） | 3 方法精析 | Yaw / Pitch / Roll 单维语义可控性 |
| 图 4 | Figure 6（`editing_new.png`） | 3 方法精析 | 细粒度属性编辑：嘴、眉、眼、pout、smile |
| 图 5 | Figure 7（`cross_new_new.png`） | 6 实验与结果 | 先生成编辑再动画 → 大姿态/表情差异下的跨重演优势 |

- 公式：2–3 个（线性导航、稀疏惩罚、编辑操作），LaTeX 取 `analysis/methodology.md` 与 `analysis/terminology.md`，写作时回 PDF 校对。
- Mermaid：1 张 edit → warp → render 流程/推理时序图。
- 替代方案：若 `3d1.png` 无法补齐，则改用已下载的 Figure 5 三面板（视频帧旋转）替代图 3，并在图题注明。

## 缺料项与处理

- `3d1.png`（Fig 4a）下载 406 → 用 `pdfimages` 从 PDF 取；仍失败则按上面的替代方案换图。
- 优化器、学习率、步数、batch、λ₁/λ₂、字典规模 M、三档结构差异 → 正文写「未披露」。
- 代码仓库 → 论文未见 → 正文写"未见代码仓库"。
- 333ms/帧口径 → 标「我们实测（二手整理）」，不写成论文数字。

## Decisions

- **D1 采用 10 节深读骨架**（用户要求完整结构与配图），不走"摘要档"。
- **D2 明确区分论文声明与事实核对**：Table 1 的"全指标最优"表述与 FID 原值冲突，正文照录 + 加事实核对注，不替论文改数。
- **D3 定性证据标注**：稀疏性与语义可控按"论文图示（定性）"标注，不写成定量结论。
- **D4 链接回补只在首现处挂一次**（《身份》86、《加速》83）。

## Risks / Trade-offs

- **可解释性主张仅定性** → 正文如实标注，并把它写进第 8 节局限。
- **多面板图拼接**（Fig 4 a/b/c）→ 用 Pillow 统一留白与白底；若三面板语义不齐（缺 Yaw）则换 Figure 5。
- **论文未披露项多** → 接受"未披露"占比高，不用推测填空。
