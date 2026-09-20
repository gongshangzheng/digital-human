---
title: "数字人系列（九）：评测指标、数据集、训练算力与产品选型"
description: "深入拆解数字人五大评测指标族的计算原理与失败模式，汇总主流数据集的格式与规模，按六条路线总结训练算力与推理资源，整理 28 个模型的输入/输出规格，分析人脸真实度评测与 deepfake 检测的适用性，设计跨路线四模型对比协议，给出产品选型与落地检查清单。"
date: 2026-06-09T13:01:47
created_at: 2026-06-09T13:01:47
updated_at: 2026-07-08T11:33:03
tags: [数字人, Benchmark, 算力, Evaluation, 产品选型, Survey, FID, FVD, SyncNet, CSIM, Dataset, 评测指标]
aliases: ["categories/AI/数字人"]
sub_id: 90
toc: true
mathjax: true
notify: true
hero_title: "评测指标、算力与产品选型"
hero_sub: "从公式直觉到可执行协议：指标怎么算、数据集用什么、算力要多少、怎么落地"
hero_tagline: "系列（九）· Metrics · Datasets · Compute · Benchmark · 产品选型"
---

> 来源：博客 gongshangzheng.github.io `src/pages/digital-human-training-inference-benchmark.html`，html2text 转换复制于 2026-09-20。原文：https://gongshangzheng.github.io/digital-human-training-inference-benchmark.html

5指标族深度拆解

15数据集格式与规模

28模型输入/输出

6技术路线算力

4模型对比协议

20+代表论文

系列位置

这一篇回答"实验和部署到底要准备什么"

前面几篇已经把数字人的任务边界和技术路线拆开：换嘴、运动空间、3DGS/NeRF、扩散基模、整帧/全身生成和实时流式蒸馏。本文把评测方法论、数据集、训练资源、推理资源和产品选型放到同一张坐标系里。 本文回答以下问题： 

  * **Part 1** ：五大评测指标（画质、时序、同步、身份、效率）到底怎么算、什么时候会骗人、用什么代码库复现？
  * **Part 2** ：六条路线的训练算力、推理资源和 benchmark 重点分别是什么？
  * **Part 3-6** ：每条路线的 loss、指标和数据集细节。
  * **Part 7** ：主流训练与评测数据集的规模、License、偏差和适用场景。
  * **Part 8** ：FlashHead / [LAM](lam-2025.html) / [UIKA](uika-2026.html) / LiteAvatar 四个类型完全不同的模型，怎么设计标准化对比协议？
  * **Part 9** ：指标陷阱与反模式清单。
  * **Part 10-11** ：如何设计自己的 benchmark？产品怎么选？PoC/MVP/规模化怎么落地？
  * **Appendix A** ：28 个模型的输入/输出规格汇总——训练时分阶段输入、推理时输入、最终输出。
  * **Appendix B** ：15 个数据集的数据组织格式（视频、音频、参考图、标注等）与磁盘规模。
  * **Appendix C** ：数字人脸真实度评测指标全景——FIQA、感知质量、deepfake 检测能否反向用作质量指标？

[←上一篇 · 第八章Avatar 类型数字人总报告](digital-human-avatar-survey.html) [本文评测指标 / 算力 / 选型](digital-human-training-inference-benchmark.html) [→下一篇产业图谱](voice-ai-digital-human-landscape.html)

**读法提示** ：本文是参考材料，不是线性叙事。做实验复现先看 Part 1 找指标代码库；选型对比直接跳 Part 8 看对比协议；设计自己的 benchmark 从 Part 7 的数据集表开始；关心成本和落地看 Part 2 和 Part 10-11。

Part 1

五大指标族：从公式直觉到失败模式

数字人的 evaluation 至少有五个维度：画质、时序、同步、身份、效率。FID、FVD 只能回答"生成分布像不像测试集"，不能单独回答嘴型准不准、身份稳不稳、首帧延迟能不能接受。本节对每个维度做三件事：解释计算原理（直觉，不是推导），列出失败模式（什么时候数字在骗你），给出可复现的代码库。#Heusel-et-al.-2017# #Unterthiner-et-al.-2018# #Chung-et-al.-2017# #Deng-et-al.-2019# #Zhang-et-al.-2018#

指标族| 常见指标| 回答的问题| 容易误读的地方  
---|---|---|---  
图像质量| FID、PSNR、SSIM、LPIPS、FaceIQA、IQA| 单帧是否清晰、是否像真实图像| 局部换嘴保留原视频大部分区域，FID/FVD 可能天然更好  
视频时序| FVD、temporal consistency、Dino-S| 跨帧是否稳定，长视频是否漂移| 短视频好不代表 5 分钟以上稳定  
音画同步| LSE-D、LSE-C、Sync-C、Sync-D、LMD| 嘴型和音频是否对齐| 同步高不等于表情自然，也不等于身份稳定  
身份保持| CSIM、ArcFace similarity、Dino-S、人工 identity score| 生成过程是否仍像同一个人| 长时生成里身份漂移通常比短片更严重  
系统效率| FPS、RTF、TTFF、FFD、显存、吞吐| 能否实时、能否流式、能否并发| 离线 FPS、批量 FPS 和单路交互延迟不是一回事  
  
### 1.1 图像质量：FID、PSNR、SSIM、LPIPS

**FID（Frechet Inception Distance）** 把生成图像和真实图像分别送入 Inception-v3，取 pool3 层 2048 维特征，假设两组特征都服从多元高斯分布，然后算两个分布之间的 Frechet 距离：

\\[ \text{FID} = \|\mu_r - \mu_g\|^2 + \text{Tr}\left(\Sigma_r + \Sigma_g - 2(\Sigma_r \Sigma_g)^{1/2}\right) \\] 

直觉上，FID 同时比较均值（"平均长什么样"）和协方差（"多样性如何"）。FID 越低，生成分布越接近真实分布。

FID 的失败模式 

  * **样本量敏感** ：少于 1000 张样本时 FID 方差大，不同论文用不同样本量算出的 FID 不可比。
  * **奖励 mode collapse** ：如果生成分布很窄但恰好在真实分布的高密度区域，FID 可能很低，但多样性为零。
  * **不测时序** ：FID 是逐帧计算的，完全忽略视频的时间连续性。
  * **局部换嘴路线的虚假优势** ：[Wav2Lip](paper-wav2lip.html)、[MuseTalk](paper-musetalk.html) 这类方法只改嘴部区域，其余像素来自原视频，FID 天然接近原视频分布。
  * **特征提取器依赖** ：Inception-v3 在 ImageNet 上训练，对人脸细节的判别力有限。clean-fid 库提供了更一致的预处理。#Kynkaamaki-et-al.-2022#

**PSNR / SSIM** 是像素级和结构级的重建质量指标。PSNR 直接衡量像素误差的对数比，SSIM 同时考虑亮度、对比度和结构相似性。它们都需要 ground truth 对齐帧，因此只适用于 self-reenactment 或有 GT 的重建任务（LAM、UIKA 的论文主实验）。PSNR 的失败模式是对空间位移敏感：一张完美但偏移 1 像素的图像 PSNR 会很低。

**LPIPS** 用预训练 VGG/AlexNet 的特征空间计算感知距离，与人眼判断的相关性比 PSNR 更强。对生成模型来说，LPIPS 通常比 PSNR 更可靠。#Zhang-et-al.-2018#

**IQA（Image Quality Assessment）** 是无参考图像质量评估的统称，代表方法包括 BRISQUE #Mittal-et-al.-2012#（自然场景统计）、NIQE #Mittal-et-al.-2013#（无需训练的盲评估）、MUSIQ #Ke-et-al.-2021#（多尺度 Transformer）和 CLIP-IQA+ #Wang-et-al.-2023#（CLIP 多模态）。它们不需要 ground truth，适合大规模筛选生成帧，但在 GAN/diffusion 生成的人脸上泛化差——训练数据是自然图像，对生成模型的系统性伪影（牙齿融合、耳朵变形）不敏感。

**FaceIQA（Face Image Quality Assessment）** 是 IQA 的人脸特化版本，代表方法包括 FaceQnet v2 #Hernandez-Ortega-et-al.-2020#（清晰度+光照+遮挡综合打分）和 CR-FIQA #Boutros-et-al.-2022#（ArcFace 识别置信度作为质量代理）。它们优化的是"这张脸能否被准确识别"，而非"这张脸看起来是否像真人"——对数字人真实度评测存在概念错位，但可快速筛除明显低质帧。详细讨论见 Appendix C。

指标| 回答什么| 不能回答什么| 代码库| 跨路线适用  
---|---|---|---|---  
FID| 生成分布是否像真实分布| 单帧质量、时序稳定、同步| `pytorch-fid`、`clean-fid`| 视频生成模型；3DGS 需先渲染为视频  
PSNR| 像素级重建精度| 感知质量、分布相似度| scikit-image、torchmetrics| 需要 GT 对齐帧  
SSIM| 结构相似性| 时序、同步、身份| scikit-image、pytorch-msssim| 同 PSNR  
LPIPS| 感知相似度| 绝对质量、时序| `lpips` pip 包| 需要 GT，但比 PSNR 更接近人判  
IQA| 无参考图像质量（清晰度/自然度）| 身份、同步、生成伪影| `pyiqa`、`musiq`| 无需 GT，适合大规模筛选；对生成脸泛化差  
FaceIQA| 人脸可用质量（识别友好度）| 视觉真实度、恐怖谷| `FaceQnet`、`CR-FIQA`| 快速筛除低质帧；不测"像不像真人"  
  
### 1.2 视频时序：FVD、Dino-S

**FVD（Frechet Video Distance）** 是 FID 的视频版：用 I3D 在视频片段上抽取时空特征，再算 Frechet 距离。与 FID 的关键区别是 FVD 同时评估时间连续性——闪烁、跳帧和动作不连贯都会拉高 FVD。#Unterthiner-et-al.-2018#

FVD 的最大陷阱是 **clip length 敏感性** 。16 帧和 32 帧算出的 FVD 差异可以超过 50%，不同论文用不同 clip length 的结果不可直接比。

**Dino-S** 用 DINOv2 #Oquab-et-al.-2024# 的自监督特征衡量相邻帧的语义一致性。它不需要 ground truth，适合评估长视频的时间稳定性。但 Dino-S 测的是特征稳定而非语义正确——一个静态画面也能得高分。

