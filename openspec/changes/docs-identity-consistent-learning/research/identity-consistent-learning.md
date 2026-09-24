# 身份一致性：为什么用单帧，以及多帧/视频提身份的尝试

> 本文件是 change `docs-identity-consistent-learning` 的支持性调研记录（`research/` 第一篇），不是 OpenSpec 规划 artifact。
> 它回答两个问题：**① 为什么现有模型只用单帧提取身份、面临什么困难？② 有没有从多帧/视频提取身份的尝试，为何成败？**
> 调研日期：2026-09-23（**两版**）。

## 0 覆盖局限与证据等级（⚠️ 必读）

- **第一版**：OpenAlex / arXiv / Google 全部不可达（`utun4` 接口消失，只剩 `utun0–3`），只有 Crossref 通 → **无新检索**，内容来自**仓库素材 + 前几轮已核实文献 + 常识**。
- **第二版（同日，VPN 恢复后补搜）**：OpenAlex `--title` 精确检索可用，**已核实 8 项**（见 §4.5 与各节 **【核】** 标记），**待核实收敛到 3 项**（§5）。
- **仍无 Google Scholar、无完整 snowballing** → 「未找到」一律读作「**本轮未找到**」。

| 标记 | 含义 |
|------|------|
| **【仓】** | 本仓库自有素材（可追溯到具体文档） |
| **【核】** | 已用 OpenAlex `--title` 核实（带被引数 / DOI），含**第二版补搜**所得 |
| **【常】** | 领域常识 / 推断，**未核实** |

## 1 结论速览

| 问题 | 答案 |
|------|------|
| 为什么只用单帧？ | **两条是设计（不是退让）**：reenactment 的任务契约就是「源图（身份）+ 驱动帧（运动）」；且**单帧是保证 `s` 与运动无关的最干净办法**（多帧会让 $s$ 带上运动统计，破坏 $z=s+r$ 的可加解耦）。另两条是成本与数据构造 |
| 单帧的困难本质是什么？ | ★ **是歧义（ambiguity），不是信息不足（insufficiency）** —— 单帧无法确定「换个角度该长什么样」，**即使模型完美也可能猜错** |
| 有从多帧/视频提身份的尝试吗？ | **有，四条成熟路线**：VFR 聚合 · 多视角 3D 重建 · 个性化扩散 · 前馈式多图聚合 |
| 为什么识别侧早就用多帧，生成侧还在用单帧？ | ★ **两者对「身份」的需求不同**：VFR 要**判别性向量**（多帧是纯收益）；生成要**能重建所有视角外观的表示**（多帧给覆盖，**不给跨视角自洽**） |
| 最要紧的警示？ | ★ **多帧聚合隐含「这些帧属于同一身份」——而这正是我们要保证的东西（循环）**；训练多帧必须来自身份已知的数据，否则会把运动差异当身份差异 |
| 本仓库已有的结论 | 「**多参考改善「看不到的角度」，但不解决「所有角度是否同一人」**」**【仓】** |
| 单目为什么做不出完整 3D 头？ | **根因已被命名**：`FlexAvatar`（2025）——「**entanglement between driving signal and target viewpoint**」→ 解法是**单目 + 多视角统一训练 + canonical 锚**（`AniGS` 用生成式多视角 canonical 图 resolve 歧义） |
| ★ 身份/运动分离判据已有工作吗？ | **有，而且 `CGF 2022` 已【逐字同构】实现**（原话：disentangles the **constant facial identity** from the **time-varying facial expressions**，两个独立 latent 子空间）；`RASA` 2026 是同类最新（分阶段 + 丢 $\beta$ 留 $\theta$）；`DSfusion` 2026 在风格侧 → **增量严格收窄为四条**（长时漂移 · 划分线要从数据学 · 逐角色单视频 · 视频生成侧）（§4.5） |
| 属性泄漏是已知问题吗？ | **是，且被命名**：`BlendFace`（ICCV 2023, **cites=58**）—— 既有方法「suffer from an **identity-attribute entanglement**」，因为 **ArcFace 有 attribute biases** |

