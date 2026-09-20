---
title: "实时通信（四）：服务端架构，P2P、SFU、MCU 与生产级 RTC 平台"
description: "深入讲解实时通信服务端架构：P2P、SFU、MCU 的取舍，LiveKit、mediasoup、Janus 的定位，以及 QoS、监控、扩容、成本和排障。"
date: 2026-06-11T17:54:18
created_at: 2026-06-11T17:54:18
updated_at: 2026-06-12T10:11:16
tags: [SFU, MCU, P2P, LiveKit, mediasoup, Janus, WebRTC, QoS]
aliases: ["categories/编程/实时通信"]
sub_id: 40
---

> 来源：博客 gongshangzheng.github.io `src/pages/realtime-communication-server-architecture.html`，html2text 转换复制于 2026-09-20。原文：https://gongshangzheng.github.io/realtime-communication-server-architecture.html

P2P直连

SFU转发

MCU混流

QoS质量控制

[←上一篇音视频链路](realtime-communication-media-pipeline.html) [第 4 篇服务端架构](realtime-communication-server-architecture.html) [→下一篇数字人应用](realtime-communication-digital-human.html)

### 本篇先解决哪些词

**P2P** 是端和端尽量直接传媒体；**SFU** 是服务器只转发不混合媒体；**MCU** 是服务器解码、混合、再编码；**Simulcast/SVC** 是同一视频提供多种质量层；**QoS** 是围绕体验质量做监控、调度和降级。

第一章

P2P、SFU、MCU 的本质区别

P2P 是端到端直连，SFU 是服务器选择性转发，MCU 是服务器解码、混流、再编码。三者不是谁替代谁，而是不同成本结构：P2P 省服务器但端侧和网络要求高；SFU 平衡延迟和扩展性；MCU 服务端成本高，但对弱设备和传统终端友好。 

架构| 服务端做什么| 优点| 缺点| 适合场景  
---|---|---|---|---  
P2P| 主要做信令，媒体尽量直连| 低成本、低链路复杂度| 多人时上行爆炸，NAT 成功率有限| 一对一、小规模 demo  
SFU| 接收多路流并选择性转发| 低延迟、可扩展、保留端侧自适应| 下行和转发带宽成本明显| 会议、直播连麦、AI 实时互动  
MCU| 解码、混合、转码后输出一路| 客户端简单、兼容传统系统| 服务器 CPU/GPU 成本高，延迟更高| 传统视频会议、录制合成、网关  
  
第二章

为什么生产系统常选 SFU

SFU（Selective Forwarding Unit，选择性转发单元）的核心是“不理解画面内容，只理解媒体流结构”。它根据订阅关系、带宽估计、simulcast/SVC 层级、活跃说话人、客户端能力，把合适的流转发给合适的人。 

### Simulcast 和 SVC 都是在准备多档画质

**Simulcast** 是发送端同时编码多路不同分辨率/码率的视频，SFU 按订阅者网络选择一层转发；**SVC** 是 Scalable Video Coding，可伸缩视频编码，把一个码流组织成基础层和增强层，弱网用户只收基础层，好网络用户再叠加增强层。

{{< mermaid >}} graph TD A["Client A 发布高/中/低三层视频"] --> S["SFU"] B["Client B 弱网订阅低层"] --> S C["Client C 大屏订阅高层"] --> S D["Recorder 订阅归档流"] --> S S --> B S --> C S --> D {{< /mermaid >}} LiveKit、mediasoup、Janus 都可以理解为 SFU/媒体服务器生态里的不同选择。**LiveKit** 更偏完整 RTC 平台和开发者体验，提供房间、权限、SDK、录制、转码等整套能力；**mediasoup** 更像底层可编程 SFU 库，适合自己搭业务控制面；**Janus** 是模块化 WebRTC Gateway，适合插件化网关和传统协议接入。 

第三章

QoS、监控和扩容：RTC 的生产工程

生产级 RTC 平台至少要观测四层：客户端采集/编码/播放，WebRTC 连接和统计，SFU 转发和订阅，机房网络和带宽成本。只看服务端 CPU 或总带宽不够，因为用户体验可能坏在某个房间、某个链路方向、某个 codec、某个运营商路径上。 

层级| 关键指标| 常见动作  
---|---|---  
客户端| capture FPS、encode time、render delay、freeze count| 降分辨率、换 codec、关闭特效  
连接| RTT、loss、jitter、available bitrate、candidate pair| 切 TURN、重启 ICE、降码率  
SFU| 订阅数、转发码率、NACK/PLI、节点负载| 迁房、限流、调度到近端节点  
成本| 出口带宽、TURN relay 占比、录制/转码资源| 多层编码、边缘部署、冷热路径拆分  
  
第四章

排障路线：从房间到单条 RTP 流

排障不要从猜开始。先确定影响范围：是所有房间、某个地域、某个运营商、某个设备型号，还是某个用户上行。再定位方向：发布端上行坏、SFU 转发坏、订阅端下行坏、播放端解码坏。最后下钻到 RTP：sequence 是否连续、jitter 是否突增、PLI/NACK 是否异常、关键帧是否到达。 

**工程经验** ：RTC 问题的定位单位不是“用户说卡”，而是“某个时间段、某个房间、某个 publisher 的某条 SSRC，在某个 subscriber 侧出现了什么统计异常”。

## Sources

  1. WebRTC project. [Real-time communication for the web](https://webrtc.org/).
  2. RFC 8445. [Interactive Connectivity Establishment (ICE)](https://datatracker.ietf.org/doc/html/rfc8445).
  3. RFC 8839. [JavaScript Session Establishment Protocol](https://datatracker.ietf.org/doc/html/rfc8839).
  4. RFC 3550. [RTP: A Transport Protocol for Real-Time Applications](https://datatracker.ietf.org/doc/html/rfc3550).
  5. RFC 3711. [The Secure Real-time Transport Protocol](https://datatracker.ietf.org/doc/html/rfc3711).
  6. LiveKit Docs. [LiveKit SFU internals](https://docs.livekit.io/reference/internals/livekit-sfu/).
  7. mediasoup documentation. [mediasoup v3 docs](https://mediasoup.org/documentation/v3/).
  8. Janus WebRTC Server. [Official documentation](https://janus.conf.meetecho.com/docs/).
