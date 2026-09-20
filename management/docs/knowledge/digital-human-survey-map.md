---
title: "数字人系列（十九）：综述地图——市面数字人综述精读对比与新模型线索"
description: "内容级对比市面四篇数字人综述：From Pixels to Portraits v8 的五族分类与公开模型实测表、Human Motion Video Generation 的三段管线、THG Taxonomy 的编辑轴、Advancing THG 的 Loss 专节，并整理 12 条新模型线索。"
date: 2026-09-07T21:21:45
created_at: 2026-09-07T21:21:45
updated_at: 2026-09-07T21:21:45
tags: [数字人, 综述, Survey, Talking Head, 文献地图]
aliases: ["categories/AI/数字人"]
sub_id: 190
papers: ["https://arxiv.org/abs/2308.16041", "https://arxiv.org/abs/2509.03883", "https://arxiv.org/abs/2406.10553", "https://arxiv.org/abs/2507.02900"]
toc: true
hero_title: "数字人综述地图"
hero_sub: "市面上有哪些综述、各自说了什么"
hero_tagline: "系列（十九）· 4 篇精读 · 内容级对比 · 12 条新线索"
---

> 来源：博客 gongshangzheng.github.io `src/pages/digital-human-survey-map.html`，html2text 转换复制于 2026-09-20。原文：https://gongshangzheng.github.io/digital-human-survey-map.html

4综述精读

12新模型线索

3类组织

11未来方向

系列（十九）

综述地图：市面数字人综述精读对比与新模型线索

数字人系列的每一篇都在回答"技术怎么做"——系列一讲实时生成的技术路线，系列三讲运动空间，系列七讲流式与蒸馏。但还有一个更基础的问题没有被正面回答过：**这个领域的综述版图长什么样？市面上有哪些综述，它们各自说了什么、独门武器是什么、我该读哪一篇？** 本篇把四篇代表性综述的原文拉下来逐篇精读——不是罗列引用，而是拆解它们各自的分类体系、独特贡献和局限，再画出与库内系列的映射关系。