## 2 Q1：为什么只用单帧，以及它面临什么

### 2.1 四条原因（前两条是设计）

| # | 原因 | 等级 |
|---|------|------|
| **1** | **任务传承**：MegaPortraits / FLOAT / AvatarForcing 这一族来自 **face reenactment**，输入契约本就是「**源图（身份）+ 驱动帧（运动）**」。单帧是**任务定义的一部分** | **【仓】**`论文笔记/float`、`knowledge/Avatar Forcing Motion Latent AutoEncoder` |
| **2** | **与可加解耦兼容** ★：$z=s+r$、$r=B\alpha$。要让 $s$ 与运动无关，**最干净的办法是只从一帧抽**。多帧会让 $s$ 带上**运动统计**（点头节奏、眨眼频率）→ 破坏可加性 → 运动侧无法独立控制 | **【常】**（推断；但与仓库「20 维窄通道**有意**防泄漏」同源） |
| **3** | **产品与成本**：单帧是用户最容易提供的输入；多帧要预处理 / 对齐 / 聚合；实时系统里身份提取发生在会话开始前 | **【常】** |
| **4** | **训练数据构造**：多帧引入「哪几帧属于同一身份」的监督问题；单帧可直接拿「同一视频任意一帧」当源 | **【常】** |

> **第 2 条是本次最值得写进设计的推论**：单帧不只是习惯，它**是解耦架构的一部分**。要把多帧引入，必须先解决「多帧如何不把运动带进 $s$」。

### 2.2 单帧面临的五个困难

| # | 困难 | 说明 | 等级 |
|---|------|------|------|
| **1** | **可观测性受限** | 一帧只给一个姿态 / 表情 / 光照 → **背面、另一侧脸、遮挡区无观测**，只能靠先验补 | **【仓】**`多参考注入` |
| **2** | **属性泄漏（attribute leakage）** | 单帧的 $s$ 里混进表情、姿态、光照。**已被命名**：`BlendFace: Re-designing Identity Encoders for Face-Swapping`（ICCV 2023, **cites=58**, DOI 10.1109/iccv51070.2023.00702）原话：既有方法「**suffer from an identity-attribute entanglement** that causes **undesired attributes swapping** because widely used identity encoders, e.g., **ArcFace, have some crucial attribute biases** owing to their pretraining on face recognition tasks」 | **【核】** |
| **3** | **没有多帧平均** | 单帧噪声、模糊、压缩伪影**直接进身份** | **【常】** |
| **4** | ★ **3D 一致性不可确定** | 单帧无法确定「这张脸换个角度该长什么样」—— **这是歧义，不是信息不足**：即使模型完美也可能猜错 | **【核】**（根因已命名，见下） |
| **5** | **身份与尺度纠缠** | 实测的「**脸部尺度漂移**」属于这类（$z=z_S+m_S$ 近似解耦的泄漏面） | **【仓】**`数字人身份` |

**第 4 条的根因已被命名，且有解法方向（本轮核实）**：

| 工作 | 原话 / 做法 |
|------|-----------|
| **`FlexAvatar: Learning Complete 3D Head Avatars with Partial Supervision`**（2025, arXiv 2512.15599） | 「**We identify the root cause of this issue as the entanglement between driving signal and target viewpoint when learning from monocular videos**」；解法是**单目 + 多视角统一训练**，用可学的 **data source tokens（bias sinks）** 区分数据来源 |
| **`AniGS`**（CVPR 2025, **cites=13**） | 用生成模型产出**细节化的多视角 canonical pose 图**，以「**resolve ambiguities** in animatable human reconstruction」，并处理 **Inconsistent** Gaussian Reconstruction |
| **`FlexAvatar`（另一篇，2025）** | 输入 **input-number-agnostic / camera-pose-free / expression-free**，用 **structured head query tokens 作 canonical anchor** 聚合到稳健 canonical 3D 表示 |

