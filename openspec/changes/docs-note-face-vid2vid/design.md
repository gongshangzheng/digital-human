## Context

- **素材**（`.cache/article-note/face-vid2vid/`，已通过 `validate-analysis.py`）：`raw/sources/face-vid2vid.html`（arXiv LaTeXML 全文，主源，含公式 LaTeX 与图题）+ `face-vid2vid.pdf`（16 页，**图号/页码权威**）；source tarball 抓取失败（406），无 LaTeX 源码；候选原图 8 张已下载到 `raw/figures/`。
- **论文元信息**：arXiv `2011.15126v3`（v1 2020-11-30，v3 2021-04-02）；标题 *One-Shot Free-View Neural Talking-Head Synthesis for Video Conferencing*；作者 Ting-Chun Wang、Arun Mallya、Ming-Yu Liu；单位 **NVIDIA Corporation**；**CVPR 2021（oral，arXiv comment）**；项目页 `https://nvlabs.github.io/face-vid2vid`；论文未给代码仓库链接。
- **图号口径**：LaTeXML 的 anchor/title 编号比 PDF 多 1，本工作区**统一采用 PDF 编号**，并已用 `pdftotext -layout` 逐图核对（Figure 3/4/6/8/10/14/15 与候选文件名一致）。
- **我方关联**：未接入该模型；它的价值是**谱系锚点**——LivePortrait 直接在其框架上升级，Ditto 的运动表示来自这条线；本文特有的「视频会议压缩」与《数字人概述/工程设计》的传输/带宽议题同源。

## Goals / Non-Goals

**Goals:**
- 按 `论文笔记/README.md` 的 10 节骨架成文；采用 6 张论文原图并逐图配中文图题与解读
- 讲清三件事：**3D 隐式关键点的三项分解**、**局部 free-view 的实现方式**、**低带宽传输（每帧 3K+6 标量）**
- 关键结论附来源锚点（章节 / 公式号 / 图号 / 表号 / 页码），数字标来源档；未披露项写「未披露」

**Non-Goals:**
- 不写对 Face Vid2vid 的实测（未接入）
- 不用「本工作区无位图」的图硬凑（Fig 12/13 不采用）
- 不改其它笔记与概述正文（仅 `liveportrait.md` 首现处的链接替换）

## 结构契约（10 节，含事实锚点）

| 节 | 标题 | 写什么（锚点） |
|---|---|---|
| 0 | 论文信息 | 表格：标题 / 作者 / 单位（NVIDIA Corporation）/ venue（CVPR 2021 oral）/ arXiv（`2011.15126v3`）/ 项目页 / 代码仓库（未给）/ papers 库条目（`arxiv-2011.15126`，**本地库未入库**） |
| 1 | 一句话总结 | 纯神经渲染、一次性（one-shot）、**可分解 3D 关键点**：身份（canonical 关键点）跨帧复用，运动只由「头姿（$R,t$）+ 表情形变 $\delta$」描述 → 局部 free-view + 低带宽（§3、§3.1、§5） |
| 2 | 问题与动机 | one-shot 说话头合成；视频会议场景的带宽约束；2D 关键点（FOMM）无法表达 3D 姿态、不能自由改视角（§1、§3.1） |
| 3 | 方法精析 | 三项分解（Eq. 1）与驱动帧的 3D 关键点计算（Eq. 2）；**不估 Jacobian**：假设头部近似刚体，取 $J_s=R_s$（与 FOMM 的机制差异）；生成侧：$K$ 个一阶近似 flow $w_k$ → 3D U-Net → softmax 组合掩码 $m_k$ → 线性合成 flow → warp 3D 外观特征 → 生成器 $G$，并额外预测遮挡掩码 $o$；图 V1/V2/V3 |
| 4 | 训练与实现细节 | 端到端联合训练 $F,\Delta,H,L,M,G$（App A.1 给各组件结构，含 DownBlock2D-64…1024、`1×1-Conv-16384`、`ResBlock3D-32×6`、`7×7×7-Conv-20/180/21`）；$H/\Delta$ 沿用 Ruiz et al. 架构、旋转角分 **66** 个 bin；6 项损失权重 $\lambda=10,1,20,10,20,5$（Eq. 3/6、App A.2）；感知损失用 VGG19 五层（权重 0.03125/0.0625/0.125/0.25/1.0）；默认 $K=20$；未披露项照写 |
| 5 | 推理与系统链路 | **free-view**：在 $R_d,t_d$ 上施加用户旋转/平移 $R_u,t_u$（局部自由视角）；**视频会议压缩**：只传关键点扰动 $\delta_{d,k}$ 与残差，等效 H.264 CRF36 下 **10.37×** 压缩、平均 **53.03 B/帧**（≈0.001618 bpp）、自适应后平均关键点 **20→11.52**；Mermaid 推理/传输时序；图 V4；与《工程设计》传输链路议题的关联 |
| 6 | 实验与结果 | Table 1 同身份重建、Table 2/4 跨身份迁移：**全部报告指标优于 fs-vid2vid / FOMM / FOMM-L / Bi-layer**；Table 3 正面化：identity/Both/FID 优于 pSp/RaR，**Angle 落后（90.9 vs 99.8）且论文未解释**；消融（two-step 关键点分解、3D warping、$K=20$、direct prediction 定量相近但**失去姿态控制**）；压缩对比（Table 6）；图 V5 |
| 7 | 相关工作与定位 | 2D 关键点线（FOMM、fs-vid2vid、Bi-layer）vs 本文的 3D 分解；正面化线（pSp、RaR）；与本仓库谱系：**Face Vid2vid → LivePortrait → Ditto**（3D 关键点/隐式表示 → 可缩放变换与可控模块 → 265 维运动空间） |
| 8 | 局限与启发 | 失败案例：有明显遮挡物（如手）时失败（Fig 14、图 V6）；论文未解释的 Angle 落后；Table 1 中 fs-vid2vid/FOMM-L 的 MS-SSIM 记为 `Nan` 且未说明；「论文局限 vs 我们结论」对照表（我方未接入，只记谱系与可复用机制）；可操作启发（可分解运动表示 → 姿态可编辑 + 低带宽） |
| 9 | 术语与符号表 | canonical keypoint、decomposable 3D keypoints、Jacobian（与 FOMM 的差异）、warp flow $w_k$、组合掩码 $m_k$、遮挡掩码 $o$、free-view、$3K+6$ 标量、perceptual / equivariance / prior 损失 |
| 10 | 相关文档 | `[[论文笔记/liveportrait]]`（下游升级，本篇是它的前置）、`[[论文笔记/ditto]]`、`[[数字人概述/数字人身份]]`、`[[数字人概述/数字人动作]]`、`[[数字人概述/工程设计]]`（传输/带宽）、项目页 |