**一句话结论** ：四篇综述恰好互补——[From Pixels to Portraits v8](https://arxiv.org/abs/2308.16041) 胜在"2026 视角 + 公开模型实测对比"，[Human Motion Video Generation](https://arxiv.org/abs/2509.03883) 胜在"全身视角 + 三段管线框架"，[THG Taxonomy](https://arxiv.org/abs/2406.10553) 胜在"把 Editing 当一级类"，[Advancing THG](https://arxiv.org/abs/2507.02900) 胜在"Loss 专节 + 百篇方法大表"。读完本篇，你可以按需索骥。

[←上一篇身份一致性](digital-human-identity-consistency.html) [枢纽页数字人系列总览](digital-human-hub.html)

精读一

From Pixels to Portraits v8：2026 视角的 THG 全景

这是你检索"talking head survey"时最常撞见的一篇。它 2023 年 8 月首发，2026 年 7 月 7 日刚刚完成第八版大更新，发表于期刊 _Computer Science Review_ #Gowda2026FPSP#。v8 相对早期版本最大的变化是：**taxonomy 从"按输入模态"升级为"按模态 + 表示/生成范式"的五族分类** ，并加入了对公开可得模型的实测对比——这两点让它从"又一篇综述"变成了值得精读的文献地图。

### 五族 taxonomy 与横切关注带

v8 把 talking head generation 分为五个家族#Gowda2026FPSP#：

家族| 子方向| 代表方法  
---|---|---  
2D 视觉/视频驱动| reenactment、motion retargeting、expression transfer、高分辨率高效动画| Face2Face、FOMM、TPSM、LivePortrait  
音频驱动| 唇形同步、audio-to-face/head、情绪风格韵律、实时流式| Wav2Lip、SadTalker、VASA-1、Teller、READ  
扩散与基础视频模型| audio-to-video diffusion、video DiT、大规模人体动画、长时生成| EMO、Hallo 1-3、OmniHuman-1  
3D / NeRF / Gaussian| 3DMM 网格、NeRF 隐式场、3DGS、视角一致渲染| GaussianAvatars、LAM、GaussianSpeech、VASA-3D  
文本/语义/编辑控制| 文本驱动、表情情绪控制、retalking、交互 avatar 控制| Write-a-speaker、TalkCLIP、EditYourself  
  
FPSP v8 的 taxonomy 与方法时间线图（图片资源未随副本复制）

FPSP v8 配图：方法 taxonomy 与时间线（图源：原论文 arXiv 2308.16041）

值得注意的是，作者明确说这五族**不互斥** ：VASA-1 既是音频驱动又是实时生成，GaussianSpeech 既是音频驱动又是 3DGS——taxonomy 应该被当作"理解每族主导设计选择"的工具，而不是严格的分区#Gowda2026FPSP#。文末还有一条横切关注带，把身份保持、唇同步、时序一致性、推理时间、显存、安全/溯源/深伪滥用列为所有家族共有的约束。

### 十条质量维度与"指标-感知脱节"论点

v8 把"一条好的 talking head 视频"拆成十条质量维度：身份保持、唇同步、视觉保真、时序一致性、自然运动与表现力、可控性、视角/几何一致性、泛化鲁棒性、效率可部署性、安全与负责任使用#Gowda2026FPSP#。十条之间是**相互牵制** 的：提升表现力可能加剧身份漂移，提高分辨率可能牺牲实时性，追求唇同步精确可能让头部运动变得僵硬。

全文最有价值的论点是：**帧级指标与人类感知严重脱节** 。PSNR/SSIM 只测像素级相似；FID/FVD 测分布但不测身份与对齐；Sync 置信度测唇同步但忽略表情自然度#Gowda2026FPSP#。作者的结论是：任何严肃的比较都必须注明驱动模态、数据集、分辨率、时长与硬件——否则数字没有意义。这与库内系列九（评测选型）和系列十二（实时性对比）的立场高度一致。

### 独家货：公开模型实测对比表

大多数综述只汇总论文里报告的数字，FPSP v8 却对公开可复现的方法做了一轮自己的实测：同一组源图像（奥巴马、詹姆斯、海姆斯沃斯、孙兴慜），比较推理时间、显存占用与人评质量#Gowda2026FPSP#：

方法| 年份| 推理时间| GPU 显存| 人评 rating  
---|---|---|---|---  
FOMM| 2019| 34 s| 2 GB| 3.45  
LipGAN / Wav2Lip| 2019| 23 s| 10.9 GB| 2.76  
Audio2Head| 2021| 20 s| 3.9 GB| 1.69  
DaGAN| 2022| 22 s| 4.6 GB| 3.27  
Video Retalking| 2022| 40 s| 4.4 GB| 3.84  
TPSM| 2022| 19 s| **1.9 GB**| **4.15**  
EmoGen| 2023| 25 s| 2.8 GB| 2.24  
SadTalker| 2023| 4 min 50 s| 4.1 GB| 3.72  
Teller| 2025| **6 s**|  3.6 GB| 4.05  
READ| 2025| 10 s| 2.9 GB| 4.08  
  
两个反直觉发现：其一，**老方法 FOMM 至今"意外能打"** ，视觉竞争力和 2019 年的指标排名完全不符；其二，2025 年的 Teller 和 READ 在把推理时间压到 6-10 秒的同时把人评维持在 4 分以上——"实时化"与"高质量"不再是单选题。作者也诚实声明这不是受控 benchmark，只是暴露指标与感知差距的例证#Gowda2026FPSP#。

### 11 条未来方向（v8 原文归纳）

  * 评测超越帧级指标（联合评估身份/同步/时序/效率/人评）
  * 长时稳定性（身份漂移、表情塌缩、背景不稳应成为标准评测项）
  * 实时与流式生成（打断、轮次切换下的质量保持）
  * 可控表现力 · 3D 一致性与交互 avatar
  * 扩散效率与蒸馏 · 多语言跨文化 · 少样本个性化
  * 公平性与数据治理 · safety-by-design · 以人为中心的评估

精读二

Human Motion Video Generation: A Survey：全身视角与三段管线

如果说 FPSP v8 的镜头对准“头”，这篇 2025 年 9 月挂到 arXiv 的综述（2509.03883，15 位作者）把镜头拉远到**整个人** ：从唱歌的头到随音乐起舞的全身 avatar#Xue2025MotionSurvey#。需要留意：它的正文统计明确标注“截至 2024-08-30”，所以它是一篇用 2025 年发布视角写就的“2024 年知识存量”全景，不含 2024-09 之后的方法。它是市面上少有的把“人体运动视频生成”作为整体任务梳理的文章，对库内系列八（Avatar 类型）和系列十七（手部）是天然的互补视角。

### 三段式管线框架

这篇综述的组织方式不是按方法罗列，而是按**生成管线的三个阶段** #Xue2025MotionSurvey#：

视觉驱动 talking head 方法时间线（图片资源未随副本复制）

FPSP v8 配图：2D 视觉/视频驱动族的方法时间线（图源：原论文 arXiv 2308.16041）

  1. **Motion Planning** ：先规划运动——包括用 LLM 做运动规划、以及从输入特征到运动序列的映射
  2. **Motion Modeling & Video Generation**：把规划好的运动变成视频——按驱动信号分为 vision-driven / text-driven / audio-driven 三线
  3. **Refinement & Output**：后处理与输出——超分、平滑、细节修复

这个"先规划、再生成、后精修"的框架比"按论文年份列时间线"更有工程价值：它直接对应你现在看到的系统分层（比如库内系列十四讲的后端 Agent 管线）。

### 七类人体表征与三类生成框架

综述沿用了 Knap 等人的分类，把人体姿态表征拆成七类#Xue2025MotionSurvey#：

表征| 作用| 典型用法  
---|---|---  
Mask| 轮廓与占位先验| 粗粒度布局控制  
Mesh| 体型与肢体弯曲细节| 弥补关键点丢失的 3D 空间信息（Champ）  
Depth| 空间关系| 遮挡部位生成（Follow-YourShape）  
Normal| 体表朝向| 姿态对齐、视觉保真  
Keypoint| 骨架| OpenPose / DWPose 条件  
Semantics| 部位语义解耦| 分部位独立操控（MagicAnimate）  
Optical Flow| 运动连续性| 抑制背景不稳定  
  
生成框架则归为 VAE、GAN、扩散（含 latent diffusion）三类，audio-driven 章节细分为唇同步、头部驱动、全身驱动、细粒度风格情绪、多语言配音五个子任务#Xue2025MotionSurvey#。

音频驱动 talking head 方法时间线（图片资源未随副本复制）

FPSP v8 配图：音频驱动族的方法时间线，Wav2Lip 到 Teller/READ 一线（图源：原论文 arXiv 2308.16041）

它指出的两大领域级挑战与 FPSP v8 呼应：**唇+头+手势的统一框架仍然缺位** ，以及**扩散路线的实时化困难** ——这正是 2025-12 之后一批动作空间模型（见线索清单）试图解决的问题。

精读三

A Comprehensive Taxonomy of TH Synthesis：把"编辑"立为一级类

这篇 2024 年 6 月的综述（arXiv 2406.10553）的独门武器是 taxonomy 的第三根轴：它把 talking head synthesis 拆成 **Portrait Generation（生成）/ Driven Mechanisms（驱动）/ Editing Techniques（编辑）** 三轴，而"编辑"在多数综述里只是附带一提#Meng2024Taxonomy#。

Driven Mechanisms 一轴里，它对 video-driven 的梳理尤其细致：先分**传统非学习** （几何变换、模板修改如 AAM/blendshape、混合变换）与**学习方法** 两段，再把 Face2Face、X2Face、FOMM、TPSM 等按是否无监督、是否端到端、是否 N-shot、是否依赖 3D 模型列表比较#Meng2024Taxonomy#——这种"传统方法也认真讲"的写法在深度学习时代的综述里很少见，对理解技术演化脉络很有帮助。

Editing 轴的价值在于点破了一个趋势：**talking head 正在从“合成问题”变成“编辑与创作问题”** ——改说话内容、调表情强度、动注视点、改语速、翻译成另一种语言，同时保持身份与真实感。这个方向库内目前没有专门文章（现有文章集中在生成侧），是明确的选题空白。局限方面，该文覆盖截至 2024 年中：扩散基础模型浪潮（Hallo/EMO 系）未纳入，3DGS 说话头仅在 audio-driven 的显式参数化小节简要收录（GaussianTalker、PSAvatar 等）。

精读四

Advancing THG：Loss 专节与百篇方法大表

2025 年 6 月的这篇（arXiv 2507.02900）筛选了约 100 篇 2017–2025.04 的高引方法，按十种范式组织：image-based、audio-based、text-based、video-based、2D-based、3D-based、distortion-based、NeRF-based、parameter-efficiency、3D animation#Rakesh2025Advancing#。

它有两个差异化价值。**第一是 Loss Function 专节** ：把各类方法的损失函数单独抽出来系统讲——重建 loss、感知 loss、GAN loss、同步专家 loss 等，这跟库内[系列十五（Loss 函数族）](digital-human-training-loss-survey.html)直接对标，可以用它来做交叉校验。**第二是每范式一张大表** ：Method / Architecture / Dataset / Highlights / Limitations / N-shot 六列，查某个方法的架构与缺陷时比读原文快得多。

需要提醒的是它的写作质量：存在明显的重复句式和表述粗糙处（同一形容词连用、句子结构断裂），阅读时建议**只看表格和章节结构，行文当参考** #Rakesh2025Advancing#。这也是四篇综述里"信息密度高但编辑质量低"的典型——适合当查表工具，不适合当教材通读。

横向对比

四篇综述对比与按需索骥

### 一张表看懂四篇综述

维度| FPSP v8| Motion Survey| THG Taxonomy| Advancing THG  
---|---|---|---|---  
arXiv / 版本| 2308.16041，v8（2026-07）| 2509.03883（2025-09）| 2406.10553（2024-06）| 2507.02900（2025-06）  
分类体系| 五族 + 横切关注带| 三段管线 × 7 类表征 × 3 类驱动| 三轴：生成 / 驱动 / 编辑| 十大范式  
独特贡献| 公开模型实测表；指标-感知脱节分析| 全身视角；管线化组织| Editing 一级类；传统方法细讲| Loss 专节；百篇大表  
覆盖截至| 2026 年中（含 3DGS/基础模型/智能体辅助）| 2024-08（原文自述统计口径）| 2024 年中| 2025-04  
主要局限| 实测表为作者自测，非受控 benchmark| talking head 只是子集，头部细节浅| 未覆盖扩散基础模型浪潮| 行文质量粗糙，需查表式阅读  
库内对应| 系列一 / 系列九 / 系列十二| 系列八 / 系列十七| 系列一 / 系列二 / 系列三| 系列十五 / 系列九  
  
### 按需索骥

### 你应该读哪篇？

  * **想了解领域全貌与最新进展** → FPSP v8（唯一覆盖到 2026 的），配库内[系列一](realtime-digital-human-survey.html)
  * **想做全身 / 手势 / 舞蹈生成** → Motion Survey，配库内[系列八](digital-human-avatar-survey.html)与[系列十七](digital-human-hand-generation.html)
  * **想做编辑 / retalking / 后期创作** → THG Taxonomy 的 Editing 轴（库内空白，选题线索）
  * **想查某个方法的 Loss / 架构细节** → Advancing THG 大表，配库内[系列十五](digital-human-training-loss-survey.html)
  * **想入门口型同步与换嘴** → FPSP audio-driven 章 + 库内[系列二](digital-human-lip-sync-video-dubbing.html)
  * **想做实时交互 avatar** → FPSP 实测表 + 库内[系列七](digital-human-streaming-distillation.html)、[系列十二](digital-human-realtime-gpu-comparison.html)、[系列十四](digital-human-backend-agent-design.html)

交叉验证

FPSP 实测表 vs 库内系列十二

FPSP v8 的实测表给了我们一个难得的机会：**用外部独立测量的数据交叉校验库内自己的 benchmark 结论** 。把它的数字放到[系列十二（实时性全景对比）](digital-human-realtime-gpu-comparison.html)的坐标系里：

  * **结论方向一致** ：FPSP 实测中 2025 年的 Teller（6s）、READ（10s）在速度与人评上同时领先，与系列十二"运动空间 / 流式路线在实时性上碾压整帧扩散路线"的结论互相印证。
  * **TPSM 的性价比反常** ：1.9 GB 显存 + 4.15 人评是全场最低成本最高分，这与系列十二里"轻量关键点路线在消费级硬件上的实用性"判断一致——值得在选型时重新重视这条 2022 年的路线。
  * **口径差异必须标明** ：FPSP 的表是作者自测（非受控 benchmark，作者原文自述），推理时间的统计口径（单帧 / 整段 / 是否含预处理）未详述；库内系列十二的数据来自论文报告 + 复现实测并注明来源。两边数字**不可直接混排** ，只能做方向性对照。

**方法论收获** ：这组交叉对照示范了读综述的正确姿势——不吸收它的数字，吸收它的"测量维度"。推理时间、显存、人评三列本身就是一份现成的评测模板，与系列十二的 GPU/FPS/延迟维度合并后，可以作为后续所有精读文章 benchmark 表的统一骨架。

线索清单

从综述里挖出的 12 条新线索

精读综述的最大红利是**顺藤摸瓜** 。以下是四篇综述中出现、且库内此前未覆盖的模型与数据集，按行动优先级分三档：

### 待精读（内容密度高，建议立题）

对象| 是什么| 出处  
---|---|---  
READ (2025)| 实时音频驱动生成，FPSP 实测表人评 4.08 / 10s，与 Teller 同级| FPSP v8  
GaussianSpeech| 音频驱动的 3DGS 说话人，FPSP 五族中 3DGS 族的代表之一| FPSP v8  
OmniHuman-1| 字节的一阶段条件人体动画，单图支持特写到全身，模糊 THG 与人体视频生成边界| FPSP v8 / Motion Survey  
EditYourself (2026)| 音频驱动 + DiT 编辑的 talking head 视频编辑，对应"编辑"选题空白| FPSP v8 / THG Taxonomy  
  
### 待跟踪（有价值，暂不立题）

对象| 一句话| 出处  
---|---|---  
Dimitra (2025)| 音频驱动扩散的表现力 talking head| FPSP v8  
Hallo3 (2025)| Hallo 系列的视频扩散 transformer 化| FPSP v8  
PGSTalker / UniGAHA / VASA-3D| 3DGS + 音频驱动的三个新变体（个性化 / 通用 / 3D 化）| FPSP v8  
GaussianEmoTalker (2026)| 情绪可控的 3DGS 说话头| FPSP v8  
TalkVid / SpeakerVid-5M| 新一代大规模多样化训练数据集（规模 ≠ 公平，需治理）| FPSP v8  
  
### 已覆盖（综述提到、库内已有文章）

LAM（[系列八](digital-human-avatar-survey.html) / [精读四十五 →](lam-2025.html)）、VASA-1（[精读五 →](paper-vasa1.html)）、Hallo（[系列五](digital-human-diffusion-foundation-avatar.html)）、EMO、LivePortrait（[精读十三 →](paper-liveportrait.html)）、SadTalker、Wav2Lip、TPSM——这些在综述里的定位可以反过来丰富库内文章的"领域坐标"段落。

结语

综述地图怎么用

四篇综述、三种粒度：FPSP v8 给你**最新的全景图和实测坐标** ，Motion Survey 给你**全身视角和管线框架** ，THG Taxonomy 给你**编辑视角和技术演化史** ，Advancing THG 给你**可查表的百方法索引** 。没有任何一篇能单独替代读原文，但组合起来，它们覆盖了一个研究者进入这个领域 90% 的导航需求。

对库内而言，这次精读也校准了系列的坐标：我们的技术路线划分与 FPSP v8 的五族高度同构（系列一/三/四/五分别对应 2D 驱动/运动空间+扩散/3DGS/基础模型），但**编辑向内容和 LLM 智能体辅助生成** 是两个明确的空白。线索清单里的 READ、GaussianSpeech、OmniHuman-1、EditYourself 是下一批精读的候选——欢迎在评论区点单。

[←上一篇身份一致性](digital-human-identity-consistency.html) [枢纽页数字人系列总览](digital-human-hub.html)

References

参考来源

### 参考来源

  * Gowda, S. N., Pandey, D., & Gowda, S. N. (2026). From Pixels to Portraits: A Comprehensive Survey of Talking Head Generation Techniques and Applications (v8). _Computer Science Review_. [arXiv:2308.16041](https://arxiv.org/abs/2308.16041)
  * Xue, H., Luo, X., Hu, Z., et al. (2025). Human Motion Video Generation: A Survey. [arXiv:2509.03883](https://arxiv.org/abs/2509.03883)
  * Meng, M., Zhao, Y., Zhang, B., et al. (2024). A Comprehensive Taxonomy and Analysis of Talking Head Synthesis: Techniques for Portrait Generation, Driving Mechanisms, and Editing. [arXiv:2406.10553](https://arxiv.org/abs/2406.10553)
  * Rakesh, V. K., Mazumdar, S., Maity, R. P., et al. (2025). Advancing Talking Head Generation: A Comprehensive Survey of Multi-Modal Methodologies, Datasets, Evaluation Metrics, and Loss Functions. [arXiv:2507.02900](https://arxiv.org/abs/2507.02900)