### 1.3 唇音同步：Sync-C / Sync-D / LSE-C / LSE-D

**SyncNet** 是唇音同步评测的核心工具。它用双流 CNN 分别处理嘴部 ROI 视频片段和音频梅尔频谱，输出两组 embedding 后算余弦相似度（Sync-C，越高越好）和欧氏距离（Sync-D，越低越好）。SyncNet 在 VoxCeleb2 上训练，主要覆盖英语、正面人脸。#Chung-et-al.-2017#

SyncNet dual-stream architecture used for lip-sync evaluation（图片资源未随副本复制）

图 2：SyncNet/唇形同步专家的双流结构——音频流与视频流各自编码后比对，是 Sync-C/Sync-D 与 LSE-C/LSE-D 指标的基础（来源：Prajwal et al., Wav2Lip, ACM MM 2020, SyncNet）。

SyncNet 的失败模式 

  * **非英语退化** ：SyncNet 在英语上训练，对中文、日语等语言的同步判断可能不准。
  * **极端姿态** ：侧脸、低头、遮挡会导致嘴部 ROI 裁剪失败。
  * **高分 ≠ 自然表情** ：SyncNet 只判断"嘴型和音频是否一致"，不判断"表情是否自然"。
  * **"一致但错误"** ：如果模型学到了错误的嘴型模式但音画仍然同步，SyncNet 无法区分。

**LSE-C / LSE-D** 是 Wav2Lip 论文引入的变体，计算方式类似但使用不同的 SyncNet 模型版本。复现时务必确认使用的是哪个 SyncNet checkpoint。#Prajwal-et-al.-2020#

### 1.4 身份保持：CSIM、ArcFace

**CSIM（Cosine Similarity of Identity embedding）** 用 ArcFace 等人脸识别模型提取参考图和生成帧的身份 embedding，计算余弦相似度。CSIM 的关键陷阱是**判别性嵌入和生成质量的脱节** ：ArcFace 是为身份判别训练的，一张模糊但"像同一个人"的图像可以得高分。此外，静态面部（几乎没有表情变化）的 CSIM 通常很高——不代表模型的表情生成能力好。#Deng-et-al.-2019#

### 1.5 系统效率：FPS、RTF、TTFF、VRAM

系统效率指标看起来最直接，却也是最容易被论文和 demo 误导的维度。FPS 必须区分离线批量、单路流式和多路并发；RTF < 1 表示实时；TTFF（Time To First Frame）对实时交互场景比 FPS 更重要；VRAM 决定了单卡能跑什么模型。

**工程实测参考** ：[工程 Benchmark 汇总页](digital-human-engineering-benchmark.html) 记录了 A10 GPU 上的真实推理数据：LiteAvatar 25.19 FPS / 7507 MiB，LAM 30 FPS / 1725 MiB，FlashHead Lite 46.7 FPS，FlashHead Pro 4.8 FPS / 7839 MiB。

{{< mermaid >}} flowchart TD Q1{"模型输出类型？"} Q1 -->|"视频帧序列"| Q2{"评估什么？"} Q1 -->|"3D 资产"| Q3{"渲染后评估 还是资产评估？"} Q1 -->|"参数化面部"| Q4{"驱动精度 还是外观质量？"} Q2 -->|"画质"| M1["FID / LPIPS"] Q2 -->|"时序稳定"| M2["FVD / Dino-S"] Q2 -->|"唇音同步"| M3["Sync-C/D"] Q2 -->|"身份保持"| M4["CSIM / ArcFace"] Q3 -->|"渲染后"| M5["同视频帧指标"] Q3 -->|"几何资产"| M6["Chamfer / F-Score"] Q4 -->|"驱动精度"| M7["AED / AKD"] Q4 -->|"外观"| M8["PSNR / SSIM / LPIPS"] {{< /mermaid >}} 

_图 1：指标选择决策树。从模型输出类型出发，引导到适合的评测指标。_

Part 2

六条路线的算力量级总表

路线| 代表方法| 训练算力量级| 推理算力量级| Benchmark 重点  
---|---|---|---|---  
轻量换嘴 /  
局部重绘| Wav2Lip  
MuseTalk| 8×V100 约 3 天  
8×H20 两阶段数十小时| 单 V100  
30–40 FPS 量级| LRS2、ReSyncED  
[HDTF](./hdtf-source-code-analysis.html)、[VFHQ](./vfhq-2022.html)  
口型同步  
身份保持  
局部画质 / artifact  
运动空间 /  
隐式关键点| [SadTalker](paper-sadtalker.html)、[LivePortrait](paper-liveportrait.html)  
[VASA-1](paper-vasa1.html)、[Ditto](paper-ditto.html)、[Teller](paper-teller.html)| 4×A6000 / 8×A100  
8×8 A800 等中高配训练| RTX 4090 或 A100 可达实时  
Teller 用 4×H800 做 200ms chunk| VoxCeleb2、Talk9、HDTF100  
[HDTF](./hdtf-source-code-analysis.html)、RAVDESS  
口型同步  
身份保持  
头动 / 表情  
实时性 / 延迟  
NeRF  
talking portrait| AD-NeRF  
RAD-NeRF  
ER-NeRF| 早期 AD-NeRF 可到天级 / 百小时级  
ER-NeRF 降到小时级| 从低 FPS 到十几 FPS  
取决于 ray sampling 与加速结构| person-specific 短视频  
画质：PSNR / LPIPS  
运动：LMD  
同步：LSE-C  
效率：FPS  
3DGS  
talking head| TalkingGaussian、GaussianTalker  
GSTalker、[EGSTalker](paper-egstalker.html)| 小时级到几十分钟级| 数十到百 FPS 量级| person-specific 3–5 分钟视频  
运动：LMD  
同步：LSE-C  
身份保持  
FPS / 长时稳定  
扩散肖像 /  
音频驱动 portrait| EMO、[Hallo](paper-hallo.html)  
[AniPortrait](paper-aniportrait.html)、[FLAP](paper-flap.html)| 单卡到 8×A100  
EMO 更披露 250h+ 数据而非 GPU| 多步扩散偏离线  
部分模型未披露标准推理耗时| [HDTF](./hdtf-source-code-analysis.html)、CelebV、[VFHQ](./vfhq-2022.html)  
CelebV-HQ、Wild  
画质：FID / FVD  
同步 / 身份  
表情 / 时序稳定  
整帧 / 全身 /  
流式基模| Animate Anyone、[OmniAvatar](paper-omniavatar.html)  
[InfiniteTalk](infinitetalk-paper.html)、[Live Avatar](live-avatar-paper.html)  
StreamAvatar、LLIA| 14B 视频基座  
64×H100 或 128×H800 量级| 离线 DiT 很慢  
蒸馏后可到 5×H800 45 FPS  
或 4090D 45–78 FPS| [HDTF](./hdtf-source-code-analysis.html)、CelebV-HQ、EMTD  
GenBench、TikTok、UBC  
长时稳定  
全身动作 / 手势  
TTFF / 延迟 / FPS  
  
算力数字只能同口径比较 

训练时长受数据量、分辨率、batch size、混合精度、并行策略和是否从预训练模型微调影响；推理速度受分辨率、采样步数、是否 batch、是否 TensorRT/FP8/INT8、是否包含音频编码和媒体链路影响。本文把它们作为路线量级，不把不同论文的数字直接排成绝对榜单。

Part 3

轻量换嘴和局部重绘：最低成本验证同步链路

轻量换嘴路线的基本假设是：原视频的大部分内容已经足够好，模型只需要改嘴部或脸部局部区域。Wav2Lip 的代表性设计是先训练一个强唇形同步专家，再用 L1、VGG perceptual、Sync loss 和 adversarial loss 约束生成器；论文级实验报告 8 张 V100 训练约 3 天、单 V100 约 40 FPS，训练和测试基准围绕 LRS2 与 ReSyncED 展开。#Wav2Lip# MuseTalk 把问题放进 latent inpainting：先用 L1 + VGG perceptual 学局部重建，再加入 face / lip adversarial discriminator 和 SyncNet 同步约束；本地精读记录的配置是 Stage 1 用 8 张 H20、200k steps、约 60 小时，Stage 2 约 30 小时，推理在 V100 上 256×256、preloaded data 条件下约 30 FPS。#MuseTalk# 

方法| 常见 loss| 常见指标| 常用 benchmark / 数据集| 适合判断  
---|---|---|---|---  
Wav2Lip| L1 重构、VGG perceptual、SyncNet sync、GAN adversarial| LSE-D、LSE-C、FID、人评| LRS2、ReSyncED| 已有视频配音是否对口型  
MuseTalk| L1、VGG、face/lip adversarial、SyncNet sync| FID、CSIM、LSE-C、用户研究| [HDTF](./hdtf-source-code-analysis.html)、[VFHQ](./vfhq-2022.html)| 局部重绘能否兼顾同步和身份  
  
这条路线的 benchmark 要特别注意"保留原视频"的优势。因为背景、头部姿态和大部分脸部纹理来自原视频，FID/FVD 往往不会暴露模型真实的可控性短板；相反，LSE-C/LSE-D、CSIM、嘴部边界 artifact 和用户研究更接近产品风险。 

Part 4

运动空间路线：把像素生成改成可缓存的运动生成

运动空间路线先把脸部、头部或身体动作压到更低维的表示里，再由渲染器把运动转成视频。SadTalker 使用 3DMM 运动系数，把表情和姿态拆给 ExpNet 与 PoseVAE。#SadTalker# LivePortrait 用隐式关键点、stitching 和 retargeting 做快速肖像动画；Stage I 在 8 张 A100 上从零训练约 10 天，Stage II 约 2 天，推理在 RTX 4090 + PyTorch 上约 12.8ms。#LivePortrait# VASA-1 把面部潜在空间和 diffusion transformer 分开：面部潜在空间模型用 4 张 RTX A6000 训练 7 天，扩散 Transformer 训练 3 天；推理在单 RTX 4090 上达到 512×512 在线 40 FPS、启动延迟约 170ms。VASA-1 评估 SC、SD、FVD25、CAPP、ΔP。#VASA1# Ditto 和 Teller 更直接面向流式系统。Ditto 用 8 张 A100、batch size 1024、500 epochs 训练 motion-space diffusion，推理报告 RTF 与 FFD；Teller 则把 motion 进一步 token 化，Stage 1 / SFT / ETM 使用 8×8 A800 量级训练，推理在 4 张 H800 上按 200ms chunk 运行。#Ditto# #Teller# 

