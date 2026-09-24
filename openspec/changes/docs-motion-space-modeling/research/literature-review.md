# 最近邻工作调研记录

> 本文件是 change `docs-motion-space-modeling` 的支持性调研记录（`research/` 第一篇），不是 OpenSpec 规划 artifact。
> 它承载 design.md「待调研知识点」的撞车判定结果，并为 `management/docs/动作空间建模/` 各篇文章提供邻居依据。
> **姊妹文件**：`research/manifold-modeling-and-projection.md`——那份答“**方法从哪来**”（ML / 图形学的低维流形方法族），本份答“**撞车边界**”（数字人侧谁占了哪一步）。
> （原属已被取代的 change `docs-brainstorming-identity-motion-space`，2026-09-23 迁入；同日追加第 5 节“空间载体”。）
> 调研日期：2026-09-23。

## 0 调研范围与通道（含覆盖局限）

| 项 | 状态 |
|----|------|
| 通道 | 首轮 `PROXY_OFF`（无 VPN）→ 仅 arXiv API + 搜狗直连；用户开启 VPN 后 `TUN_OK`（默认路由 `utun4`，Google 200） |
| 检索方式 | arXiv API 关键词检索约 40 次查询（`--field all`）+ 6 篇 HTML 全文精读；OpenAlex 标题/引用查询 |
| **局限性 1** | **OpenAlex 在首轮持续 429**（IP 限流），**引用网络与被引数据不完整** |
| **局限性 2** | arXiv 关键词检索噪声大（"latent space" 命中大量生物医药论文），**非 arXiv 的会议论文与 2026 年最新工作可能漏检** |
| **局限性 3** | 未走 Google/DBLP/Semantic Scholar 的系统性 snowballing |
| **结论强度** | 足以支撑"撞车风险从**中**上调为**高**"的判断；**不足以**支撑"没有工作做过 X"的断言 |

## 1 结论速览

把七类工作并排后，**只剩一格未被占据**：

```
                       情绪空间显式化   身份无关   逐人特化   生成期约束   量化人间差异
                       ────────────   ────────  ────────  ────────   ──────────
LES-Talker 2024             ✅            ✅         ❌         ✅          ❌
EDTalk++ 2025               ✅            ✅         ❌         ✅          ❌
PSM 2022                    ❌            —         ✅         ❌          ❌
逐人 AU 归一化 2015          ❌            —         ✅         ❌          ❌
情绪可控生成族 2023–2026     ✅            ✅         ❌         ✅          ❌
───────────────────────────────────────────────────────────────────────────
**本项目的位置**             ✅            ✅         ✅         ✅          ✅   ← 唯一空格
```

**补充第五个邻居**：`Live Speech Portraits`（ACM TOG 2021，cites=162）已做了“**逐角色空间 + manifold projection**”以保个体说话习惯，**但落在【音频输入侧】**；本项目是**动作隐变量输出侧**且目标是**漂移治理**。

**唯一空格**：把 LES-Talker 那个**数据集级**的平均情绪空间换成**逐角色**的，并**量化同一情绪在不同角色间的偏离**。

## 2 直接邻居（五组）

### 2.1 LES-Talker — 线性情绪空间 ★ 最接近"情绪子空间"

