## Context

身份验证模型（人脸识别 / 人脸比对）是本项目绕不开的**外部依赖**，但库内没有它的技术介绍：

- `数字人概述/数字人身份` 里 `ArcFace`、`CurricularFace`、`AdaFace` 以"CSIM 这把借来的尺子"出现，解释了五类失效与我们的实测，但没有解释这些编码器自己是怎么训练的、彼此差在哪、为什么会被当成事实标准。
- `knowledge/digital-human-identity-consistency`（博客系列十八导入）第 2.4 节给了一小段人脸识别编码器谱系（VGG-Face 2015 → FaceNet 2015 → ArcFace 2019 → CurricularFace / AdaFace → SFace / GhostFaceNet 2023），只为"同族不同几何、换尺子排名翻转"这一节服务，不是模型综述。
- 外部站点 `~/gongshangzheng.github.io` 已核查：`src/pages/arcface-2018.html` 是一篇 ArcFace 单篇深读（问题精确形式、测地线距离、additive angular margin、为什么加在角度上、sub-center ArcFace、ArcFace 反演），`digital-human-training-loss-survey.html` 有"1.5 身份保持损失 / ArcFace 身份损失"一节但只讲生成侧怎么用这个 loss。**没有**从任务定义、损失谱系、数据与骨干工程到选型的身份验证模型综述。

因此本变更只做一件新增、一件收敛：

1. 在 `management/docs/技术介绍/` 新增一篇**通用**身份验证模型技术介绍，作为可复用术语入口（与同目录已存在的 `dpo-直接偏好优化.md` 平级）。
2. 收敛 `数字人概述/数字人身份` 的度量段落，把通用原理改为链接，项目实测继续留在原处。

## Goals / Non-Goals

**Goals:**

- 讲清身份验证的任务本体：验证 / 识别检索 / 聚类的共同基础是"可泛化的度量空间"，开集设定为何不能沿用闭集分类思维，embeddings + 余弦/距离这一统一接口从哪来。
- 讲清评测：verification 与 identification 两套协议、TAR@FAR / EER / CMC / TPIR@FPIR 等指标的语义、基准代际（基准到饱和后领域为何转向非受限场景），以及"跨协议 / 跨编码器不可直接比"这条边界。
- 讲清损失谱系：分类式 softmax → center loss → triplet / contrastive（FaceNet）→ 归一化 softmax（NormFace）→ 大 margin 族（SphereFace 乘性角间隔、CosFace 加性余弦间隔、ArcFace 加性角间隔），并给出 ArcFace 的公式、几何直觉与 `s` / `m` 的作用。
- 讲清"损失之外"：数据规模与清洗、骨干网络、大规模身份分类器的工程代价（Partial FC 一类）、标签噪声治理（sub-center ArcFace），结论是"同损失换数据/骨干的收益常大于换 loss"。
- 讲清 ArcFace 之后为什么没有被全面替代：AdaFace（按图像质量自适应 margin）、MagFace（用模长表达质量）、ElasticFace（随机 margin）、CurricularFace（课程式难负样本）、UniFace 一类各自针对哪种失败模式，适用在哪。
- 给出场景到模型的选型对照，并明确"生成侧把人脸识别模型当裁判 / 损失 / 奖励 / 选帧器"时的边界。

**Non-Goals:**

- 范围**限定人脸**（face verification / recognition）。不展开声纹、证件 OCR、活体检测、防伪与远程身份核验业务链路（已获用户确认）。
- 不写任何具体数字人模型的实验细节或数值：方向游走、锚点引导、Learned Anchor Force、CSIM 当 loss 放弃等全部留在 `数字人概述/数字人身份`，本文只做原理与接口层面的指向。
- 不写成论文导读合集：每篇只取它解决的问题、机制、代价与适用场景，不逐篇复述实验表。
- 不新增前后端功能、目录排序常量、依赖；不改 `server/` 与 `web/`。

