---
title: "数字人工程解读（八）：LiteAvatar 源码：纯 CPU 实时 2D 数字人驱动引擎"
description: "深度解析 HumanAIGC/lite-avatar 仓库：一个可在纯 CPU 上实现 30fps 实时推理的 2D 数字人 audio2face 库，涵盖 Paraformer 特征提取、ONNX 口型预测与轻量级面部生成器的完整调用链。"
date: 2026-06-16T14:55:00
created_at: 2026-06-16T14:55:00
updated_at: 2026-06-16T14:55:00
tags: ["lite-avatar", "audio2face", "cpu-inference", "onnxruntime", "digital-human", "paraformer", "源码解读"]
aliases: ["categories/AI/数字人/数字人工程解读"]
sub_id: 80
---

> 来源：博客 gongshangzheng.github.io `src/pages/lite-avatar-source-code-analysis.html`，html2text 转换复制于 2026-09-20。原文：https://gongshangzheng.github.io/lite-avatar-source-code-analysis.html

第一章

项目定位与核心能力

**LiteAvatar** 是由 HumanAIGC 开源的轻量级 2D 数字人驱动库，专为**纯 CPU 环境** 设计，无需 GPU 加速即可实现 30fps 实时推理。它被广泛集成于 [OpenAvatarChat](https://github.com/HumanAIGC-Engineering/OpenAvatarChat) 等交互式数字人系统中，作为默认的轻量级 Avatar 后端。

**核心价值：** 在消费级笔记本或边缘设备上，仅靠 CPU 即可驱动逼真的口型同步与面部动画，极大降低了数字人应用的部署门槛。 

### 技术栈概览

模块| 技术选型| 作用  
---|---|---  
音频特征提取| Paraformer (FunASR)| 将原始音频转换为语义/声学特征序列  
口型参数预测| ONNX Runtime + model_1.onnx| 根据音频特征预测 32 维面部参数  
面部图像生成| PyTorch JIT (net_encode/net_decode)| 将参数渲染为嘴部区域图像  
视频合成| FFmpeg + OpenCV| 帧拼接、音视频对齐、掩码融合  
  
第二章

系统架构与主调用链

LiteAvatar 的推理流程是一个典型的**三阶段 Pipeline** ：音频 → 特征 → 参数 → 图像。整个流程在 `lite_avatar.py` 的 `liteAvatar` 类中编排，核心推理逻辑封装在 `audio2mouth_cpu.py` 的 `Audio2Mouth` 类中。

{{< mermaid >}} sequenceDiagram participant User as 用户/调用方 participant LA as liteAvatar participant A2M as Audio2Mouth participant PF as Paraformer participant ONNX as ONNX Model participant GEN as Face Generator User->>LA: handle(audio_file, result_dir) LA->>LA: read_wav_to_bytes() LA->>A2M: inference(input_audio) A2M->>PF: extract_para_feature() PF-->>A2M: au_data (声学特征) A2M->>ONNX: run(input_au, input_ph) ONNX-->>A2M: output (32维参数序列) A2M->>A2M: mouth_smooth() A2M-->>LA: param_res LA->>LA: make_silence() / interp_param() loop 每帧并行渲染 LA->>GEN: param2img(param, bg_frame_id) GEN-->>LA: mouth_img LA->>LA: merge_mouth_to_bg() end LA->>User: test_demo.mp4 {{< /mermaid >}} 

### 关键入口文件

  * `lite_avatar.py`：主控类，负责模型加载、数据预处理、多线程渲染调度与视频合成。
  * `audio2mouth_cpu.py`：核心推理模块，封装 ONNX 会话与滑动窗口参数生成逻辑。
  * `extract_paraformer_feature.py`：Paraformer 特征提取器，将原始波形转为模型输入特征。
  * `download_model.sh`：从 ModelScope 下载 `lm.pb`、`model.pb` 和 `model_1.onnx` 三个权重文件。

第三章

核心源码深读

### 3.1 Audio2Mouth：滑动窗口推理与平滑

`Audio2Mouth.inference()` 是整个系统的“大脑”。它采用**1秒滑动窗口** 策略处理长音频，避免显存/内存溢出，同时通过重叠区域加权融合保证时序连续性。
    
    
    # audio2mouth_cpu.py - Audio2Mouth.inference() 核心片段
    interval = 1.0  # 每次处理1秒音频
    frag = int(interval * 30 / 5 + 0.5)  # 重叠帧数（约6帧）
    
    while True:
        # 截取当前窗口的音频特征
        input_au = au_data[start_frame:end_frame]
        input_ph = ph_data[start_frame:end_frame]
        
        # ONNX 推理：输出32维面部参数
        output, feat = self.audio2mouth_model.run(
            ['output', 'feat'],
            {'input_au': input_au, 'input_ph': input_ph, 
             'input_sp': self.sp, 'w': self.w}
        )
        
        # 重叠区域线性插值融合，消除拼接痕迹
        if frame_id < len(param_res):
            scale = min((len(param_res) - frame_id) / frag, 1.0)
            value = (1 - scale) * new_value + scale * old_value
            param_res[frame_id][key] = round(value, 3)
    

工程亮点 

滑动窗口的 `frag` 设计是关键：既保证了上下文连续性，又避免了全局推理的高延迟。最终还通过 `butter_lowpass_filtfilt` 四阶巴特沃斯低通滤波对参数序列做后处理，消除高频抖动，使口型运动更自然。

### 3.2 liteAvatar：多线程渲染与静音处理

`liteAvatar.handle()` 是离线生成的入口。它将参数序列分发到多个工作线程（`face_gen_loop`），每个线程独立调用 `param2img()` 生成嘴部图像，再通过 `merge_mouth_to_bg()` 与背景帧融合。
    
    
    # lite_avatar.py - 静音检测与参数抑制
    sil_scale = np.zeros(len(param_res))
    sound = AudioSegment.from_raw(...)
    start_end_list = detect_silence(sound, 500, -50)  # 检测静音段
    
    # 静音段内将参数向 neutral_pose 插值回归
    for ii in range(len(param_res)):
        for key in param_res[ii]:
            neu_value = bg_param[int(key)]
            param_res[ii][key] = (
                param_res[ii][key] * (1 - sil_scale[ii]) + 
                neu_value * sil_scale[ii]
            )
    

这一机制确保了说话人在停顿时嘴巴自然闭合，而非保持上一个发音的口型，显著提升了视觉真实感。

### 3.3 面部生成器：Encoder-Decoder 架构

面部生成由两个 TorchScript 模型组成：`net_encode.pt` 和 `net_decode.pt`。Encoder 将参考帧编码为隐向量，Decoder 接收隐向量 + 32维参数，输出嘴部区域图像。这种解耦设计使得同一套参数可以适配不同风格的 Avatar。

![](media/images/lite-avatar-source-code-analysis/paraformer_struct.webp)

Paraformer ASR 模型结构图（来源：LiteAvatar 仓库 weights 目录）

第四章

如何使用 LiteAvatar

### 4.1 环境安装
    
    
    # 推荐 Python 3.10 + CUDA 11.8（CPU 推理可不装 CUDA）
    pip install -r requirements.txt

核心依赖包括 `onnxruntime`（推理引擎）、`funasr`（ASR 特征）、`torch`（面部生成）、`opencv-python` 和 `ffmpeg`（视频处理）。

### 4.2 模型下载
    
    
    # Linux / macOS
    bash download_model.sh
    
    # Windows
    download_model.bat

脚本会从 ModelScope 下载三个文件并放置到 `./weights/` 目录：

文件| 用途| 目标路径  
---|---|---  
`lm.pb`| Paraformer 语言模型| `weights/speech_paraformer-.../lm/`  
`model.pb`| Paraformer 声学模型| `weights/speech_paraformer-.../`  
`model_1.onnx`| Audio2Mouth 口型预测模型| `weights/`  
  
### 4.3 离线推理命令
    
    
    python lite_avatar.py \
      --data_dir /path/to/sample_data \
      --audio_file /path/to/audio.wav \
      --result_dir /path/to/result

参数| 说明| 示例  
---|---|---  
`--data_dir`| Avatar 数据目录（含 bg_video.mp4、ref_frames/、net_encode.pt 等）| `./data/sample_data`  
`--audio_file`| 输入音频文件（WAV 格式，16kHz 单声道）| `test.wav`  
`--result_dir`| 输出目录，生成的 MP4 保存为 `test_demo.mp4`| `./output`  
  
注意事项 

音频必须为 **16kHz 单声道 WAV** 。若使用其他格式，需先用 ffmpeg 转换：`ffmpeg -i input.mp3 -ar 16000 -ac 1 output.wav`。更多 Avatar 风格可从 [LiteAvatarGallery](https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery) 下载。

### 4.4 在 OpenAvatarChat 中集成

LiteAvatar 是 OpenAvatarChat 的默认 Avatar 后端。在配置文件中指定 handler 即可启用：
    
    
    # config/chat_with_openai_compatible.yaml
    LiteAvatar:
      module: avatar/liteavatar/avatar_handler_liteavatar
      avatar_name: 20250408/sample_data
      fps: 25
      enable_fast_mode: false
      use_gpu: true

通过 `uv run scripts/download_models.py --handler liteavatar` 可一键下载所需模型权重。

第五章

性能、局限与工程启示

### 5.1 性能表现

  * **CPU 推理** ：在主流笔记本 CPU 上可达 30fps，满足实时对话需求。
  * **GPU 加速** ：设置 `use_gpu=True` 可进一步降低延迟，适合高并发场景。
  * **内存占用** ：ONNX 模型 + TorchScript 生成器总计约 500MB，远低于全 3D 方案。

### 5.2 已知局限

适用范围 

LiteAvatar 仅支持**正面或微侧脸** 的 2D Avatar。大角度转头、表情剧烈变化或多人场景不在支持范围内。其设计目标是“轻量、实时、够用”，而非“照片级真实”。

### 5.3 可迁移的工程经验

  1. **滑动窗口 + 重叠融合** 是处理长序列推理的经典范式，兼顾了效率与时序连续性。
  2. **静音检测回退到中性姿态** 是提升数字人自然度的低成本有效手段。
  3. **ONNX + TorchScript 混合部署** ：推理密集的 ASR/A2M 用 ONNX 获得跨平台兼容性，生成器保留 PyTorch JIT 以利用动态形状优势。
  4. **参数化面部表示** （32维）比直接像素生成更易控制、更易插值、更易压缩，是实时数字人的优选中间表征。

### 参考资料

  * [HumanAIGC/lite-avatar GitHub 仓库](https://github.com/HumanAIGC/lite-avatar)
  * [OpenAvatarChat 项目](https://github.com/HumanAIGC-Engineering/OpenAvatarChat)
  * [LiteAvatarGallery ModelScope](https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery)
  * [Paraformer ASR Model](https://modelscope.cn/models/iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch)
  * [Text/Speech-Driven Full-Body Animation (IJCAI 2022)](https://www.ijcai.org/proceedings/2022/0826.pdf)
