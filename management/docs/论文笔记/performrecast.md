---
title: PerformRecast 模型笔记
author: 汤问
date: 2026-09-24
tags: [数字人, 模型笔记, PerformRecast, 表情编辑, 头姿解耦, FLAME, 显式3D关键点, 边界对齐]
arxiv_id: 2603.19731
order: 65
summary: PerformRecast（虎鲸文娱，CVPR 2026）指出 LivePortrait 的关键点变换运算顺序（先乘头姿再加表情）会让表情形变混入头姿信息，无法真正做到“只改表情、头不动”；改成与 FLAME 前向一致的先加表情再乘头姿后即继承 3DMM 的自然解耦，再用 Pixel3DMM 跟踪的 49 个显式 3D 关键点做 FLAME Loss 替掉四项辅助损失与第二训练阶段，并用边界对齐模块（BAM）修好面部/非面部边界错位；论文还构建了基于 MetaHuman 的表情编辑 benchmark，支持 Replacement 与 Enhancement 两种推理模式
---

# PerformRecast

## 论文信息

| 项 | 值 |
|---|---|
| 标题 | PerformRecast: Expression and Head Pose Disentanglement for Portrait Video Editing |
| 作者 | Jiadong Liang、Bojun Xiong、Jie Tian、Hua Li、Xiao Long、Yong Zheng、Huan Fu |
| 单位 | HUJING Digital Media & Entertainment Group（虎鲸文娱） |
| venue / 年份 | CVPR 2026（博客登记；arXiv 正文未声明会议，引用时须注明该口径） |
| arXiv | `2603.19731v1` |
| 代码 / 数据 | https://github.com/youku-aigc/PerformRecast（论文称开源代码与数据） |
| papers 库 | **未入库**（frontmatter 只写 `arxiv_id`，不写 `papers_id`） |

## 一句话总结

**把 warping 类肖像动画的关键点变换公式改成与 3DMM（FLAME）一致，就免费继承了「表情与头姿解耦」。**

- **一个公式改动**：LivePortrait 是 $x=s\cdot(x_c R+\delta)+t$（先乘头姿再加表情），PerformRecast 改成 $x=s\cdot((x_c+\delta)R)+t$（先加表情再乘头姿），与 FLAME 前向过程一致，使表情形变 $\delta$ 在规范空间中定义、不再混入头姿信息。
- **显式监督替掉隐式约束**：用 Pixel3DMM 从视频跟踪 FLAME 参数，取 **49 个显式 3D 关键点**分三组（$V_c$ / $V_{exp}$ / $V_{kp}$）用 Wing Loss 直接监督运动提取器，从而丢弃 LivePortrait 的**四项辅助损失**（等变、关键点先验、形变先验、头姿），且**不需要** LivePortrait 的第二阶段（stitching / retargeting）。
- **边界对齐模块（BAM）**：用 Teacher-Student 架构把面部与非面部区域分开监督，解决表情编辑时关键点运动场越界导致的面部边界错位。
- **两种推理模式**：Replacement（只替换表情 $\delta_d$）与 Enhancement（叠加表情增量 $\delta_{d,i}-\delta_{d,0}$），分别对应「整段表演替换」与「局部增强」两种后期场景；并构建了基于 MetaHuman 的表情编辑 benchmark。

## 问题与动机

任务设定：**expression-only portrait video performance editing**——给一段已有视频，只修改演员的面部表情，严格保持头部姿态、镜头运动、背景与身份不变。

这与主流的**肖像动画**（portrait animation）有本质区别：肖像动画是「从静到动」（用驱动视频驱动一张静态照片），表情编辑是「**从动到动**」（修改已有视频中的表情）。后者对解耦的要求更硬——一旦头姿被动，整个镜头就废了。

论文的判断是：**大多数现有方法（无论 GAN 还是 Diffusion）都做不到表情与头姿的真正解耦**。根因不在容量，而在**运动表示的数学结构**：