## Decisions

### 1. 落点、命名与元数据

在 `management/docs/技术介绍/` 新建 `face-verification-models.md` 与同名 sidecar `face-verification-models.json`。理由：与同目录 `dpo-直接偏好优化.md` 同为"可复用技术介绍"；英文 slug 稳定、URL 友好，与 `knowledge/` 英文 slug 惯例一致。

- frontmatter：`title`（《人脸身份验证模型》）、`author: 汤问`、`date`、`tags`（如 `[人脸识别, 身份验证, 度量学习, ArcFace, margin loss]`）、`summary`（一句话概括覆盖范围）、`order: 20`（同目录 DPO 已占 10）。
- sidecar：`changelog` 记初版；`related` 以对象形式登记 `数字人概述/数字人身份`（主要消费方）、`knowledge/digital-human-identity-consistency`（被批判的度量证据）、`技术介绍/dpo-直接偏好优化`（同目录兄弟篇）。
- 跨文档链接使用 `[[数字人概述/数字人身份|数字人身份]]` 形态；仅链接已存在文档，落笔前逐个核验 slug。

### 2. 完整二级章节结构

目标读者：需要在项目内理解、引用或评估人脸身份验证模型的研发读者；用途是库内术语入口与选型依据，与任何具体数字人模型解耦。正文只用 `##` / `###`，标题具体、不使用"概述 / 背景"类空桶标题。

**实施修正（2026-09-23）**：本仓库 13/13 既有文档都在 frontmatter 之后保留一个与 `title` 一致的 `#` 标题行，文档列表 / 详情与页面目录依赖该约定；因此本文档同样以 `# 人脸身份验证模型` 作为正文标题行，其下仍只用 `##` / `###`，不跳级。