> **含义**：单目歧义的**根因是「驱动信号 × 目标视角」纠缠**（不是单纯缺数据），所以解法不是「多喂几张」，而是**统一训练 + canonical 锚**。

> **另**：把「单帧不够」说成「信息不足」会误导选型——**多帧只有真的覆盖了缺失视角时才降低歧义**；多帧都是同一角度，聚合不解决问题。

## 3 Q2：从多帧/视频提身份的尝试，以及成败原因

### 3.1 成功的四条路线

| 路线 | 代表 | 成功原因 | 代价 |
|------|------|---------|------|
| **① Video Face Recognition（VFR）** ★ | 逐帧特征 + **聚合**（平均池化 / 注意力池化 / quality-aware / RNN） | **多帧聚合降噪**；对遮挡与姿态鲁棒；「同身份多帧」是天然监督 | **它解决「识别」，不是「生成」** —— 输出只是一个身份向量，**不需要 3D 一致** |
| | **【核】三条经典**：`Neural Aggregation Network for Video Face Recognition`（CVPR 2017, **cites=421**）—— **变长输入**（variable number of face images）+ **两个注意力块**自适应聚合到**凸包内**单一特征；`Attention-Aware Deep RL for Video Face Recognition`（ICCV 2017, **cites=199**）—— **丢弃误导 / 混淆帧**（= 质量感知选帧）；`Eigen-PEP for Video Face Recognition`（2015, **cites=134**） | ★ **「变长 + 注意力聚合 + 质量感知选帧」三件套 2017 年就成型** —— 比 UIKA 的「任意数量」早 8 年 | |
| **② 多视角 3D 头像重建** | NerFACE / INSTA / IMavatar / GaussianTalker · **UIKA** · **FlexAvatar** · **LAM** | **把身份训进资产** → 视角自由 + 跨镜头一致 | **注册训练成本**（换身份要重训）；单图/少图时**背面与遮挡区缺观测** → 生成式补全可能给出**互不兼容**的细节 |
| **③ 个性化扩散** | DreamBooth / Textual Inversion / **Subject-Diffusion**（【核】**cites=71**：单参考图、免 test-time 微调） | **多图提供多视角与多光照覆盖** → 主体一致性提升 | per-subject 微调（免微调是进步） |
| **④ 前馈式多图聚合** | **UIKA**（UV 对应 + 双流注意力，聚合**任意数量无位姿图像**，220 FPS 渲染；训练用 **7,500+ 合成身份、32 张 H20 两周**）· **FlexAvatar**（**1–4 张**无位姿无表情标签，重建 ~0.4s、驱动 ~22ms/帧） | 把「聚合」做成**一次前向**，避免 per-subject 优化 | **训练数据与算力极大** |
| | **【核】`FlexAvatar: Flexible Large Reconstruction Model...`**（2025）：**input-number-agnostic / camera-pose-free / expression-free**，靠 **structured head query tokens 作 canonical anchor** 聚合，轻量 UNet 解码器配 **UV-space position maps** 出细节形变 | ★ 「**变长输入 → canonical 锚**」是这一族的核心机制 | |

### 3.2 失败 / 受限的八条模式

