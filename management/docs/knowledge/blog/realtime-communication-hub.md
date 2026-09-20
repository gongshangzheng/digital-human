---
title: "实时通信工程总览：从网络到 WebRTC，再到数字人实时互动"
description: "实时通信系列 Hub：按网络基础、WebRTC 核心（含 coturn 实操）、音视频链路、服务端架构和数字人应用组织 RTC/WebRTC 的系统学习路径。"
date: 2026-06-11T17:54:18
created_at: 2026-06-11T17:54:18
updated_at: 2026-06-12T10:11:16
tags: [RTC, WebRTC, LiveKit, SFU, 音视频, 数字人]
sub_id: 0
hero_title: "实时通信工程总览"
hero_sub: "从网络到 WebRTC，再到数字人实时互动"
hero_tagline: "网络基础 · WebRTC 协议 · 媒体链路 · 服务端架构 · 数字人应用"
aliases: ["实时通信", "RTC", "WebRTC 系列", "categories/编程/实时通信/index", "categories/编程/实时通信"]
---

> 来源：博客 gongshangzheng.github.io `src/pages/realtime-communication-hub.html`，html2text 转换复制于 2026-09-20。原文：https://gongshangzheng.github.io/realtime-communication-hub.html

5专题文章

2核心链路

RTC实时通信

WebRTC浏览器标准

系列总纲

实时通信到底在做什么

实时通信（Real-Time Communication, RTC）不是单一协议，而是一整套工程系统：网络要尽量低延迟，媒体要能被采集、编码、分包、缓冲和同步，浏览器要穿过家庭路由器、企业防火墙和运营商网络建立安全连接，服务端要决定媒体是端到端直连、服务器转发还是服务器混流，业务还要处理弱网、监控、扩容、成本和排障。 

**一句话主线** ：实时通信的本质，是在不可控网络上，把连续时间里的音频、视频和数据流，尽量低延迟、可恢复、可观测地送到对端。

这个系列按工程链路拆成五篇：先理解网络为什么会抖、会丢、会排队；再看 WebRTC 如何建连和加密；然后进入音视频如何分包、反馈、缓冲和同步；接着看多人通信里的直连、转发和混流架构，以及 LiveKit、mediasoup、Janus 这些工程实现；最后落到实时数字人，解释 ASR、LLM、TTS、Avatar 如何接进 RTC。 

### 先建立一张术语地图

**RTC** 是实时通信这个大领域；**WebRTC** 是浏览器和客户端常用的一套实时通信协议栈；**NAT** 是把内网地址转换成公网访问地址的网络机制；**RTP/RTCP** 是音视频媒体包和控制反馈；**P2P/SFU/MCU** 分别代表端到端直连、服务器选择性转发、服务器混流；**ASR/LLM/TTS/Avatar** 是数字人把“听、想、说、动”串起来的 AI 模块。后面的每篇文章都会先解释本篇术语，再进入协议和工程细节。

阅读目录

五篇文章如何读

顺序| 文章| 解决的问题  
---|---|---  
01| [网络基础：延迟、抖动、丢包与拥塞控制](realtime-communication-network-basics.html)| 为什么实时系统怕排队，为什么 UDP 常用于媒体，为什么“带宽够”不等于体验好。  
02| [WebRTC 核心：SDP、ICE、STUN/TURN、coturn 部署、DTLS/SRTP](realtime-communication-webrtc-core.html)| 浏览器如何从“两个陌生端”变成一条可加密传媒体的连接，以及如何自建 STUN/TURN 服务。  
03| [音视频链路：采集、编码、RTP/RTCP、Jitter Buffer 与 A/V Sync](realtime-communication-media-pipeline.html)| 声音和画面如何从设备进入编码器，如何被分包传输，如何在接收端恢复连续播放。  
04| [服务端架构：P2P、SFU、MCU 与生产级 RTC 平台](realtime-communication-server-architecture.html)| 多人会议、直播连麦、实时互动课和 AI Agent 通话为什么通常需要 SFU。  
05| [数字人实时通信：ASR/LLM/TTS/Avatar 如何接进 RTC](realtime-communication-digital-human.html)| 实时数字人如何把语音识别、大模型、语音合成、视频生成和 WebRTC 串成低延迟闭环。  
  
[Hub实时通信工程总览](realtime-communication-hub.html) [→下一篇网络基础](realtime-communication-network-basics.html)

知识图谱

从网络到业务的分层模型

{{< mermaid >}} graph TD A["业务体验：通话、会议、数字人、互动直播"] --> B["RTC 服务端：P2P / SFU / MCU / 录制 / 转码"] B --> C["WebRTC 建连：SDP / ICE / STUN / TURN / DTLS"] C --> D["媒体传输：RTP / RTCP / SRTP / DataChannel"] D --> E["媒体处理：采集 / 编码 / Jitter Buffer / A/V Sync"] E --> F["网络基础：UDP / TCP / 延迟 / 抖动 / 丢包 / 拥塞"] {{< /mermaid >}} 

**学习建议** ：不要从 API 开始背。先抓住“网络不可控 → WebRTC 建连 → RTP 连续传媒体 → 服务端转发扩展 → 业务闭环优化”这条主线，再回头看每个协议字段。

## Sources

  1. WebRTC project. [Real-time communication for the web](https://webrtc.org/).
  2. RFC 8445. [Interactive Connectivity Establishment (ICE)](https://datatracker.ietf.org/doc/html/rfc8445).
  3. RFC 3550. [RTP: A Transport Protocol for Real-Time Applications](https://datatracker.ietf.org/doc/html/rfc3550).
  4. LiveKit Docs. [LiveKit SFU internals](https://docs.livekit.io/reference/internals/livekit-sfu/).
