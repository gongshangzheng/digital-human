---
title: 论文笔记
author: 汤问
date: 2026-09-22
tags: [digital-human, 论文笔记]
summary: 数字人论文/模型统一笔记库：一篇一个论文/模型、夹内平铺，含 10 节统一模板与篇目清单。
---

# 论文笔记

> 数字人论文/模型统一笔记库（技术路线总纲见 [[数字人概述/数字人介绍与技术路线|数字人介绍与技术路线]]），**一篇一个论文/模型**，夹内平铺、不嵌套。合并原"模型介绍"。
> 历史博客精读（~90 篇）已入 papers 库（带 blog_url），此处只写新写的笔记。

## 统一模板（10 节骨架，口径同 `article-note` skill 的 `references/note-structure-template.md`）

标题只用 `##` 与 `###`；公式用 `$...$`（行内）或 `$$...$$`（块级）写 LaTeX，渲染走 KaTeX，每个公式后配符号表与中文解释；需要保留未解析的原始 TeX 时可另附代码块（代码块内的 `$` 不参与解析）；图片用绝对 URL `/api/management/docs-assets/<slug>/<file>`，图题写成 `![图 N · 说明](url)`。

| 节 | 标题 | 职责 | 必备元素 |
|---|---|---|---|
| 0 | 论文信息 | 标题/作者/单位/venue/arXiv/项目页/代码仓库/papers 库条目 | 表格 |
| 1 | 一句话总结 | 价值主张 + 3–5 条贡献 | 列表 |
| 2 | 问题与动机 | 背景、矛盾、已有方法局限、insight | 数据点 + 动机图 |
| 3 | 方法精析 | 主链路、模块、公式、机制差异 | Mermaid + ≥2 公式 + 架构图 |
| 4 | 训练与实现细节 | 数据、预处理、优化、训练成本 | 10 项配置披露表 |
| 5 | 推理与系统链路 | 输入、生成、后处理、输出 | Mermaid 时序 |
| 6 | 实验与结果 | 配置、指标、基线、主结果、消融、失败案例 | 配置表 + 对比表 + 主结果图 |
| 7 | 相关工作与定位 | 前置工作及机制差异 | 对比表 |
| 8 | 局限与启发 | 作者局限、我们的实测结论、可操作启发 | 分层列表 + 「论文局限 vs 我们结论」对照表 |
| 9 | 术语与符号表 | 中英术语和变量 | 两张表 |
| 10 | 相关文档 | knowledge/ 精读链接、数字人概述链接、papers 库条目 | 链接列表 |

**工程层怎么放**：不再单列 `## 在我们体系中的角色` 大节。接入状态、我们的改动/优化/否证记录写进**第 8 节「局限与启发」的「我们的实测」子节**（并做「论文局限 vs 我们结论」对照），具体实验矩阵与代码细节外链到 `数字人概述/` 与相邻 `knowledge/` 专题，本篇不复制。

**为什么换**：旧模板的四节（`## 是什么` / `## 架构核心` / `## 在我们体系中的角色` / `## 与复盘各线的关联`）把「论文层」压得太粗，无法承载公式、消融、配置披露与配图；10 节骨架与 `article-note` 流水线（素材 → 分析 → 结构审批 → 写作 → 校验）配套，且每篇都有 sidecar `<slug>.json`。

## 现有清单