SadTalker modular pipeline with ExpNet and PoseVAE（图片资源未随副本复制）

图 3：SadTalker 的模块化管线——ExpNet 预测表情系数、PoseVAE 生成头姿、Face Render 合成图像，是运动空间路线训练资源与指标拆解的典型（来源：Zhang et al., SadTalker, CVPR 2023, main pipeline）。

子路线| 代表方法| loss 重点| metrics 重点| benchmark  
---|---|---|---|---  
3DMM / 参数运动| SadTalker| 表情系数重构、Sync loss、VAE ELBO、KL| 同步、身份、头动自然度| VoxCeleb、talking head 对比集  
隐式关键点| LivePortrait| GAN、perceptual、face identity、landmark guide、stitching/retargeting| PSNR、SSIM、LPIPS、L1、CSIM、eye direction MAE、FID| TalkingHead-1KH、[VFHQ](./vfhq-2022.html)  
motion diffusion| VASA-1、Ditto| clean motion MSE、速度/加速度 temporal loss、initial loss、adaptive weights| FVD、CSIM、Sync-C/D、RTF、FFD、CAPP、ΔP| VoxCeleb2、Talk9、HDTF100  
motion token AR| Teller| RVQ reconstruction + commitment、AR token prediction、region mask reconstruction| FID、FVD、Sync-C、Sync-D、Time| AVSpeech、[VFHQ](./vfhq-2022.html)、[HDTF](./hdtf-source-code-analysis.html)、RAVDESS  
  
Part 5

NeRF 与 3DGS：专人资产的训练成本和渲染效率

3D/显式可渲染表示路线的 benchmark 和通用视频生成很不一样：它通常是 person-specific，先用某个目标人物的几分钟到几小时视频训练一个资产，再用新音频或新 motion 驱动它。AD-NeRF 把头和躯干建成 NeRF，在 RTX 3090 上训练约 36 小时、推理仅 0.04 FPS；ER-NeRF 通过区域感知和高效表示在 RTX 3080Ti 上把训练降到 2 小时、推理到 34 FPS。#ADNeRF# #ERNeRF# #DigitalHuman3DGS# 3D Gaussian Splatting 把渲染瓶颈从体渲染的 ray marching 转成显式 Gaussian rasterization。TalkingGaussian 的训练约 1.5 小时、推理 70.42 FPS；GaussianTalker 训练 4.5 小时、59.24 FPS；GSTalker 训练 40 分钟、实时 125 FPS；EGSTalker 训练 3.7 小时、68.51 FPS。#TalkingGaussian# #GaussianTalker# #GSTalker# #EGSTalker# 通用前馈模型（LAM、UIKA）与 person-specific 方法有本质区别：它们训练一次大模型，推理时从任意输入图像一次前馈生成 3DGS 资产，无需逐身份训练。LAM 在 A100 上达 280.96 FPS、iPhone 16 上通过 WebGL 达 35 FPS；UIKA 在 A100 上达 220 FPS，训练用 32×H20 约 2 周。#He-et-al.-2025# #UIKA-2026# 

UIKA feed-forward universal head avatar pipeline（图片资源未随副本复制）

图 4：UIKA 的前馈式通用头部头像管线，从任意数量 pose-free 图像一次前馈生成可动画 3DGS 资产（来源：Wu et al., UIKA, CVPR 2026 Highlight, pipeline）。

模型| 类型| GPU| 分辨率| FPS| 训练时间| 来源  
---|---|---|---|---|---|---  
**AD-NeRF**|  person-specific| 1× RTX 3090| 450×450| ~0.04| 36 h| 论文 #Guo-et-al.-2021#  
**ER-NeRF**|  person-specific| 1× RTX 3080Ti| 256² rays| 34| 2 h| 论文 #Li-et-al.-2023#  
**TalkingGaussian**|  person-specific| 1× GPU| —| 70.42| ~1.5 h| 论文 #Li-et-al.-2025#  
**GaussianTalker**|  person-specific| 1× GPU| —| 59.24| ~4.5 h| 论文 #Cho-et-al.-2024#  
**GSTalker**|  person-specific| 1× RTX 3090| —| 125| 40 min| 论文 #Chen-et-al.-2024#  
**EGSTalker**|  person-specific| 1× RTX 3090| —| 68.51| 3.7 h| 论文 #Zhu-et-al.-2025#  
**LAM**|  通用前馈| 1× A100| 512×512| 280.96| 前馈（200 epochs / VFHQ 15K clips）| 论文 #He-et-al.-2025#  
**UIKA**|  通用前馈| 1× A100| 512×512| 220| 前馈（150K steps / 32×H20 / ~2 周）| 论文 #UIKA-2026#  
  
**读表提示** ：person-specific 方法（AD-NeRF → EGSTalker）的训练时间指为每个目标人物单独训练一个模型；通用前馈方法（LAM、UIKA）的训练时间指大模型的预训练成本，推理时只需一次前向传播即可生成任意身份的 3DGS 资产。

[SentiAvatar](paper-sentiavatar.html) 属于 motion controller：它用 8 张 A100 训练 R-VQVAE、Motion Foundation Model、SFT 和 Infill Transformers，报告约 0.3 秒生成 6 秒 motion 输出，benchmark 是 SuSuInterActs 与 BEATv2，指标包括 R@1、FID、ESD、Diversity、FGD、BC 和用户研究。#SentiAvatar# 

Part 6

扩散肖像、整帧全身和流式基模：从离线质量到实时系统

扩散肖像路线的优势是表情和画面质量，代价是多步采样。Hallo 使用 8 张 A100、两阶段各 30,000 steps、512×512 训练，benchmark 覆盖 [HDTF](./hdtf-source-code-analysis.html)、CelebV 和 Wild，指标包括 FID、FVD、Sync-C、Sync-D、E-FID；AniPortrait 的 Audio2Lmk 在单张 A100 上训练，Lmk2Video 用 4 张 A100、每阶段约 2 天。#Hallo# #AniPortrait# #EMO# 整帧与全身路线把背景、身体和场景也纳入生成。Animate Anyone 用内部 5K character video clips，评测 UBC fashion video 和 TikTok；OmniAvatar 基于 Wan2.1-T2V-14B 做 LoRA 音频适配；InfiniteTalk 基于 Wan2.1-I2V-14B，使用约 2000 小时数据和 64 张 H100 80G 训练。#AnimateAnyone# #OmniAvatar# #InfiniteTalk# 实时流式路线的关键不是"换一个更快采样器"，而是把训练目标、因果注意力、蒸馏、量化、流水线和缓存一起改。Live Avatar 用 14B Wan-S2V 初始化，Stage 1 用 128×H800 训练 25K steps，推理默认 4-step，5×H800 达到 45.2 FPS / 1.21s TTFF。StreamAvatar 把双向扩散改为 block-wise causal attention 并蒸馏；LLIA 则用 consistency model、INT8 和 pipeline parallelism，在 RTX 4090D 上 512×512 45 FPS。#LiveAvatar# #StreamAvatar# #LLIA# 

路线| 常见训练目标| 评估重点| benchmark / 数据集| 典型风险  
---|---|---|---|---  
音频扩散肖像| diffusion denoising、latent reconstruction、L1 landmark / mesh、audio-visual attention alignment| FID、FVD、Sync-C/D、E-FID、用户研究| [HDTF](./hdtf-source-code-analysis.html)、CelebV、Wild、[VFHQ](./vfhq-2022.html)、CelebV-HQ| 推理慢、短片好但交互延迟高  
整帧 / 全身 DiT| flow matching / diffusion denoising、LoRA 适配、reference / pose / audio condition| FID、FVD、Sync-C/D、CSIM、人评、长时一致性| UBC、TikTok、[HDTF](./hdtf-source-code-analysis.html)、CelebV-HQ、EMTD| FID/FVD 对局部编辑和整帧重生成不公平  
流式蒸馏| flow matching、DMD / self-forcing、AR distillation、adversarial refinement、consistency training| FPS、TTFF、ASE、IQA、Sync-C、Dino-S、长视频身份| GenBench、AVSpeech、long / short split| 只优化短视频会漏掉长时身份漂移和首帧延迟  
  
Part 7

数据集全景：训练、评测与偏差

数字人的数据集大致分三类：训练数据（用于学参数）、评测数据（用于算指标）和两用数据。选择数据集时不只看规模，还要看 License 是否允许商用、人口统计学偏差是否匹配目标场景、分辨率和帧率是否与实验设置对齐。

数据集| 规模| 分辨率| License| 训练 / 评测| 使用它的模型| 局限性 / 偏差  
---|---|---|---|---|---|---  
[**HDTF**](./hdtf-source-code-analysis.html)|  362 speakers, 10K clips, 15.8h| 512p| Research only| 两者| FlashHead、LAM、UIKA、SadTalker、Hallo| 正面为主、studio 光照、英语为主  
[**VFHQ**](./vfhq-2022.html)|  15,204 clips, ~3M frames| 512p| CC-BY-NC-SA| 两者| LAM、UIKA、FlashHead、LivePortrait、MuseTalk| 访谈场景，多身份，但非商业  
**VoxCeleb2**|  6,112 speakers, 1M+ utterances| 多分辨率| CC-BY| 训练为主| SyncNet 预训练、VASA-1、Ditto| YouTube 提取，噪声多，多人种  
**CelebV-HQ**|  35,666 clips, 多属性标注| 512p+| Research| 评测为主| Hallo、AniPortrait、OmniAvatar、InfiniteTalk| 名人视频，属性标注丰富  
**LRS2 / LRS3**|  LRS2: 150K+ clips (TED)| 256p-512p| LRS2: CC-BY| 两者| Wav2Lip| TED 演讲场景，英语，正面  
[**MEAD**](./mead-2020.html)|  60 speakers, 281K clips, 39h| 384p| Research| 训练| FlashHead（VividHead 组成）| 多视角、多情绪，studio 环境  
**NeRSemble-v2**|  多视角 studio 采集| 高分辨率| Research| 评测| UIKA| studio 光照，身份数少但 3D 一致性监督强  
**VividHead**|  60K speakers, 330K clips, 782h| 512p| 未公开| 训练| FlashHead| 从 10K 小时清洗，15 种语言  
**AVSpeech**|  290K clips (YouTube)| 多分辨率| CC-BY| 训练| Live Avatar、Teller| 噪声大，YouTube 提取，质量参差  
**RAVDESS**|  24 actors, 多情绪| HD| CC-BY-NC-SA| 评测| Teller| 表演情绪，规模小但受控  
**UIKA Synthetic**|  7500+ 身份 × 9 视角 × 13K+ 帧| 512p| 自建| 训练| UIKA| SphereHead + LivePortrait 合成，与真实分布有偏移  
**EMTD**|  情绪丰富的 talking head| HD| Research| 评测| InfiniteTalk| 侧重情绪表达  
  
