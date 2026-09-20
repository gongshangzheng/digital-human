---
title: "数字人工程解读（三）：OpenAvatarChat 源码：LiteAvatar 实时数字人的模块化设计与 WebRTC 部署"
description: "深度解读 OpenAvatarChat 仓库：LiteAvatar 实时数字人的 Handler Pipeline 架构、RTC 流媒体数据通路、coturn TURN 服务部署与端口（3478/5349/49152+）配置详解。"
date: 2026-06-16T14:56:00
created_at: 2026-06-16T14:56:00
updated_at: 2026-06-16T14:56:00
tags: [数字人, OpenAvatarChat, LiteAvatar, WebRTC, TURN, coturn, fastrtc, 数字人部署, 端口配置, Handler Pipeline]
aliases: ["categories/AI/数字人/数字人工程解读"]
sub_id: 30
toc: true
mathjax: false
notify: true
hero_title: "OpenAvatarChat 源码解读"
hero_sub: "从 Handler Pipeline 到 TURN 端口：LiteAvatar 数字人的模块化设计与部署全链路"
---

> 来源：博客 gongshangzheng.github.io `src/pages/open-avatar-chat-liteavatar.html`，html2text 转换复制于 2026-09-20。原文：https://gongshangzheng.github.io/open-avatar-chat-liteavatar.html

**一句话总结** ：OpenAvatarChat 是 HumanAIGC 团队开源的模块化实时数字人对话系统。本文以 LiteAvatar（2D 说话头）模式为切⼊点，深度分析其 Handler Pipeline 数据通路、WebRTC 流媒体链路，以及 coturn TURN 服务的端口部署细节——特别是 49152+ 范围内的端口数量如何与并发数挂钩。

第⼀章

项目定位与整体架构

### OpenAvatarChat 是什么

**OpenAvatarChat** 是一个开源的模块化交互数字人对话系统，由 HumanAIGC 团队开发维护。它不是一个单一模型，而是一个**把 ASR、LLM、TTS、Avatar 渲染、WebRTC 流媒体编排成实时对话管线的框架** #repo-readme#。

核心特点——

  * **多模态交互** ：支持文本、语音、视频。用户对着摄像头说话，数字人实时回应
  * **模块化架构** ：每个环节（ASR、LLM、TTS、Avatar）可独立替换，组件来自 SenseVoice、Qwen、CosyVoice、LiteAvatar 等开源项目
  * **多种数字人方案** ：LiteAvatar（2D 说话头）、[LAM](lam-2025.html)（3D Gaussian Splat）、[MuseTalk](paper-musetalk.html)（唇形同步）、FlashHead（扩散模型）
  * **低延迟** ：通过 VAD 检测、音频缓冲、帧率控制，平均响应约 2.2 秒#repo-readme#

### 支持的数字人类型

数字人方案| 技术路线| 模式| 硬件要求  
---|---|---|---  
LiteAvatar| TTS2Face（参数驱动）| 2D| 较低，有 GPU 即可  
LAM| Audio2Expression + 3D Gaussian Splat| 3D| 需要 GPU  
MuseTalk| 扩散模型 + 唇形同步| 2D| 需要 GPU  
FlashHead| 扩散模型实时流式| 2D| 需要 GPU  
  
### 宏观架构：从浏览器到数字人渲染

整个系统分为三个运行单元——前端 WebUI、FastAPI 服务端和 ChatEngine 推理管线。它们通过 WebRTC 音频视频流和 WebSocket 数据通道连在一起#repo-code-rtc#。

{{< mermaid >}} flowchart TB subgraph Browser["浏览器 (Vue3 前端)"] UI["VideoChat / WSVideoChat"] Media["getUserMedia (摄像头+麦克风)"] end subgraph FastAPI["FastAPI 服务 (8282)"] Static["Static Files (/ui/*)"] InitConfig["/openavatarchat/initconfig"] WebRTCOffer["/webrtc/offer (fastrtc)"] end subgraph ChatEngine["ChatEngine Handler Pipeline"] Client["RtcClient Handler"] VAD["SileroVad"] ASR["SenseVoice"] LLM["Qwen-Plus (DashScope API)"] TTS["CosyVoice (Bailian API)"] Avatar["HandlerTts2Face (LiteAvatar)"] end Media -->|"WebRTC (H.264)"| WebRTCOffer WebRTCOffer --> Client Client --> VAD --> ASR --> LLM --> TTS TTS -->|"AVATAR_AUDIO"| Avatar Avatar -->|"AVATAR_VIDEO + AVATAR_AUDIO"| Client Client -->|"WebRTC Track"| Media Static --> UI InitConfig --> UI {{< /mermaid >}} 

