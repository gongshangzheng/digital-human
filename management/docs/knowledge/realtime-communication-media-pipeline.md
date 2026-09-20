---
title: "实时通信（三）：音视频链路，采集、编码、RTP/RTCP、Jitter Buffer 与 A/V Sync"
description: "深入讲解实时音视频从设备采集到浏览器播放的完整链路：采集、编码、RTP 分包、RTCP 反馈、Jitter Buffer、丢包恢复与音画同步。"
date: 2026-06-11T17:54:18
created_at: 2026-06-11T17:54:18
updated_at: 2026-06-12T10:11:16
tags: [RTP, RTCP, Jitter Buffer, A/V Sync, Opus, H264, VP8, AV1]
aliases: ["categories/编程/实时通信"]
sub_id: 30
---

> 来源：博客 gongshangzheng.github.io `src/pages/realtime-communication-media-pipeline.html`，html2text 转换复制于 2026-09-20。原文：https://gongshangzheng.github.io/realtime-communication-media-pipeline.html

RTP媒体分包

RTCP反馈控制

Jitter缓冲吸收

Sync音画同步

[←上一篇WebRTC 核心](realtime-communication-webrtc-core.html) [第 3 篇音视频链路](realtime-communication-media-pipeline.html) [→下一篇服务端架构](realtime-communication-server-architecture.html)

### 本篇先解决哪些词

**采集** 是从麦克风和摄像头取原始声音画面；**编码器** 把原始媒体压缩成可传输的码流；**Codec** 是编码和解码规则；**RTP/RTCP** 负责媒体包和反馈；**Jitter Buffer** 用缓冲吸收网络抖动；**A/V Sync** 负责让声音和画面对齐。

第一章

从摄像头到屏幕，中间不是一根管子

一帧视频进入 RTC 系统后，会经历采集、预处理、编码、RTP 分包、网络发送、接收重排、抖动缓冲、解码、渲染。音频也类似，只是音频通常更敏感：人能容忍视频降清晰度，却很难忍受声音断断续续。 {{< mermaid >}} graph LR A["Capture 采集"] --> B["Preprocess 前处理"] B --> C["Encode 编码"] C --> D["RTP packetize 分包"] D --> E["Network 网络"] E --> F["Jitter Buffer 重排缓冲"] F --> G["Decode 解码"] G --> H["Render 播放"] {{< /mermaid >}} 

**链路视角** ：端到端延迟不是一个模块决定的，而是采集周期、编码队列、网络排队、jitter buffer、解码和渲染共同叠加。

第二章

编码器：在清晰度、码率和延迟之间做交换

音频常用 Opus，因为它能覆盖语音和音乐，支持低延迟、可变码率、包丢失隐藏。视频常见 H.264、VP8、VP9、AV1，不同 codec 在压缩效率、硬件支持、编码复杂度和专利生态上各有取舍。 

### Codec 是“压缩和还原媒体”的约定

**Codec** 是 coder-decoder 的缩写。发送端用编码器把原始音视频压缩成码流，接收端用解码器还原成可播放的声音和画面。Opus 是音频 codec；H.264、VP8、VP9、AV1 是视频 codec。

Codec| 优势| 工程注意点  
---|---|---  
Opus| 低延迟、语音质量好、抗丢包能力强| 音频优先级通常高于视频，弱网时先保声音  
H.264| 硬件支持广，兼容性强| 不同 profile/level 可能导致协商或解码问题  
VP8/VP9| WebRTC 生态成熟，适合浏览器| 硬件加速覆盖不如 H.264 稳定  
AV1| 压缩效率高，适合高质量低码率| 编码复杂度和设备支持仍需评估  
  
第三章

RTP/RTCP：媒体包和控制反馈

RTP（Real-time Transport Protocol，实时传输协议）负责承载媒体流。它的核心字段包括 sequence number、timestamp、SSRC、payload type。**sequence number** 是包序号，用于检测丢包和乱序；**timestamp** 是媒体时间戳，用于恢复播放时间线；**SSRC** 是同步源标识，用来区分不同媒体流；**payload type** 映射到具体 codec。 RTCP（RTP Control Protocol，RTP 控制协议）负责反馈统计和控制：接收端报告丢包、jitter、RTT；发送端根据反馈调整码率；当关键帧丢失时，接收端可以通过 **PLI** （Picture Loss Indication，画面丢失指示）或 **FIR** （Full Intra Request，完整帧请求）请求新关键帧，也可以通过 **NACK** 请求重传部分 RTP 包。 

### Jitter Buffer

Jitter Buffer 是接收端缓冲区，用来吸收网络包到达时间的不均匀。它会在低延迟和稳定播放之间权衡：缓冲越小越实时，但越容易卡；缓冲越大越稳，但互动延迟越高。

第四章

A/V Sync：音画同步靠同一条时间线

音频和视频是不同 RTP 流，采样率和时间戳单位也不同。接收端需要借助 RTCP Sender Report 把 RTP timestamp 映射到 NTP 时间，进而把音频和视频对齐到同一条墙钟时间线。否则就会出现声音先到、嘴型后到，或者画面先动、声音滞后的体验问题。 

数字人场景的同步更敏感

普通会议里几十毫秒的音画偏差可能不明显，但数字人嘴型和语音强绑定。ASR、TTS、Avatar 生成、编码和 WebRTC 播放任一环节延迟漂移，都会被用户感知为“嘴不对”。

## Sources

  1. WebRTC project. [Real-time communication for the web](https://webrtc.org/).
  2. RFC 8445. [Interactive Connectivity Establishment (ICE)](https://datatracker.ietf.org/doc/html/rfc8445).
  3. RFC 8839. [JavaScript Session Establishment Protocol](https://datatracker.ietf.org/doc/html/rfc8839).
  4. RFC 3550. [RTP: A Transport Protocol for Real-Time Applications](https://datatracker.ietf.org/doc/html/rfc3550).
  5. RFC 3711. [The Secure Real-time Transport Protocol](https://datatracker.ietf.org/doc/html/rfc3711).
  6. LiveKit Docs. [LiveKit SFU internals](https://docs.livekit.io/reference/internals/livekit-sfu/).
  7. mediasoup documentation. [mediasoup v3 docs](https://mediasoup.org/documentation/v3/).
  8. Janus WebRTC Server. [Official documentation](https://janus.conf.meetecho.com/docs/).