_表：数字人主流数据集汇总。_

### 数据集-模型交叉矩阵

数据集| FlashHead| LAM| UIKA| LiteAvatar  
---|---|---|---|---  
[HDTF](./hdtf-source-code-analysis.html)| T + E| E| T| —  
[VFHQ](./vfhq-2022.html)| T + E| T + E| T + E| —  
VoxCeleb2| —| —| —| —  
CelebV-HQ| —| —| —| —  
[MEAD](mead-2020.html)| T (VividHead)| —| —| —  
NeRSemble-v2| —| —| T + E| —  
VividHead| T| —| —| —  
  
_表：数据集-模型交叉矩阵。T = 训练使用，E = 评测使用。LiteAvatar 是工程工具，不使用学术数据集。_

**License 警示** ：[HDTF](./hdtf-source-code-analysis.html) 和 CelebV-HQ 仅限研究使用；[VFHQ](./vfhq-2022.html) 为 CC-BY-NC-SA（非商业）；VoxCeleb2 为 CC-BY（可商用）。如果目标是产品选型，评测集的法律风险要单独评估。

Part 8

苹果和橘子怎么比：四模型标准化对比协议

FlashHead、LAM、UIKA 和 LiteAvatar 是四种类型完全不同的数字人模型。它们各自的论文用不同的指标、在不同的数据集上报告结果。直接比较 FlashHead 的 FID 和 LAM 的 PSNR，就像比较汽车的风阻系数和自行车的链条效率。

### 8.1 模型定位

模型| 类型| 输入| 输出| 论文自报指标| 设计意图  
---|---|---|---|---|---  
**FlashHead**|  2D 视频 DiT| 参考图 + 音频流| 视频帧序列| FID, FVD, Sync-C, Sync-D, FPS| 消费级 GPU 实时流式数字人  
**LAM**|  3DGS 重建| 单张图像| 可动画 3D Gaussian 资产| PSNR, SSIM, LPIPS, CSIM, AED, AKD| 单图→可驱动 3D 资产，跨平台实时  
**UIKA**|  3DGS 重建| 1-N 张 pose-free 图像| 可动画 3D Gaussian 资产| PSNR, SSIM, LPIPS, CSIM, AED, APD| 任意输入→高质量 3D 头部资产  
**LiteAvatar**|  2D 参数化面部| 音频（16kHz WAV）| 面部动画帧| 无学术指标| 纯 CPU 实时，工程部署工具  
  
### 8.2 桥接策略：输出归一化 + 两层指标

对比的前提是让四个模型的输出进入同一格式：所有模型统一输出 25fps、512×512 的视频帧序列。LAM/UIKA 用测试音频驱动 FLAME 参数 → 固定虚拟相机渲染视频；FlashHead/LiteAvatar 直接使用原生输出。

层次| 指标| 适用模型| 说明  
---|---|---|---  
**Tier 1（通用）**|  Sync-C, Sync-D, CSIM, FPS, VRAM| 全部四个模型| 任何音频驱动的面部动画都能算。Sync-C/D 测唇音同步，CSIM 测身份保持，FPS/VRAM 测系统效率。  
**Tier 2（类型专属）**|  FID, FVD| FlashHead, LiteAvatar| 视频生成模型可直接算；LAM/UIKA 渲染后也可算但受渲染器影响。  
| PSNR, SSIM, LPIPS, AED, AKD| LAM, UIKA| 需要 GT 对齐帧，仅 self-reenactment 可算。  
  
**两层分开报告，不合成单一分数。**

### 8.3 测试集与人评

**测试集** ：标准集（[HDTF](./hdtf-source-code-analysis.html) 75 videos + [VFHQ](./vfhq-2022.html) 50 clips）与论文对齐；压力集（长音频 >60s、非英语、极端姿态、歌唱）测边界；身份集（20 身份 × 3 张参考图）测稳定性。

**人评** ：30 人，within-subject 设计，4 维度 1-5 分 MOS（唇音同步、身份匹配、自然度、整体偏好），Latin Square 随机化，Krippendorff's alpha + Wilcoxon signed-rank test + Bonferroni correction。

{{< mermaid >}} flowchart LR subgraph Inputs["统一输入"] A["参考图像"] --> B["测试音频"] end subgraph Models["四模型推理"] B --> C["FlashHead\n→ 视频帧"] B --> D["LAM\n→ 3DGS → 渲染视频"] B --> E["UIKA\n→ 3DGS → 渲染视频"] B --> F["LiteAvatar\n→ 视频帧"] end subgraph Normalize["输出归一化"] C --> G["512×512, 25fps"] D --> G E --> G F --> G end subgraph Metrics["统一评测"] G --> H["Tier 1: Sync + CSIM + FPS"] G --> I["Tier 2: FID/FVD 或 PSNR/AED"] G --> J["人评 MOS"] end {{< /mermaid >}} 

_图 2：四模型标准化对比流程。_

解读注意事项 

  * **LiteAvatar 的低画质是设计取舍** ：纯 CPU 30 FPS 的工程工具，不是研究模型。
  * **LAM/UIKA 的独特优势不体现在 Tier 1** ：一次建模、无限驱动的 3D 资产复用能力是视频生成模型做不到的。
  * **FPS 口径不同** ：FlashHead 96 FPS 在 RTX 4090 上，LiteAvatar 30 FPS 在纯 CPU 上，跨硬件只看 FPS 会误导。

Part 9

指标陷阱：什么时候数字在骗你

反模式| 为什么是陷阱| 正确做法  
---|---|---  
只报 FID 不报 Sync| FID 不测唇音同步| lip-sync 模型必须同时报告 Sync-C/D  
跨分辨率比 PSNR| 256×256 和 512×512 的 PSNR 没有可比性| 统一分辨率后再算 PSNR  
SyncNet 在非英语上未校准| SyncNet 训练数据是英语+正面| 跨语言用同一版本 SyncNet + 同一 face detector；补充人评  
FPS 不标口径| 论文 FPS 可能排除预处理、后处理和音频编码| 标注：模型 forward / 端到端 / 含音频管线  
CSIM 高 = 模型好| 静态面部 CSIM 天然高| CSIM + AED（表情距离）联合报告  
短视频 FVD 好 = 长视频稳定| 16 帧 FVD 看不出 1 分钟后的漂移| 补充 30s/60s 长视频 Dino-S 和定性检查  
  
Part 10

怎样设计自己的 benchmark 和产品选型

如果目标是复现实验，benchmark 可以沿论文设置走；如果目标是产品选型，建议把测试集拆成四组。 

评测包| 应该包含| 推荐指标| 适用路线  
---|---|---|---  
公开复现包| LRS2 / [HDTF](./hdtf-source-code-analysis.html) / [VFHQ](./vfhq-2022.html) / VoxCeleb2 / CelebV-HQ 子集| FID、FVD、Sync-C/D、CSIM、LPIPS| 所有论文复现  
业务样本包| 真实客户形象、真实话术、真实音频设备| 人工 MOS、身份保持、失败率、可审核性| 产品选型  
压力样本包| 长音频、侧脸、遮挡、强表情、唱歌、跨语言| 长时 Dino-S、Sync、artifact rate、重试率| 实时和长视频路线  
系统延迟包| ASR/TTS、avatar、编码、推流、网络、队列| TTFF、RTF、p50/p95 latency、GPU memory、吞吐| 实时交互系统  
  
{{< mermaid >}} flowchart TD Q1{"目标是离线内容还是实时交互？"} Q1 -->|"离线内容"| A1["优先 FID / FVD / CSIM / 人评"] Q1 -->|"实时交互"| Q2{"是否要长时稳定？"} Q2 -->|"否，短对话"| A2["Sync-C/D + RTF + TTFF + p95 latency"] Q2 -->|"是，长直播"| A3["长视频身份 + Dino-S + Sync + drift rate + 重置策略"] Q1 -->|"专人资产"| A4["训练时间 + FPS + LMD + LSE-C + held-out frames"] {{< /mermaid >}} 

_图 3：数字人 benchmark 设计决策树。论文指标解决"能否复现"，业务指标解决"能否上线"。_

### 从 benchmark 回到产品选型

业务目标| 优先路线| 核心评估| 主要风险  
---|---|---|---  
已有视频多语言配音| Wav2Lip / MuseTalk  
轻量换嘴| LSE-C / LSE-D  
边界 artifact  
局部画质| 口型边界  
情绪不一致  
素材授权  
客服 / 会议 avatar| LivePortrait / VASA-1 / Ditto  
运动空间 talking head| RTF / FFD / TTFF  
身份保持  
长时稳定| 表情僵硬  
身份漂移  
故障降级  
专人高保真形象| 3DGS / NeRF  
专人资产路线| 训练小时数  
FPS  
LMD / LSE-C| 采集成本  
跨姿态泛化  
资产维护  
虚拟主播短视频| Hallo / AniPortrait / EMO / OmniAvatar  
整帧或全身生成| FVD / CSIM / Sync  
动作自然度  
人评| 生成失败率  
审核成本  
重试成本  
实时互动讲解 / 直播| Live Avatar / StreamAvatar  
流式基模 + 蒸馏| FPS / TTFF / p95 latency  
长视频 identity  
并发吞吐| 首帧延迟  
长时漂移  
多卡调度  
  
**选型口径** ：离线内容生产可以优先追求表现力和人评质量；实时交互必须把首帧延迟、端到端延迟、长时稳定和降级策略放在画质之前。

Part 11

PoC、MVP 与规模化的落地检查

数字人项目的失败经常不是模型不可用，而是阶段错配：PoC 阶段追求生产级画质，MVP 阶段没有监控和降级，规模化阶段才发现许可证、肖像权、声音权或单位经济模型不成立。