| # | 模式 | 等级 |
|---|------|------|
| **1** | **多帧把【运动】带进身份**（污染）→ 破坏解耦。**与 AvatarForcing v1/v2 的教训同源** | **【仓】+【常】** |
| **2** | **聚合顺序与冲突处理**：清晰正脸 + 模糊侧脸 + 不同时间照片互相矛盾；**简单拼接会被重复样本稀释** | **【仓】**原话 |
| **3** | **固定数量编码器在【输入数变化】时失效** | **【仓】**原话 |
| **4** | **多视角数据本身不一致**（`AniGS` 处理 **Inconsistent** Gaussian Reconstruction；生成式多视角之间的差异需要建模） | **【仓】+【核】** |
| **5** | **大姿态**：CoFE 用多个专家（ArcFace/CLIP/DINOv2）**按层门控**，参数 **+18.5%** | **【仓】** |
| **6** | **低频轮廓 vs 高频纹理要分流**：ConsisID 为此 **+0.5B 参数** | **【仓】** |
| **7** | ★ 「**多参考改善「看不到的角度」，但不解决「所有角度是否同一人」**」 | **【仓】**原话 |
| **8** | **多图/视频监督需要【跨视角成对标注】** → 构造成本高于通用人脸识别 | **【仓】**`身份一致性判别器` 末段 |

## 4 两个综合判断（本文件的核心产出）

### 判断 1：**VFR（识别）与头像生成（生成）对「身份」的需求不同 —— 多帧的经验不能直接搬**

```
VFR 需要：一个【判别性】的身份向量（对姿态/光照不变）
          → 多帧聚合是【纯收益】

生成 需要：一个【能重建所有视角外观】的身份表示
          → 多帧给的是【覆盖】，但【不保证跨视角自洽】
          → 所以「多参考改善看不到的角度，但不解决所有角度是否同一人」
```

**这解释了为什么识别侧早就用多帧、而生成侧还在用单帧。**

### 判断 2：多帧聚合有一个**隐含前提，而且它是循环的**

> 多帧聚合假设「这些帧属于同一身份且身份不变」—— **而这正是我们要保证的东西。**

**后果**：训练时的多帧必须来自**身份已知**的数据（同一视频 / 同一角色）。否则会把**运动差异当成身份差异**去学 —— **又回到 v1 的坑**。

## 4.5 ★ 直接邻居：身份 / 运动分离判据是否已有工作（本轮核实，**第二版已读方法**）

### 4.5.1 三篇的问题与解法（读原文后）

**① `RASA`（2026, HiDream.ai + 合肥工大, arXiv 2608.28219）**

- **问题**：跨身份角色动画的核心挑战是**两类能力的固有纠缠** —— 跨身份**空间映射**（位置 / 尺度 / 骨骼比例对齐）与**运动控制**（关节 articulation / 体感一致 / 视角连贯）。既有做法的失败：预处理式**有信息损失**；**深层特征融合「把结构校准与外观渲染纠缠在一起」** → 视觉伪影 + 运动迁移不稳定
- **解法：按「生成阶段」解耦**
  - **SPC（Spatial Prior Calibrator）**：融合参考身份与驱动姿态 → 生成**空间已接地的初始噪声 latent**（位置 / 尺度 / 比例已对齐）→「**几何差异在生成起点就中和**」
  - **IMG（Inherent Motional Guider）**：★ **显式丢弃 subject-specific shape 参数 $\beta$，只用 articulation 参数 $\theta$** 构造 motion prior，得到「**strict geometry invariance**」；编码成语义运动向量 $\mathbf{m}\in\mathbb{R}^{T\times263}$，注入 DiT **中间层**
- **核心洞见（原话）**："geometric discrepancies must be neutralized at the **generative onset**, while complex motion semantics require **deep, consistent guidance**"
- 附带基准 **CIM-Bench**

**② `Facial Animation with Disentangled Identity and Motion using Transformers`（*CGF* 2022, cites=15, DOI 10.1111/cgf.14641）**

- **问题**：3D 面部形状序列（3D+time）的建模
- **解法**：用 **transformer autoencoder 学 motion manifold**，可建模**任意长度**的 3D 几何序列（self-attention 自适应地捕捉帧间相关）；**原话**：「**disentangles the constant facial identity from the time-varying facial expressions** … using **two separate codes** to represent neutral identity and the performance itself within **separate latent subspaces**」
- 于是得到 **identity-agnostic performance**，可与**任意新身份 code 配对**，过 **identity-modulated performance decoder** → 输出指定身份与长度的 mesh 序列
- 应用：performance synthesis / **retargeting** / key-frame interpolation / 缺失数据补全 / denoising / retiming

