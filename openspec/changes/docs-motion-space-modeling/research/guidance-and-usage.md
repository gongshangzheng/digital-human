# 具体怎么用：引导、后验采样、粒子引导、轨迹条件

> 本文件是 change `docs-motion-space-modeling` 的支持性调研记录（`research/` 第三篇），不是 OpenSpec 规划 artifact。
> 它回答：**把逐角色先验/轨迹拿到手之后，具体怎么加进生成？**
> 姊妹文件：`literature-review.md`（撞车边界）· `manifold-modeling-and-projection.md`（方法与轨迹与坐标系）。
> 调研日期：2026-09-23。被引数取自 OpenAlex 同日。通道：`TUN_OK`（VPN 已连），OpenAlex `--title` 精确查。

## 0 覆盖局限

- 只有 OpenAlex 标题精确检索；**无 Google Scholar / 无完整 snowballing**；S2 仍 429
- 因此"未找到"一律读作"**本轮未找到**"
- 未读全文（只有摘要），**公式细节需落笔前回原文核对**

## 1 结论速览

| 问题 | 答案 |
|------|------|
| 有现成的引导机制吗？ | **有，而且是四种成熟范式**（末尾表） |
| 有没有"直接对 flow matching 做引导"的现成方法？ | **有** —— `Training Free Guided Flow Matching with Optimal Control`（2024）★ |
| "音频 → 点"该用什么框架？ | **后验采样**：$p(\alpha\mid a)\propto p(a\mid\alpha)p_p(\alpha)$（DPS 2022）★ |
| "整条轨迹"级引导有现成吗？ | **有** —— Particle Guidance（2023）+ **EDDY（2026，flow matching 版）**★ |
| "用轨迹当条件"有现成吗？ | **有** —— motion in-betweening / IKMo / Motion Manifold Flow Primitives ★ |
| "单图/少样本角色特化"有现成吗？ | **有** —— Subject-Diffusion（2024）· ASMNet（2024）· PSM（2022，见另一份文件） |

## 2 四条主流做法（"具体怎么用"的全部候选）

| # | 机制 | 代表 | 怎么用 | 与我们的关系 |
|---|------|------|-------|------------|
| **1** | **Classifier-Free Guidance** | Ho & Salimans 2022（**cites=754**） | 用无条件与条件的**差**做引导，**不需要额外分类器** | 把"角色条件"注入的**最简形式**；无需新模型 |
| **2** | **后验采样** | `Diffusion Posterior Sampling for General Noisy Inverse Problems` 2022（**cites=158**） | $p(\alpha\mid a)\propto p(a\mid\alpha)\,p_p(\alpha)$：**似然项 + 先验项** | **"音频 → 点"的正解**：先验当正则项 ★ |
| **3** | **粒子 / 联合引导（轨迹级）** | `Particle Guidance` 2023（arXiv 2310.13102）· **`EDDY` 2026（arXiv 2605.06553，flow matching 版，边缘保持）** | 在**联合粒子系统**上定义一个时变势能 → 引导**整条轨迹** | **轨迹级引导的实现方式**；且 **EDDY 明确支持 flow matching** ★ |
| **4** | **训练免费的目标损失引导** | `Training Free Guided Flow Matching with Optimal Control` 2024（arXiv 2410.18070） | **优化目标损失 $R(x_1)$ 同时靠近先验**；做法是**梯度穿过 ODE 采样过程** | **最贴你们**：不用重训、直接引导 flow ★ |

**另一条相关线（动作空间里的 score field）**：`Diffusion Policy: Visuomotor Policy Learning via Action Diffusion`（2024, *IJRR*, **cites=536**）—— "学习**动作分布 score 函数**的梯度，在推理时沿这个**梯度场**迭代优化（Langevin 动力学）"。**这就是"在动作空间里做引导"的机器人版**，而且它做的是**动作序列**（轨迹级）。

## 3 轨迹作为条件（"用轨迹"的三条现成做法）

