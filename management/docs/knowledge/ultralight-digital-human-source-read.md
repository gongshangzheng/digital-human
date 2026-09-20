---
title: "数字人工程解读（六）：Ultralight-Digital-Human：一个能塞进手机的数字人"
description: "逐文件拆解首个开源超轻量数字人：6 通道 masked 重建、MobileNet 风格 UNet、双音频编码器、L1+VGG 损失，以及最硬核的 wenet 流式推理工程。"
date: 2026-06-05T12:59:20
created_at: 2026-06-05T12:59:20
updated_at: 2026-07-08T11:33:03
tags: ["数字人", "源码解读", "唇形同步", "UNet", "MobileNet", "流式推理", "ONNX", "Ultralight-Digital-Human"]
aliases: ["categories/AI/数字人/数字人工程解读"]
sub_id: 60
hero_title: "Ultralight-Digital-Human 源码解读"
mathjax: true
---

> 来源：博客 gongshangzheng.github.io `src/pages/ultralight-digital-human-source-read.html`，html2text 转换复制于 2026-09-20。原文：https://gongshangzheng.github.io/ultralight-digital-human-source-read.html

~3000行 Python

<1M音频+UNet 体积

2音频编码器

2.5k+GitHub Star

系列位置

序章：从产业图谱回到一行行代码

