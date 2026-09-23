---
title: "图像压缩论文精读（十七）：GFVC，生成式人脸视频编码与标准化综述"
description: "深读 DCC 2024 综述《Generative Face Video Coding Techniques and Standardization Efforts: A Review》：用 analysis-synthesis 框架统一 16 个 GFVC 方法，按 6 类 facial representation 做 taxonomy，并把人脸视频压缩写进 VVC SEI message 与 JVET 标准化时间线。"
date: 2026-07-11T19:36:25
created_at: 2026-07-11T19:36:25
updated_at: 2026-07-11T19:36:25
tags: ["generative-compression", "face-video-coding", "model-based-coding", "MPEG-JVET", "VVC-SEI"]
aliases: ["categories/AI/图像压缩/图像压缩论文精读"]
sub_id: 170
papers: ["https://arxiv.org/abs/2311.02649"]
repos: ["https://github.com/Berlin0610/Awesome-Generative-Face-Video-Coding"]
notify: true
mathjax: true
hero_title: "GFVC 综述"
hero_sub: "DCC 2024 · CityU & Alibaba"
hero_tagline: "用深度生成模型复活 model-based coding，并把人脸视频压缩写进 VVC SEI"
paper_title: "Generative Face Video Coding Techniques and Standardization Efforts: A Review"
paper_authors: "Bolin Chen, Jie Chen, Shiqi Wang, Yan Ye"
paper_affiliation: "香港城市大学；Alibaba Group"
paper_venue: "Data Compression Conference (DCC) 2024 · arXiv 2311.02649 (2023)"
paper_doi: "10.48550/arXiv.2311.02649"
paper_url: "https://arxiv.org/abs/2311.02649"
paper_code: "https://github.com/Berlin0610/Awesome-Generative-Face-Video-Coding"
---

> 来源：博客 gongshangzheng.github.io `src/pages/gfvc-survey-2023.html`，html2text 转换复制于 2026-09-20。原文：https://gongshangzheng.github.io/gfvc-survey-2023.html

6facial representation

16GFVC 方法

8JVET 提案

1950sMBC 起源

核心问题：人脸视频能否不传像素只传"参数"

当你拿起手机和别人视频通话时，每一帧人脸画面都被 H.264 / HEVC / VVC 这类传统编解码器切成宏块、做运动补偿、残差变换、熵编码——压缩的对象始终是**像素残差** #Bross et al., 2021#。这套 hybrid 框架为通用视频而生，并不针对人脸信号的统计特性优化。于是一个很早就被提出的反问在低带宽时代重新变得诱人：能不能干脆不传像素，只传描述人脸的少量"参数"，解码端再用一个模型把人脸"合成"出来？

这个思路叫 **Model-Based Coding (MBC)** ，可以追溯到 1950 年代 #Aizawa and Huang, 1995#。它在 1990 年代被写进 MPEG-4 part 2 标准，用 Facial Animation Parameters 描述人脸运动——但最终"长期未获广泛部署" #Chen B. et al., 2023#。原因很简单：当时的 synthesis model 太弱，重建出来的人脸画质太差，工程上没法用。

这篇 DCC 2024 综述 #Chen B. et al., 2023# 讲的故事，正是 MBC 在深度生成模型成熟后的"复活"。作者 Bolin Chen、Jie Chen、Shiqi Wang（香港城市大学）与 Yan Ye（Alibaba）把 2019 年以来基于 FOMM #Siarohin et al., 2019#、Face_vid2vid #Wang et al., 2021# 等深度动画模型的==生成式人脸视频编码==（Generative Face Video Coding, GFVC）方法，统一进一个 analysis-synthesis 框架，并梳理了 2023 年 JVET 把它标准化为 VVC SEI message 的完整提案链。

**一句话定位** ：这篇综述不是讲"某个新方法"，而是把 16 个 GFVC 方法抽象成同一骨架、给出统一评测协议、并把它们推进 MPEG/JVET 标准化议程——是一份地图，而非施工图。

第一章 · 问题剖析

传统 codec 与早期 MBC 的双重困境

要理解 GFVC 为什么在这个时间点被重新激活，得先看清它要替代的两条旧路各自卡在哪里。

### 传统 hybrid codec：为通用视频而生，不为人脸优化

H.264/AVC #Wiegand et al., 2003#、H.265/HEVC #Sullivan et al., 2012#、H.266/VVC #Bross et al., 2021# 走的是"预测 + 变换 + 熵编码"的 hybrid 路线，压缩对象是像素残差，优化目标是 pixel-level fidelity（PSNR/SSIM）。这套框架对通用自然视频极其成功，但综述在 §1 直指其软肋：它们"not designed with the particular statistical characteristics of face visual signal" #Chen B. et al., 2023#。也就是说，人脸视频中真正占码率的其实是==少量运动参数==（嘴型、表情、头部姿态），而 hybrid codec 仍在逐块地编码像素残差，在超低码率区会过度平滑、丢细节。