阶段| 验证目标| 退出条件| 不该过早投入  
---|---|---|---  
PoC| 链路能否跑通| 口型 / 身份 / 延迟达标  
许可证无明显阻塞  
目标用户不反感| 大规模多卡训练  
全身高真实生成  
复杂运营后台  
MVP| 是否有人持续使用| 留存和会话时长稳定  
故障率可控  
单路成本有基线| 盲目扩并发  
绑定单一供应商  
忽略内容审核  
规模化| 是否能持续赚钱| 单位经济为正  
合规审计通过  
监控、调度、降级完备| 无授权形象商用  
无备用路线  
只按 demo FPS 估成本  
  
上线前还要单独检查许可证。Wav2Lip README 提示存在商业 API；MuseTalk 主许可证为 MIT；LivePortrait 主仓库为 MIT，但部分 InsightFace 相关模型仅限非商业研究；SadTalker 使用 Apache-2.0。代码许可证、模型权重许可证、依赖模型条款和训练数据授权要分开看。#Wav2Lip-GitHub# #MuseTalk-License# #LivePortrait-License# #SadTalker-License#

Appendix A

模型输入/输出规格汇总

下表按技术路线整理 28 个模型的输入、输出和多阶段训练配置。多阶段模型分别列出每个训练阶段的输入；推理时输入单独标注。#Wav2Lip# #MuseTalk# #SadTalker# #LivePortrait# #VASA1# #Ditto# #Teller#

模型| 路线| 训练输入| 推理输入| 最终输出| 训练阶段  
---|---|---|---|---|---  
**Wav2Lip**|  轻量换嘴| 视频帧 + 对应音频梅尔频谱| 任意视频 + 任意音频| 唇形同步视频（原视频嘴部替换）| Stage 1: SyncNet 专家训练  
Stage 2: GAN 生成器（L1+VGG+Sync+adversarial）  
**MuseTalk**|  局部重绘| 视频帧 + 音频梅尔频谱 + 嘴部 mask| 视频/图像 + 音频| 唇形同步视频（latent inpainting）| Stage 1: L1+VGG 基础重建（8×H20, 200K steps）  
Stage 2: face/lip adversarial + SyncNet（~30h）  
**SadTalker**|  3DMM 运动| 视频数据集（VoxCeleb 等）+ 3DMM 表情系数 GT| 单张图像 + 任意音频| 带动画面部视频| Stage 1: ExpNet 表情系数预测（+ lip-sync 判别器）  
Stage 2: PoseVAE 条件姿态生成  
Stage 3: 面部渲染网络（运动系数→图像 warp）  
**LivePortrait**|  隐式关键点| 参考图 + 驱动视频（提取关键点运动）| 参考图 + 驱动运动（视频/关键点序列）| 动画肖像视频| Stage I: 隐式关键点+外观网络（8×A100, ~10天）  
Stage II: stitching+retargeting（~2天）  
**VASA-1**|  motion diffusion| 参考图 + 音频 + 凝视/距离条件| 参考图 + 音频 + 可选条件| 512×512 talking head 视频| Stage 1: 面部潜在空间模型（4×A6000, 7天）  
Stage 2: DiT 扩散（3天）；推理 40 FPS  
**Ditto**|  motion diffusion| 视频帧（330 身份，~50h）→ Motion Extractor 提取 265D 运动表示 + HuBERT 音频特征 + 控制信号| 源图像 + 音频 + 可选控制信号（凝视/情绪/姿态/眼部状态）| talking head 视频（DiT 生成 265D 运动 → 预训练渲染器合成画面）| Motion Extractor / Renderer 预训练（LivePortrait 式）+ 条件 DiT 训练（8×A100, batch 1024, 500 epochs）  
**Teller**|  motion token AR| AVSpeech 662h + VFHQ 2h（motion RVQ token + Whisper 音频嵌入）| 源肖像图 + 流式音频 200ms chunks + 自回归运动 token 上下文| 流式 talking head 视频（25 FPS，4×H800 端到端 <200ms）| Stage 1 预训练: AR Transformer（8×8 A800, batch 1024, 40 epochs）+ SFT（32h, 10 epochs）  
Stage 2: ETM 时序细化模块（VAE + 3D U-Net temporal attention, 30 epochs）  
**AD-NeRF**|  NeRF portrait| 目标人物短视频（3-5min）+ 对应音频 + DeepSpeech 特征 + 3DMM 姿态| 专人 NeRF 模型 + 新音频特征 + 头部姿态序列| talking head 视频（Head-NeRF + Torso-NeRF 分别渲染合成）| Stage 1: Head-NeRF 训练  
Stage 2: Torso-NeRF 训练（以 Head 初始化）；共 ~167.6h  
**ER-NeRF**|  NeRF portrait| 目标人物短视频 + 音频 + DeepSpeech/Wav2Vec 特征 + 3DMM 姿态 + AU45| 专人 NeRF 模型 + 新音频特征 + 头部姿态序列| talking head 视频（tri-plane hash grid 渲染）| Stage 1: Head NeRF（100K iters）  
Stage 2: Lip 微调（patch LPIPS, 125K iters）  
Stage 3: Torso NeRF（200K iters）；训练 8.9h，推理 15 FPS  
**TalkingGaussian**|  3DGS head| 目标人物 3-5min 视频 + 音频 + DeepSpeech/HuBERT 特征 + 3DMM 姿态 + AU| 专人 3DGS 模型（融合后）+ 新音频特征 + 头部姿态序列| 实时 talking head 视频（GS 光栅化渲染）| Stage 1: Mouth 3DGS 训练  
Stage 2: Face 3DGS 训练（可并行）  
Stage 3: Fuse 融合训练；训练 ~1.5h，推理 70 FPS  
**GaussianTalker**|  3DGS head| 目标人物视频 + 音频 + 音频特征 + 3DMM 姿态 + 面部解析 mask| 专人 3DGS 模型 + 新音频特征 + 头部姿态| 实时 talking head 视频（面部/身体 3DGS 分别渲染）| 面部 3DGS + 身体 3DGS 分离训练；~4.5h，59 FPS  
**GSTalker**|  3DGS head| 目标人物视频 + 音频 + HuBERT/DeepSpeech 特征 + 头部姿态 + 语义解析 mask| 专人 3DGS + 形变场模型 + 新音频特征 + 头部姿态 + 眨眼特征| 实时 talking head 视频（GS 光栅化，125 FPS）| Stage 1: 静态 Gaussian 初始化（~1min）  
Stage 2: 音频条件形变场训练（100K iters, ~40min 总）  
**EGSTalker**|  3DGS head| 目标人物视频 + 音频 + 音频特征 + 3DMM 姿态 + 表情参数| 专人 3DGS 模型 + 新音频特征 + 头部姿态 + 表情参数| 实时 talking head 视频（expression-guided GS 渲染，68 FPS）| expression-guided Gaussian splatting；~3.7h  
**SentiAvatar**|  motion controller| SuSuInterActs 动捕数据（63 关节 6D 旋转 + ARKit 51 维表情 + 同步语音）+ 200K+ 预训练运动序列| 语音音频 + 动作/表情文本标签 + 可选上文运动上下文| 3D 动画参数（63 关节旋转 + 51 维 ARKit 表情），驱动游戏引擎中的 3D 角色| Stage 1: R-VQVAE 运动/表情 token 化  
Stage 2: Motion FM 预训练（Qwen-0.5B, 200K 序列）  
Stage 3: SFT 角色微调  
Stage 4: Infill Transformer（8×A100）  
**EMO**|  扩散肖像| 参考图 + 音频| 参考图 + 音频| 肖像动画视频| Stage 1: 面部预训练（250h+ 数据）  
Stage 2: 音频-肖像对齐  
**Hallo**|  扩散肖像| 参考图 + 音频| 参考图 + 音频| 肖像动画视频| Stage 1: 面部预训练  
Stage 2: 级联潜扩散（8×A100, 各 30K steps）  
**AniPortrait**|  扩散肖像| Audio2Lmk: wav2vec2 特征 → 3D mesh / 6D 姿态 GT  
Lmk2Video: VFHQ+CelebV-HQ 视频 + MediaPipe 2D 关键点| 参考图 + 音频（或驱动视频关键点序列）| 肖像动画视频（512×512，最长约 10s）| Audio2Lmk: Audio2Mesh + Audio2Pose（单 A100）  
Lmk2Video Stage 1: 2D 组件+ReferenceNet+PoseGuider（4×A100, 2天, 300K steps）  
Lmk2Video Stage 2: 冻结其余，训练 motion module（2天, 40K steps）  
**FLAP**|  扩散肖像| 视频（HDTF+CelebV-HQ+VFHQ）+ 逐帧 FLAME 120D 系数（旋转/眼/下颌/表情）| 参考图 + 音频（→ Audio-to-FLAME 生成 FLAME 系数）+ 可选用户控制| 可控 talking head 视频（512×512）| PFT 三阶段：Stage 1 头部运动图像训练（150K steps）  
Stage 2 表情图像训练（冻结运动层, 150K steps）  
Stage 3 视频时序训练（50K steps, SD1.5+AnimateDiff 初始化）  
**Animate Anyone**|  全身生成| 参考图 + pose 序列| 参考图 + pose 序列| 全身动画视频| 内部 5K character video clips 训练  
**OmniAvatar**|  全身 DiT| 参考图/视频 + 音频| 参考图 + 音频| 音频驱动全身视频| Wan2.1-T2V-14B + LoRA 音频适配  
**InfiniteTalk**|  全身 DiT| 源视频 + 音频 + 稀疏关键帧| 参考视频/图像 + 音频 + 上下文帧| 长视频音频驱动 talking head| Wan2.1-I2V-14B 微调（~2000h, 64×H100 80G）  
**Live Avatar**|  流式基模| 参考图 + 音频 + 上下文帧| 参考图 + 音频流| 实时流式视频| Stage 1: 128×H800 25K steps  
推理 4-step, 5×H800 → 45.2 FPS / 1.21s TTFF  
**StreamAvatar**|  流式蒸馏| 参考图 + 音频| 参考图 + 音频流| 实时流式视频| 双向扩散 → block-wise causal attention + 蒸馏  
**LLIA**|  流式蒸馏| 参考图 + 音频| 参考图 + 音频流| 实时流式视频| consistency model + INT8 + pipeline parallelism；4090D 45 FPS  
**FlashHead**|  2D 视频 DiT| 参考图 + 音频 + 运动上下文帧| 参考图 + 音频流（~1.32s chunks）+ 自回归运动帧| 实时流式 talking head 视频（512×512, 25fps；Lite 96 FPS / Pro 10.81 FPS）| Stage 1: 流式感知时空预训练（flow-matching MSE, 100K steps, 32×H20）  
Stage 2: Oracle 引导双向蒸馏（DMD + latent regression）  
**LAM**|  3DGS 重建| 视频帧序列 + FLAME 参数（VFHQ 15K clips，每步采样 8 帧）| 单张图像（→ 一次前向生成 3DGS 资产）+ FLAME 驱动参数| 可动画 3D Gaussian 资产（经 LBS 动画 + 光栅化渲染为实时视频；WebGL 部署，iPhone 26-38 FPS）| 统一训练：L1+LPIPS+mask+offset loss（200 epochs）；单阶段，无分步优化  
**UIKA**|  3DGS 重建| 视频帧序列（VFHQ+HDTF+NeRSemble-v2+合成数据 7500+ 身份）| 1-N 张 pose-free 图像（→ 生成 3DGS 资产）+ FLAME 驱动参数| 可动画 3D Gaussian 头部资产（LBS 动画 + GS 渲染，220 FPS；推理耗时随视角数增长）| 统一端到端训练 150K steps（32×H20）；含 UV 对应估计器 + MM-Transformer + UV 解码器，单阶段联合优化  
**LiteAvatar**|  参数化面部| 预训练参数化面部模型（未公开训练细节）| 音频（TTS 输出，16kHz）→ audio2param 提取面部参数（30 FPS）| 参数化面部渲染帧（H×W×3 RGB, 25 FPS；纯 CPU 推理）| audio2param（音频→参数）+ param2video（参数→渲染帧）；C++ 核心实现  
  