| 做法 | 出处 | 要点 |
|------|------|------|
| **Motion in-betweening** | `Robust motion in-betweening` 2020, *ACM TOG*（**cites=263**） | **时序稀疏的关键帧**当约束 → 生成过渡（对抗式 RNN） |
| **轨迹 + 姿态双通道条件** | `IKMo: Image-Keyframed Motion Generation with Trajectory-Pose Conditioned Motion Diffusion Model` 2025（arXiv 2505.21146） | 轨迹与姿态**解耦**，**两阶段**条件框架（先细化输入、再并行编码） |
| **motion manifold + flow + 条件轨迹** ★ | `Motion Manifold Flow Primitives for Task-Conditioned Trajectory Generation` 2025, *IEEE RA-L*（arXiv 2407.19681） | 明确建立在**运动流形假设**上（轨迹位于**低维非线性子空间**），用 **flow** 生成**条件轨迹** —— **形状最接近我们要做的** |

## 4 单图 / 少样本角色特化

| 做法 | 出处 | 要点 |
|------|------|------|
| **单参考图、免 test-time 微调** | `Subject-Diffusion` 2024, *ACM MM*（**cites=71**） | 一张参考图即可个性化；**不需要 test-time fine-tuning** |
| **动作 + 风格双条件** | `ASMNet` 2024, *Cyborg and Bionic Systems*（cites=12） | 生成既合**动作标签**又带**风格特征**的序列 |
| **逐人模型 vs 通用模型** | `PSM` 2022（见 `literature-review.md` §2.3） | 逐人 encoder-decoder，从**无标注视频**学；**只刻画不生成** |

**⚠ 与本项目结论的冲突要注意**：`Subject-Diffusion` 证明了**外观类**个性化单图可行；但我们的结论是**运动习惯**（节奏/条件耦合）**给不了**——两者不矛盾：单图能定"长什么样"，定不了"怎么动"。

## 5 对项目的落点（"具体怎么使用"的推荐路线）

```
第 0 步（零训练，验证"有没有用"）
    非参数 r_p（锚帧库 = 该角色真实视频的 α 与转移对）
    + 机制 1（CFG 形式的引导）或 机制 3（重采样）
    → 量：越界率、漂移速率

第 1 步（小训练，让 r_p 可微）
    拟合该角色的局部密度/转移模型
    + 机制 4（Training-Free Guided Flow Matching，梯度穿过 ODE）
    → 引导平滑、可做强度谱

第 2 步（轨迹级，给长时保证）
    机制 3 的 **EDDY 形式（flow matching 版粒子引导）**，权重 = r_p(α_{1:T})
    → 整条轨迹有界；注意 KV cache 要能分支

第 3 步（架构级，修根因）
    给 Flow 加角色条件（条件向量 / 少样本嵌入 / 基拆分）
```

**"音频 → 点"用机制 2**（后验采样）：$p(\alpha\mid a)\propto p(a\mid\alpha)p_p(\alpha)$ —— 先验项正好补上音频给不出的那一半自由度。

## 6 待补调研

- [ ] 读全文核对公式：**Training-Free Guided Flow Matching**（2410.18070）· **EDDY**（2605.06553）· **Motion Manifold Flow Primitives**（2407.19681）
- [ ] **EDDY 的"边缘保持"是否意味着它可以长期不破坏分布**（与长时保持直接相关）
- [ ] Motion in-betweening / IKMo 的**约束形式**（硬约束 vs 软引导）—— 决定"刚性还是柔性"
- [ ] 是否有工作把**逐角色先验**当引导项（而不是把文本/类别当引导项）
- [ ] `Diffusion Policy` 那条线的**动作序列 score field** 能否直接照搬到 20 维 α 序列
- [ ] 中文侧（搜狗）是否有"运动流形 + flow + 条件轨迹"的同题工作

## 7 一句话版

> **"具体怎么用"在文献里已经是一套成熟工具箱**：CFG（cites=754）给最简引导形式；**后验采样**（2022）给"音频→点"的框架（先验即正则）；**Training-Free Guided Flow Matching**（2024）给"直接引导 flow 且不重训"的做法；**Particle Guidance / EDDY**（2023 / 2026）给**轨迹级引导**，而 EDDY 明确支持 **flow matching**；**motion in-betweening / IKMo / Motion Manifold Flow Primitives** 给"用轨迹当条件"。我们的组合是：**后验采样的形式 + 逐角色先验当引导项 / 重采样权重 + 轨迹级粒子引导**。