| 节 | 标题 | 论点与结论 | 必备元素 |
|---|---|---|---|
| 1 | `## 身份验证到底在解什么` | 从"两张脸是不是同一个人"切入，区分 verification（1:1 比对）、identification / retrieval（1:N 检索）、clustering（无注册库聚类）；开集设定决定训练分类与部署任务不同构；共同基础是"同一嵌入空间 + 余弦/距离阈值"这一统一接口。结论：要的是**跨身份可比、跨条件稳定的嵌入空间**，而不是把人分对。 | 任务形式化小表；`注册 → 提特征 → 比对/检索 → 阈值判定` 的 Mermaid 图；术语表首列（verification / identification / open-set / gallery / probe）。 |
| 2 | `## 怎么衡量一个验证模型` | 指标分两族：verification 的 ROC / TAR@FAR / EER，identification 的 CMC / TPIR@FPIR；协议不可互换。基准代际：早期受限协议到饱和后，领域转向非受限、跨姿态、大规模检索的评测集。结论：**排行榜数字只在协议内可比**，跨协议、跨编码器、跨数据集不可直接比。 | 指标语义表；基准代际表（协议 → 测什么 → 为什么淘汰）；一条"跨编码器读数差"的边界说明（引用库内已有批判文档，不新造数字）。 |
| 3 | `## 从分类损失到度量学习` | 演进链条：softmax CE（只求分对）→ center loss（拉紧类内）→ triplet / contrastive（FaceNet 显式拉近推远）→ 归一化 softmax（NormFace：把分类放到超球面）→ 大 margin 族：SphereFace 乘性角间隔、CosFace 加性余弦间隔、ArcFace 加性角间隔。给出 ArcFace 的 logit 与损失公式，说明为什么在角空间加 margin 几何上更干净、`s` 与 `m` 各自控制什么、调大调小各自坏在哪。结论：**归一化 + 大 margin** 是当前主流范式，ArcFace 是其中代表而非唯一。 | ArcFace 公式（`$$...$$`）+ 符号表；大 margin 族对照表（方法 / margin 形式 / 直觉 / 代价）；`softmax → 归一化 → 加 margin` 的 Mermaid 谱系图。 |
| 4 | `## 决定上限的不只是损失` | 三件事和损失同样决定结果：数据（规模、清洗、人种/年龄/姿态覆盖、长尾与标签噪声）、骨干（IR-ResNet 到轻量网与 Transformer 类）、大规模身份分类器的工程代价（全量分类头过重 → Partial FC 一类采样方案）。指出同一损失换数据/骨干的收益常大于换损失函数的收益。结论：**先看数据与骨干，再谈损失选型**。 | 影响因素表；"数据 / 骨干 / 损失 / 工程" 的 Mermaid 汇总图。 |
| 5 | `## 自适应 margin 与鲁棒性改进` | ArcFace 用固定 margin、对所有样本一视同仁，于是低质样本被硬性约束、标签噪声被放大。后续工作分两路：按**样本质量/难度**自适应（AdaFace 按质量、MagFace 用模长编码质量、CurricularFace 课程式强调难负样本、ElasticFace 随机 margin）与按**噪声结构**改进（sub-center ArcFace 用多子中心兜噪声标签）。逐条说明各自针对的失败模式与代价。结论：ArcFace 之后是"让 margin 更懂数据"，**不存在无条件的全面替代**；低质/遮挡/监控场景优先对比 AdaFace 与 MagFace。 | 方法对照表（方法 / 核心改变 / 处理的问题 / 适用场景）；谱系 Mermaid（ArcFace → 自适应 / 噪声鲁棒两支）。 |
| 6 | `## 作为数字人度量与损失时，人脸识别模型的边界` | 人脸识别编码器是为"两张真实照片是否同一人"训练的；生成侧把它挪用作 CSIM 度量、身份损失、强化学习奖励、选帧器，这四种挪用共享同一批假设。按库内已有批判文档给出五类已知失效（风格化、时序漂移、环境不鲁棒、长时演变、度量循环性）的**机制级**解释，并明确它是**必要条件而非充分条件**。结论：嵌入的训练分布决定它在哪里有效，跨域使用必须显式声明度量边界。 | 四角色挪用 Mermaid 图；失效机制表（失效 → 机理 → 触发条件）；指向 `[[数字人概述/数字人身份|数字人身份]]` 的实测结论与 `knowledge/digital-human-identity-consistency` 的批判证据，本文不复制数值。 |
| 7 | `## 场景到模型的选型对照` | 把前面所有结论收成一张对照：照片域验证/检索、非受限监控与低质图像、轻量端侧、百万级以上身份库、生成侧评测与风格化域、需要质量评估或拒识。结论：默认从 ArcFace 系基线起步，按数据质量、规模与是否跨域分叉选择，且任何选择都要配与场景匹配的协议与人工检查。 | 场景 → 推荐方法 → 理由 → 注意边界 的对照表。 |
| 8 | `## 术语与符号表` | 汇总全文术语与符号，使读者无需回翻。 | 术语表（verification / identification / margin / TAR@FAR / Partial FC 等）+ 符号表（`x`、`W`、`θ`、`s`、`m`、`N` 等）。 |

公式只出现在第 3 节且为通用形式（ArcFace 及其同族的 logit / loss），不引用任何某个数字人模型的取值。第 2、5、6 节涉及的具体数字**只允许转引库内已有文档并标注其来源**，不新造、不凭记忆写。

### 3. 与《数字人身份》及其他文档的职责边界

- `技术介绍/face-verification-models.md`：只讲通用原理与谱系（任务、协议指标、损失、数据骨干、自适应改进、挪用边界、选型）。
- `数字人概述/数字人身份.md`：保留项目自身实测与结论（模长/方向假说、锚点引导、训练期条件化 v1/v2、Learned Anchor Force、CSIM 当 loss 放弃、锚帧库口径），把"人脸识别嵌入的余弦相似度为什么是事实标准、ArcFace 与后继者差在哪"改为链接到新文档，不重复解释。
- `knowledge/digital-human-identity-consistency.md`：外部导入源，视为只读证据，**不修改**；新文档只引用其结论。
- 本次对《数字人身份》的改动限定在度量段落：**压缩重复的通用人脸识别解释**（例如"人脸识别嵌入的余弦相似度为何是事实标准"、编码器代际枚举）改为指向新文档的链接，项目实测、数值、表格、图原样保留。