_表：28 个数字人模型的输入/输出规格。多阶段训练分别列出；推理输入指部署时所需。#EGSTalker# #SentiAvatar# #Hallo# #AniPortrait# #FLAP# #OmniAvatar# #InfiniteTalk# #LiveAvatar# #StreamAvatar# #LLIA# #Yu-et-al.-2026# #He-et-al.-2025# #Wu-et-al.-2026# #LiteAvatar#_

**读表提示** ：推理输入越简单（如 LiteAvatar 只需音频），部署门槛越低；但输入越丰富（如 InfiniteTalk 需要源视频+音频+关键帧），可控性越强。注意两类根本不同的模型范式：**（1）专人模型** （AD-NeRF / ER-NeRF / TalkingGaussian / GSTalker / EGSTalker）对每个目标人物单独训练一个 NeRF/3DGS 模型，推理时用该模型 + 新音频生成视频；**（2）通用模型** （LAM / UIKA）对任意输入图像做一次前向即生成可复用 3DGS 资产，再用任意音频/运动驱动渲染。多阶段训练的模型通常前一阶段学基础能力（身份/空间结构），后一阶段学音频驱动/时序一致性。

Appendix B

数据集数据组织格式与规模

Part 7 汇总了数据集的 License 和适用场景，本节补充每个数据集**实际提供什么类型的数据** （视频、音频、参考图像、3D 扫描、标注等）以及磁盘规模。选择数据集时，除了看 License 和规模，还要看数据组织格式是否与模型训练管线匹配。

数据集| 数据类型| 视频/帧| 音频| 参考图| 关键标注| 规模| 获取方式  
---|---|---|---|---|---|---|---  
[**HDTF**](./hdtf-source-code-analysis.html)|  视频 + 音频| MP4, 512×512, 25fps| WAV（需自行从视频提取）| 需从视频截取首帧| 时间段标注、crop 窗口、缩放比| 368 clips / ~362 人 / ~15.8h / ~10-15 GB| GitHub 元数据 + YouTube URL 自下载  
[**VFHQ**](./vfhq-2022.html)|  视频 + 音频| MP4, ≥512×512| 内嵌（需自行提取）| 无（从视频截取）| 5 阶段质量筛选标签| 16,827 clips / 7,228 源视频 / ~30-50 GB| GitHub 工具 + YouTube  
**VoxCeleb2**|  视频 + 音频| MP4, 多种分辨率| AAC/WAV, 16kHz+| 无| Speaker ID、性别、国籍| ~150K utterances / 6,112 人 / >2000h / ~300+ GB| URL 列表（视频已下架，需自下载）  
**CelebV-HQ**|  视频 + 标注| MP4, ≥512×512| 内嵌| 无（从视频截取）| 83 种面部属性、情绪、bbox| 35,666 clips / 15,653 人 / ~50-80 GB| GitHub + youtube_dl 脚本  
**LRS2**|  视频 + 音频 + 文本| MP4, 576p/720p| 内嵌, 16kHz| 无| 逐句文本转录、词对齐| ~96K utterances / ~220h / ~30-40 GB| 申请下载（非商业研究）  
**LRS3**|  视频 + 音频 + 文本| MP4, 720p/1080p| 内嵌, 16kHz| 无| 逐句文本转录、词对齐| ~152K utterances / ~430h / ~50-70 GB| 申请下载（非商业研究）  
[**MEAD**](./mead-2020.html)|  多视角视频 + 音频| MP4, 384p, 7 视角同步| 独立音轨（录音棚采集）| 可从视频截取| 8 情绪 × 3 强度 × 7 视角| ~281K clips / 60 人 / ~39h / ~100-200 GB| 百度网盘 / Google Drive  
**NeRSemble-v2**|  多视角帧序列| JPG 帧, 7.1MP, 73fps, 16 相机| **无** （纯视觉重建）| 多视角帧均可作参考| 相机内外参、FLAME 参数| 4,700+ seqs / 220+ 人 / ~500GB-1TB| 申请访问（研究用途）  
**VividHead**|  视频 + 音频| MP4, 512×512, 3-60s/clip| 严格时间对齐语音| 可从视频截取| 语言、年龄、族裔元数据| 330K clips / ~60K 人 / 782h / ~200-400 GB| 未公开（Soul AI Lab 内部）  
**AVSpeech**|  视频 + 音频| YouTube 原始质量, 3-10s/clip| 内嵌（单人清晰语音）| 无| CSV 元数据（YouTube ID、bbox）| ~290K videos / ~4700h / ~1-2 TB| CSV 元数据 + YouTube 自下载  
**RAVDESS**|  视频 + 音频| MP4, 720p H.264| WAV 48kHz / AAC 48kHz| 可从视频截取| 8 情绪 × 2 强度（文件名编码）| 7,356 files / 24 人 / **24.8 GB**|  Zenodo 直接下载  
**UIKA Synthetic**|  合成多视角| 渲染图, 512×512, 9 视角| **无** （纯视觉）| 9 视角渲染图| FLAME pose/expression 参数| 7,500+ 身份 × 9 视角 × 13K+ 帧| 未公开（UIKA 自建管线）  
**EMTD**|  视频 + 音频| HD, 全身/半身| 内嵌| 可从视频截取| 情绪标签| 未公开| 研究获取  
**UBC Fashion**|  视频 + Pose| MP4, HD| **无语音** （背景/无声）| 可从视频截取| OpenPose/DWPose 骨骼关键点| 数千 clips / ~10-30 GB| 论文附带  
**GenBench**|  视频 + 音频| 多种分辨率| CosyVoice 合成语音| Gemini/Qwen 生成| 角色类型、视角、范围| Short: 100×10s + Long: 15×5min+| 论文附带  
  
_表：15 个主流数据集的数据组织格式与规模。加粗"无"表示该数据集不提供此类数据。_

数据格式与模型训练的匹配 

  * **音频提取** ：HDTF、VFHQ、VoxCeleb2、CelebV-HQ 等数据集的音频内嵌在视频中，训练前需要用 ffmpeg 提取独立音轨（`ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 16000 output.wav`）。
  * **参考图截取** ：大多数 talking head 数据集不提供独立参考图像，需要从视频中截取首帧或指定帧作为 one-shot 参考图。
  * **纯视觉数据集** ：NeRSemble-v2 和 UIKA Synthetic 不含音频，仅用于 3D 重建和几何评估；音频驱动需要额外配对。
  * **Pose 数据集** ：UBC Fashion 提供骨骼关键点而非音频，适用于 pose-driven 全身动画评测（Animate Anyone 路线），不适用于 lip-sync 评测。
  * **磁盘估算** ：磁盘大小为估算值，实际取决于编码格式、帧率和压缩率。VoxCeleb2 原始文件已下架，实际可用性取决于 YouTube 视频是否仍在线。

Appendix C

数字人脸真实度评测：指标全景与 deepfake 检测的适用性

Part 1 覆盖了五大通用指标族（画质、时序、同步、身份、效率），但数字人的核心用户体验是**"看起来像不像真人"** ——这个问题比任何单一指标都更复杂。本节补充三方面内容：人脸专用质量评估（FIQA）、感知质量最新进展、以及 deepfake 检测能否反向用作真实度指标。

### C.1 人脸专用质量评估（FIQA）

FIQA（Face Image Quality Assessment）是专门针对人脸图像的质量评估，区别于通用 IQA。但需要注意：**现有 FIQA 方法几乎全部以"人脸识别性能"为优化目标** ——其质量定义是"这张脸能否被准确识别"，而非"这张脸看起来是否像真人"。直接用于数字人真实度评测存在概念错位，但可作为辅助筛除指标。

方法| 原理| 对数字人评测的价值| 局限| 代码库  
---|---|---|---|---  
**FaceQnet v2** #Hernandez-Ortega-et-al.-2020#| ResNet50 综合打分（清晰度、光照、遮挡、姿态）| 快速筛除明显低质帧| 训练目标是"识别友好度"，对 GAN/diffusion 伪影不敏感| `uam-biometrics/FaceQnet`  
**CR-FIQA** #Boutros-et-al.-2022#| ArcFace 识别置信度作为质量代理| 高质量帧排序| 如果生成脸骗过 ArcFace，CR-FIQA 会给高分——恰恰是评测想检测的问题| `fdbtrs/CR-FIQA`  
**SDD-FIQA** #Ou-et-al.-2022#| 同一人脸多次嵌入的分布一致性| 评估稳定性| 计算开销大，同样依赖识别模型| Ou et al. 2022  
**MagFace** #Meng-et-al.-2021#| 识别+质量联合优化，quality 从特征 magnitude 推导| 端到端质量感知| 质量定义仍是"识别友好度"| Meng et al. 2021  
**SER-FIQ** #Terhorst-et-al.-2020#| 人脸嵌入不确定性作为质量信号| 不确定性感知的筛选| 不确定性反映识别模型困惑度，不等于视觉真实度| Terhorst et al. 2020  
**[DSL-FIQA](dsl-fiqa-2024.html)** #Chen-et-al.-2024#| 双集合退化学习 + Landmark-Guided Transformer，优化感知质量而非识别可用性| GFIQA 方向最新代表，比 BFIQA 更适合评估数字人生成帧的感知质量| 跨数据集泛化 PLCC 仅 0.42；依赖 landmark detector；代码无 License| 深度解读  
  