**③ `Style-Disentangled Diffusion`（ICASSP 2026, DSfusion）**

- **问题**：co-speech **身体动作**生成难出「抽象的个人风格」；少有人**从音频**学这个特征；**解耦的彻底性与可解释性**都难
- **解法**：从 **multi-ID 数据集**学**每个说话人的个人风格**；引入 **style disentanglement module** 提升解耦度与可解释性（摘要截断，训练细节未取到）

### 4.5.2 ★★ 最重要的发现：CGF 2022 **逐字同构**于我们的上游命题

> 「**constant facial identity**」vs「**time-varying facial expressions**」，两个**独立 latent 子空间**

**这就是「不变 / 变化分解」** —— 而且**已经被实现过**（for 3D mesh sequences），2022 年。

**因此（必须改口径）**：
- 我们**不能**说这个分解是「命名的纠缠」（那还只是 RASA 的措辞）
- 也**不能**说这是「我们发现的问题」
- **正确表述**：**该分解在 3D 面部 mesh 上已实现（CGF 2022）；RASA 2026 是同类最新（全身 / 分阶段）；DSfusion 是风格侧**

### 4.5.3 与本项目的对比（六轴）

| 轴 | `RASA` 2026 | `CGF 2022` | `DSfusion` 2026 | **本项目** |
|---|---|---|---|---|
| 对象 | 全身角色动画（SMPL） | 3D 面部 mesh 序列 | 语音驱动身体动作 | **2D 视频生成的隐运动变量（20D $\alpha$）** |
| 分离什么 | 空间映射 vs 运动控制 | **恒定身份 vs 时变表情** | 风格 vs 内容/身份 | **不变（身份）vs 变化（运动风格）** |
| 怎么分离 | 分阶段 + 丢 $\beta$ 留 $\theta$ | **两个 code + 两个 latent 子空间** | style disentanglement module | **学出划分线**（不假定分工） |
| 分离的「凭据」 | **SMPL 自带 $\beta/\theta$ 分工** | **3DMM 的中性身份 vs performance** | 多 ID 数据集的风格 | **一条轨迹的时间不变性** |
| 下游目标 | 跨身份动画质量 | retargeting / 插值 / 补全 / 去噪 | 风格可控 + 身份泛化 | **长时身份不漂 + 逐角色运动风格 + 约束生成** |
| **长时漂移** | ✗ 未涉及 | ✗ 未涉及 | ✗ 未涉及 | ★ **核心问题** |

### 4.5.4 我们的增量（严格收窄为四条）

```
① 长时漂移      三篇都不涉及「长时段漂移与漂移率」——这是我们的核心
② 划分线要从数据学   RASA / CGF 都【依赖现成参数化模型自带的分工】
                （SMPL β/θ；3DMM 中性身份 vs expression）；
                20 维 α 里【没有这种自带分工】→ 划分线本身要被学出来
③ 逐角色 + 单视频   CGF 的 identity code 是「可换的」，不是「从单角色视频
                学其专属运动习惯」；DSfusion 用 multi-ID 数据集
④ 视频生成侧       不是 3D mesh / 3DMM，而是在【已有生成模型的隐运动变量】上
```



**结论：有，而且不止一篇。** 这直接影响「共享上游命题」的新颖性判断。