### 4. 参考论文清单（已核实）

**核实方法**：本机 `search.py --probe` = `PROXY_OFF`（VPN 未连），arXiv API 直连不可用；改用 **OpenAlex（直连可用）** 逐条按标题检索、按 `10.48550/arxiv.<id>` DOI 反查确认，缺项用 **Semantic Scholar** 补。下表每行的 arXiv / DOI 均已实际请求校验过。

凡写进正文的论文以此为唯一白名单；未在表内的编号不得出现。标 ☆ 为核心引用，其余为可选（可按篇幅裁剪）。

#### 第 1 节 任务定义与统一接口

| 论文 | 出处 | 标识 | 用途 |
|---|---|---|---|
| ☆ DeepFace: Closing the Gap to Human-Level Performance in Face Verification | CVPR 2014 | doi:10.1109/CVPR.2014.220 | 深度学习人脸验证的起点，闭集分类式训练的代表 |
| ☆ FaceNet: A Unified Embedding for Face Recognition and Clustering | CVPR 2015 | doi:10.1109/CVPR.2015.7298682 / arXiv:1503.03832 | 提出 embedding + 距离阈值的统一接口与 triplet 损失 |
| Deep Face Recognition（VGGFace） | BMVC 2015 | doi:10.5244/C.29.41 | 大规模身份分类训练的早期范式 |

#### 第 2 节 评测协议与基准代际

| 论文 | 出处 | 标识 | 用途 |
|---|---|---|---|
| ☆ Labeled Faces in the Wild（原始技术报告 2007；本文引其综述） | Springer 2016 综述 | doi:10.1007/978-3-319-25958-1_8 | 受限协议基准，用于说明"基准饱和后领域为何转向非受限场景" |
| ☆ The MegaFace Benchmark: 1 Million Faces for Recognition at Scale | CVPR 2016 | doi:10.1109/CVPR.2016.527 | 1:N 检索协议与百万级干扰项 |
| ☆ IARPA Janus Benchmark-C: Face Dataset and Protocol | ICB 2018 | doi:10.1109/ICB2018.2018.00033 | 非受限视频/跨姿态协议，TAR@FAR 与 TPIR@FPIR 的标准来源 |
| MS-Celeb-1M: A Dataset and Benchmark for Large-Scale Face Recognition | ECCV 2016 | arXiv:1607.08221 | 训练数据规模化里程碑 |
| WebFace260M: A Benchmark Unveiling the Power of Million-Scale Deep Face Recognition | CVPR 2021 | arXiv:2103.04098 | 数据规模与清洗对上限的影响 |
| Masked Face Recognition Challenge: The InsightFace Track Report | ICCVW 2021 | doi:10.1109/ICCVW54120.2021.00165 / arXiv:2108.08191 | 遮挡场景下的评测口径 |
| （库内）`knowledge/digital-human-identity-consistency` | — | 库内文档 | 转入"跨编码器 / 跨协议不可直接比"的证据，标注为转引 |

#### 第 3 节 损失谱系