### C.2 感知质量与人脸真实度指标

除了 Part 1 已覆盖的 FID/FVD/LPIPS，以下指标对数字人脸真实度有更直接的评测价值：

指标| 原理| 适用场景| 局限  
---|---|---|---  
**DISTS** #Ding-et-al.-2020#| 结构和纹理的联合感知相似度| 比 LPIPS 更适合纹理丰富的生成脸| 基于 ImageNet 预训练，非人脸特化；需要 GT  
**CLIP-IQA+** #Wang-et-al.-2023#| CLIP 多模态无参考质量评估| 无 GT 时的生成质量评估| 泛化性好但在人脸生成领域未充分验证  
**MANIQA** #Yang-et-al.-2022# / **MUSIQ** #Ke-et-al.-2021#| Transformer 无参考 IQA| 大规模无参考筛选| 在自然图像上训练，对 GAN/diffusion 系统性伪影泛化差  
**FaceSSIM / Face-LPIPS**|  在人脸裁剪区域上计算 SSIM #Wang-et-al.-2004# / LPIPS #Zhang-et-al.-2018#| 比全图指标更聚焦脸部| 非独立论文方法，而是多篇 talking head 论文（如 Wav2Lip #Prajwal-et-al.-2020#、LivePortrait #LivePortrait#）中自定义的裁剪区域 SSIM/LPIPS  
**AKD / MKD**|  关键点欧氏距离（Average / Mean Keypoint Distance）| 面部几何准确性| 只测几何，不测纹理/光影；定义因论文而异，常见于 LivePortrait #LivePortrait#、SadTalker #SadTalker#  
**ΔP / CAPP**|  表情参数变化幅度/一致性| 表情驱动自然度| 依赖特定 3DMM/AU 参数化模型；见 Ditto #Ditto#、VASA-1 #VASA1#  
  
### C.3 Deepfake 检测能否反向用于真实度评测？

一个直觉性的想法是：如果 deepfake 检测器判断生成脸为"真"，说明它足够真实。但这个推理存在根本性问题。

检测器| 原理| 能否反向用？| 理由  
---|---|---|---  
**XceptionNet** #Rossler-et-al.-2019#| 空域伪造痕迹（压缩伪影、混合边界）| 部分能| 在 face swap 上训练，对 diffusion/talking head 泛化差；分数未经校准  
**EfficientNet + NoisePrint** #Cozzolino-et-al.-2019#| 高层语义 + 噪声残差融合| 部分能| 噪声分析对 GAN checkerboard artifact 有捕获能力，但噪声模式 ≠ 视觉真实度  
**Face X-ray** #Li-et-al.-2020#| 预测混合边界位置和强度| **能（局部路线）**|  对 Wav2Lip/MuseTalk 等局部换嘴的 blending 质量有直接参考价值；对端到端全脸生成失效  
**Multi-attention (MAT)** #Zhao-et-al.-2021#| 多尺度注意力定位伪造线索| 部分能| 可提供"哪里不真实"的空间热力图，但注意力权重为二分类优化  
**FTCN** #Guo-et-al.-2022#| 频域时序不一致性检测| **能（视频场景）**|  频域时序异常与数字人"闪烁""抖动""唇形突变"直接对应；比 FVD 更有针对性  
**频谱分析 (DCT)** #Wang-et-al.-2020#| GAN/扩散模型的频谱特征性异常| 能| 频谱异常与生成模型固有缺陷直接关联，不受语义内容影响；适合作为组合指标的一个分量  
  
为什么 deepfake 检测不适合直接用作质量指标 

  * **目标错位** ：Deepfake 检测优化二分类准确率，数字人质量评估是多维连续评估。检测器的 decision boundary 不等于质量梯度。
  * **训练分布偏移** ：现有检测器主要在 face swap 数据上训练（FF++ #Rossler-et-al.-2019#、Celeb-DF #Li-et-al.-2020-celebdf#、DFDC #Dolhansky-et-al.-2020#），对 diffusion/NeRF/3DGS 生成的数字人泛化差。高质量 EMO 生成可能被标记为"真"（不像已知伪造），低质量但有新伪影的生成可能被标记为"假"——两种情况都无法反映真实质量。
  * **分数不可解释** ：检测器 softmax 输出未经校准，0.7 和 0.8 之间没有明确的质量语义。
  * **数字人 vs deepfake 的本质区别** ：数字人有明确的驱动信号（音频/文本）可供同步评估，deepfake 没有；数字人的质量标准是"看起来自然、同步、一致"，deepfake 的标准是"不被检测到"——两者优化方向根本不同。

### C.4 推荐的分层真实度评测框架

综合 Part 1 的通用指标和本节的专项目标，推荐以下分层评估框架：

层级| 维度| 推荐指标| 说明  
---|---|---|---  
**L0** 基础质量| 清晰度/可用性| FaceQnet v2 或 CR-FIQA| 快速筛除明显低质帧；不作为最终评分  
**L1** 图像真实度| 感知质量| LPIPS（有GT）/ CLIP-IQA+（无GT）/ DISTS| 比 FID 更适合单样本评估  
**L1** 图像真实度| 分布相似度| FID（clean-fid，≥1000 样本）| 仅用于模型间横向比较  
**L2** 身份保真度| 身份一致性| CSIM (ArcFace cosine)| one-shot 场景必须报告  
**L2** 身份保真度| 几何准确性| AKD / landmark distance| 补充 CSIM 的纹理盲区  
**L3** 时序质量| 视频连贯性| FVD（注明 clip length）+ FTCN 频域时序分| FVD 看整体，FTCN 看频域异常  
**L3** 时序质量| 帧间稳定| Dino-S / temporal consistency| 长视频漂移检测  
**L4** 同步质量| 唇音同步| SyncNet LSE-C / LSE-D| talking head 必报  
**L5** 融合质量| 局部拼接| Face X-ray blending score| 仅适用于局部换脸/换嘴路线  
**L6** 生成痕迹| 频谱异常| DCT 频谱分析| 检测 GAN/diffusion 固有伪影  
**L7** 人类感知| 综合主观| MOS（多维度、within-subject、≥30 人）| 金标准，但不可自动化  
  
**关键原则** ：没有单一指标能回答"这个数字人好不好"，必须多维度组合。无参考指标（CLIP-IQA+、FaceQnet）用于大规模筛选，有参考指标（LPIPS、CSIM）用于精确对比。Deepfake 检测器的特定组件（Face X-ray 的 blending 检测、FTCN 的频域时序分析、DCT 频谱分析）可抽取为专项工具，但不应直接用作质量分数。

未来研究方向 

  * **Digital Human Quality Benchmark** ：需要专门的 benchmark，覆盖 NeRF/3DGS/diffusion/autoregressive/GAN/局部换嘴 等多条路线的生成样本，配合人类标注的多维质量分数。现有 FF++/Celeb-DF/DFDC 均不适用。
  * **Face-specific Perceptual Metric** ：在人脸生成数据上训练感知质量模型，而非复用 ImageNet 预训练的 LPIPS/VGG。
  * **Uncanny Valley 量化** ：目前没有任何自动指标能捕获"恐怖谷"效应，需要结合 FACS、微表情分析和心理物理学实验。
  * **Long-term Exposure Study** ：现有用户研究都是短时暴露，数字人在实际使用中是长时间暴露的，感知质量可能随时间变化。
  * **Cross-modal Consistency** ：数字人是音视频联合产物，需要超越唇音同步，评估表情-语调匹配、手势-语义匹配等跨模态一致性。

Conclusion

指标是工具，不是答案

数字人没有一个统一 benchmark 能覆盖所有路线。轻量换嘴的核心是同步和边界质量；运动空间的核心是低维运动是否稳定、可控、实时；NeRF/3DGS 的核心是专人资产训练成本和渲染效率；扩散肖像和整帧全身路线的核心是表现力、长时一致性和采样成本；流式基模则必须把 FPS、TTFF、长视频身份和系统链路一起评估。

跨路线对比（如 FlashHead vs LAM vs UIKA vs LiteAvatar）需要输出归一化和两层指标体系，不能合成单一分数排名。产品选型时，先把业务目标翻译成评测维度，再从本文的指标族和数据集表中选择合适的工具。

### 一页速查

  * **五大指标族** ：画质（FID/PSNR/SSIM/LPIPS）、时序（FVD/Dino-S）、同步（Sync-C/D）、身份（CSIM）、效率（FPS/RTF/TTFF/VRAM）。
  * **跨路线对比** ：Sync-C/D + CSIM + FPS + VRAM 是通用指标。FID/FVD 仅适用于视频输出；PSNR/SSIM 仅适用于有 GT 的重建任务。
  * **最低成本验证** ：Wav2Lip / MuseTalk，看 LSE-C、CSIM、FID 和真实素材边界。
  * **实时 talking head** ：LivePortrait / VASA-1 / Ditto / Teller，看 RTF、FFD、Sync-C/D 和首帧。
  * **专人高保真资产** ：3DGS 优先于传统 NeRF，看训练小时数、FPS、LMD 和 LSE-C。
  * **离线高表现力** ：Hallo / AniPortrait / EMO / InfiniteTalk，看 FVD、Sync、CSIM、人评和失败样本。
  * **实时大模型路线** ：Live Avatar / StreamAvatar / LLIA，看 TTFF、FPS、长时 identity 和并发成本。
  * **模型输入/输出** （Appendix A）：28 个模型的训练输入、推理输入、最终输出和多阶段配置汇总。
  * **数据集格式与规模** （Appendix B）：15 个数据集的数据类型（视频/音频/参考图/标注）、磁盘大小和获取方式。
  * **真实度评测** （Appendix C）：FIQA（FaceQnet/CR-FIQA）、感知质量（DISTS/CLIP-IQA+）、deepfake 检测的适用性分析；推荐 L0-L7 分层评测框架。