- **出处**：arXiv [2411.09268v2](https://arxiv.org/abs/2411.09268)（2024-11-14）；已被 **IEEE Transactions on Affective Computing** 接收（DOI `10.1109/taffc.2026.3676758`，OpenAlex 记为 2026）。作者 Guanwen Feng 等（西安电子科技大学 + 澳门大学）。项目页 <https://peterfanfan.github.io/LES-Talker/>
- **核心想法**：情绪不是标签，而是空间里的**向量**；情绪编辑 = **向量变换**。

```
线性情绪空间 𝔼（共 41 维）
├─ 行动子空间 𝔸 = { u = (e₁,…,e₁₇) }    ← 17 维，直接对应 17 个 Facial Action Unit
└─ 隔离子空间 𝕀 = { v = (e₁₈,…,e₄₁) }   ← 24 维，承载"细微情绪细节"
显式假设： level_emo 在 𝔼 中【线性变化】
每一维都有物理对应物 → 可解释
```

- **做法**：中性视频逐帧抽 AU 值 → 映射进 𝔸 / 𝕀 得到向量；目标"情绪 + 强度"就是空间里的另一个向量；用 **LES 向量 + 3DMM 系数两路中间表示**，再用 CDAN（Cross-Dimension Attention Net）挖两者相关性，指导 3D 模型形变
- **覆盖**：8 种情绪 × 17 个面部单元 × 连续强度（>0），基底来自 **MEAD** 数据集，取 level 1/2/3 作锚
- **⚠ 最要命的一处细节**——AU 归一化用的**是整个数据集**的统计量：

$$\mathrm{Opt}_1(AU_i) = \frac{AU_i - \mu_D}{\sigma_D}$$

$\mu_D,\sigma_D$ 为数据集级均值与标准差。**这就是"统计上的平均行为空间"，已显式写在公式里。**

> **对本项目的意义**：LES 是**通用情绪空间**，没有做逐角色特化。**本项目只需把 $\mu_D,\sigma_D$ 换成逐人基线 $\mu_{p},\sigma_{p}$，并证明由此产生的差异是结构性的**——方法骨架可直接复用 LES。

### 2.2 EDTalk / EDTalk++ — 四空间正交基 + 基库 ★ 最接近"可插拔子空间"

- **出处**：[EDTalk](https://arxiv.org/abs/2404.01647)（arXiv 2404.01647，ECCV 2024）；[EDTalk++](https://arxiv.org/abs/2508.13442)（2025-08-19）
- **核心想法**：把面部动力学**完全解耦**成四个独立潜在空间，每个空间由一组**可学习基的线性组合**定义。

```
四个空间： mouth / pose / eye / expression
每个空间 = 一组可学习基（learnable bases），线性组合定义具体运动
约束：     基之间【强制正交】，以保证"独立、互不干扰"
产物：     学到的基存进对应 bank（基库）
           → 原文："enabling shared visual priors with audio input"
```

- **三条可迁移的论点**：
  1. **正交性是保证"独立"的手段**——与"这个空间该动哪一块"直接对应
  2. **bank = 共享视觉先验**——与我们的**锚帧库是同一概念**，但它的库是**学出来的正交基**，我们的库是**全帧入库的方向字典**（见 `knowledge/数据集整理专题`）
  3. 架构是 **identity source + 独立运动源**：身份一路，嘴/头姿/眼/表情各一路
- **它自称解决的两个前置缺口**：各分量要 ① 互不干扰 ② **可保存并共享给不同模态输入**

### 2.3 PSM（Person-Specific Models）★★★ 几乎逐条命中"通用 + 逐人"

- **出处**：[arXiv 2211.08279v1](https://arxiv.org/abs/2211.08279)（2022-11-15）。OpenAlex 记为 **cites=0**（疑似仅有 arXiv 版），**因此拿不到引用网络**
- **核心想法**：**每个个体训一个模型**，学出"脱开身份与结构特征的面部运动嵌入"；与"跨个体训练的通用模型"对照

| 本项目的表述 | PSM 原话 |
|---|---|
| ① 每个角色有特定行为空间；所有角色有通用行为空间 | 一个 **Person-Specific Model (PSM)** vs 一个 **General Model (GM)**——GM 是 "trained across individuals and characterizes **general patterns** of facial movements" |
| ② 统计所有角色行为得到平均空间 | GM 即跨个体统计出的通用模式 |
| ③ 给新角色、提取其视频动作做特化 | "**knowledge learned on a person can quickly and effectively be transferred to a new person**" |
| ④ 特化后指导生成 | **❌ 缺失——它只做嵌入与重建，不做生成与控制** |

- **技术要点**：自监督、encoder-decoder、**one model per individual**、从**无标注**面部视频学、**课程式时序学习**利用帧间连续性；数据 DISFA，涉及 12 个 AU（AU 1/2/4/5/6/9/12/15/17/20/25/26）
- **与本项目的关系**：**它是"分析/刻画"，本项目是"生成/约束"。这是唯一也是关键的一步差。**

### 2.4 逐人 AU 归一化（2015）— 证明第 2 步该怎么做

- **出处**：[Cross-dataset learning and person-specific normalisation for automatic Action Unit detection](https://doi.org/10.1109/fg.2015.7284869)（2015，OpenAlex cites=425）
- **核心想法**：因"个体差异巨大"，AU 分类器性能高度依赖**逐人中性脸基线**，故对每个人做归一化
- **对本项目的意义**：**逐人基线在 AU 检测领域是 2015 年就有的标准做法**；但**没人把它搬到生成侧的情绪空间上**。这既降低了方法的"新意门槛"，也给了方法"有先例可依"的合理性。

### 2.5 Live Speech Portraits — 逐角色空间 + 投影（但在**音频输入侧**）★

- **出处**：Lu 等，*ACM Transactions on Graphics* **2021**，DOI `10.1145/3478513.3480484`，**cites=162**；arXiv [2109.10595](https://arxiv.org/abs/2109.10595)
- **原话**：「第一阶段是一个深度神经网络，提取深层音频特征并配合 **manifold projection** 把特征**投影到目标人的 speech space**」；动机是「wild audio 与 target speech space 之间的域差……使系统**无法保留个体的说话习惯（individual talking idiosyncrasies）**」
- **它做了什么**：**逐角色空间 + 投影**——把输入特征拉回“这个人自己的说话空间”，以保住个体差异
- **⚠ 关键限定（读全文后确认）**：它是**音频特征侧（输入侧）**的投影，**不是动作隐变量输出侧**。**概念同形，位置不同。**
- **对本项目的意义**：它是数字人侧**最近的一个邻居**。它证明了“逐角色空间 + 投影”在数字人是可做的；**也给本项目圈定了差异**：换到**动作隐变量的输出侧**、用来治**漂移**而不是保个体域差

### 2.6 跨身份重演谱系 — 雷 4 的证据

[FReeNet](https://arxiv.org/abs/1905.11805)（2019）、[LI-Net](https://arxiv.org/abs/2104.02850)（2021）、[Fine-grained Identity Preserving Landmark Synthesis](https://arxiv.org/abs/2110.04708)（2021）、[Finding Directions in GAN's Latent Space for Neural Face Reenactment](https://arxiv.org/abs/2202.00046)（2022）；加上本仓库已收录的 `论文笔记/face-vid2vid`、`论文笔记/liveportrait`。
→ **"用 A 的动作驱动 B"不是新贡献**（design 第 14 节雷 4）。

## 3 情绪可控生成族（2023–2026，密集红海）

| 论文 | 出处 | 核心想法 |
|------|------|---------|
| DreamTalk | [2312.09767](https://arxiv.org/abs/2312.09767)（2023-12） | 扩散模型做情绪头像，**可方便指定个性化情绪** |
| EMOdiffhead | [2409.07255](https://arxiv.org/abs/2409.07255)（2024-09） | **连续**情绪强度控制 |
| EmotiveTalk | [2411.16726](https://arxiv.org/abs/2411.16726)（2024-11） | 音频信息解耦 + 情绪视频扩散 |
| SPEAK | [2405.07257](https://arxiv.org/abs/2405.07257)（2024-05） | 头姿与情绪可调 |
| **EmoHead** | [2503.19416](https://arxiv.org/abs/2503.19416)（2025-03） | **操纵语义表情参数**生成情绪头 |
| Gen-AFFECT | [2508.09461](https://arxiv.org/abs/2508.09461)（2025-08） | 细粒度表情 + **身份一致**（2D 头像） |
| MoDiTalker | [2403.19144](https://arxiv.org/abs/2403.19144)（2024-03） | 运动解耦的扩散头 |
| Multi-Scale Compensatory Codebooks | [2412.00719](https://arxiv.org/abs/2412.00719)（2024-12） | 多尺度补偿码本，分离运动与外观 |
| Speech-Mesh Representation | [2503.20308](https://arxiv.org/abs/2503.20308)（2025-03） | 3D 头生成的新表示 + **感知对齐评价指标** |
| **AUHead** | [2602.09534](https://arxiv.org/abs/2602.09534)（2026-02） | **两阶段 AU 控制**，正对"细粒度情绪控制缺失" |

**共同想法**：情绪必须脱离离散标签，变成**连续、可指定、可组合**的量。这个共识在 2023 年就已形成。

## 4 “把空间显式建出来、推理期使用”——三个**先例领域**（不是分类轴）

> **口径修正（2026-09-23）**：本节原称“三支范式”，但它**不是一条分类轴**——三个方向分属不同年代与领域（2018 GAN / 2023 LLM 可解释性 / 2024 机器人世界模型），互不排斥、层级不同。它们只能证明“**这件事很常见**”，不承担分类职能。分类轴见 design《三条正交分类轴》（载体 / 几何 / 操作）。

> 这一节的作用是**降低"建空间"本身的新颖性权重**：它是成熟工具，不是贡献。

| 支 | 核心想法 | 代表 |
|----|---------|------|
| **GAN 隐空间方向** | 在隐空间找语义方向，推理期沿方向调；方向可跨身份搬运 | [Finding Directions in GAN's Latent Space](https://arxiv.org/abs/2202.00046)；StyleGAN W/W+ 编辑一族 [2105.14230](https://arxiv.org/abs/2105.14230)、[2204.12530](https://arxiv.org/abs/2204.12530)、[2208.12408](https://arxiv.org/abs/2208.12408) |
| **激活引导 / 表示工程** | 在模型**中间激活**上找方向，推理期加向量控制行为 | [2403.05767](https://arxiv.org/abs/2403.05767)、[2512.07667](https://arxiv.org/abs/2512.07667)、[PaCE 2406.04331](https://arxiv.org/abs/2406.04331)、[2602.15293](https://arxiv.org/abs/2602.15293)、[2605.10664](https://arxiv.org/abs/2605.10664)；**情绪版**：[EmoShift 2601.22873](https://arxiv.org/abs/2601.22873)（语音情绪激活引导） |
| **潜在动作模型** | 从无标注视频反推抽象**动作空间**，供世界模型/机器人使用 | [CLAM 2505.04999](https://arxiv.org/abs/2505.04999)、[DiLA 2605.15725](https://arxiv.org/abs/2605.15725)、[Character Animation Survey 2504.19056](https://arxiv.org/abs/2504.19056)、[Style-ERD 2203.02574](https://arxiv.org/abs/2203.02574) |

## 5 空间载体：现有模型一般怎么建立这个动作空间

**问题**：建立这个空间是用了一个**独立模型**，还是别的形式？

**答案：四种载体，主流是「独立的小自编码器」。**

| 载体 | 做法 | 代表 | 独立模型？ | 数据需求 |
|------|------|------|-----------|---------|
| **A 解析 / 统计参数空间** | 不训生成模型，用现成参数化表示 | FLAME / 3DMM（PCA 拟合数千次 3D 扫描）；ARKit blendshape（商业校准）；**AU 强度**（LES-Talker 用**外部 AU 检测器** + 解析映射得 41 维） | ❌ | 数千次 3D 扫描 / 专有校准数据 / 仅需 AU 检测器 |
| **B 独立的小自编码器** ★ | 单独训 encoder/decoder，其 latent 即空间；**训练后常被冻结** | **FLOAT / Avatar Forcing 的 Motion Latent AE**（$\alpha$ 20D + QR 正交基 $B$）；**PSM** 的 per-person encoder-decoder；**EDTalk++** 的四个轻量模块（learnable orthogonal bases + banks） | ✅ **主流** | 大量无标注视频（自监督） |
| **C 生成器自身的隐变量** | 无独立模块，空间 = 内部某层激活 | **VASA-1** 隐式 latent；GAN 的 $W$ 空间 | ❌ | 隐在生成器训练里 |
| **D 离散码本** | VQ-VAE / 多尺度码本，空间是词表 | Multi-Scale Compensatory Codebooks 等 talking-head 工作 | ✅ | 无标注视频 |

**几何形式**另有四类：**线性正交基**（$B$，QR 构造）· **PCA**（3DMM）· **码本**（离散）· **弯曲流形**（VAE / normalizing flow 的 latent）。

### 5.1 我们这个链路的实例（FLOAT / Avatar Forcing）

来源：本仓库 `knowledge/Avatar Forcing Motion Latent AutoEncoder`、`论文笔记/float.md`。

```
α ∈ ℝ^20   运动自由度（真正可独立变化的只有 20 个方向）
B ∈ ℝ^{512×20}   Direction 模块构造的【QR 正交方向基】
r = Bα ∈ ℝ^512  给 Flow / renderer 的运动接口
s ∈ ℝ^512   appearance / identity code
z = s + r
```

- **Motion Latent AutoEncoder 是独立模块**，阶段一单独训练：Adam、batch 8、lr $2\times10^{-4}$、**460k steps、约 9 天、单张 A100**；数据 HDTF + RAVDESS + VFHQ，预处理后 **14,362** 训练片段；$d=512$、**$M=20$ 正交方向**
- 训练后**被冻结**（Avatar Forcing Stage 2 冻结 motion AE）
- **20 维窄通道是【有意】用来减少身份泄漏的**——reenactment 的设计目标就是“复制动作、不复制长相”
- **正交基的现成收益**：$\langle w_{r\to\hat D},\mathbf{v}_k\rangle=\lambda_k(\hat D)$，系数可**闭式**取出 → test-time 线性编辑（$\lambda$-control）。FLOAT 明确把**正交显式基**作为相对 **VASA-1 隐式 latent** 的差异化点

### 5.2 对项目的三条含义

1. **我们已在“B + 线性正交基”这一格**。所以**“建立空间”不是新建模块，而是给已有的 $\alpha$ 空间加结构**（加逐角色映射、加身份保持子空间、加投影算子）——**成本量级完全不同**
2. **正交让“投影 / 夹紧”可以闭式化**：越界检测与夹紧能直接在**系数层面**做，不需要解优化问题
3. **反面代价**：$\alpha$ 的语义**不可读**（Ditto 靠逐维扰动反推建立控制映射）；且 20 维的容量是**已定约束**——“够不够”在动手前必须先测

## 6 理论后盾：个体/文化差异（主张的根据，但不作为贡献）

心理学早已论证**情绪的面部表达不是普适的**：

- [Evidence and a computational explanation of cultural differences in facial expression recognition](https://doi.org/10.1037/a0020019)（*Emotion*, 2010）——不同文化的人**更擅长识别同文化者的表情**（实验 + 神经计算模型复现）
- [In the eye of the beholder? Universality and cultural specificity](https://doi.org/10.1080/00207594.2011.626049)（2011）——编码/解码的普适性之争，结论偏特异性
- [逐人 AU 归一化](https://doi.org/10.1109/fg.2015.7284869)（2015）——工程侧确认个体差异不可忽略

**双重后果**：
- ✅ **是** Level 2 主张的理论根据——"同一情绪在不同人脸上不是同一个东西"被论证了 15 年以上
- ❌ **不是**贡献——前提早已成立，把前提当贡献会被直接驳回

## 7 对本项目定位的影响（须同步进 design.md）

1. **撞车风险**：**中 → 高**。四组直接邻居分别占据了"情绪空间显式化""可插拔解耦空间""逐人运动建模""跨身份驱动"
2. **主张必须收窄为一步连接**：*通用平均情绪空间 → 逐角色情绪空间*，并**量化人间偏离**
3. **判决实验升为前置条件**：文章的存亡取决于"逐角色情绪方向是否显著发散"。**它必须在写任何方法之前先跑**
4. **方法骨架可复用**：LES 给出了显式的 $\mu_D,\sigma_D$ 归一化，本项目只需替换为 $\mu_{p},\sigma_{p}$ 并证明差异是结构性的
5. **"建空间"本身不能当贡献**：第 4 节三个先例领域已成常识

## 8 未完成 / 待补调研

- [ ] **引用网络不完整**：OpenAlex 首轮 429；且 **PSM 记为 cites=0**，需换语义学者/Google Scholar 补被引检索，确认有无工作把"逐人面部运动"接上"情绪空间"
- [ ] **未读全文**：AUHead (2602.09534)、EmoHead (2503.19416)、EMOdiffhead (2409.07255)、EmotiveTalk (2411.16726)
- [ ] **未验证**：LES-Talker 是否在实现中隐含 identity-conditioned 情绪处理（若已隐含，本项目主张会被进一步压缩）
- [ ] **未覆盖**：非 arXiv 的会议论文（CVPR/WACV/ICCV 2024–2026）、中文顶会工作
- [ ] **待确认**：是否存在工作做了"情绪区域的跨角色发散度量"（第 1 节对照表最后一列）
- [ ] **待确认**：是否已有工作把"**运动隐变量的越界量**"作为漂移度量（`06` 的新颖性）
- [ ] **未核实**：$\alpha$ 的**逐角色绑定关系**（是否逐角色绑定、$B$ 是否冻结、20 维语义是否已解释）——这是 `04` 的前提
- [x] **已完成**：空间载体形式调研（第 5 节，四种载体）

## 9 一句话版

> **"情绪是线性空间里的向量"已被做（LES-Talker）；"通用模型 + 逐人模型"已被做（PSM）；"把空间建出来在推理期用"是常识（三个先例领域）；用独立小自编码器建空间是主流做法（四种载体）。本项目唯一的主张是那条没人接上的边：把通用平均的空间换成逐角色的，并证明这个替换带来的差异是结构性的、可测量的、可用于约束生成的。**