## 图表与公式清单

| 图号 | 论文来源 | 落位 | 解读要点 |
|---|---|---|---|
| 图 1 | Figure 2（`fig-2-overview.png`） | 3 方法精析 | 外观来自源图、运动只用表情与头姿即可重建驱动视频 |
| 图 2 | Figure 3（`fig-3-feature-extraction.png`） | 3 方法精析 | 源/驱动两路特征提取与 3D canonical 关键点来源 |
| 图 3 | Figure 4（`fig-4-keypoint-pipeline.png`） | 3 方法精析 | **3D 隐式关键点在做什么**：逐点保留前 5 个关键点合成，直观展示每个点携带的信息 |
| 图 4 | Figure 10（`fig-10-compression.png`） | 5 推理与系统链路 | 视频会议压缩框架：只传关键点扰动与残差 |
| 图 5 | Figure 6（`fig-6-voxceleb-compare.png`） | 6 实验与结果 | VoxCeleb2 上的定性对比 |
| 图 6 | Figure 14（`fig-14-failure.png`） | 8 局限与启发 | 遮挡物（手）导致的失败案例 |

- **公式**：3–4 个（三项分解 Eq. 1、驱动帧关键点 Eq. 2、6 项总损失 Eq. 3/6、组合 flow 的线性合成），LaTeX 取自 HTML 的 `annotation`，写作时回 PDF 校对。
- **Mermaid**：1 张（推理与传输时序：关键点扰动 → 合成 → warp → 生成）。
- 可选（不占图位）：Figure 8（跨身份迁移）、Figure 15（binary residual 修压缩伪影）。
- **不采用**：teaser（小图网格）、Figure 12/13（HTML 无位图，需从 PDF 截且属实现细节）。

## 缺料项与处理

- **未入本地 papers 库**（`data/papers.db` 无 `arxiv-2011.15126`）→ 正文条目按规范写 `arxiv-2011.15126`，sidecar `notes` 记明；是否补录由用户决定。
- HTML 无 Figure 12/13 位图 → 不采用这两张。
- Table 1 的 `Nan` 与正面化 Angle 落后 → 照录原值 + 事实核对注，不替论文解释。
- 代码仓库未给出 → 正文写「论文未给出」。

## Decisions

- **D1 采用 10 节深读骨架**（与 liveportrait/lia-x/float 同规格）。
- **D2 定位为「谱系锚点 + 可复用机制」**：第 8 节明确未接入；把「可分解运动表示 → 姿态可编辑 + 低带宽」写成可操作启发。
- **D3 图号统一采用 PDF 编号**，与候选文件名一致（已逐图核对），避免 LaTeXML 的 +1 偏移。
- **D4 双向互链**：本篇第 10 节链 `liveportrait`；`liveportrait.md` 首现处回链本篇。

## Risks / Trade-offs

- **与 `liveportrait.md` 内容重叠**（Eq. 1、组件与损失同源）→ 本篇只写 Face Vid2vid 自身的机制与动机，LivePortrait 的升级点仍归其本笔记，不重复展开。
- **图片分辨率有限**（HTML 位图；`fig-6` 2.4MB、`fig-2` 1.6MB）→ 转 WebP 并降采样；`fig-10` 仅 66KB，若过小改用 PDF 提取版本。
- **论文年代较早（2020/2021）** → 评测协议与当代方法不可直接横比，正文只按论文自报口径引用并标注。