上一篇[产业图谱](voice-ai-digital-human-landscape.html)把视角拉到了整条产业链的高空，看的是「这门生意长什么样」。这一篇我们重新落地，钻进一个具体的开源仓库，看「最小可用的数字人到底是怎么写出来的」。 主角是 [anliyuan/Ultralight-Digital-Human](https://github.com/anliyuan/Ultralight-Digital-Human)，作者自称**第一个开源的、如此轻量级的数字人模型** ，目标是**能在移动设备上实时运行** 。#ULDH-repo# 它的代码总量只有约 3000 行 Python，模型小到「音频编码器 + UNet 两个模型加起来体积可以压到 1M 以内」，却能跑出像样的口型同步效果，还被 [LiveTalking](https://livetalking-doc.readthedocs.io/) 这样的实时数字人框架收作内置模型之一。#LiveTalking# 对于想理解「数字人最小内核」的人来说，它几乎是最好的入门读物——足够小，能一口气读完；又足够完整，从预处理、训练到离线/流式推理一条龙都有。 

**这篇文章读什么** ：我会按「**预处理 → 模型 → 训练 → 离线推理 → 流式推理** 」的真实数据流，逐个文件拆解它的设计。每个技术判断都对应到具体文件和函数，不靠脑补。重点讲清楚三件事：它为什么这么小、口型是怎么被音频驱动出来的、以及移动端实时这件事在工程上是怎么抠出来的。

图 1：项目 README 中的效果 demo（来源：项目 README，演示视频为康辉老师口播片段）。

Overview

项目概览：它是什么，不是什么

在读代码前，先把定位钉死，避免误读。 

维度| 事实  
---|---  
一句话定位| 音频驱动的、per-person（一人一模型）的超轻量唇形同步数字人  
路线归属| 属于 [Wav2Lip](paper-wav2lip.html) 一脉的「**遮嘴重建** 」路线：把嘴部涂黑，让网络根据音频 + 身份把嘴补回来  
训练范式| 个性化：每个人录一段 3~5 分钟视频，训一个专属模型，不是通用大模型  
音频编码器| 两套可选：**HuBERT** （效果更好，25fps）和 **wenet** （更快、可移动端实时，20fps）  
许可证| README badge 标注 Apache-2.0（仓库未单独提供 LICENSE 文件，商用请向作者确认）  
不是什么| 不是「一张照片直接生成」的零样本方案，也不是全身/整帧生成；它只重绘人脸下半部分  
  
理解这个项目的一把钥匙 

它的「轻」不是某一处优化，而是**三个减法叠加** ：只重绘人脸下半部分（不是整张脸/整帧）、用 MobileNet 风格的深度可分离卷积（不是普通卷积）、一人一模型（不需要泛化到所有人）。理解了这三个减法，就理解了它能塞进手机的根本原因。

Architecture

仓库地图与模块依赖

仓库是扁平结构，核心文件不多。按职责分四组：**预处理** （data_utils/）、**模型** （unet.py）、**训练** （train.py + datasetsss.py）、**推理** （inference.py 离线 / dihuman_run.py 流式）。把它们零散动作统一起来的，是一个共用工具模块 `face_utils.py`。 {{< mermaid >}} flowchart TD V["输入视频 3~5min"] --> P["data_utils/process.py  
一键预处理"] P -->|ffmpeg 抽音频16k| WAV["aud.wav"] P -->|ffmpeg 抽帧| IMG["full_body_img/*.jpg"] P -->|检测关键点| GL["get_landmark.py  
SCRFD + PFLD"] GL --> LMS["landmarks/*.lms"] WAV --> AF["hubert.py / wenet_infer.py  
音频特征"] AF --> NPY["aud_hu.npy / aud_wenet.npy"] IMG --> DS["datasetsss.py  
MyDataset"] LMS --> DS NPY --> DS DS --> TR["train.py  
Model + L1 + VGG感知损失"] TR --> CKPT["checkpoint *.pth"] CKPT --> INF["inference.py  
离线逐帧合成"] CKPT --> O2O["pth2onnx.py"] O2O --> ONNX["unet.onnx"] ONNX --> STR["dihuman_run.py  
wenet 流式推理"] FU["face_utils.py  
裁脸/遮嘴/音频窗口 共用工具"] -.-> DS FU -.-> INF UN["unet.py  
轻量 UNet 模型"] -.-> TR UN -.-> INF UN -.-> O2O {{< /mermaid >}} 

_图 2：仓库模块依赖与数据流。实线是数据流向，虚线是被依赖的核心代码。注意`face_utils.py` 被数据集、离线推理共用——这是作者把「裁脸口径」统一到一处的关键。_

**一个值得学的工程习惯** ：裁脸 bbox 怎么算、嘴部矩形涂多大、音频窗口取几帧——这些「几何约定」如果散落在各文件，训练和推理稍有不一致就会导致口型对不上。作者把它们全部收进 `face_utils.py` 的常量和函数里（`FACE_CROP_SIZE`、`MASK_RECT`、`AUDIO_HALF_WINDOW`…），保证训练/推理同一口径。这是小项目里难得的纪律。

Stage 1 · Preprocess

预处理链：把一段视频变成训练素材

一切从 `data_utils/process.py` 的一行命令开始：`python process.py YOUR_VIDEO --asr hubert`。它串起四个步骤。 

### 四步流水线

步骤| 函数| 做什么  
---|---|---  
1\. 抽音频| `extract_audio`| ffmpeg 把视频音轨抽成 16kHz 单声道 `aud.wav`  
2\. 抽帧| `extract_images`| 逐帧存成 `full_body_img/{i}.jpg`；并**强制校验帧率** （hubert=25，wenet=20）  
3\. 关键点| `get_landmark`| 对每帧检测人脸关键点，存成 `landmarks/{i}.lms`  
4\. 音频特征| `get_audio_feature`| 调 `hubert.py` 或 `wenet_infer.py` 把 wav 转成特征 npy  
  
这里有个容易被忽视的硬约束：**帧率必须严格匹配音频编码器** 。`_check_fps` 里如果发现视频 fps 不等于要求值会直接抛错。原因在后面会讲清楚——音频特征和视频帧要在时间轴上一一对齐，帧率错了就全错。 

### 两级人脸链：SCRFD + PFLD

关键点检测（`get_landmark.py`）是一个两级流程，也是轻量化思路的体现： 
    
    
    # get_landmark.py（精简）
    # 第一级：SCRFD 检测人脸框 + 5 个关键点
    self.det_net = SCRFD('./scrfd_2.5g_kps.onnx', confThreshold=0.1, nmsThreshold=0.5)
    # 第二级：PFLD_GhostOne 在裁出的人脸上回归密集关键点
    self.pfld_backbone = PFLD_GhostOne()  # 轻量关键点网络
    ...
    landmarks = self.pfld_backbone(input)        # 预测偏移
    pre_landmark = landmarks[0] + self.mean_face # 叠加平均脸 → 绝对坐标
    

先用 **SCRFD** （一个轻量人脸检测器，2.5G FLOPs 量级）框出人脸，再用 **PFLD-GhostOne** （GhostNet 风格的超轻量关键点网络）回归关键点。值得注意的是 PFLD 输出的是**相对平均脸（mean face）的偏移量** ，加上 `mean_face.txt` 才得到真实坐标——这是 PFLD 系列的经典做法，让网络只学「这张脸和平均脸差多少」，比直接回归绝对坐标更稳。#PFLD# 

### 音频特征：HuBERT 怎么对齐到帧

以 HuBERT 为例（`hubert.py`），它加载 `facebook/hubert-large-ls960-ft`，把 16kHz 波形编码成 `[T, 1024]` 的隐藏状态。关键在最后一步对齐： 
    
    
    # hubert.py：把 T 维补成偶数后 reshape 成每帧 2×1024
    hubert_hidden = make_even_first_dim(hubert_hidden).reshape(-1, 2, 1024)
    

HuBERT 的 CNN 下采样让每秒约产生 50 个特征向量，而视频是 25fps，所以**每个视频帧正好对应 2 个 HuBERT 向量** （50/25=2），reshape 成 `[帧数, 2, 1024]` 就让音频和视频帧对齐了。这就是为什么 hubert 模式要求视频必须是 25fps——它是被音频特征的产出速率反向约束的。 

Stage 2 · Model

模型结构：一个会「听声补嘴」的轻量 UNet

`unet.py` 是整个项目的心脏。它本质是一个 **条件图像修复（inpainting）网络** ：输入一张嘴部被涂黑的脸，外加音频条件，输出把嘴补全后的脸。 

### 输入输出契约

张量| 形状| 含义  
---|---|---  
图像输入 `x`| `[B, 6, 160, 160]`| 6 通道 = 参考帧(3 BGR) + 涂黑嘴部的当前帧(3 BGR)  
音频输入 `audio_feat`| wenet `[B,128,16,32]` / hubert `[B,16,32,32]`| 当前帧的音频特征窗口  
输出| `[B, 3, 160, 160]`| sigmoid 归一化的人脸下半部分  
  
为什么图像输入要 6 通道？这是遮嘴重建路线的精髓：**涂黑的当前帧** 告诉网络「脸的姿态、表情、背景长这样，但嘴没了」，**参考帧** 提供「这个人的牙齿、嘴唇质感长这样」的身份信息。网络的任务就是结合两者 + 音频，把嘴画回去。 

### 轻量化的核心：InvertedResidual

整个 UNet 没有一个普通的 3×3 卷积，全部换成了 MobileNetV2 的 **Inverted Residual** 块——先 1×1 升维、再做 depthwise 3×3、最后 1×1 降维。这是它能这么小的根本： 
    
    
    # unet.py：InvertedResidual 的核心三段
    self.conv = nn.Sequential(
        nn.Conv2d(inp, hidden_dim, 1, 1, 0, bias=False),          # 1x1 升维
        nn.BatchNorm2d(hidden_dim), nn.ReLU(inplace=True),
        nn.Conv2d(hidden_dim, hidden_dim, 3, stride, 1,
                  groups=hidden_dim, bias=False),                 # depthwise 3x3
        nn.BatchNorm2d(hidden_dim), nn.ReLU(inplace=True),
        nn.Conv2d(hidden_dim, oup, 1, 1, 0, bias=False),          # 1x1 降维
        nn.BatchNorm2d(oup),
    )
    

主干通道是 `[32, 64, 128, 256, 512]`，代码注释还贴心地告诉你：想跑在更弱的设备上，把通道改成 `[16,32,64,128,256]`、并同步改音频分支即可。这种「留好压缩旋钮」的设计对移动端落地很友好。 

### 音画如何融合：在 bottleneck 处 concat

音频特征不是随便拼进去的，而是先经过专门的 `AudioConvWenet` / `AudioConvHubert` 分支卷积到和图像 bottleneck 相同的 512 维，然后在 UNet **最深处** 拼接、融合： 
    
    
    # unet.py：Model.forward 的融合三行
    x5 = self.down4(x4)                          # 图像编码到 bottleneck: 512 维
    audio_feat = self.audio_model(audio_feat)    # 音频也编码到 512 维
    x5 = torch.cat([x5, audio_feat], dim=1)      # 拼成 1024 维
    x5 = self.fuse_conv(x5)                       # 融合并压回 256 维
    

{{< mermaid >}} flowchart LR subgraph 图像编码 I["6ch 160x160"] --> D1["down x4"] --> B["bottleneck 512"] end subgraph 音频编码 A["audio_feat"] --> AC["AudioConv*"] --> AB["512"] end B --> C["concat → 1024"] AB --> C C --> F["fuse_conv → 256"] F --> U["up x4 + skip"] U --> O["sigmoid → 3ch 160x160"] {{< /mermaid >}} 

_图 3：音画融合发生在 UNet 最深的 bottleneck。这样做的好处是：浅层 skip connection 保留高频细节（牙齿、嘴唇边缘），而音频只在语义最浓缩的地方注入「该张多大嘴」的控制信号。_

Stage 3 · Train

训练设计：用「遮嘴重建」自监督

训练（`train.py` \+ `datasetsss.py`）最巧妙的地方是**不需要任何人工标注** ——目标就是原视频帧本身。 

### 样本是怎么造出来的

`MyDataset.__getitem__` 每次造一条样本： 
    
    
    # datasetsss.py（精简）
    target_T, masked_T = self._build_target_and_masked(idx)  # 当前帧：原图 + 涂黑嘴
    ref_T = self._build_reference(idx)                        # 随机另一帧作为身份参考
    img_concat_T = torch.cat([ref_T, masked_T], dim=0)       # 6 通道输入
    audio_feat = gather_audio_window(self.audio_feats, idx)  # 当前帧前后各 4 帧音频
    

注意 **reference 是随机取的另一帧** （不是当前帧），这样网络才能学会「从一张不同表情的脸里提取身份，而不是直接抄当前帧的嘴」。监督信号 target 就是当前帧没被涂黑的原始下半脸——这是一个干净的自监督重建任务。 

### 损失函数：L1 + 一点点感知损失
    
    
    # train.py
    loss_pixel = pixel_criterion(preds, labels)          # L1
    loss_perceptual = perceptual_loss(preds, labels)     # VGG19 conv3_3 上的 MSE
    return loss_pixel + 0.01 * loss_perceptual
    

像素级 **L1 损失** 保证整体颜色/结构对，权重 0.01 的 **VGG19 感知损失** （在 conv3_3 特征上算 MSE）负责让牙齿、嘴唇的纹理更自然、不糊。VGG 只作特征提取器、全程 `requires_grad_(False)`。 

关于 SyncNet 的取舍 

Wav2Lip 那一脉通常会加一个 **SyncNet 同步判别损失** 来强化口型与音频的对齐。但本项目作者在 README 和最近一次重构里明确说明：他做了大量 SyncNet 实验，发现在这个 pipeline 里对最终观感和口型同步的提升非常有限，因此**已彻底移除全部 SyncNet 相关代码** 。#ULDH-repo# 这是一个「实测驱动的减法」——读代码时确实在 train.py 里找不到任何 SyncNet 痕迹，与 README 说法一致。

Stage 4 · Inference

离线推理：逐帧合成一段视频

`inference.py` 把训练好的模型应用到一段新音频上，逐帧吐出视频。它的主循环按音频特征的帧数走，每帧做四件事：挑一张素材帧 → 构造 6 通道输入 → UNet 预测 → 贴回原图。 {{< mermaid >}} sequenceDiagram participant M as 主循环(按音频帧) participant P as _FramePicker participant N as UNet participant B as _paste_back loop 每一帧音频 M->>P: next() 取素材帧索引 P-->>M: 来回播放的帧 idx M->>M: 读图+关键点, 构造6通道输入 M->>N: net(img_concat, audio_window) N-->>M: 预测的人脸下半部 inner M->>B: 贴回 crop → resize → 覆写原图 B-->>M: 合成帧 M->>M: writer.write(frame) end {{< /mermaid >}} 

_图 4：离线推理主调用链。音频帧数决定视频长度，素材帧由 FramePicker 来回循环提供。_

### 两个值得点名的工程细节

#### 来回播放避免「跳帧穿帮」

音频可能很长，但素材视频只有几分钟。如果素材播完从头循环，会在接缝处出现明显跳变。作者用 `_FramePicker` 让帧索引按 `0,1,…,N-1,N-2,…,1,0,1,…` 来回弹（pingpong），首尾自然衔接，看起来就像人在自然地小幅摆动。 

#### 诚实的代码注释：推理与训练的 mismatch

训练时 reference 是随机另一帧，但推理时（`_prepare_unet_input`）reference 直接用了当前帧自己。代码注释毫不掩饰地写道：「 _推理时 reference 用当前帧自己（与训练存在轻微 mismatch，但作者原始设计如此）_ 」。这种把已知瑕疵写进注释的诚实，比假装完美更值得信任——它提示二次开发者：这是一个可以改进的点。 

Stage 5 · Streaming

流式推理：移动端实时的工程硬功夫

`dihuman_run.py` 是整个仓库工程难度最高、也最有参考价值的文件。离线推理可以「等音频全部就绪再慢慢算」，但实时对话要求**音频边来边出画面** 。这一版只用 wenet（因为它够快），并且全程跑 ONNX。 

### 核心难题：流式下怎么攒音频、怎么对齐

它定义了一组写死的协议参数，每一个都对应一个现实约束： 

参数| 值| 含义  
---|---|---  
`FRAME_LEN`| 160| 10ms@16k 的一帧 PCM  
`WENET_TRIGGER_LEN`| 11040| 攒够 690ms 音频才做一次 encoder  
`WENET_CHUNK_DROP`| 800| 每次 encoder 后丢弃 50ms（滑窗前进）  
`UNET_FEAT_WINDOW`| 8| UNet 需要攒够 8 帧音频特征才出口型  
`SILENCE_THRESHOLD`| 100| 连续 100 帧空音频 → 切静音模式  
`PLAY_PRE_PAD`| 13440| 播放队列前置静音，补偿处理延迟做音视频对齐  
  
### 状态机：说话 / 静音两种模式

`DiHumanProcessor.process` 本质是一个状态机。每来一帧 10ms 音频就判断一次： {{< mermaid >}} stateDiagram-v2 [*] --> 静音 静音 --> 说话: 检测到非空音频 说话 --> 说话: 攒够690ms→encoder→攒够8帧→UNet出口型 说话 --> 静音: 连续100帧空音频 静音 --> 静音: 每5帧吐1张素材帧(idle) {{< /mermaid >}} 

_图 5：流式推理状态机。静音时不跑模型、只循环播素材帧（省电省算力）；说话时才真正驱动 encoder 和 UNet。_

### wenet 流式 encoder 的 cache 三件套

流式语音编码不能每次都从头算，否则延迟爆炸。wenet 的 chunk 流式推理靠三个 cache 在帧间传递历史： 
    
    
    # dihuman_run.py：wenet encoder 的流式状态
    self.offset = np.ones((1,), dtype=np.int64) * 100
    self.att_cache = np.zeros([3, 8, 16, 128], dtype=np.float32)   # 注意力 KV cache
    self.cnn_cache = np.zeros([3, 1, 512, 14], dtype=np.float32)   # 卷积 cache
    

每次 encoder 推理都把上一次的 `att_cache` / `cnn_cache` 喂进去、再更新出来，这样只算新来的 chunk 就能拿到等价于「看了全部历史」的特征。这是流式 ASR/语音编码的标准范式，作者直接复用到了数字人上。 

**README 里那条「前 20 秒不说话」的玄机** ：作者在 README 里反复强调，录训练视频时**前 20 秒不要说话、可以做点小动作** 。读完流式代码就懂了——这 20 秒静默素材正是静音模式下 `_next_idle_img` 循环播放的「待机帧」。没有它，数字人在没人说话时就会僵住或乱动。文档约定和代码实现在这里完美咬合。

### 从 .pth 到 .onnx

流式版跑的是 ONNX，所以需要先用 `pth2onnx.py` 把训练好的 UNet 导出。它不只是导出，还用 `np.testing.assert_allclose` 对比 PyTorch 和 ONNXRuntime 的输出（`rtol=1e-03`），确保转换没有引入数值偏差才算通过——这是一个负责任的导出脚本该有的样子。 

Review

工程评价：优点、局限与复现风险

### 优点

  * **真的小、真的快** ：遮嘴重建 + 深度可分离卷积 + 一人一模型三重减法，作者称在 2080 这样的卡上多并发时「每帧音频+视频处理耗时 10ms 以内」（需转 ONNX）。#ULDH-repo#
  * **代码克制、口径统一** ：核心几何约定收进 `face_utils.py`，训练/推理一致，二次开发不容易踩坑。
  * **文档与代码咬合** ：README 的使用约定（帧率、20 秒静默）都能在代码里找到对应实现。
  * **诚实** ：对推理/训练 mismatch、SyncNet 取舍都在注释/README 里如实说明。

### 局限

  * **per-person** ：每换一个人就要重新录视频、重新训练，不能即插即用（作者透露正在做非个性化版本，尚未开源）。
  * **只重绘下半脸** ：眼神、眉毛、头部姿态不被音频驱动，表现力有上限。
  * **对录制质量敏感** ：README 明确警告噪声/回音/人声不清会显著拉低效果。
  * **流式代码偏 demo** ：作者说明流式部分只提供思路、未做深度优化，且参数多为写死，落地需要重构。

### 复现风险

  * 依赖 `facebook/hubert-large-ls960-ft`（需联网下载）和 wenet 的 `encoder.onnx`（需从作者给的网盘单独下载）。
  * 帧率必须严格匹配（hubert=25/wenet=20），否则预处理直接报错。
  * 流式版需要先 `pth2onnx.py` 导出，且 wenet encoder 的 cache 形状与具体 encoder 模型强绑定。

Takeaways

可迁移经验与系列衔接

抛开这个具体项目，有几条设计经验可以带走： 

三条可复用的设计模式 

**1\. 把「约定」集中到一处。** 任何「训练和推理必须一致」的口径（裁切、归一化、窗口大小），都应该收进一个共用模块用常量表达，而不是散落复制。`face_utils.py` 是范本。

**2\. 用「遮挡重建」做自监督。** 想让网络学会「根据条件 X 补全被遮的区域 Y」，遮嘴重建这套范式可以迁移到很多图像编辑任务，且完全不需要标注。

**3\. 流式 = 离线逻辑 + 缓存 + 状态机。** 把一个离线算法改成流式，核心就是：定义触发长度（攒多少才算一次）、用 cache 传递历史、用状态机区分忙/闲。`dihuman_run.py` 把这三件事演示得很清楚。

回到系列：从序章 Survey 的技术地图，到中间几篇的算法路线，再到 [CyberVerse](cyberverse-realtime-digital-human-agent.html) 的系统拼装和上一篇的[产业图谱](voice-ai-digital-human-landscape.html)，我们一直在不同尺度上看数字人。这一篇把放大镜调到最细，落到一个能一口气读完的真实仓库——你会发现，所谓「能塞进手机的数字人」，拆开看不过是**几个想清楚了的减法 + 一些抠到毫秒的工程纪律** 。这也是整个系列想传达的核心：数字人不是魔法，是一层层可拆解的工程。 

[←上一篇 · 第七章实时语音 AI 与数字人产业图谱](voice-ai-digital-human-landscape.html) [系列目录数字人系列 Hub](digital-human-hub.html) [本文 · 第八章Ultralight 源码解读](digital-human-hub.html)

### 参考来源

  * anliyuan. Ultralight-Digital-Human（源码、README、commit 历史）. [github.com/anliyuan/Ultralight-Digital-Human](https://github.com/anliyuan/Ultralight-Digital-Human)
  * LiveTalking 文档（将 Ultralight-Digital-Human 列为内置数字人模型之一）. [livetalking-doc.readthedocs.io](https://livetalking-doc.readthedocs.io/zh-cn/latest/usage.html)
  * Guo et al. PFLD: A Practical Facial Landmark Detector. [arXiv:1902.10859](https://arxiv.org/abs/1902.10859)
  * Prajwal et al. A Lip Sync Expert Is All You Need (Wav2Lip). [arXiv:2008.10010](https://arxiv.org/abs/2008.10010)
  * Hsu et al. HuBERT: Self-Supervised Speech Representation Learning. [arXiv:2106.07447](https://arxiv.org/abs/2106.07447)
  * Yao et al. WeNet: Production-oriented Streaming and Non-streaming End-to-End Speech Recognition. [arXiv:2102.01547](https://arxiv.org/abs/2102.01547)