### 早期 MBC：思路对了，合成太弱

另一条路是 MBC。综述 §2.1 把它的历史链梳理得很清楚：Pearson & Robinson 1985 #Pearson and Robinson, 1985# 论极低数据率可视通信；Musmann 1989 提出对象导向的 analysis-synthesis 编码 #Musmann et al., 1989#；Aizawa、Harashima、Saito 1989 的 MBASIC 系统用参数化 3D 人脸模型做超低码率人脸编码 #Aizawa et al., 1989#；Hotter 1994 优化对象分析-合成 codec #Hotter, 1994#；Aizawa & Huang 1995 在 Proc. IEEE 上做了 MBC 的 landmark survey #Aizawa and Huang, 1995#；Lopez & Huang 1995 用 3D head model 做人脸专用压缩 #Lopez and Huang, 1995#。

这些工作在"压缩什么"上和今天的 GFVC 几乎同源——都是 encoder 用 analysis model 把人脸压成语义参数、decoder 用 synthesis model 重建。它们的瓶颈不在"压不下去"，而在"synthesis model 太弱 → 重建质量 poor → 没法落地"。综述原话："limited by the inadequate synthesis technique at that time, the overall reconstruction quality was poor" #Chen B. et al., 2023#。MPEG-4 part 2 把这套 MBC 写成了独立标准，但长期没部署起来。

### 深度生成模型补上最后一环

转机来自生成模型。VAE #Kingma and Welling, 2014#、GAN #Goodfellow et al., 2014#、Diffusion #Dhariwal and Nichol, 2021# 让高质量人脸合成成为可能，尤其是 FOMM #Siarohin et al., 2019# 这类 face reenactment / animation 模型——它们用一阶运动关键点把 driving video 的运动迁移到单张源图，正好补上了 MBC 缺失的"高质量 synthesis"那一环。于是 MBC 的 analysis-synthesis 范式在 AIGC 时代以 GFVC 之名复活，并在 2023 年被 JVET 重新推上标准化议程。

### 30 年的 survey-to-survey 接力

有意思的是，Aizawa & Huang 1995 那篇 Proc. IEEE 正是 1990 年代 MBC 的 landmark survey，而本篇综述是 2023 年的 GFVC survey——两者相隔近 30 年，叙事结构上存在明显的对标呼应：都从"very low bit-rate"应用切入，都以 analysis-synthesis 为骨架，都以标准化前景收尾。读这篇综述时，把它放在这条 30 年的接力线上，能更好地理解它的定位。

第二章 · 统一框架

GFVC 的 analysis-synthesis 骨架与 6 类 facial representation

综述的方法论第一步是"抽象"：把 FOMM、DAC、Face_vid2vid、CFTE、IFVC 等 16 个具体算法塞进同一个编解码框架。这个抽象是后面 taxonomy 和评测协议的前提。

### Encoder：key frame 走传统，inter frame 走生成

输入的人脸视频被分成两路。Key-reference frame 用传统 codec（HEVC/VVC）压成 I picture——因为它承担身份、外观、纹理信息，生成模型不擅长稳定保持这些，交给成熟的 VVC intra 编码更可靠。Inter frame 则走生成通道：用 analysis model 提取 compact facial symbols（具体形式见下方 taxonomy），经 context-adaptive arithmetic coder 进 bitstream。

GFVC general framework（图片资源未随副本复制）

图 1(a)：GFVC 通用框架。编码端 key-reference frame 走传统 VVC，inter frame 用 analysis model 提取 compact facial symbols 进 bitstream；解码端把 key-frame 与 facial information 联合送入 synthesis model 重建视频（来源：Chen et al., 2023, Fig.1）。

### Decoder：synthesis model 把参数"合成"回人脸

解码端拿到两路 bitstream 后合并：先解码 key-reference frame（VVC I 帧解码），再解析 compact facial information（算术解码得到 facial symbols），最后把 (key-reference frame, facial information) 联合送入 synthesis model（深度生成网络）重建视频 #Chen B. et al., 2023#。这里的 synthesis model 就是 FOMM / Face_vid2vid 这类深度动画生成网络。

用数学符号把这套路 form 化：设 key-reference frame 为 $I_{\mathrm{ref}}$，第 $t$ 个 inter 帧为 $I_t$，encoder 的 analysis model 为 $A(\cdot)$，decoder 的 synthesis model 为 $S(\cdot)$，则整条链路可写成：

$$
z_t = A(I_t),\qquad \hat{I}_t = S\!\left(I_{\mathrm{ref}},\, z_t\right)
$$