| 论文 | 出处 | 标识 | 用途 |
|---|---|---|---|
| ☆ A Discriminative Feature Learning Approach for Deep Face Recognition（Center Loss） | ECCV 2016 | doi:10.1007/978-3-319-46478-7_31 | 从"分对类"到"拉紧类内"的第一步 |
| ☆ FaceNet（triplet） | CVPR 2015 | arXiv:1503.03832 | 度量学习的代表 |
| ☆ NormFace: L2 Hypersphere Embedding for Face Verification | ACM MM 2017 | arXiv:1704.06369 | 归一化 + 尺度因子，把分类问题放到超球面上 |
| ☆ SphereFace: Deep Hypersphere Embedding for Face Recognition | CVPR 2017 | doi:10.1109/CVPR.2017.713 / arXiv:1704.08063 | 乘性角度间隔（A-Softmax） |
| ☆ CosFace: Large Margin Cosine Loss for Deep Face Recognition | CVPR 2018 | doi:10.1109/CVPR.2018.00552 / arXiv:1801.09414 | 加性余弦间隔（AM-softmax） |
| ☆ ArcFace: Additive Angular Margin Loss for Deep Face Recognition | CVPR 2019 / TPAMI 2021 | doi:10.1109/CVPR.2019.00482 / arXiv:1801.07698 / doi:10.1109/TPAMI.2021.3087709 | 加性角度间隔；本文核心公式与几何直觉的来源 |

#### 第 4 节 数据、骨干与大规模分类器工程

| 论文 | 出处 | 标识 | 用途 |
|---|---|---|---|
| ☆ Partial FC: Training 10 Million Identities on a Single Machine | ICCVW 2021 | arXiv:2010.05222 | 千万级身份的全量分类头为何不可行；Glint360K 来源 |
| ☆ Killing Two Birds with One Stone: Efficient and Robust Training of Face Recognition CNNs by Partial FC | CVPR 2022 | arXiv:2203.15565 | 部分 FC 的效率与鲁棒性改良 |
| VGGFace2: A Dataset for Recognising Faces across Pose and Age | FG 2018 | arXiv:1710.08092 | 数据覆盖（姿态 / 年龄）对泛化的影响 |
| MobileFaceNets: Efficient CNNs for Accurate Real-Time Face Verification on Mobile Devices | CCBR 2018 | arXiv:1804.07573 | 轻量骨干一支 |
| TransFace: Calibrating Transformer Training for Face Recognition from a Data-Centric Perspective | ICCV 2023 | doi:10.1109/ICCV51070.2023.01887 | Transformer 类骨干的代表 |
| SFace: Sigmoid-Constrained Hypersphere Loss for Robust Face Recognition | IEEE TIP 2021 | doi:10.1109/TIP.2020.3048632 | 合成数据训练与轻量部署 |
| GhostFaceNets: Lightweight Face Recognition Model From Cheap Operations | IEEE Access 2023 | doi:10.1109/ACCESS.2023.3266068 | 轻量骨干的另一种取法 |

#### 第 5 节 自适应 margin 与鲁棒性改进

| 论文 | 出处 | 标识 | 用途 |
|---|---|---|---|
| ☆ Sub-center ArcFace: Boosting Face Recognition by Large-Scale Noisy Web Faces | ECCV 2020 | doi:10.1007/978-3-030-58621-8_43 | 每类 K 个子中心兜噪声标签（"噪声鲁棒"支） |
| ☆ CurricularFace: Adaptive Curriculum Learning Loss for Deep Face Recognition | CVPR 2020 | arXiv:2004.00288 | 课程式强调难负样本 |
| ☆ MagFace: A Universal Representation for Face Recognition and Quality Assessment | CVPR 2021 | doi:10.1109/CVPR46437.2021.01400 / arXiv:2103.06627 | 用 embedding 模长编码样本质量 |
| ☆ AdaFace: Quality Adaptive Margin for Face Recognition | CVPR 2022 | arXiv:2204.00964 | 按图像质量自适应 margin；低质场景重点对比对象 |
| ElasticFace: Elastic Margin Loss for Deep Face Recognition | CVPRW 2022 | doi:10.1109/CVPRW56347.2022.00164 | 随机 margin 提升泛化 |
| UniFace: Unified Cross-Entropy Loss for Deep Face Recognition | ICCV 2023 | doi:10.1109/ICCV51070.2023.01895 | 统一损失视角 |
| Fair Loss: Margin-Aware Reinforcement Learning for Deep Face Recognition | ICCV 2019 | doi:10.1109/ICCV.2019.01015 | 按类内/类间状态动态调 margin |