第二章

LiteAvatar 数据通路：从麦克风到数字人帧

### Handler Pipeline 执行模型

ChatEngine 的核心设计是 **Handler Pipeline** ——每个 Handler 有明确的输入/输出数据类型（ChatDataType），引擎自动按依赖关系串联它们#repo-code-chat-engine#。

LiteAvatar 模式下（配置文件 `chat_with_openai_compatible_bailian_cosyvoice.yaml`），Pipeline 包含以下 Handler：

顺序| Handler| 模块路径| 输入类型| 输出类型  
---|---|---|---|---  
1| RtcClient| client/rtc_client/client_handler_rtc| MIC_AUDIO, CAMERA_VIDEO| —  
2| InterruptHandler| logic/interrupt/interrupt_handler| INTERRUPT Signal| Signal 转发  
3| SileroVad| vad/silerovad/vad_handler_silero| MIC_AUDIO| VAD 分段  
4| SenseVoice| asr/sensevoice/asr_handler_sensevoice| Audio Segment| HUMAN_TEXT  
5| LLMOpenAICompatible| llm/openai_compatible/...| HUMAN_TEXT| AVATAR_TEXT  
6| CosyVoice (Bailian)| tts/bailian_tts/...| AVATAR_TEXT| AVATAR_AUDIO  
7| LiteAvatar| avatar/liteavatar/avatar_handler_liteavatar| AVATAR_AUDIO| AVATAR_VIDEO + AVATAR_AUDIO  
  
Pipeline 自动编排 

你不需要手动串联 Handler。ChatEngine 根据每个 Handler 的 `get_handler_detail()` 返回的输入/输出类型自动建立数据流转关系。新增一个 Avatar Handler 只需实现相同接口即可替换。

### LiteAvatar Worker：独立进程的音频到视频转换

LiteAvatar 的核心是 **HandlerTts2Face** （位于 `src/handlers/avatar/liteavatar/avatar_handler_liteavatar.py`），它管理一个或多个 **LiteAvatarWorker** 子进程#repo-code-liteavatar#。

Worker 的生命周期——

{{< mermaid >}} sequenceDiagram participant TTS as TTS Handler participant Handle as HandlerTts2Face.handle() participant Worker as LiteAvatarWorker (子进程) participant Algo as TTS2Face Algo (C++) participant Output as 共享内存 → RTC Stream TTS->>Handle: AVATAR_AUDIO (numpy array) Handle->>Worker: audio_in_queue.put(SpeechAudio) Worker->>Worker: START 事件 → audio_input_loop Worker->>Algo: audio2param(audio_bytes) Algo-->>Worker: 面部参数 (30fps) Worker->>Algo: param2video Algo-->>Worker: 视频帧 (H×W×3) Worker->>Output: video_out_queue (共享内存) Output-->>Handle: _media_out_loop 读取 Handle->>Handle: submit_data(AVATAR_VIDEO) {{< /mermaid >}} 

关键源码——Worker 启动触发的 START 事件#repo-code-worker-start#：
    
    
    # src/handlers/avatar/liteavatar/liteavatar_worker.py
    def _event_input_loop(self):
        while True:
            event = self.event_in_queue.get()
            if event == Tts2FaceEvent.START:
                if not self.session_running:
                    self.session_running = True
                    self.processor.start()
                    self.audio_input_thread = threading.Thread(target=self._audio_input_loop)
                    self.audio_input_thread.start()
                    logger.info("Avatar session started")

Worker 使用 **共享内存** （SharedMemoryBufferPool）在主进程和子进程间传输音频/视频数据，避免序列化开销。主进程的 `_media_out_loop` 从共享内存池中取出视频帧和音频数据，封装为 `ChatData` 提交到 Pipeline。

第三章

WebRTC 流媒体链路：fastrtc + aiortc

### RtcStream：连接前后端的桥梁

RTC 流媒体由 **RtcStream** （位于 `src/service/rtc_service/rtc_stream.py`）负责。它继承自 `fastrtc.AsyncAudioVideoStreamHandler`，实现了三个关键方法#repo-code-rtc-stream#：

方法| 方向| 功能  
---|---|---  
`receive(frame)`| 前端 → 后端| 接收麦克风音频，写入 Pipeline (MIC_AUDIO)  
`emit()`| 后端 → 前端| 从 Pipeline 读取 AVATAR_AUDIO，发送到 WebRTC audio track  
`video_emit()`| 后端 → 前端| 从 Pipeline 读取 AVATAR_VIDEO，发送到 WebRTC video track  
  