| 文件 | 定位 | 状态 |
|------|------|------|
| `avatar-forcing.md` | 深读 + 工程层（微调/漂移实验/流式接入） | ✅ 已完成（10 节骨架 + 6 图 + sidecar） |
| `ditto.md` | 深读 + 工程层（TRT 实时化/流式管线） | ✅ 已完成（10 节骨架 + 6 图 + sidecar） |
| `liveact.md` | 深读 + 工程层（SoulX-LiveAct 接入） | ✅ 已完成（10 节骨架 + 7 图 + sidecar） |
| `omnimate.md` | 深读 + 定位层（开放时长交互：GPC 进度条件 + MRCM 多参考身份） | ✅ 已完成（10 节骨架 + 5 图 + sidecar） |
| `interactive-avatar.md` | 深读（实时无限流式：RRM 意图感知 + 长短视觉记忆 + DMD）｜**与 `omnimate.md` 同团队**（西交大 + 中国电信 TeleAI，重叠作者 Quanyue Song / Yishan He / Zhixiang He / Caigui Jiang / Zhizhi Guo）｜论文 [arXiv:2606.22905](https://arxiv.org/abs/2606.22905) InteractiveAvatar: Real-Time Streaming Video Generation for Consistent and Intent-Aware Avatars | 待写 |
| `talker-t2av.md` | 深读 + 工程层（接入与验证）｜论文 [arXiv:2604.23586](https://arxiv.org/abs/2604.23586) Talker-T2AV: Joint Talking Audio-Video Generation with Autoregressive Diffusion Modeling | ✅ 已完成（10 节骨架 + 1 图 + 2 Mermaid + sidecar） |
| `liveportrait.md` | 深读 + 定位层（未接入：隐式关键点表示、stitching/retargeting 控制） | ✅ 已完成（10 节骨架 + 5 图 + sidecar） |
| `lia-x.md` | 深读 + 定位层（未接入：可解释 latent、40D motion code 与身份特征注入） | ✅ 已完成（10 节骨架 + 5 图 + sidecar） |
| `float.md` | 深读 + 定位层（基座：Avatar Forcing 复用的 motion latent 空间） | ✅ 已完成（10 节骨架 + 6 图 + sidecar） |
| `face-vid2vid.md` | 深读 + 定位层（LivePortrait 前置：3D 隐式关键点与 free-view） | ✅ 已完成（10 节骨架 + 6 图 + sidecar） |
| `performrecast.md` | 深读 + 定位层（未接入：FLAME 一致变换解耦表情/头姿、49 点显式监督、BAM；表情-only 编辑与两种推理模式）｜论文 [arXiv:2603.19731](https://arxiv.org/abs/2603.19731) PerformRecast: Expression and Head Pose Disentanglement for Portrait Video Editing | ✅ 已完成（10 节骨架 + 6 图 + sidecar，order: 90） |
| `fpsattention.md` | 深读（FP8 量化 × 稀疏注意力协同） | ✅ 已完成（10 节骨架 + 3 图 + sidecar，order: 130） |
| `blade.md` | 深读（块稀疏注意力 × 步数蒸馏联合训练） | ✅ 已完成（论文标注：2 图 + 5 公式 + sidecar） |
| `nar.md` | 深读（邻域自回归建模；需从头训练） | ✅ 已完成（论文标注：3 图 + 2 公式 + sidecar） |
| `flashar.md` | 深读（自回归生成的后训练加速；配图受抓取限制） | ✅ 已完成（论文标注：1 图 + 2 Mermaid + 10 公式 + sidecar） |
| `latent-spatial-memory.md` | 深读（隐空间空间记忆；注意：任务是相机轨迹 world model） | ✅ 已完成（论文标注：3 图 + 7 公式 + sidecar） |
| `worldattention.md` | 方案笔记（无同行评议论文：代码/README 证据；HSA 稀疏 + 分层 KV） | ✅ 已完成（D2 骨架 + 1 Mermaid + 2 公式 + sidecar） |
| `zipar.md` | 深读（空间局部性并行解码；零训练） | ✅ 已完成（论文标注：3 图 + 3 公式 + sidecar） |
| `dax.md` | 方案笔记（无同行评议论文：仓库 benchmark；算子/系统组合优化） | ✅ 已完成（D2 骨架 + 1 Mermaid + 2 公式 + sidecar） |
| `turbodiffusion.md` | 深读（步数蒸馏 + 系统优化栈；无原图，图均为无图题定性帧对比） | ✅ 已完成（2 Mermaid + 4 公式 + sidecar） |
| `inferix.md` | 深读（block-diffusion 推理引擎；证据等级＝引擎能力/待自测） | ✅ 已完成（2 图 + 2 Mermaid + 3 公式 + sidecar） |
| `vorch-streamer.md` | 深读（实时长时 T2AV 流式：后训练框架、暴露偏差与漂移治理、因果生成下“该说哪一段”）｜论文 [arXiv:2608.05663](https://arxiv.org/abs/2608.05663) Vorch-Streamer: Extending Human Audio-Visual Generation to Real-Time Long-Form Streaming | ✅ 已完成（10 节骨架 + 4 图 + sidecar，order: 40） |
| `causal-forcing.md` | 深读（自回归扩散蒸馏：frame-level injectivity 与条件期望解、TF 优于 DF、causal ODE + asymmetric DMD、causal CD；Avatar Forcing 被引最高的后续工作）｜论文 [arXiv:2602.02214](https://arxiv.org/abs/2602.02214) Causal Forcing: Autoregressive Diffusion Distillation Done Right for High-Quality Real-Time Interactive Video Generation | ✅ 已完成（10 节骨架 + 6 图 + sidecar） |
| `wan-streamer.md` | 深读（端到端实时交互基座）｜论文 [arXiv:2606.25041](https://arxiv.org/abs/2606.25041) Wan-Streamer v0.1: End-to-end Real-time Interactive Foundation Models | 待写 |
| `adaptok.md` | 深读（自适应 token 分配 + 时间因果的 1D 视频分词；用于「从视频提角色身份」的适用性评估，见 [[数字人概述/数字人领域问题|数字人领域问题]] 第七章）｜论文 [arXiv:2505.17011](https://arxiv.org/abs/2505.17011) Learning Adaptive and Temporally Causal Video Tokenization in a 1D Latent Space | ✅ 已完成（10 节骨架 + 5 图 + sidecar） |
| `tivtok.md` | 深读（时间不变/时变 token 分解：TIV 跨帧复用 + TV 逐帧残差，SIF 涌现分解、IB 广播解码；用于「从视频提角色身份」的适用性评估，见 [[数字人概述/数字人领域问题|数字人领域问题]] 第七章）｜论文 [arXiv:2606.17590](https://arxiv.org/abs/2606.17590) TivTok: Broadcasting Time-Invariant Tokens for Scalable Video Tokenization | ✅ 已完成（10 节骨架 + 5 图 + sidecar） |
| `rasa.md` | 深读（**跨身份角色动画**：把「跨身份空间映射」与「运动控制」两类能力的**固有纠缠**显式解耦，向 DiT 注入结构化先验；原话 the inherent entanglement of two capabilities）｜论文 [arXiv:2608.28219](https://arxiv.org/abs/2608.28219) RASA: Disentangled Spatial-Motional Priors for Cross-Identity Character Animation | 待写 |
| `facial-animation-disentangled.md` | 深读（**用 transformer 学 motion manifold** 并解耦身份与运动；可建模任意长度的 3D 几何序列）｜论文 *Computer Graphics Forum* 2022（cites=15, DOI 10.1111/cgf.14641）Facial Animation with Disentangled Identity and Motion using Transformers | 待写 |
| `style-disentangled-diffusion.md` | 深读（从 **multi-ID 数据集**学**每个说话人的个人风格**，引入 **style disentanglement module** 提升解耦度与可解释性；**语音驱动身体动作**）｜论文 ICASSP 2026（DOI 10.1109/icassp55912.2026.11462327）Style-Disentangled Diffusion for Controllable and Identity-Generalized Speech-Driven Body Motion Generation | 待写 |
| `pixel3dmm.md` | 深读（**单图 3D 人脸重建 / FLAME 跟踪**：screen-space 逐像素**法向 + UV** 先验（DINOv2 ViT-Base 特征，主干学习率降 10×，轻量头；作者明确说明 DPT 头只增加耗时、不提升下游重建）；PerformRecast 的**显式监督来源**，我们评测框架已有 `driving_mode: pixel3dmm`）｜论文 [arXiv:2505.00615](https://arxiv.org/abs/2505.00615) Pixel3DMM: Versatile Screen-Space Priors for Single-Image 3D Face Reconstruction（ICLR 2026，Giebenhain 等） | 待写 |


> **新增登记说明（2026-09-24，Pixel3DMM）**：
> - `pixel3dmm`（arXiv:2505.00615，ICLR 2026，Giebenhain 等）为本轮新增。它不是"又一篇生成模型"，而是 **tracking / 显式监督信号的来源**：[[论文笔记/performrecast|PerformRecast]] 靠它跟踪的 49 个显式 3D 关键点做 FLAME Loss，从而丢掉 LivePortrait 的四项辅助损失与第二阶段；FlexAvatar 用它给野外单图估 FLAME；UIKA 借它的 screen-space UV 配方（对照显示它在**头发边界处不如 UIKA 平滑**（UIKA 用的是 frozen DINOv3 + DPT head，与 Pixel3DMM 的 DINOv2 + 轻量头不是同一配方））。
> - **我们已经在用它**：`knowledge/3dgs-methods-research.md` 的依赖清单写了「Pixel3DMM（完整追踪功能需要）：`easy-pixel3dmm` + `pytorch3d` + `nvdiffrast`」，且评测框架已有 `driving_mode: pixel3dmm`——写笔记时这一层要单独交代。
> - **未入 papers 库**（既不在 `papers.db` 也不在 `blog_papers.json`），frontmatter 只登记 `arxiv_id`。
> - **引文纠错**：博客 `paper-performrecast` 的参考文献曾把 `arXiv:2505.00615` 的标题误写为 "A Large-Scale Dataset of 3D Face Annotations for Digital Humans"（**编号对、标题错**），本轮已修；`uika-2026` 页引的一直是正确标题。

> 新增登记说明（2026-09-23）：
> - `talker-t2av` 之前只在 papers 库之外（知识库固定阅读上游版本 `6712f62`），现已补上论文出处 arXiv:2604.23586（v2，2026-08-04）。
> - `vorch-streamer` 为本轮新增。它把我们这条主线里最核心的矛盾（自回归复用生成块作上下文 ⇒ exposure bias ⇒ 长时误差与视觉漂移累积）写成了首要困境，与 [[论文笔记/avatar-forcing|Avatar Forcing]]（历史 offset 递归）和 [[论文笔记/liveact|SoulX-LiveAct]]（ARPP/ConvKV）属同一问题的直接对照，建议与两者相邻阅读。

> 新增登记说明（2026-09-24）：
> - `interactive-avatar` 为本轮新增，**同队作品是 `omnimate` 而不是 `omniavatar`**：InteractiveAvatar（arXiv:2606.22905，2026-06）与 OmniMate（arXiv:2607.23023，2026-07）同属西交大 + 中国电信 TeleAI，重叠作者 Quanyue Song / Yishan He / Zhixiang He / Caigui Jiang / Zhizhi Guo；两者机制互补（前者攻长时视觉一致性与意图感知 RRM，后者攻开放式回合的 GPC 进度控制）。
> - **易混提醒**：OmniMate 的标题末尾就是 “for **Interactive Avatars**”，所以“OmniMate + InteractiveAvatar 同队”很容易被记成“OmniAvatar + InteractiveAvatar”；OmniAvatar（arXiv:2506.18866）是浙大 + 阿里的另一条线；另有 OmniHuman-1（arXiv:2502.01061）属字节跳动，不要与前两者并列。
> - `interactive-avatar` 未入 papers 库，将来写笔记时 frontmatter 只登记 `arxiv_id`。

> 新增登记说明（2026-09-23，第三批 · **身份 × 运动解耦**）：
> 以上三篇由「身份一致性 vs 运动风格」的边界调研引入（见 `openspec/changes/docs-identity-consistent-learning/research/identity-consistent-learning.md` §4.5）。三篇都指向**同一个上游命题**——身份与运动的**纠缠与解耦**，但**分解轴各不相同**：
> - `rasa`（2026，最新）：**能力分离** —— 跨身份空间映射 vs 运动控制
> - `facial-animation-disentangled`（CGF 2022）：**表示分离** —— motion manifold + 身份/运动解耦
> - `style-disentangled-diffusion`（ICASSP 2026）：**风格解耦 + multi-ID 个性化**（身体动作）
> **⚠ 易混提醒**：这三篇的解耦轴与本项目拟研究的「**时间不变性分离**（一条轨迹里"不变"vs"变"）」**不是同一条轴**。写笔记时须在第 8 节「局限与启发」里对照说清，**避免把不同轴的解耦当成同一件事**；也不得把该上游命题写成"我们发现的问题"。

## 生成侧加速十篇（素材已备）

上表最后十篇来自**视频推理加速**方向，素材已经在知识库与博客里（《视频生成训练与推理加速专题》与 `video-gen-acceleration`），**《数字人加速》里已点名这十个工作但还没加链接**——笔记写成后回该篇补链接。

## 命名规范

- 文件名 = 论文/模型短名 slug，frontmatter 必填 `arxiv_id`（有则填）、`papers_id`（**仅当该论文确实在 papers 库中时才写**；库只从博客精读清单 `blog_papers.json` 导入，其余论文留空）、`date`、`summary`、`tags`；每篇配同名 sidecar `<slug>.json`
- 每篇由独立单篇 change（`docs-note-<slug>`）实施：先「资料整理」后「动笔写作」
- 图片存 `management/docs/_assets/<slug>/`（与笔记 slug 对齐），引用用绝对 URL

> **同名论文易混提醒**：`avatar-forcing.md` 对应 `arXiv:2601.00664`（KAIST，CVPR 2026）。另有 `arXiv:2603.14331`「AvatarForcing: One-Step Streaming…」（浙大 + 快手 Kling）同名易混，不设本篇；引用前先看第 0 节的区分说明。
