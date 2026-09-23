## Context

- **素材**（`.cache/article-note/float/`，已通过 `validate-analysis.py`）：**source tarball 抓取成功**——LaTeX 源码（`raw/source-tar/sec/0..6*.tex`、`preamble.tex`、`main.bbl`）为公式与图题的权威；`raw/source-tar/figure/*.pdf` 为 32 张矢量原图；`raw/sources/float.pdf` 取页码；`raw/sources/float.md` 是转换残片，不用。
- **论文元信息**：arXiv `2412.01064v5`（v1 2024-12-02，v5 2025-09-19）；标题 *FLOAT: Generative Motion Latent Flow Matching for Audio-driven Talking Portrait*；作者 Taekyung Ki、Dongchan Min、Gyeongsu Chae；单位 KAIST + DeepBrain AI（`main.tex` 首页邮箱与脚注）；**ICCV 2025**（arXiv comment）；项目页 `https://deepbrainai-research.github.io/float/`；论文未给出代码仓库（tex 内无 GitHub 链接）。
- **我方关联**：Avatar Forcing 复用 FLOAT 的 motion latent（我们实际接入的是 `models/avatarforcing/` 里重训过的版本，非 FLOAT 原权重）；因此本篇定位为「**上游源头 + 我们主线的基座**」，第 8 节只写定位与关联，不写对 FLOAT 原模型的实测。
- 用户已明确要求：与 liveportrait / lia-x 同等规格——完整 10 节结构 + 配图。

## Goals / Non-Goals

**Goals:**
- 按 `论文笔记/README.md` 的 10 节骨架成文；采用 6 张论文原图（矢量图栅格化 → WebP）并逐图配中文图题与解读
- 讲清两阶段机制：阶段一预训练 motion latent 空间（显式身份/运动分解 + 正交基），阶段二在该空间做 OT 流匹配生成运动并解码
- 关键结论附来源锚点（tex 文件 + 节标题 / 公式号 / 图表号），数字标来源档；未披露项写「未披露」

**Non-Goals:**
- 不写对 FLOAT 原权重/原代码的实测（未接入原模型）
- 不用「补充视频」类图充当证据；不为凑结构编造数字
- 不改其它笔记与概述正文（仅链接替换）

## 结构契约（10 节，含事实锚点）

| 节 | 标题 | 写什么（锚点） |
|---|---|---|
| 0 | 论文信息 | 表格：标题 / 作者 / 单位（KAIST、DeepBrain AI）/ venue（ICCV 2025）/ arXiv（`2412.01064v5`）/ 项目页 / 代码仓库（论文未给出）/ papers 库条目（`arxiv-2412.01064`，**注意尚未入本地 papers 库**） |
| 1 | 一句话总结 | 两阶段：① 用 LIA 系自编码器预训练出**具显式身份-运动分解与正交基的 motion latent 空间**；② 在该空间用 **OT 路径流匹配**生成 talking motion latent，再由 motion latent decoder 解码成视频；默认 NFE=10、Euler；情绪经 speech-driven 7 类 softmax + incremental CFV 控制（3_methods §4；`fig:overview`） |
| 2 | 问题与动机 | 像素空间扩散昂贵；整体面部 latent（VASA-1 类）容量大但不能直接编辑；情绪与姿态等条件缺乏可控接口（1_intro；2_related §2.2） |
| 3 | 方法精析 | 主链路：源图 → 编码器得 latent 并**显式分解**为身份项与运动项 → 构造驱动条件 $c_t$ → transformer 向量场预测器（**帧级 AdaLN + 帧级 gating + 掩码自注意力，窗口 $2T$ 邻帧**）→ 流匹配采样 → 解码。公式：latent 分解与正交基、流匹配目标（OT 直线插值）、条件构造、test-time 线性编辑闭式解（`eq:lambda`）；图 F2/F3/F4 |
| 4 | 训练与实现细节 | **阶段一**（suppl §A.4）：Adam、batch 8、lr $2\times10^{-4}$、460k steps、约 9 天、单张 A100；数据 HDTF + RAVDESS + VFHQ，预处理后 14,362 训练片段 / 49 测试片段；损失项与权重（$\lambda_{lp}=10$、$\lambda_{comp\text{-}lp}=100$、eye/lip adv=1、eye/lip FSM=100、full-adv=1；$\mathcal{L}_{comp\text{-}lp}$ 用 VGG-19 四级特征金字塔 $N=4$）；**阶段二**配置以 `analysis/experiment.md` 表格为准；未披露项照写 |
| 5 | 推理与系统链路 | 采样：NFE=10、Euler 一阶 ODE、$\gamma_a=2$、$\gamma_e=1$；效率随步数变化见 F5（V100）；Mermaid 推理时序；与我们链路的关系：Avatar Forcing 复用该 motion latent 空间（我们接入的是重训版），低维运动空间 + 轻量渲染是本仓库主线 |
| 6 | 实验与结果 | Table 1（HDTF/RAVDESS）：FID/FVD/LSE-D/LSE-C 最优，**CSIM 输 Hallo、E-FID/P-FID 输 EchoMimic**；**必须带 $^{\dagger}$ 脚注（原始 $256\times256$ 输出）**；Table 2 附加条件结果；消融：帧级 AdaLN 优于 cross-attention、flow matching 相比扩散在相当画质下唇同步更好且 NFE 更低、$\mathcal{L}_{comp\text{-}lp}$ 提升面部保真；图 F5（效率）、F6（情绪重定向） |
| 7 | 相关工作与定位 | 谱系：LIA/LivePortrait/Ditto（隐式运动表示 + warp）、VASA-1（整体 latent）、Hallo/EchoMimic/EDTalk/AniTalker/SadTalker（像素或 3DMM 条件扩散）；差异点：**正交基带来的 test-time 可编辑性**与流匹配的低 NFE |
| 8 | 局限与启发 | 论文局限（suppl §D）：情绪仅 7 类基本情感；训练数据偏正面（$\lvert\text{yaw}\rvert\ge20^\circ$ 或戴配件易失败）→ 图 F7；「论文局限 vs 我们结论」对照表（我方写：未接入原权重，但 Avatar Forcing 在同空间重训并加因果流式 + DPO，长时漂移治理见《数字人身份》）；可操作启发（低维可编辑空间 + 少量步数流匹配） |
| 9 | 术语与符号表 | motion latent / 正交基 / flow matching 与 OT 路径 / NFE / AdaLN / CFV（incremental classifier-free guidance for video）/ $\gamma_a,\gamma_e$ / 身份项与运动项符号 |
| 10 | 相关文档 | `[[论文笔记/avatar-forcing]]`（复用其 motion latent）、`[[论文笔记/ditto]]`、`[[论文笔记/liveportrait]]`、`[[数字人概述/数字人身份]]`、`[[数字人概述/数字人动作]]`、`[[数字人概述/数字人加速]]`、`knowledge/Avatar Forcing Motion Latent AutoEncoder`、项目页 |