[←上一篇 · 第八章Avatar 类型数字人总报告](digital-human-avatar-survey.html) [系列目录数字人系列总览](digital-human-hub.html) [→下一篇产业图谱](voice-ai-digital-human-landscape.html)

### 参考来源

  * Heusel, M. et al. (2017). GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium (FID). [arXiv:1706.08500](https://arxiv.org/abs/1706.08500)
  * Unterthiner, T. et al. (2018). Towards Accurate Generative Models of Video (FVD). [arXiv:1812.01717](https://arxiv.org/abs/1812.01717)
  * Chung, J. S. et al. (2017). Out of Time: Automated Lip Sync in the Wild (SyncNet). [arXiv:1611.01599](https://arxiv.org/abs/1611.01599)
  * Prajwal, K. R. et al. (2020). Wav2Lip: Accurately Lip-syncing Videos In The Wild (LSE-C/D). [arXiv:2008.10010](https://arxiv.org/abs/2008.10010)；本系列精读：[Wav2Lip](paper-wav2lip.html)
  * Deng, J. et al. (2019). ArcFace: Additive Angular Margin Loss for Deep Face Recognition (CSIM). [CVPR 2019](https://arxiv.org/abs/1801.07698) · [精读 →](arcface-2018.html)
  * Zhang, R. et al. (2018). The Unreasonable Effectiveness of Deep Features as a Perceptual Metric (LPIPS). [CVPR 2018](https://arxiv.org/abs/1801.03924)
  * 本系列精读：[Wav2Lip](paper-wav2lip.html)
  * 本系列精读：[MuseTalk](paper-musetalk.html)
  * Zhang, W. et al. (2023). SadTalker. [arXiv:2211.12194](https://arxiv.org/abs/2211.12194)；本系列精读：[SadTalker](paper-sadtalker.html)
  * Guo, J. et al. (2024). LivePortrait. 本系列精读：[LivePortrait](paper-liveportrait.html)
  * Xu, S. et al. (2024). VASA-1. 本系列精读：[VASA-1](paper-vasa1.html)
  * 本系列精读：[Ditto](paper-ditto.html)
  * 本系列精读：[Teller](paper-teller.html)
  * 本系列专题：[3DGS 与 NeRF 数字人路线](digital-human-3dgs-nerf-avatar.html)
  * Guo, Y. et al. (2021). AD-NeRF. [arXiv:2103.11078](https://arxiv.org/abs/2103.11078)
  * Li, J. et al. (2023). ER-NeRF. [arXiv:2307.09323](https://arxiv.org/abs/2307.09323)
  * TalkingGaussian. [arXiv HTML](https://arxiv.org/html/2404.15264)
  * GaussianTalker. [arXiv HTML](https://arxiv.org/html/2404.14037)
  * GSTalker. [arXiv HTML](https://arxiv.org/html/2404.19040)
  * EGSTalker. [arXiv HTML](https://arxiv.org/html/2510.08587v1)；本系列精读：[EGSTalker](paper-egstalker.html)
  * SentiAvatar. [arXiv:2604.02908](https://arxiv.org/abs/2604.02908)；本系列精读：[SentiAvatar](paper-sentiavatar.html)
  * 本系列精读：[Hallo](paper-hallo.html)
  * 本系列精读：[AniPortrait](paper-aniportrait.html)
  * EMO: Emote Portrait Alive. [arXiv HTML](https://arxiv.org/html/2402.17485v1)
  * 本系列精读：[FLAP](paper-flap.html)
  * Animate Anyone. [arXiv HTML](https://arxiv.org/html/2311.17117v2)
  * OmniAvatar. [arXiv HTML](https://arxiv.org/html/2506.18866v1)
  * 本系列精读：[InfiniteTalk](infinitetalk-paper.html)
  * 本系列精读：[Live Avatar](live-avatar-paper.html)
  * StreamAvatar. [arXiv HTML](https://arxiv.org/html/2512.22065v2)
  * 本系列专题：[扩散基模与整帧数字人路线](digital-human-diffusion-foundation-avatar.html)
  * Yu, T. et al. (2026). SoulX-FlashHead. [arXiv:2602.07449](https://arxiv.org/pdf/2602.07449)；本系列精读：[FlashHead](paper-soulx-flashhead.html)
  * He, Y. et al. (2025). LAM: Large Avatar Model. [arXiv:2502.17796](https://arxiv.org/abs/2502.17796)；本系列精读：[LAM](lam-2025.html)
  * Wu, Z. et al. (2026). UIKA: Fast Universal Head Avatar. [arXiv:2601.07603](https://arxiv.org/abs/2601.07603)；本系列精读：[UIKA](uika-2026.html)
  * HumanAIGC/lite-avatar. [GitHub](https://github.com/HumanAIGC/lite-avatar)；本系列源码解读：[LiteAvatar](lite-avatar-source-code-analysis.html)
  * Rudrabha/Wav2Lip official repository. [GitHub](https://github.com/Rudrabha/Wav2Lip)
  * TMElyralab/MuseTalk LICENSE. [MIT License](https://github.com/TMElyralab/MuseTalk/blob/main/LICENSE)
  * KwaiVGI/LivePortrait LICENSE and README. [GitHub](https://github.com/KwaiVGI/LivePortrait)
  * OpenTalker/SadTalker LICENSE. [Apache-2.0](https://github.com/OpenTalker/SadTalker/blob/main/LICENSE)
  * Hernandez-Ortega, J. et al. (2020). FaceQnet: Quality Assessment for Face Recognition Systems. [GitHub](https://github.com/uam-biometrics/FaceQnet)
  * Boutros, F. et al. (2022). CR-FIQA: Face Image Quality Assessment by Confidence-Ranked Face Recognition. [GitHub](https://github.com/fdbtrs/CR-FIQA)
  * Meng, Q. et al. (2021). MagFace: A Universal Representation for Face Recognition and Quality Inference. [CVPR 2021](https://arxiv.org/abs/2103.06627)
  * Li, Y. et al. (2020). Face X-ray for Discovering Unknown Face Synthesis. [CVPR 2020](https://arxiv.org/abs/1912.13458)
  * Guo, Z. et al. (2022). Exploring Frequency Adversarial Attacks for Face Forgery Detection. [arXiv:2203.15691](https://arxiv.org/abs/2203.15691)
  * Wang, J. et al. (2023). Exploring CLIP for Assessing the Look and Feel of Images (CLIP-IQA+). [AAAI 2023](https://arxiv.org/abs/2207.12396)
  * Ding, K. et al. (2020). Image Quality Assessment: Unifying Structure and Texture Similarity (DISTS). [arXiv:2004.07728](https://arxiv.org/abs/2004.07728)
  * Wang, K. et al. (2020). MEAD: A Large-scale Audio-visual Dataset for Emotional Talking-face Generation. [ECCV 2020](https://wywu.github.io/projects/MEAD/MEAD.html)；本系列精读：[MEAD](mead-2020.html)
  * Ou, F. et al. (2022). SDD-FIQA: Unsupervised Face Image Quality Assessment with Similarity Distribution Distance. [ICCV 2021 (extended)](https://arxiv.org/abs/2109.08570)
  * Chen, W.-T. et al. (2024). DSL-FIQA: Assessing Facial Image Quality via Dual-Set Degradation Learning and Landmark-Guided Transformer. _CVPR 2024_. [arXiv:2406.09622](https://arxiv.org/abs/2406.09622)；本系列精读：[DSL-FIQA](dsl-fiqa-2024.html)
  * Terhorst, P. et al. (2020). SER-FIQ: Unsupervised Estimation of Face Image Quality Based on Clustering. [CVPR 2020](https://arxiv.org/abs/2003.09332)
  * Yang, S. et al. (2022). MANIQA: Multi-dimension Attention Network for No-Reference Image Quality Assessment. [CVPRW 2022](https://arxiv.org/abs/2204.08950)
  * Ke, J. et al. (2021). MUSIQ: Multi-scale Image Quality Transformer. [ICCV 2021](https://arxiv.org/abs/2108.05997)
  * Wang, Z. et al. (2004). Image Quality Assessment: From Error Visibility to Structural Similarity. [IEEE TIP 2004](https://ieeexplore.ieee.org/document/1284395)
  * Rossler, A. et al. (2019). FaceForensics++: Learning to Detect Manipulated Facial Images. [ICCV 2019](https://arxiv.org/abs/1901.08971)
  * Cozzolino, D. et al. (2019). NoisePrint: A CNN-Based Camera Fingerprint for Detecting and Locating Image Forgeries. [CVPR 2019](https://arxiv.org/abs/1908.08980)
  * Zhao, Y. et al. (2021). Multi-Attentional Deepfake Detection. [CVPR 2021](https://arxiv.org/abs/2103.02406)
  * Wang, S.-Y. et al. (2020). CNN-generated images are surprisingly easy to spot... for now. [CVPR 2020](https://arxiv.org/abs/1912.11035) · [精读 →](mead-2020.html)
  * Li, Y. et al. (2020). Celeb-DF: A Large-scale Challenging Dataset for DeepFake Forensics. [CVPR 2020](https://arxiv.org/abs/1909.12962)
  * Dolhansky, B. et al. (2020). The DeepFake Detection Challenge (DFDC) Dataset. [arXiv:1910.08854](https://arxiv.org/abs/1910.08854)
  * Mittal, A. et al. (2012). No-Reference Image Quality Assessment in the Spatial Domain (BRISQUE). [IEEE TIP 2012](https://ieeexplore.ieee.org/document/6329921)
  * Mittal, A. et al. (2013). Making a "Completely Blind" Image Quality Analyzer (NIQE). [IEEE Signal Processing Letters 2013](https://ieeexplore.ieee.org/document/6353522)
  * Kynkaamaki, S. et al. (2022). Improved Precision and Recall of Generative Models (clean-fid). [GitHub](https://github.com/GaParmar/clean-fid)
  * Oquab, M. et al. (2024). DINOv2: Learning Robust Visual Features without Supervision. [TMLR 2024](https://arxiv.org/abs/2304.07193)
Ding, K. et al. (2020). Image Quality Assessment: Unifying Structure and Texture Similarity. [arXiv:2004.07728](https://arxiv.org/abs/2004.07728)