- LivePortrait 的关键点变换是 $x_{s}=s_s\cdot(x_{c,s}R_s+\delta_s)+t_s$，即**先乘头姿 $R$ 再加表情 $\delta$**。
- 因为旋转会改变表情形变在 3D 空间中的基准方向，$\delta$ 里不可避免会混入头姿信息，模型无法精确控制「只改表情」。
- 而 3DMM（FLAME）天然用独立参数表示身份、表情、头姿，是**自然解耦**的：它先加身份与表情混合形状、再乘头姿旋转。

![图 1 · 任务示意：上排编辑源视频中演员的表情，下排用驾驶视频动画化静态肖像（论文 Figure 1）](/api/management/docs-assets/performrecast/teaser.webp)

图 1 给出本文的两种能力。它支撑「同一个模型既能做表情编辑、也能做肖像动画」这一主张；注意它展示的是效果而非机制，机制在下文。

运算顺序的差异是整篇论文的题眼：

```mermaid
flowchart TB
    subgraph LP["LivePortrait：先旋转再加表情"]
        A1["规范关键点 $$x_c$$"] --> A2["乘头姿 $$R$$"]
        A2 --> A3["加表情 $$\delta$$"]
        A3 --> A4["缩放 $$s$$ + 平移 $$t$$"]
    end
    subgraph PR["PerformRecast：先加表情再旋转"]
        B1["规范关键点 $$x_c$$"] --> B2["加表情 $$\delta$$"]
        B2 --> B3["乘头姿 $$R$$"]
        B3 --> B4["缩放 $$s$$ + 平移 $$t$$"]
    end
    subgraph FL["FLAME 3DMM"]
        C1["模板网格 $$T$$"] --> C2["加身份 $$B_S$$ + 表情 $$B_E$$"]
        C2 --> C3["乘头姿 $$\theta$$"]
    end
    PR -.->|与 FLAME 一致| FL
```

## 方法精析

### 预备：LivePortrait 与 Pixel3DMM

PerformRecast 建立在 LivePortrait 的框架上：外观特征提取器 $\mathcal{F}$（本工作换成 **DINOv2** 预训练 backbone）、运动提取器 $\mathcal{M}$（**ConvNeXt-V2-Tiny**）、warping 模块 $\mathcal{W}$ 与 SPADE 解码器 $\mathcal{G}$。运动提取器从源帧与驱动帧预测规范关键点 $x_c\in\mathbb{R}^{K\times3}$、头姿 $R\in\mathbb{R}^{3\times3}$、表情形变 $\delta\in\mathbb{R}^{K\times3}$、缩放 $s\in\mathbb{R}^3$ 与平移 $t\in\mathbb{R}^3$。

LivePortrait 的变换公式（式 1）：