### H.264 编码管道

OpenAvatarChat 在启动时通过 monkey-patch 方式强制 H.264 编码（位于 `client_handler_rtc.py` 的模块级初始化代码），确保视频兼容性和硬件加速#repo-code-h264#：
    
    
    # src/handlers/client/rtc_client/client_handler_rtc.py
    async def patched_set_remote_description(self, sessionDescription):
        await original_set_remote(self, sessionDescription)
        for transceiver in self._RTCPeerConnection__transceivers:
            if transceiver.kind == "video":
                capabilities = get_capabilities("video")
                current_codecs = transceiver._codecs
                refiltered = filter_preferred_codecs(current_codecs, capabilities.codecs)
                transceiver._codecs = refiltered  # H.264 优先
                logger.info(f"Video codecs negotiated: {[c.mimeType for c in transceiver._codecs[:2]]}")

fastrtc 版本兼容性 

当前版本为 `fastrtc==0.0.34` \+ `aiortc==1.14.0`。在非 localhost 环境下可能遇到 `Received ICE candidate for unknown connection` 警告——ICE candidate 在 PeerConnection 就绪前到达导致时序冲突。建议使用 SSH 隧道（`ssh -L 8282:localhost:8282`）做本地测试，或升级 fastrtc 到最新版本。

第四章

TURN 服务部署与端口配置（关键）

不看这里的端口配置，数字人 100% 罢工 

如果你从公网访问服务器（非 localhost），WebRTC 的 ICE 连接需要穿透 NAT。没有 TURN 服务做数据中继，浏览器和服务器之间的媒体流将无法建立——你会看到"数字人永远在加载中"。以下端口必须全开。

### 端口完整清单

端口| 协议| 服务| 用途| 说明  
---|---|---|---|---  
8282| TCP| FastAPI (uvicorn)| HTTPS 服务| 前端页面 + /webrtc/offer API + /openavatarchat/initconfig  
3478| TCP + UDP| coturn| TURN 信令| STUN 绑定请求 + TURN 分配请求  
5349| TCP| coturn| TURNS 信令| TURN over TLS，加密媒体中继信令  
49152–49164| UDP| coturn| 媒体中继| 实际音频/视频数据中转端口范围  
  
### 端口数量与并发数的关系

每个 WebRTC PeerConnection 需要 **2 个 UDP 中继端口** ——一个用于 RTP 音频，一个用于 RTP 视频。因此#inference-ports#：

**并发数 n → 至少需要 2n 个端口**

具体换算——

  * 配置 `concurrent_limit: 2` → 需要 4 个端口
  * 配置 `concurrent_limit: 5` → 需要 10 个端口
  * 配置 `concurrent_limit: 10` → 需要 20 个端口

当前推荐范围 `49152–49164` 提供 13 个端口，可支持最多 6 个并发连接。如需更高并发，扩大 `max-port` 即可。

### coturn 配置示例
    
    
    # /etc/turnserver.conf
    listening-port=3478
    tls-listening-port=5349
    listening-ip=0.0.0.0
    relay-ip=172.19.207.124         # 服务器内网 IP
    external-ip=47.110.95.197       # 服务器公网 IP
    min-port=49152                  # 媒体中继起始端口
    max-port=49164                  # 媒体中继结束端口
    verbose
    fingerprint
    lt-cred-mech
    user=username:password          # 与 YAML 配置保持一致
    realm=openavatarchat

### YAML 配置中的 TURN
    
    
    # config/chat_with_openai_compatible_bailian_cosyvoice.yaml
    RtcClient:
      module: client/rtc_client/client_handler_rtc
      connection_ttl: 900
      turn_config:
        turn_provider: turn_server
        urls:
          - "turn:47.110.95.197:3478?transport=tcp"
          - "turn:47.110.95.197:3478?transport=udp"
          - "turns:47.110.95.197:5349?transport=tcp"
        username: "admin"
        credential: "admin"

常见坑：TURN 凭证不匹配 

YAML 中的 `username`/`credential` 必须与 `/etc/turnserver.conf` 中 `user=` 后的值一致。此外，阿里云等云服务器需要在**安全组规则** 中显式开放上述所有端口——仅防火墙开放不够。

### SSL 证书

从 localhost 以外访问需要 HTTPS（浏览器要求）。OpenAvatarChat 默认读取 `ssl_certs/localhost.crt` 和 `ssl_certs/localhost.key`，可通过 `scripts/create_ssl_certs.sh` 生成自签名证书#repo-deploy-doc#。