#### 第 6 节 挪用到生成侧的边界（已按用户裁决收敛到 ☆ 6 篇）

| 论文 | 出处 | 标识 | 用途 |
|---|---|---|---|
| ☆ Arc2Face: A Foundation Model for ID-Consistent Human Faces | CVPR 2025 | arXiv:2403.11641 | "嵌入容量即 CSIM 天花板"的探针 |
| ☆ Face Consistency Benchmark for GenAI Video（FCB） | arXiv 2025 | arXiv:2505.11425 | 双协议 × 六编码器的排名反转 |
| ☆ ID-Sim: An Identity-Focused Similarity Metric | arXiv 2026 | arXiv:2604.05039 | 把"对环境不变、对身份敏感"写成公理 |
| ☆ StyleID: A Perception-Aware Dataset and Metric for Stylization-Agnostic Facial Identity Recognition | arXiv 2026 | arXiv:2604.21689 | 风格化域上 ArcFace 判定降到抛硬币 |
| ☆ Identity-GRPO: Optimizing Multi-Human Identity-preserving Video Generation via Reinforcement Learning | arXiv 2025 | arXiv:2510.14256 | ArcFace 当 RL 奖励的预测准确率不合格 |
| ☆ VBench-2.0: Advancing Video Generation Benchmark Suite for Intrinsic Faithfulness | arXiv 2025 | arXiv:2503.21755 | Human Identity 维度直接挪用人脸识别模型 |
| （库内）`knowledge/digital-human-identity-consistency` | — | 库内文档 | 换脸时代、ConsisID、PuLID、ID-V2V、FaceShifter / SimSwap 的转述与证据来源 |

**已按用户裁决退出白名单**：FaceShifter `arXiv:1912.13457`、SimSwap `arXiv:2106.06340`、ConsisID `arXiv:2411.17440`、PuLID `arXiv:2404.16022`、ID-V2V `arXiv:2607.22830`。这五篇在正文里只作为机制叙述出现，不单列引用，需要证据时指向库内文档。保留备查，如后续需要可直接从本行恢复。

#### 未核实与不引用

- **OpenS2V-Nexus**：OpenAlex 仅有会议 DOI `10.52202/085713-4982`，arXiv 编号在 `PROXY_OFF` 下无法核实 → 若正文需要这一口径分歧，改为引用库内 `knowledge/digital-human-identity-consistency` 的转述，或开启 VPN 后补核实。
- 未进入白名单的编号一律不写入正文；素材摘要阶段如发现更好的替代或补充，需回写本表后再动笔。
- **正文可引用的总数**：第 1–5 节 29 行 / **28 篇**（FaceNet 在第 1、3 节各出现一次，其中 ☆ 17 篇）+ 第 6 节 ☆ 6 篇 = **34 篇**（☆ 23 篇），另加库内文档转引。

#### 素材获取状态（2026-09-23）

| 层级 | 覆盖 | 说明 |
|---|---|---|
| 书目（DOI / arXiv） | 34 篇全部 | OpenAlex 逐条反查 + S2 补，前期已发现并修正 9 个错误编号 |
| 摘要原文 | 21 篇 | OpenAlex `abstract_inverted_index` 直取原文，已存档于对话记录 |
| 无摘要 | Center Loss、sub-center ArcFace | Center Loss 仅做谱系定位（依据 CosFace 摘要对其定位的表述）；sub-center ArcFace 改用本地博客深读页 |
| 机制级细节 | ArcFace 公式链、sub-center K 与噪声率、IBUG-500K | 来自本地 `~/gongshangzheng.github.io/src/pages/arcface-2018.html`（含 `L_1 → L_2 → L_3` 推导与统一 `(m_1,m_2,m_3)` 框架，标注来源为原论文） |
| 生成侧 6 篇 | 5 篇有本地深读页 + 摘要；Identity-GRPO 仅摘要 | 本地页：`arc2face-2024` / `face-consistency-benchmark-2025` / `id-sim-2026` / `styleid-2026` / `vbench2-2025` |