| 工作 | 出处 | 它怎么表述这个纠缠 |
|------|------|------------------|
| **`RASA: Disentangled Spatial-Motional Priors for Cross-Identity Character Animation`** ★ | 2026, arXiv **2608.28219** | 「**The core challenge lies in the inherent entanglement of two capabilities: cross-identity spatial mapping**（aligning position, scale, and skeletal proportions）**and motion control**（refining joint articulation, volumetric consistency, and view coherence）」；做法是把**空间映射与运动控制解耦**，向 DiT 注入结构化先验 |
| **`Facial Animation with Disentangled Identity and Motion using Transformers`** | *Computer Graphics Forum* 2022, **cites=15** | 在 3D 形变模型上**用 transformer 学 motion manifold**（可建模任意长度的 3D 几何序列），并**解耦身份与运动** |
| **`Style-Disentangled Diffusion for Controllable and Identity-Generalized Speech-Driven Body Motion Generation`** | ICASSP 2026 | 从 **multi-ID 数据集**学**每个说话人的个人风格**；引入 **style disentanglement module** 提升解耦度与可解释性 |

**三条重要差别（本项目仍可立足之处）**：

1. **分解轴不同**：`RASA` 是**能力分离**（空间映射 vs 运动控制）；`Facial Animation with Disentangled...` 是**表示分离**；本项目是**时间不变性分离**（一条轨迹里「不变的」vs「变的」）。**沿时间的不变性划分这条轴，本轮未见同名工作。**
2. **`RASA` 是跨身份驱动**（source 驱动 target）；本项目是**同一身份的逐角色特化**。
3. **风格那篇是身体动作 + multi-ID 数据集**；本项目是**面部 + 单角色视频**。

**⚠ 因此：共享上游命题不能宣称是「我们发现的问题」** —— 必须写明「这是已被命名的问题（引上述三篇），我们的增量是**时间不变性这条轴** + **逐角色 + 单视频**」。

## 5 待核实（收敛后 3 项 + 1）

**本轮已核实并落进正文**：`BlendFace`（属性泄漏, cites=58）· VFR 三经典（NAN cites=421 / ADRL cites=199 / Eigen-PEP cites=134）· `FlexAvatar` 两篇（单目歧义的根因命名 + 变长输入聚合）· `AniGS`（CVPR 2025, cites=13）· **身份 / 运动分离的三篇直接邻居**（§4.5）· `Subject-Diffusion`（cites=71）。

**仍待核实**：

- [ ] **UIKA 的原文与消融**：标题检索未命中（`UIKA` 被印尼高校论文占满）→ 按 UV 对应 / 双流注意力的关键词再查；重点是**参考数变化与大姿态的失败模式**
- [ ] **三通道判别器**（身份 / 质量 / 时序漂移）是否已有实现 —— `数字人领域问题` §一 把它列为**验收要求**，但「是否有人真的这么做」本轮未找到
- [ ] **`RASA` / `Facial Animation with Disentangled...` 全文**：确认它们的「不变性」定义与本项目的**时间不变性轴**是否真的不同（决定 DC54 的表述强度）
- [ ] 中文侧（搜狗）同题工作

## 6 一句话版

> **单帧不是退让，是解耦架构的一部分**（多帧会让 $s$ 带上运动统计）；它的根本困难是**歧义而非信息不足**，而**歧义的根因已被命名**（`FlexAvatar`：driving signal × target viewpoint 纠缠）。多帧/视频提身份在**识别**侧（VFR：变长 + 注意力聚合 + 质量感知选帧，2017 年就成型）与**资产**侧（多视角 3D 重建，变长输入聚合到 canonical 锚）都是成熟的成功路线，在**生成**侧仍是覆盖问题而非自洽问题 —— 「**多参考改善看不到的角度，但不解决所有角度是否同一人**」。而多帧聚合的隐含前提（「这些帧属于同一身份」）**与我们要证明的东西循环**。**最后**：身份/运动分离这个上游命题**已被实现过** —— `CGF 2022` 的「**constant facial identity vs time-varying expressions + 两个 latent 子空间**」与我们的命题**逐字同构**；`RASA` 2026 是最新同类（分阶段、丢 $\beta$ 留 $\theta$）。我们的增量**严格收窄为四条**：**① 长时漂移 ② 划分线要从数据学（20 维 α 没有自带分工） ③ 逐角色单视频 ④ 视频生成侧**。