第五章

快速开始与配置指引

### 三步启动 LiteAvatar

前置条件 

需要设置 `DASHSCOPE_API_KEY` 环境变量（阿里云百炼 API Key），或在项目根目录创建 `.env` 文件。LLM 和 TTS 均通过百炼 API 调用，不消耗本地 GPU 资源。
    
    
    # 1. 克隆 + 子模块
    git clone https://github.com/HumanAIGC-Engineering/OpenAvatarChat.git
    cd OpenAvatarChat
    git submodule update --init --recursive --depth 1
    
    # 2. 安装依赖
    uv run install.py --config config/chat_with_openai_compatible_bailian_cosyvoice.yaml
    
    # 3. 下载 LiteAvatar 模型
    uv run scripts/download_models.py --handler liteavatar
    
    # 4. 启动
    uv run src/demo.py --config config/chat_with_openai_compatible_bailian_cosyvoice.yaml

命令参数| 作用| 如何替换  
---|---|---  
`--config`| 指定 YAML 配置文件| 替换为 `chat_with_lam.yaml` 体验 3D 数字人，或 `chat_with_openai_compatible_bailian_cosyvoice_flashhead.yaml` 体验 FlashHead  
`--handler liteavatar`| 指定下载模型的目标 Handler| 不同 Handler 对应不同模型：`sensevoice`、`silero_vad` 等  
`DASHSCOPE_API_KEY`| 百炼 API Key| 在 [阿里云百炼控制台](https://dashscope.console.aliyun.com/) 创建  
  
### 关键配置文件字段
    
    
    # config/chat_with_openai_compatible_bailian_cosyvoice.yaml (核心字段)
    chat_engine:
      concurrent_limit: 2                # 最大并发数，影响 TURN 端口需求
      handler_configs:
        RtcClient:
          connection_ttl: 900            # 会话超时（秒）
          output_video_fps: 24           # 输出帧率（MuseTalk 用 24；LiteAvatar 用 25）
        LiteAvatar:
          avatar_name: "20250408/sample_data"  # 模型名称（从 ModelScope 下载）
          fps: 25                        # 必须与 output_video_fps 一致
          use_gpu: true                  # 是否使用 GPU 加速

第六章

常见问题与排错指南

### 数字人永远在加载中

检查顺序——

  1. `resource/avatar/liteavatar/20250408/sample_data` 目录是否存在。若不存在，运行 `uv run scripts/download_models.py --handler liteavatar`
  2. 服务日志中是否出现 `Avatar process is ready` 和 `Avatar session started`。只有前者没有后者说明 TTS 音频没有成功触发 Pipeline
  3. 浏览器 Console 中是否有 `Unknown connection` 或 ICE 相关错误
  4. 如果是公网访问，端口 3478/5349/49152-49164 是否在阿里云安全组中开放

### coturn 凭证问题

coturn 日志中查看 `/var/tmp/turn_*.log`，如果出现 `401 Unauthorized`，说明 YAML 中的 username/credential 与 `/etc/turnserver.conf` 不匹配。

### SSL 证书不被信任

自签名证书在浏览器中会显示"不安全"警告，但不影响 WebRTC 功能。生产环境建议使用 Let's Encrypt 或购买正式证书。

### 参考资料

  * OpenAvatarChat README.md — 项目定位、核心卖点、快速开始命令 #repo-readme#
  * OpenAvatarChat 部署文档 — 网络环境说明、SSL 证书、TURN 服务配置 #repo-deploy-doc#
  * src/handlers/client/rtc_client/client_handler_rtc.py — RTC Client Handler，WebRTC 初始化和 H.264 编码注入
  * src/service/rtc_service/rtc_stream.py — RtcStream 类，前后端 WebRTC 音频视频双向桥接
  * src/chat_engine/ — ChatEngine、HandlerManager、数据流转编排
  * src/handlers/avatar/liteavatar/ — HandlerTts2Face、LiteAvatarWorker、共享内存 Buffer Pool
  * src/handlers/avatar/liteavatar/liteavatar_worker.py — _event_input_loop，START 事件触发 Worker 启动
  * src/handlers/client/rtc_client/client_handler_rtc.py — patched_set_remote_description，H.264 codec 注入
  * 端口并发关系：每个 PeerConnection 需要 2 个 UDP 端口（RTP Audio + RTP Video），n 并发需 2n 端口。基于 WebRTC 协议规范和 coturn 实战经验推断。