其中 $z_t$ 就是 compact facial representation（keypoints / landmarks / semantics / compact feature 等，随方法而变）。注意 $z_t$ 的维度远小于 $I_t$ 的像素数——这正是"超低码率"的来源；而 $S$ 不做像素级反变换，而是用生成模型的强推理能力从 $(I_{\mathrm{ref}}, z_t)$ 合成人脸。这一步决定了 ==GFVC 不优化像素保真==，所以后面的评测协议才弃用 PSNR/SSIM。

这个 ==hybrid 结构==（一半传统、一半生成）是后面标准化为何走 SEI 路线的关键依据：facial parameters 本质上是附着在 VVC bitstream 上的补充信息，天然适合封进 SEI message，而不需要另起炉灶写一个新标准。整条 pipeline 的数据流如下：

{{< mermaid >}} flowchart LR A["face video {I_t}"] --> B{"分流"} B -->|"key/ref frames"| C["传统 VVC  
I-picture 编码"] B -->|"inter frames"| D["analysis model A()"] D --> E["compact facial symbols z_t"] E --> F["context-adaptive  
arithmetic coder"] C --> G["bitstream"] F --> G G --> H["arithmetic decoder"] H --> I["synthesis model S()"] C --> I I --> J["reconstructed {Î_t}"] {{< /mermaid >}} 

### 6 类 facial representation：taxonomy 的分类维度

综述的分类维度是单一的、显式定义的：==facial representation==，即 encoder 提取出来、传输、decoder 用来重建的中间表示形式。Figure 1(b) 给出 6 种 representation 的示意，Table 1 则把 16 个方法按此归类（其中 RDAC 引入第 7 个混合类"2D Keypoints + Residual Map"）。

Facial representations（图片资源未随副本复制）

图 1(b)：6 种 facial representation——2D landmarks、2D keypoints、3D keypoints、segmentation map、facial semantics、compact feature（来源：Chen et al., 2023, Fig.1）。

方法| 时间| Facial Representation| 关键特性  
---|---|---|---  
**FOMM** #Siarohin et al., 2019#| NeurIPS 2019| 2D Keypoints| 用 2D keypoints 学复杂面部运动与仿射变换，无先验信息，是 keypoint-based GFVC 的基石  
**DAC** #Konuko et al., 2021#| ICASSP 2021| 2D Keypoints| 设计 FOMM-based 视频会议 codec，取得 promising RD 性能  
**VSBNet**|  ICMEW 2021| 2D Landmarks| 视觉敏感性网络 + 辅助帧 + 置信度图，提升人脸保真度  
**Face_vid2vid** #Wang et al., 2021#| CVPR 2021| 3D Keypoints| 无需 3D 图形模型即可自由视角神经 talking-head 合成，可做超低码率会议  
**Mob M-SPADE** #Oquab et al., 2021#| CVPRW 2021| Segmentation Map| SPADE 架构 + 分割图，首个在移动 CPU 上实时的 GFVC 系统  
**SNRVC**|  DCC 2022| Facial Semantics| 用一系列语义解耦面部运动信息，低码率下重建人脸  
**CFTE** #Chen et al., 2022#| DCC 2022| Compact Feature| 端到端推理框架，把时序演化变换为 compact feature 表示  
**C3DFD**|  DCC 2022| Facial Semantics| 用 compact 3D face descriptor 做超低码率数字人通信  
**MAX-RS**|  CVPRW 2022| 2D Keypoints| 多源帧 + 视角聚合选择做多视角神经人脸视频压缩  
**DMRGP**|  ICIP 2022| Compact Feature| 动态多参考预测，把大头部运动转为小运动  
**HDAC**|  ICIP 2022| 2D Keypoints| 分层编码方案，改善长期依赖、缓解背景遮挡  
**CVC_STR**|  BMVC 2022| 2D Keypoints| 帧插值器降码率 + patch-wise 超分提质量  
**Bi-Net**|  ICME 2022| 2D Keypoints| 码率可调混合 GFVC，像素级双预测 + 低码率 FOMM + 无损 keypoints  
**CTTR** #Chen et al., 2023c#| TCSVT 2023| Compact Feature| 时空对抗训练，改善动态轨迹学习与时序一致性  
**IFVC** #Chen et al., 2023b#| arXiv 2023| Facial Semantics| 内部维度增加机制，支持人机交互（头部平移/旋转/眨眼/嘴动）  
**RDAC**|  ICIP 2023| 2D Keypoints + Residual| 预测式编码残差信息以提升质量（唯一双表征项）  
  
从分布看，2D Keypoints 类最多（7 个方法，FOMM 为基础），Compact Feature 与 Facial Semantics 各 3 个，2D Landmarks / 3D Keypoints / Segmentation Map 各 1 个。2022 年是爆发期（8 篇），2023 年出现 RDAC 这一"keypoint + residual"的混合类，暗示纯 keypoint 路线开始向像素级保真回退。综述在 §2.1 末句明确点出三条演进轴：更 compact 的 facial representation（降码率）、更 realistic 的重建（提感知质量）、可解释的 bitstream editing（扩应用）——IFVC 让 internal dimension 可被人交互（头平移、旋转、眨眼、嘴动），把"码流"从只读变成可编辑，正是第三条轴的体现。

**Taxonomy 的隐含边界** ：这个 7 类划分在"facial representation"维度上内部自洽，但它只看表示形式，不看生成模型类型（GAN/Diffusion）、输入模态（audio-driven 在 bib 里出现但 Table 1 不收）、训练方式（端到端 vs 两阶段）。这是为可读性做的权衡，也是 SEI syntax 设计需求的直接投影——不同 representation 对应不同 syntax element，taxonomy 与标准化叙事天然对齐。

第三章 · 评测协议

如何让 16 个异质方法在同一把尺子下可比

既然是综述，最重的方法论价值之一是给一份可复用的统一评测协议，让 16 个异质算法（不同 representation、不同生成模型）在同一标尺下可比。§2.2 沿用的是 IFVC #Chen et al., 2023b# 论文里的 common test conditions——这一点要记住，因为协议本身出自作者自家工作。

### 数据集与编码配置

测试数据集选 VoxCeleb #Nagrani et al., 2017# 的 50 个 talking face 视频序列，每个 crop 成 10 秒（250 帧 @ 25fps），分辨率 256×256，色度格式 RGB 444。注意这里的 ==RGB 444 而非 YUV 420==——主流视频 codec 评测常用 YUV420，这里改 RGB 444 是因为 GFVC 的生成模型在 RGB 域训练/推理，感知指标 DISTS/LPIPS 也在 RGB 域计算。这是一个为被测对象量身定做的选择，但也意味着与 VVC 的 YUV420 结果不能直接横比（综述未明确讨论这一限制）。

编码配置上，VVC 基线用 VTM 的 Low-Delay-Bidirectional (LDB) 配置（贴合视频会议场景），QP 设 45/47/50/52；GFVC 端的 key-reference picture 用 VTM 10.0 #JVET-S2002# 编为 I picture，QP 设 37/42/47/52，inter 帧用 facial parameters 经 context-adaptive arithmetic coder 压缩。两套 QP 独立扫描，只在 47/52 重叠——这是混合 codec 评测的细节陷阱，也使得"外观质量"与"运动质量"的码率分配可分别刻画。

### 指标选择：为什么弃用 PSNR/SSIM

这是整套协议最关键的方法论判断。综述原话："Since GFVC methods do not optimize for pixel-level distortion fidelity, traditional measures like Peak Signal-to-Noise Ratio (PSNR) and Structural Similarity Index (SSIM) are not suitable to measure the quality of the reconstructed video." #Chen B. et al., 2023# 因此改用两个 feature-domain 感知指标：DISTS（Deep Image Structure and Texture Similarity）#Ding et al., 2020# 和 LPIPS（Learned Perceptual Image Patch Similarity）#Zhang et al., 2018#。

逻辑链很清晰：GFVC 不优化像素保真（analysis-synthesis，生成模型重建）→ PSNR/SSIM 度量像素/结构误差、与人类感知错位 → 改用 feature-domain 感知指标。

指标悖论：连 DISTS/LPIPS 也不够 

综述在 §4 挑战 3 里自己承认：DISTS/LPIPS 虽在 feature domain 提出，但"lack consideration of strong facial priors"——它们是通用感知指标，不针对人脸特有的 identity 保持、表情准确度、唇音同步。综述点名需要 #Li et al., 2023# 这类 face-specific 专用度量。也就是说：传统指标不能用、现有感知指标也不充分——这就是 GFVC 评测当前的方法论困境。

### 评测配置披露表

配置项| 披露状态| 值 / 说明  
---|---|---  
评测数据集| 已披露| VoxCeleb，50 个 talking face 序列  
评测指标| 已披露| DISTS ↓ / LPIPS ↓（明确弃用 PSNR/SSIM）  
Baseline 方法| 已披露| VVC / FOMM / MRAA / Face_vid2vid / CFTE / IFVC（共 6 条曲线）  
推理硬件| 未披露| 原文未给出 GPU 型号/数量  
推理分辨率| 已披露| 256×256，RGB 444，25fps，10s/250帧  
推理环境| 部分披露| VTM 10.0（VVC 参考软件）；GFVC 各方法框架未统一给出  
VVC baseline 配置| 已披露| VTM LDB，QP {45, 47, 50, 52}  
GFVC key-ref 配置| 已披露| VTM 10.0 I-picture，QP {37, 42, 47, 52}；inter 帧用 context-adaptive arithmetic coder  
RD 数值表| 未披露| 仅 Figure 4 曲线，未给 kbps / BD-rate / DISTS-LPIPS 具体值  
  
**读表提示** ：作为综述，本文不含各 GFVC 方法的训练超参、GPU、FLOPs、参数量、latency——这些需下沉到 Table 1 各原文献与 JVET 提案。评测配置表大量"未披露"是 survey 性质决定的，不算缺陷，但读者需明确这一点。

第四章 · 标准化方法学

把 GFVC 塞进 VVC bitstream：SEI 与互操作

这是综述方法论含量最高的一章——不是讲怎么压缩，而是讲==怎么把一类生成式压缩方法标准化进现有标准体系==。

### 为什么用 SEI 而非新标准

GFVC 的 hybrid 设计（key frame 走 VVC、inter 帧走 facial parameters）天然就是附着在 VVC bitstream 上的补充信息。而 SEI（Supplemental Enhancement Information）的定义正是"additional and supplemental data inserted into a coded video bitstream to enhance the use of transported video" #Chen B. et al., 2023#。所以把 facial parameters 封进 GFV SEI message 让它伴随 VVC bitstream，是最低侵入、最快落地的标准化路径——不需要新标准，只需在 VVC SEI namespace 里加一类消息。

这与 MPEG-4 part 2 当年把 MBC 写成独立 part 形成对比：MBC 当时是独立标准，落地失败；GFVC 现在选 SEI 附加，是吸取了 MBC 的教训。

### JVET 提案链：从首提到 common text

综述 §3 把标准化过程梳理成一条提案链，从 2023 年 1 月到 10 月跨 6 次 JVET 会议：

提案| 会议| 时间| 贡献  
---|---|---|---  
**JVET-AC0088** #JVET-AC0088#| 29th JVET| 2023-01| 首提 GFV SEI message：VVC 图作 base + 少量 bit 表达 facial semantics  
**JVET-AD0051** #JVET-AD0051#| 30th JVET| 2023-04| 泛化支持多种 facial representation 的 common syntax  
**JVET-AE0080 / AE0083 / AE0280** #JVET-AE0083#| 31st JVET| 2023-07| 通用 syntax + 定义 decoder↔NN 接口；AE0083 给开源模型清单 + VTM↔生成网络示例实现  
**JVET-AF0146**|  32nd JVET| 2023-10| 对 3D facial landmarks syntax 做 refinement 与 grouping  
**JVET-AF0048** #JVET-AF0048#| 32nd JVET| 2023-10| 引入 flow/parameter translator 解决非端到端编解码器互操作  
**JVET-AF0234** #JVET-AF0234#| 32nd JVET| 2023-10| 把 AF0048 合并进 AE0280 common text → 当前最新统一文本（Figure sei 出处）  
**m64987** #Ye et al., 2023#| MPEG| 2023-10| Ye 等建议推动成立新 Ad hoc Group，进入系统化调研阶段  
  
### TranslatorNN() / GeneratorNN()：互操作性的接口设计

这是标准化方法学的核心创新，解决一个工程现实问题：现实里 GFVC 的 analysis model（encoder 侧）和 synthesis model（decoder 侧）往往不是一起训练的（FOMM 系都不是 end-to-end）。当 encoder 用算法 A 的 analysis model、decoder 用算法 B 的 synthesis model 时，facial parameters 的语义/维度/分布对不上，直接喂会重建崩掉。

解决方案是在 decoder 前插一个 **TranslatorNN()** （parameter translator 或 flow translator），把 encoder 侧的 parameter/flow"翻译"成 decoder 侧 synthesis model 能吃的格式；而 **GeneratorNN()** 就是那个 synthesis model 本身。综述借 Figure 2 说明了处理流程 #JVET-AF0234#。

GFV SEI for Face Generation（图片资源未随副本复制）

图 2(a)：GFV SEI for Face Generation 的处理顺序。TranslatorNN() 在 encoder/decoder matched 时可旁路，mismatched 时启用翻译保兼容（来源：JVET-AF0234, Fig.）。

GFV SEI for Face Fusion（图片资源未随副本复制）

图 2(b)：GFV SEI for Face Fusion 路径，GeneratorNN() 作为 synthesis model 把翻译后的 facial parameters 与 key-reference 合成重建视频（来源：JVET-AF0234, Fig.）。

关键设计：TranslatorNN() 在 encoder 与 decoder ==matched==（端到端联合训练）时可旁路省算力，==mismatched== 时启用翻译保兼容。设重建质量为 $Q$，AF0048 的实验给出明确的两档对比：

$$
Q_{\mathrm{matched}} \;>\; Q_{\mathrm{mismatched\,+\,translator}},\quad \text{后者 still acceptable}
$$

即 mismatched 配合 translator 的质量虽略低于 matched，但仍可接受；若不启用 translator 则质量进一步下降（此为综述隐含的工程推断，非显式实验档位）#Chen B. et al., 2023#。形式化地，TranslatorNN $T(\cdot)$ 把 encoder 侧参数翻译到 decoder 侧 synthesis model 的语义空间：当 matched 时 $z_t$ 与 $S$ 同源，$T$ 可为单位映射（旁路）；当 mismatched 时需 $T(z_t) \neq z_t$ 做分布/维度对齐，$\hat{I}_t = S(I_{\mathrm{ref}},\, T(z_t))$。

**方法论价值** ：这其实是把"互操作性"问题从"要求全行业用同一个模型"转化为"要求各写一个适配器"——标准化史上常见的==接口与实现分离==思路。只规定 SEI syntax 这个"协议"，不规定 GeneratorNN 这个"实现"：不同厂商可各自优化自己的 GeneratorNN（竞争），但都遵守同一份 GFV SEI syntax（互通），mismatch 时靠 TranslatorNN 兜底（退化而非不可用）。

第五章 · 实验验证

RD 曲线说了什么、没说什么

综述 §2.2 在 50 个 VoxCeleb 序列上对比了 VVC、FOMM、MRAA、Face_vid2vid、CFTE、IFVC 六条曲线，分别用 Rate-DISTS 和 Rate-LPIPS 呈现。

Rate-DISTS performance（图片资源未随副本复制）

图 3(a)：Rate-DISTS 性能对比。所有生成式压缩方法显著优于 VVC，并能工作在传统 codec 难以触及的超低码率区（来源：Chen et al., 2023, Fig.4）。

Rate-LPIPS performance（图片资源未随副本复制）

图 3(b)：Rate-LPIPS 性能对比。IFVC（作者最新方法）在曲线上表现最优（来源：Chen et al., 2023, Fig.4）。

综述给出的结论是定性的：==所有生成式压缩方法显著优于最新的 VVC codec==，且它们能工作在传统 codec 难以到达的超低码率区 #Chen B. et al., 2023#。其中 IFVC（作者团队最新工作）在 DISTS/LPIPS 曲线上表现最优。

交叉验证提示 

读这组 RD 图时需要意识到一个立场信号：6 条曲线里 CFTE 和 IFVC 都是作者自家方法，且 IFVC 在曲线上表现最优——存在"自家方法自证最优"的潜在偏差。Table 1 的 16 个方法中，作者团队（Chen / Wang / Ye）bib 署名确认的至少 3 个（CFTE、CTTR、IFVC），另有 DMRGP、C3DFD 等合作署名工作；JVET 提案链（8 个 JVET 提案 + MPEG 侧 m64987）几乎全部由作者团队驱动。这不影响综述的框架价值，但 RD 数值与标准化进展叙述应交叉验证非作者团队的独立工作（如 Konuko 的 DAC/HDAC/RDAC、Volokutin 的 MAX-RS、Agarwal 的 CVC_STR）。此外，原文仅给图不给数据表，未提供具体 kbps、BD-rate 百分比、各方法在某码率点的 DISTS/LPIPS 值。

第六章 · 讨论与启发

四大挑战与可带走的工程启发

综述 §4 列了 3 个应用（超低码率通信、用户动画滤镜、元宇宙）和 4 个挑战。3 个应用的核心卖点是：key-reference 帧间隔拉大、两 key 之间每时刻只传少量 facial parameters，相对全部用 VVC 编码能显著降码率，工作在传统 codec 难以触及的超低码率区——综述原话称之为 "significantly reducing the coded bit rate compared to coding all pictures using VVC" #Chen B. et al., 2023#。

### 四大挑战

**1\. 重建质量不稳定。** 根因是深度生成模型能力限制 + GFVC 内在机制（texture 由 key-frame 提供、motion/posture 用 compact representation）。症状是背景区域出现 objectionable distortions、嘴/眼局部动作不准。综述给的对策建议很具体：**大运动时更频繁发送 key-reference pictures** #Chen B. et al., 2023#——这是值得记下的设计 hint。

**2\. 解码器复杂度高。** GFVC decoder 远重于 VVC decoder（要跑生成网络），与传统"encoder 重 decoder 轻"的广播假设相反——但对下行带宽紧张、终端算力充足的会议场景合理。已有缓解证据：Mob M-SPADE #Oquab et al., 2021# 证明经仔细简化可在移动 CPU 上实时解码，未来寄望 NN 专用硬件加速。

**3\. 缺乏合适的感知评测。** 前文"指标悖论"已展开：PSNR/SSIM 不适用 GAN 重建，DISTS/LPIPS 又缺 facial prior，需要 #Li et al., 2023# 这类 face-specific 度量。协议里也未评测时序一致性、identity 漂移、lip-sync——这些对 talking face 至关重要但逐帧算的 DISTS/LPIPS 捕捉不到。

**4\. 模型可解释性不足。** GFVC 两端都是黑箱，传统 codec 几十年积累的"可分析失真来源"能力在这里缺失。理解模型内部"为何、如何"支持 GFVC 任务，才能像传统 codec 那样逐模块调优。

### 可带走的启发

维度| 传统 hybrid (VVC)| 早期 MBC| GFVC  
---|---|---|---  
压缩对象| 像素残差| 语义参数/面部边缘| compact facial representation  
重建方式| 像素级反变换| synthesis model（poor）| 深度生成模型  
码率范围| 中高| 极低但质量差| 超低 + 高感知质量  
优化目标| pixel fidelity (PSNR/SSIM)| 早期无系统指标| feature-domain (DISTS/LPIPS)  
标准化形态| H.264/265/266 完整标准| MPEG-4 part 2（未广泛部署）| VVC SEI message（进行中）  
编解码器关系| 同标准强绑定| analysis-synthesis 同源| 多为非端到端 → 需 TranslatorNN()  
  
从这条对比线能读出几个可操作启发：第一，==压缩对象的迁移是范式级的==——从信号→参数→compact representation，MBC 走到"参数"但 synthesis 太弱，GFVC 把参数细化成更 compact 的 representation 同时 synthesis 升级为深度网络，才让"超低 + 高质量"同时成立。第二，==标准化形态的选择反映教训==——MBC 当年做成独立标准落地失败，GFVC 吸取教训选 SEI 附加、互操作靠 TranslatorNN，落地风险更低。第三，==GFVC 把复杂度从 encoder 挪到了 decoder==，这对会议场景合理，对广播场景则未必。第四，作为窄域技术，GFVC 只对人脸视频有效，非人脸内容完全失效——不能替代通用 codec。

局限层面，TranslatorNN 是工程解不是理论解，mismatched 情况下质量"acceptable"但低于 matched，意味着 SEI 标准化后的==实际部署质量上限低于学术 SOTA==——这是标准化的代价，综述坦承但未给消除路径。可复现性上，综述提供的是地图而非施工图：框架/协议/标准化路线扎实自洽，但复现某个具体方法仍缺 facial representation 精确格式、arithmetic coder 上下文模型、网络权重、码率统计口径、translator 训练细节，需下沉到 Table 1 各原文献与 JVET 提案。

结语：窄域、超低码率、生成式

这篇综述把 GFVC 定位成"窄域、超低码率、生成式"的垂直方向：它不是通用视频压缩的替代，而是在视频会议、数字人、元宇宙这些==人脸中心场景==里有不可替代的码率优势。综述本身的贡献不在提出新方法，而在四件事：把 16 个算法统一进 analysis-synthesis 框架、按 facial representation 做出 7 类 taxonomy、给出可复用评测协议、梳理出从 MPEG-4 MBC 到 JVET GFV SEI 的 30 年标准化接力。

读完最大的收获，是看清了"为什么是这个时间点"——MBC 思路 1950 年代就有，1990 年代写进标准却因 synthesis 太弱而搁置，直到深度生成模型补上最后一环才以 GFVC 复活，并在 2023 年被 JVET 以 SEI 附加（而非独立标准）的形式重新推上标准化议程。这条历史弧线本身就是 model-based coding 在 AIGC 时代的命运注脚。距离普惠落地，它还有标准成熟度、评测标准化、重建稳定性、解码复杂度几道关——但作为方向入门、标准化跟踪、窄域产品预研，这篇综述是直接入口。

### 参考来源

  * Chen, B. et al. (2023). Generative Face Video Coding Techniques and Standardization Efforts: A Review. _Data Compression Conference (DCC) 2024_. [arXiv:2311.02649](https://arxiv.org/abs/2311.02649) · [项目页](https://github.com/Berlin0610/Awesome-Generative-Face-Video-Coding)
  * Siarohin, A. et al. (2019). First Order Motion Model for Image Animation. _NeurIPS 2019_. [arXiv:2003.09063](https://arxiv.org/abs/2003.09063)
  * Wang, T.-C. et al. (2021). One-Shot Free-View Neural Talking-Head Synthesis for Video Conferencing. _CVPR 2021_. [arXiv:2011.15026](https://arxiv.org/abs/2011.15026)
  * Chen, B. et al. (2022). Beyond Keypoint Coding: Temporal Evolution Inference with Compact Feature Representation for Talking Face Video Compression (CFTE). _DCC 2022_ , pp. 13–22. [DOI:10.1109/DCC52660.2022.00009](https://doi.org/10.1109/DCC52660.2022.00009)
  * Chen, B. et al. (2023). Interactive Face Video Coding: A Generative Compression Framework (IFVC). [arXiv:2302.09919](https://arxiv.org/abs/2302.09919)
  * Chen, B. et al. (2023). Compact Temporal Trajectory Representation for Talking Face Video Compression (CTTR). _IEEE TCSVT_.
  * Konuko, G. et al. (2021). Ultra-Low Bitrate Video Conferencing Using Deep Image Animation (DAC). _ICASSP 2021_ , pp. 4210–4214. [DOI:10.1109/ICASSP39728.2021.9414731](https://doi.org/10.1109/ICASSP39728.2021.9414731)
  * Oquab, M. et al. (2021). Low Bandwidth Video-Chat Compression using Deep Generative Models (Mob M-SPADE). _CVPRW 2021_ , pp. 2388–2397.
  * Bross, B. et al. (2021). Overview of the Versatile Video Coding (VVC) Standard and its Applications. _IEEE TCSVT_ , 31(10). [arXiv:2203.10837](https://arxiv.org/abs/2203.10837)
  * Wiegand, T. et al. (2003). Overview of the H.264/AVC Video Coding Standard. _IEEE TCSVT_ , 13(7), 560–576.
  * Sullivan, G.J. et al. (2012). Overview of the High Efficiency Video Coding (HEVC) Standard. _IEEE TCSVT_ , 22(12), 1649–1668.
  * Aizawa, K. & Huang, T.S. (1995). Model-based image coding: advanced video coding techniques for very low bit-rate applications. _Proc. IEEE_ , 83(2), 259–271. [DOI:10.1109/5.364463](https://doi.org/10.1109/5.364463)
  * Aizawa, K., Harashima, H. & Saito, T. (1989). Model-based analysis synthesis image coding (MBASIC) system for a person's face. _Signal Processing: Image Communication_ , 1(2), 139–152.
  * Musmann, H.G. et al. (1989). Object-oriented analysis-synthesis coding of moving images. _Signal Processing: Image Communication_ , 1(2), 117–138.
  * Hotter, M. (1994). Optimization and efficiency of an object-oriented analysis-synthesis coder. _IEEE TCSVT_ , 4(2), 181–194. [DOI:10.1109/76.285624](https://doi.org/10.1109/76.285624)
  * Pearson, D.E. & Robinson, J.A. (1985). Visual communication at very low data rates. _Proc. IEEE_ , 73(4), 795–812.
  * Lopez, R. & Huang, T.S. (1995). Head pose computation for very low bit-rate video coding. _CAIP 1995_.
  * Kingma, D.P. & Welling, M. (2014). Auto-Encoding Variational Bayes. _ICLR 2014_. [arXiv:1312.6114](https://arxiv.org/abs/1312.6114)
  * Goodfellow, I. et al. (2014). Generative Adversarial Nets. _NeurIPS 2014_.
  * Dhariwal, P. & Nichol, A. (2021). Diffusion Models Beat GANs on Image Synthesis. _NeurIPS 2021_.
  * Ding, K. et al. (2020). Image Quality Assessment: Unifying Structure and Texture Similarity (DISTS). _IEEE TPAMI_.
  * Zhang, R. et al. (2018). The Unreasonable Effectiveness of Deep Features as a Perceptual Metric (LPIPS). _CVPR 2018_.
  * Nagrani, A., Chung, J.S. & Zisserman, A. (2017). VoxCeleb: a large-scale speaker identification dataset. _INTERSPEECH 2017_.
  * Li, Y. et al. (2023). Perceptual Quality Assessment of Face Video Compression: A Benchmark and An Effective Method. [arXiv:2304.07056](https://arxiv.org/abs/2304.07056)
  * Chen, J. et al. (2020). Algorithm description for Versatile Video Coding and Test Model 10 (VTM 10). _JVET doc. JVET-S2002_.
  * Chen, B. et al. (2023). AHG9: Generative Face Video SEI Message. _JVET doc. JVET-AC0088_ , 2023-01.
  * Chen, B. et al. (2023). AHG9: Common SEI Message of Generative Face Video. _JVET doc. JVET-AD0051_ , 2023-04.
  * Chen, B. et al. (2023). AHG9: Common SEI Message of Generative Face Video. _JVET doc. JVET-AE0083_ , 2023-07.
  * Chen, B. et al. (2023). A Study on Decoder Interoperability of Generative Face Video Compression. _JVET doc. JVET-AF0048_ , 2023-10.
  * Chen, B. et al. (2023). AHG9: Common Text for Generative Face Video SEI Message. _JVET doc. JVET-AF0234_ , 2023-10.
  * Ye, Y. et al. (2023). On VVC-assisted ultra-low rate generative face video coding. _MPEG doc. m64987_ , 2023-10.

[←上一篇图像压缩论文精读（十六）：AEIC](aeic-shallow-encoder-ultra-low-bitrate-2024.html) [枢纽页图像压缩系列总览](image-compression-hub.html)

下一篇暂缺