**证据层级限制（需用户知悉）**：`PROXY_OFF` 下 arXiv 全文不可读，除上述本地深读页外，其余论文的机制描述停**摘要 + 标题级**。若正文需要逐篇数值或公式，需开 VPN 后补全文核实，否则正文只能写到摘要能支撑的粒度。

#### 审核门禁

上表即素材白名单。设计确认后提交**素材摘要**（每篇只取：问题设定、机制、代价 / 边界、拟用在文档哪一节），用户确认口径后才进入撰写；第 3 节公式需在摘要中给出原始形态与符号定义。

## Risks / Trade-offs

- [写成论文导读合集，失去技术介绍的可复用性] → design 明确 Non-Goals 与"每篇只取问题/机制/代价/场景"的取材粒度；第 5 节用对照表而非逐篇小节。
- [范围漂移成"数字人身份一致性综述"或"通用身份核验业务综述"] → 第 6 节只做接口与边界，业务核验（声纹、证件、活体）明确列为 Non-Goal。
- [与《数字人身份》重复或口径冲突] → 边界见 Decision 3；新文档不复制项目实测数值，《数字人身份》保留唯一事实源。
- [凭记忆写公式或书目编号] → 素材阶段逐篇核实并以官方版本为准；未核实编号不写入正文。
- [网络不可用导致无法核实一手资料] → 素材阶段先探测；不可核实的条目在摘要中显式标注，交由用户裁决。
- [新目录顺序被破坏] → `order: 20` 放在 DPO 之后，不运行 `renumber`，不改既有文档 order。

## Migration Plan

1. 用户审核本 design（含完整章节结构）并确认；如有异议先改 design 再继续。
2. 提交素材摘要（损失谱系组 + 自适应改进组 + 评测与边界组）供第二次审核，确认口径。
3. 创建 `management/docs/技术介绍/face-verification-models.md` 与 sidecar；按 Decision 3 收敛 `数字人概述/数字人身份.md` 的度量段落与 sidecar `related`。
4. 校验：frontmatter / sidecar JSON 合法性、站内链接目标存在、公式定界符、Mermaid 可渲染、文档列表与详情接口能返回新 slug；运行 `openspec validate --change docs-add-face-verification-model-intro`。
5. 回滚：删除新文档与 sidecar，还原《数字人身份》的链接与措辞；不涉及代码、数据库或服务端状态。

## Resolved Decisions（用户已确认）

| # | 事项 | 结论 |
|---|---|---|
| 1 | 范围 | **只做人脸**（face verification / recognition）；声纹、证件核验、活体检测、防伪明确排除 |
| 2 | slug | **`face-verification-models.md`** + `face-verification-models.json`（英文，URL 友好） |
| 3 | 对《数字人身份》的改动 | **压缩其度量小节中重复的通用人脸识别解释 + 加链**；项目实测、数值、表格、图全部保留 |
| 4 | 第 5 节是否单列"后继者"一节、标题怎么写 | **不单开一节**；标题定为 `## 自适应 margin 与鲁棒性改进`，**不冠"ArcFace 之后"前缀**。"后续有没有替代"由正文论述回答，不进标题 |
| 5 | 参考清单篇幅 | **§6 只保留 ☆ 级 6 篇**（Arc2Face / FCB / ID-Sim / StyleID / Identity-GRPO / VBench-2.0）；FaceShifter / SimSwap / ConsisID / PuLID / ID-V2V **不引用**，改为指向库内文档 |