## 图表与公式清单

| 图号 | 论文来源 | 落位 | 解读要点 |
|---|---|---|---|
| 图 1 | `fig:overview`（`overview-long-6.pdf`） | 3 方法精析 | 全链路：显式身份-运动分解 → 条件构造 → 流匹配生成 |
| 图 2 | `fig:cfmt`（`frame-wise-vector-field-predictor-block.pdf`） | 5 推理与系统链路 | 推理期逐帧向量场预测块的结构与上下文组织 |
| 图 3 | `fig:wo_comp_lp_1`（`wo_comp_loss_2-1.pdf`） | 6 实验与结果（消融） | $\mathcal{L}_{comp\text{-}lp}$ 对细粒度运动与保真的作用（实写作时由「3 方法精析」调整为消融小节，与图 4/5 同属实验证据） |
| 图 4 | `fig:fps`（`speed-w-steps.pdf`） | 6 实验与结果 | 效率随去噪步数的变化（V100） |
| 图 5 | `fig:emotion_redirection`（`emotion_redirection.pdf`） | 6 实验与结果 | 情绪预测可被显式重定向 + CFV 强化 |
| 图 6 | `fig:failure_case_supp1`（`failure_case.pdf`） | 8 局限与启发 | 非正面脸与配件的失败案例 |

- **公式**：3–4 个（motion latent 显式分解、流匹配目标 / OT 路径、条件构造、test-time 线性编辑闭式解），LaTeX 一律取自 `raw/source-tar/sec/*.tex` 原文。
- **Mermaid**：1 张（推理/条件构造时序）。
- 可选替换：F8 `fig:sota_compare`（定性对比）可替换图 3；F9 `fig:lambda_control`、F10 `fig:additional_condition`、F13 `fig:ood_supp` 作为备选，按图位取舍。
- **不采用**：依赖补充视频的图（`ecfg_scale_supp`、`ablation_diffusion_supp_*`）、重复的补充定性对比（`sota_comparison_supp_*`）、第一阶段可视化碎片、用户研究界面截图、跨来源对比（`emo-vasa-1`）。

## 缺料项与处理

- **FLOAT 不在本地 papers 库**（`data/papers.db` 无 `arxiv-2412.01064`）→ 正文「papers 库条目」按命名规范写 `arxiv-2412.01064` 并在 sidecar `notes` 里记明未入库；是否补录由用户决定，本轮不写库。
- 矢量图需先栅格化（`pdftoppm`/`pdftocairo`，长边 ≥1600px）再转 WebP——`figures.py convert` 只吃位图。
- tex 自定义节号与 PDF 页码口径不一致 → 引用统一写「文件名 + 节标题」，避免两种口径混用。
- 阶段二完整超参、向量场预测器层数等未披露项 → 正文写「未披露」。

## Decisions

- **D1 采用 10 节深读骨架**（与 liveportrait/lia-x 同规格），不走轻量档。
- **D2 定位为「上游基座 + 我方关联」**：第 8 节明确「未接入 FLOAT 原权重」，只写 Avatar Forcing 在同空间重训这一事实性关联。
- **D3 Table 1 引用必须带 $^{\dagger}$ 脚注**，并注明 FLOAT/Hallo/EchoMimic 分辨率未明示，避免读者误判同分辨率对比。
- **D4 链接回补首现处一次**：《数字人动作》42/63、《数字人身份》88、《数字人介绍与技术路线》91。
- **D5 图题标注「论文 Figure N」**，图号正文连续。

## Risks / Trade-offs

- **信息密度高但披露完整**（本论文超参披露度远高于 LivePortrait/LIA-X）→ 第 4 节可按披露表实写，避免「未披露」堆叠。
- **矢量图栅格化后体积** → 转 WebP 并限制长边/体积；若超限优先降采样而不是删图。
- **与《数字人身份》已有 Avatar Forcing 叙述重复** → 本篇只写 FLOAT 自身机制与血缘，流式改造/漂移治理仍归《数字人身份》与 `avatar-forcing` 笔记。