$$
\left\{
\begin{array}{lr}
x_{s}=s_{s}\cdot(x_{c,s}R_{s}+\delta_{s})+t_{s},&\\
x_{d}=s_{d}\cdot(x_{c,s}R_{d}+\delta_{d})+t_{d},&
\end{array}
\right.
$$

| 符号 | 含义 |
|---|---|
| $x_c$ | 规范关键点（canonical），源帧与驱动帧共享同一组 |
| $R$ | 头部姿态旋转（$3\times3$） |
| $\delta$ | 表情形变（每关键点 3 维） |
| $s,t$ | 缩放因子（3 维）与平移（3 维） |
| 下标 $s,d$ | 源帧 / 驱动帧 |

同时用 **Pixel3DMM** 从输入视频跟踪每帧的 FLAME 参数：身份 $\beta\in\mathbb{R}^{300}$、表情 $\psi\in\mathbb{R}^{100}$、头姿 $\theta\in\mathbb{R}^{15}$（颈、下颌、左右眼球四个关节各一个 3 维旋转，加一个全局头姿旋转）。

FLAME 的前向过程（式 2）：

$$
M(\beta,\theta,\psi)=W(T_P(\beta,\theta,\psi),\mathbf{J}(\beta),\theta,\mathcal{W}),\quad
T_P(\beta,\theta,\psi)=\mathbf{T}+B_S(\beta;\mathcal{S})+B_P(\theta;\mathcal{P})+B_E(\psi;\mathcal{E})
$$

| 符号 | 含义 |
|---|---|
| $\mathbf{T}$ | 零姿态、零表情下的模板网格 |
| $B_S(\beta;\mathcal{S})$ | 身份混合形状 |
| $B_E(\psi;\mathcal{E})$ | 表情混合形状 |
| $B_P(\theta;\mathcal{P})$ | 姿态混合形状（本任务不需要） |
| $W(\cdot)$ | 线性混合蒙皮 |

关键点在于：FLAME 是**先加身份与表情形变、再乘头姿旋转**。PerformRecast 只需把 LivePortrait 的公式改成同一顺序。

### FLAME 一致的关键点变换

改进后的变换公式（式 3）：

$$
\left\{
\begin{array}{lr}
x_{s}=s_{s}\cdot\big((x_{c,s}+\delta_{s})R_{s}\big)+t_{s},&\\
x_{d}=s_{d}\cdot\big((x_{c,s}+\delta_{d})R_{d}\big)+t_{d},&
\end{array}
\right.
$$

$\delta$ 现在在规范空间中定义，旋转统一施加在「已塑形」的关键点上，头姿与表情在数学上解耦。

![图 2 · 框架总览：运动提取器出规范关键点/头姿/表情形变/缩放/平移，改进后的变换结果与 Pixel3DMM 跟踪结果算 FLAME Loss，再经 warping 与解码器重建（论文 Figure 2）](/api/management/docs-assets/performrecast/ljd_method.webp)

### 三组显式关键点与 FLAME Loss

改公式只是第一步。为了让运动提取器学到**有物理意义**的关键点，论文从 Pixel3DMM 重建的 FLAME 网格顶点上选取 $K=49$ 个显式 3D 关键点，分三组监督（层次递进，每组只引入一个新变量）：

| 关键点组 | 从哪个网格提取 | 含哪些因素 | 监督对象 |
|---|---|---|---|
| $V_{c,i}$ | 规范网格 $T_c$（头姿、表情置零） | 只含身份形变 | $x_c$ |
| $V_{exp,i}$ | $T_{exp}$（加表情 + 下颌/眼球关节，颈与全局头姿置零） | 身份 + 表情 | $x_c+\delta$ |
| $V_{kp,i}$ | $T_{kp}$（全部 FLAME 参数启用） | 身份 + 表情 + 头姿 | $x_s$ / $x_d$ |

FLAME Loss 用 Wing Loss 计算三组关键点与对应变换结果的距离（式 4）：

$$
\mathcal{L}_{\text{FLAME}}=\text{Wing}(x_{c,s},V_{c,s})+\text{Wing}(x_{c,d},V_{c,d})
+\text{Wing}(x_{c,s}+\delta,V_{\text{exp},s})+\text{Wing}(x_{c,d}+\delta,V_{\text{exp},d})
+\text{Wing}(x_{s},V_{\text{kp},s})+\text{Wing}(x_{d,\text{self}},V_{\text{kp},d})
$$

| 符号 | 含义 |
|---|---|
| $\text{Wing}(\cdot,\cdot)$ | Wing Loss，对 landmark 局部误差更敏感 |
| $x_{d,\text{self}}=s_d\cdot((x_{c,d}+\delta_d)R_d)+t_d$ | 额外算的自驱动关键点（用驱动帧自己的参数），加速训练 |
| $V_{\text{exp}}$ 排除颈与全局头姿 | 因为表情主要含眼球朝向与下颌运动，不含颈部旋转 |

![图 3 · 49 个显式 3D 关键点在 FLAME 网格上的分布，覆盖前额、眉毛、眼眶、眼球、鼻子、嘴唇与下颌（论文 Figure 4）](/api/management/docs-assets/performrecast/keypoints.webp)

图 3 说明监督信号的空间覆盖。它支撑「显式关键点之所以能替掉隐式约束，是因为它在几何上覆盖了面部的主要运动区域」这一结论。

**丢弃四项辅助损失**：因为 FLAME Loss 提供了远比 LivePortrait 原损失更强的监督，PerformRecast 丢弃了隐式关键点等变损失、关键点先验损失、形变先验损失与头姿损失；头姿 $R$ 通过自监督即可学好。此外，由于解耦更好，**不需要** LivePortrait 的第二阶段（stitching 与 retargeting 模块）。

总损失（式 5）：

$$
\mathcal{L}_{\text{animate}}=\mathcal{L}_{\text{FLAME}}+\mathcal{L}_{P,\text{cascade}}+\mathcal{L}_{1,\text{cascade}}+\mathcal{L}_{G,\text{cascade}}+\mathcal{L}_{\text{faceid}}
$$

| 符号 | 含义 |
|---|---|
| $\mathcal{L}_{P,\text{cascade}}$ | 级联感知损失，在全局/面部/嘴唇三区分别计算 |
| $\mathcal{L}_{1,\text{cascade}}$ | 级联 $L_1$ 损失，同样三区 |
| $\mathcal{L}_{G,\text{cascade}}$ | 级联 GAN 损失（全局/面部/嘴唇三个从零训练的判别器） |
| $\mathcal{L}_{\text{faceid}}$ | ArcFace 身份保持损失 |

### 边界对齐模块（BAM）

表情编辑有一个特有失败：只替换表情而保持头姿时，warping 模块生成的**关键点运动场会越界影响面部以外区域**，导致面部与非面部之间出现错位。

BAM 用 Teacher-Student 架构解决（式 7、8）：

$$
\mathcal{L}_{\text{facial}}=\mathcal{L}_{P,\text{facial}}+\mathcal{L}_{1,\text{facial}},\qquad
\mathcal{L}_{\text{non-facial}}=\mathcal{L}_{P,\text{non-facial}}+\mathcal{L}_{1,\text{non-facial}}
$$

| 符号 | 含义 |
|---|---|
| Teacher $M_t$ | 用完整动画损失（式 5）训练；面部区域表情精确，但全局有错位 |
| $\hat{I}_s^t$ | Teacher 对源帧只替换表情后的中间结果 |
| Student $M_s$ | 面部区：对比 Teacher 的 $\hat{I}_s^t$；非面部区：对比源帧 $I_s$ |
| $\mathcal{L}_{\text{facial}}$ / $\mathcal{L}_{\text{non-facial}}$ | 分别在面部/非面部区域计算的感知 + $L_1$ |

![图 4 · BAM：上为 Teacher-Student 分区监督，下为有无 BAM 的视觉对比（红圈标出错位区域）（论文 Figure 3）](/api/management/docs-assets/performrecast/teacher-student.webp)

图 4 是 BAM 的必要性证据：没有 BAM 时面部边界出现明显错位（红圈处），有 BAM 后消失。

## 训练与实现细节

整体是 **Teacher-Student 两阶段**：先用 $\mathcal{L}_{\text{animate}}$ 训 Teacher $M_t$，再训 Student $M_s$（在 $\mathcal{L}_{\text{animate}}$ 之外加 BAM 的 $\mathcal{L}_{\text{facial}}$ 与 $\mathcal{L}_{\text{non-facial}}$）。训练时对关键点 $x_s,x_d$ 加小方差高斯噪声提升鲁棒性，推理时不加。

十项配置披露表：

| # | 项 | 值 | 披露 |
|---|---|---|---|
| 1 | 数据集 | VFHQ、MEAD、Nersemble、FEED、ETH-XGaze + 网络视频（含高清动画与影视） | 已披露 |
| 2 | 数据规模 | **597,331** video clips | 已披露 |
| 3 | 预处理 | 输入输出 $512\times512$；MetaHuman 原始 $2560\times1440$ 裁成方图并缩放 | 已披露 |
| 4 | 模型初始化 | 外观提取器基于预训练 DINOv2；模型主体从头训练 | 已披露 |
| 5 | batch size | 8 per GPU | 已披露 |
| 6 | 学习率 / 调度 | 外观 $5\times10^{-5}$；运动 / warp / 解码器 $1.2\times10^{-4}$；全局/面部/嘴唇判别器 $1\times10^{-4}$ / $2.5\times10^{-5}$ / $1.5\times10^{-5}$；**调度未披露** | 部分 |
| 7 | 优化器 | Adam | 已披露 |
| 8 | 训练轮数 / 步数 | **未披露**（仅给总时长约 1 周） | 部分 |
| 9 | 硬件 / 成本 | **128 × NVIDIA H20，约 1 周** | 已披露 |
| 10 | 随机种子 / 复现 | **未披露**；代码与数据开源 | 部分 |

BAM 的面部/非面部 mask 计算：用 LivePortrait 的预训练 2D landmark 检测器提每帧 203 个 landmark，将源帧 landmark 外扩后取凸包作为面部区域，其余为非面部区域。

## 推理与系统链路

论文给出三种推理设定：

```mermaid
flowchart LR
    S["源视频帧 $$I_{s,i}$$"] --> F["外观提取 $$\mathcal{F}$$（DINOv2）"]
    S --> M["运动提取 $$\mathcal{M}$$（ConvNeXt-V2-Tiny）"]
    D["驱动视频帧 $$I_{d,i}$$"] --> M
    M --> X["关键点变换：Replacement 只换 $$\delta_d$$；Enhancement 叠加 $$\delta_{d,i}-\delta_{d,0}$$"]
    F --> W["warping $$\mathcal{W}$$"]
    X --> W
    W --> G["SPADE 解码器 $$\mathcal{G}$$"]
    G --> O["输出帧"]
```

**Replacement 模式**（式 6）：

$$
\left\{
\begin{array}{lr}
x_{s}=s_{s}\cdot\big((x_{c,s}+\delta_{s})R_{s}\big)+t_{s},&\\
x_{d}=s_{s}\cdot\big((x_{c,s}+\delta_{d})R_{s}\big)+t_{s},&
\end{array}
\right.
$$

缩放、头姿、平移全部来自源帧，**只有表情 $\delta_d$ 来自驱动帧**——纯「只换表情」。

**Enhancement 模式**（式 9）：

$$
\left\{
\begin{array}{lr}
x_{s,i}=s_{s,i}\cdot\big((x_{c,s}+\delta_{s,i})R_{s,i}\big)+t_{s,i},&\\
x_{d,i}=s_{s,i}\cdot\big((x_{c,s}+\delta_{s,i}+\delta_{d,i}-\delta_{d,0})R_{s,i}\big)+t_{s,i}.&
\end{array}
\right.
$$

用驱动视频的表情**增量** $\delta_{d,i}-\delta_{d,0}$ 叠加到源帧原始表情 $\delta_{s,i}$ 上，适用于「表演基本可用、只需局部增强」。

**肖像动画**：训练同款变换（式 3），驱动帧的 $s_d,R_d,\delta_d,t_d$ 全部来自驱动帧，外观 $f_s=\mathcal{F}(I_s)$ 来自源帧。

![图 5 · 两种推理模式的典型使用场景（论文 Figure 5）](/api/management/docs-assets/performrecast/two_infer_modes.webp)

推理效率：论文称在**消费级 GPU** 上达到 **6 images/second**（具体型号未披露）。相比多步去噪的扩散方法，这是 GAN-warping 路线的部署优势。

## 实验与结果

### MetaHuman 测试 benchmark

论文自行构建：从 18 段专业面部动作演员的表演视频提取表情参数；选 20 个 MetaHuman 数字人，每个渲染 19 段视频（18 段带表情 + 1 段无表情），所有视频加预定义头姿旋转。原始 $2560\times1440$、150 帧、30 FPS，裁方后缩放至 $512\times512$。Replacement 模式随机取一种表情为源、另一种为驱动；Enhancement 模式取无表情视频为源。两模式各得 20 组 source-driving-GT 三元组。

### 表情编辑主结果（Table 1，Replacement 与 Enhancement 两列）

| 方法 | PSNR↑ | SSIM↑ | LPIPS↓ | CSIM↑ | MAE(°)↓ | AED↓ | APD↓ | FID↓ | FVD↓ |
|---|---|---|---|---|---|---|---|---|---|
| SkyReels-A1 | 24.91 | 0.859 | 0.162 | 0.716 | 13.08 | 0.716 | 0.016 | 50.20 | 1249.70 |
| Hunyuan-Portrait | 22.43 | 0.792 | 0.169 | 0.736 | 10.40 | 0.661 | 0.035 | 38.60 | 1925.07 |
| FantasyPortrait | 23.95 | 0.820 | 0.188 | 0.734 | 16.78 | 0.795 | 0.017 | 60.44 | 606.63 |
| Wan-Animate | 22.82 | 0.802 | 0.132 | 0.614 | 11.97 | 0.700 | 0.024 | 28.10 | 849.22 |
| Act-Two（闭源商用） | 20.83 | 0.791 | 0.163 | 0.682 | 15.96 | 0.790 | 0.072 | 36.19 | 322.07 |
| LivePortrait | 27.73 | 0.899 | 0.059 | 0.749 | 10.47 | 0.610 | 0.016 | 14.36 | 165.10 |
| **PerformRecast（Replacement）** | **29.27** | **0.914** | **0.047** | **0.761** | **9.12** | **0.499** | **0.012** | **12.01** | **102.99** |
| **PerformRecast（Enhancement）** | **30.27** | **0.922** | **0.039** | **0.819** | **6.82** | **0.447** | **0.010** | **10.77** | **90.25** |

读法：Replacement 模式下 PerformRecast 全面领先，PSNR 比 LivePortrait 高 1.54、FID 低 2.35、FVD 低 62.11；Enhancement 模式各项更进一步。四个被改造的扩散方法即使改成「锁源帧头姿 + 用驱动表情」也仍明显落后——论文把原因归为扩散方法本身不具备 expression-only 编辑能力（论文不在正文做它们的定性对比）。

### 消融（Table 1 下半）

| 变体 | PSNR↑ | FID↓ | FVD↓ | 相对完整模型的掉点 |
|---|---|---|---|---|
| 完整模型 | 29.27 | 12.01 | 102.99 | — |
| w/ LP 关键点变换（换回 LivePortrait 公式） | 27.06 | 27.68 | 288.84 | PSNR −2.21，FID 翻倍+ |
| w/o FLAME Loss | 24.99 | 18.40 | 188.11 | PSNR −4.29（掉点最多） |
| w/o BAM（去 Teacher-Student） | 27.73 | 14.41 | 136.41 | PSNR −1.54，FID +2.40 |

结论：**FLAME Loss 是最关键组件**（去掉后 PSNR 掉 4.29）；**公式改动是其次**（换回 LivePortrait 公式 FID 由 12.01 涨到 27.68）；BAM 主要在像素级指标与边界视觉质量上起作用。注意消融里换回 LivePortrait 公式的变体仍保留了 FLAME Loss 等其他部分，因此它单独测的是「公式顺序」的贡献。

### 肖像动画（Table 2，VFHQ 官方测试集 50 视频）

Self-reenactment（左半）与 cross-reenactment（右半，仅 CSIM/MAE/AED/APD）：

| 方法 | PSNR↑ | SSIM↑ | LPIPS↓ | CSIM↑ | MAE(°)↓ | AED↓ | cross CSIM↑ | cross MAE↓ |
|---|---|---|---|---|---|---|---|---|
| LivePortrait | 22.88 | 0.7891 | 0.165 | 0.8008 | 6.595 | 0.3419 | 0.6595 | 12.63 |
| FYE | 20.19 | 0.7168 | 0.2118 | 0.7618 | 11.83 | 0.5676 | 0.7187 | 15.44 |
| AniPortrait | 21.03 | 0.7334 | 0.1809 | 0.7654 | 10.01 | 0.4143 | 0.6894 | 18.69 |
| **PerformRecast** | 22.71 | **0.7895** | **0.159** | **0.8434** | **4.998** | **0.2606** | 0.6966 | **10.96** |

论文结论：self-reenactment 上除 PSNR 外所有指标最优；cross-reenactment 上表情精度最优。**两处非全面领先须保留**：self 的 PSNR 略低于 LivePortrait（22.71 vs 22.88）；cross 的 CSIM，FYE（0.7187）高于 PerformRecast（0.6966）——论文解释 FYE 等身份相似度更高但其余指标全面落后，并指出 EMOPortrait 的 MAE/APD 更低但背景严重模糊。

附表 **Table 3**（MEAD self-reenactment，随机划分 70 视频）：论文称 PerformRecast 在**所有指标**上最优（附录 K.2）。

### 失败案例

![图 6 · 典型失败案例：源视频闭嘴而驱动视频张嘴时，牙齿区域模糊（论文 Figure 10/15）](/api/management/docs-assets/performrecast/limitation.webp)

当源视频嘴巴闭合、驱动需要张嘴时，模型在**牙齿区域**产生模糊。作者归因于 **GAN 的生成上限**：它本质是「搬移」而非「生成」，无法像扩散模型那样合成源视频中不可见的内容。这是 GAN-warping 路线相对扩散路线的固有代价。

## 相关工作与定位

| 方法 | 运动表示 | 表情/头姿解耦 | 生成能力 | 与 PerformRecast 的关系 |
|---|---|---|---|---|
| Face Vid2vid | 可分解 3D 隐式关键点（canonical + 头姿 + 形变） | 三项分解但隐式 | warp + GAN | 谱系上游：确立隐式关键点三项分解 |
| LivePortrait | 隐式关键点 + scale factor + stitching/retargeting | 运算顺序导致 $\delta$ 混入头姿 | warp + GAN | 直接基座；本文改其公式、去其第二训练阶段 |
| 扩散类（SkyReels-A1 / Hunyuan-Portrait / FantasyPortrait / Wan-Animate / Act-Two） | 视频 latent 或隐式表示 | 难以解耦，需额外改造 | 可合成未见内容 | 被本文改造后仍不擅长 expression-only 编辑 |
| **PerformRecast** | **显式 49 点 FLAME 关键点**（+ FLAME 一致变换） | **数学解耦** | warp + GAN（未见区域弱） | 用 3DMM 的数学结构约束 warping 表示 |

一句话定位：**它不提出新网络，而是用 3DMM 的数学结构去约束 warping 方法的运动表示**——把「堆损失约束隐式关键点」换成「让变换公式与物理模型一致 + 用显式 3D 关键点直接监督」。

## 局限与启发

### 论文自己承认的局限

- **GAN 生成上限**：无法合成源视频中不可见的区域（闭嘴时的牙齿），失败案例见上。
- 论文把未来方向定为「**3DMM 的解耦能力 + 大规模预训练扩散模型的生成能力**」结合。
- 49 个关键点的选取是**手工设计**的，能否自动学最优配置未回答。
- 学习率调度、checkpoint 策略、随机种子、6 FPS 的 GPU 型号均**未披露**。

### 论文缺口 vs 我们结论

| 论文承认/未披露 | 我们的结论 |
|---|---|
| 未知区域（牙齿）生成模糊 | **未接入**，无第一手结论；登记为「GAN-warping 路线的素材边界」——不适合需要合成未见内容的镜头 |
| 训练超参不完整（调度/种子/步数）、性能型号未披露 | **未接入**；照搬其训练配方有风险，但「公式改动 + 显式监督」的机制可直接借鉴 |
| 手工选 49 个关键点 | **未接入**；记录为该表示的一个开放设计点 |
| self 的 PSNR、cross 的 CSIM 非最优 | 只照录，不替论文解释；引用时保留例外 |

### 可操作启发

1. **公式一致性 > 损失堆叠**。让关键点变换与 FLAME 一致，比堆更多辅助损失更有效——对任何需要解耦（姿态/表情/身份）的任务，先问「我的变换公式与物理模型一致吗」，往往比加损失更省。
2. **显式监督 > 隐式学习**。当有可靠外部工具（Pixel3DMM）能给监督时，直接用显式 3D 关键点监督，可以丢掉大量为隐式表示发明的正则项，这是它能否掉四项损失的原因。
3. **Teacher-Student 分区监督是通用模式**。当全局损失在某个区域造成质量下降时，训一个 Teacher 提供该区域的局部监督，是可以复用的工程手段。
4. **GAN 的生成上限要提前算进选型**。它擅长「搬移已知内容」，不擅长「合成未见内容」；需要后者时扩散仍不可替代。

## 术语与符号表

| 术语 | 英文 | 含义 |
|---|---|---|
| 表情-only 编辑 | expression-only portrait video performance editing | 只改已有视频的表情，头姿/镜头/背景/身份不变 |
| 肖像动画 | portrait animation | 用驱动视频驱动静态肖像 |
| 规范关键点 | canonical keypoints | $x_c$，源/驱动共享，编码身份几何 |
| 表情形变 | expression deformation | $\delta$，每关键点 3 维 |
| 缩放正交投影 | scale orthographic projection | $x=s\cdot(\cdot)+t$ 的形式 |
| 等变损失 | equivariance loss | 施加已知 2D 变换后关键点应按同变换改变（本文丢弃） |
| 边界对齐模块 | Boundary Alignment Module (BAM) | Teacher-Student 分区监督 |
| 3DMM / FLAME | 3D Morphable Face Model / FLAME | 用独立参数表示身份/表情/头姿的参数模型 |
| Wing Loss | — | 对 landmark 局部误差更敏感的损失 |

| 符号 | 含义 |
|---|---|
| $x_c,x_s,x_d$ | 规范 / 源 / 驱动关键点 |
| $R,s,t$ | 头姿旋转、缩放、平移 |
| $\delta$ | 表情形变 |
| $\beta,\psi,\theta$ | FLAME 身份、表情、头姿参数 |
| $V_c,V_{exp},V_{kp}$ | 三组显式 3D 关键点 |
| $x_{d,\text{self}}$ | 驱动帧自驱动关键点（加速训练用） |
| $M_t,M_s$ | Teacher / Student 模型 |
| $\hat{I}_s^t$ | Teacher 的面部表情替换中间结果 |
| $\mathcal{L}_{\text{FLAME}},\mathcal{L}_{\text{animate}}$ | FLAME Loss / 总动画损失 |
| $\mathcal{L}_{\text{facial}},\mathcal{L}_{\text{non-facial}}$ | BAM 分区损失 |

**易混提示**：`Replacement` 与 `Enhancement` 是两种**推理模式**，不是训练阶段；论文的 Training Pipeline 是 Teacher-Student **两阶段**。另外，Table 1/2 中 `MAE` 指眼球方向的平均角度误差，`AED/APD` 指平均表情/姿态距离，量纲各不相同，不可跨列比较。

## 相关文档

- 谱系上游（本篇的直接基座）：[[论文笔记/liveportrait|LivePortrait 模型笔记]]、[[论文笔记/face-vid2vid|Face Vid2vid 模型笔记]]
- 下游使用该运动空间：[[论文笔记/ditto|Ditto 模型笔记]]、[[论文笔记/avatar-forcing|Avatar Forcing 模型笔记]]
- 主题文档：[[数字人概述/数字人身份|数字人身份]]、[[数字人概述/数字人动作|数字人动作]]
- 文献地图：[[数字人概述/数字人关键技术地图|数字人关键技术谱系]]（隐式关键点与潜空间导航）
- 背景：[[knowledge/数字人基础|数字人基础]]
- 代码：https://github.com/youku-aigc/PerformRecast
