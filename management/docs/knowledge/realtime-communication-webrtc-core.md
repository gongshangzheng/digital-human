---
title: "实时通信（二）：WebRTC 核心，SDP、ICE、STUN/TURN、DTLS/SRTP"
description: "深入讲解 WebRTC 建连和安全传输主链路：SDP Offer/Answer、ICE candidate、STUN/TURN、DTLS 握手、SRTP 加密与 DataChannel。"
date: 2026-06-11T17:54:18
created_at: 2026-06-11T17:54:18
updated_at: 2026-06-12T10:11:16
tags: [WebRTC, SDP, ICE, STUN, TURN, DTLS, SRTP, DataChannel]
aliases: ["categories/编程/实时通信"]
sub_id: 20
---

> 来源：博客 gongshangzheng.github.io `src/pages/realtime-communication-webrtc-core.html`，html2text 转换复制于 2026-09-20。原文：https://gongshangzheng.github.io/realtime-communication-webrtc-core.html

SDP媒体协商

ICE连通性检查

DTLS密钥协商

SRTP媒体加密

[←上一篇网络基础](realtime-communication-network-basics.html) [第 2 篇WebRTC 核心](realtime-communication-webrtc-core.html) [→下一篇音视频链路](realtime-communication-media-pipeline.html)

### 本篇先解决哪些词

**SDP** 是媒体能力说明书；**ICE** 是在 NAT 和防火墙后寻找可连通路径的流程；**STUN** 用来发现公网映射地址；**TURN** 是直连失败时的媒体中继；**DTLS** 是 UDP 上的安全握手；**SRTP** 是加密后的 RTP 媒体传输；**DataChannel** 是 WebRTC 中传实时数据的通道。

第一章

WebRTC 不只是一个 API，而是一套建连协议栈

WebRTC（Web Real-Time Communication）给浏览器提供实时音视频和数据传输能力。应用层看到的是 `RTCPeerConnection`、`getUserMedia` 和 `RTCDataChannel`：`RTCPeerConnection` 管连接和媒体传输，`getUserMedia` 从摄像头/麦克风采集媒体，`RTCDataChannel` 传低延迟数据。但真正让通话建立起来的是一条协议链：先协商媒体能力，再寻找可达路径，再完成安全握手，最后传 SRTP 媒体包。 

**最小心智模型** ：SDP 说“我能收发什么”，ICE 说“我从哪里能连上”，DTLS 说“我们如何安全交换密钥”，SRTP 说“后续媒体包怎么加密传”。

{{< mermaid >}} sequenceDiagram participant A as Browser A participant S as Signaling Server participant B as Browser B A->>S: SDP Offer S->>B: SDP Offer B->>S: SDP Answer S->>A: SDP Answer A-->>B: ICE candidates + connectivity checks A-->>B: DTLS handshake A-->>B: SRTP media / SCTP DataChannel {{< /mermaid >}} 

第二章

SDP：不是传媒体，而是描述媒体

SDP（Session Description Protocol，会话描述协议）本身不传音视频，它描述一次会话的媒体能力和传输参数：有哪些 audio/video m-line，支持哪些 codec，payload type 如何映射，是否启用 simulcast，使用哪些 RTP header extension，DTLS fingerprint 是什么。 

### 把 SDP 想成一张媒体菜单

**m-line** 表示一类媒体通道，例如音频或视频；**codec** 是编码格式，例如 Opus、H.264 或 VP8；**payload type** 是 RTP 包里用来标识 codec 的编号；**fingerprint** 是 DTLS 证书指纹，用来确认后续安全握手没有被中间人替换。

### Offer/Answer 模型

发起方生成 Offer，列出自己愿意发送和接收的媒体能力；接收方返回 Answer，选择双方都支持的 codec、方向和传输参数。信令服务器只负责转发 SDP，不理解媒体内容也可以工作。

实际排障时，SDP 能回答很多问题：为什么没有 H.264、为什么只协商到单声道、为什么没有 RID/simulcast、为什么方向是 `recvonly` 而不是 `sendrecv`。很多“WebRTC 没画面”的问题，不在媒体包，而在 SDP 阶段已经协商错了。 

第三章

ICE、STUN、TURN：在复杂网络里找到一条路

ICE（Interactive Connectivity Establishment，交互式连通性建立）负责连接建立。很多客户端都在 NAT（Network Address Translation，网络地址转换）后面，内网地址不能被公网直接访问。浏览器会收集多种 candidate，也就是“候选连接地址”：本机地址、通过 STUN 发现的公网映射地址、通过 TURN 获取的中继地址。然后两端成对测试这些 candidate，选择优先级最高且能连通的一对。 

Candidate 类型| 来源| 含义| 代价  
---|---|---|---  
host| 本机网卡| 局域网或本机地址| 低，但跨 NAT 常不可达  
srflx| STUN| NAT 映射后的公网地址| 低，依赖 NAT 类型  
relay| TURN| 中继服务器分配地址| 连通率高，但消耗服务器带宽  
  
线上必须准备 TURN

只配 STUN 的 demo 在家庭网络可能可用，但在企业内网、对称 NAT、UDP 受限或跨境网络里会大量失败。TURN 是连通率保险，不是锦上添花。

第四章

coturn 实操：从零搭建 STUN/TURN 服务

理解了 STUN 和 TURN 的原理之后，下一步是在自己的服务器上把它们跑起来。**coturn** 是目前最主流的开源 STUN/TURN 实现，同时支持 STUN 和 TURN 两种协议，生产环境广泛使用。 

### STUN 与 TURN 的协作关系

客户端建连时，ICE 流程会先尝试 STUN 发现公网映射地址，如果直连失败再回退到 TURN 中继。coturn 一个程序同时承担这两个角色： 
    
    
            Client A                Client B
                │                       │
                ▼                       ▼
         ┌─────────────┐         ┌─────────────┐
         │  先尝试 STUN │         │  先尝试 STUN │
         │  如果失败    │         │  如果失败    │
         │      ↓      │         │      ↓      │
         │   TURN      │         │   TURN      │
         └──────┬──────┘         └──────┬──────┘
                │                       │
                └───────────┬───────────┘
                            │
                        coturn
              （实现 STUN 和 TURN 的程序）

### 安装 coturn

在 Ubuntu/Debian 上可以直接用包管理器安装，不需要从源码编译： 
    
    
    # 更新软件包
    sudo apt update
    
    # 安装 coturn
    sudo apt install coturn -y
    
    # 查看版本
    turnserver --help | head -1

### 配置 turnserver.conf

安装完成后，先备份默认配置，再编辑主配置文件： 
    
    
    sudo cp /etc/turnserver.conf /etc/turnserver.conf.bak
    sudo vim /etc/turnserver.conf

以下是一份生产可用的最小配置，每一项都有明确用途： 
    
    
    # 监听端口
    listening-ip = 0.0.0.0
    listening-port=3478
    tls-listening-port=5349
    
    # 外部 IP（替换为你的服务器公网 IP）
    external-ip=YOUR_PUBLIC_IP
    
    # 启用指纹验证（WebRTC 要求）
    fingerprint
    
    # 使用长期凭证机制（推荐，比短期凭证更安全）
    lt-cred-mech
    
    # 用户认证（格式：用户名:密码）
    user=webrtc:YourStrongPassword
    
    # Realm（域名标识，与客户端配置对应）
    realm=turn.example.com
    
    # 日志
    log-file=/var/log/turnserver/turnserver.log
    verbose
    
    # 中继端口范围（防火墙需放行此区间）
    min-port=49152
    max-port=65535
    
    # 安全加固：拒绝私有 IP 作为 relay 目标
    no-multicast-peers
    denied-peer-ip=0.0.0.0-0.255.255.255
    denied-peer-ip=10.0.0.0-10.255.255.255
    denied-peer-ip=172.16.0.0-172.31.255.255
    denied-peer-ip=192.168.0.0-192.168.255.255

关键配置说明

**fingerprint** ：WebRTC 规范要求 TURN 消息携带指纹，不启用会导致浏览器拒绝连接。

**lt-cred-mech** ：长期凭证机制，用户名密码在配置文件中静态设定，适合自建服务。短期凭证（time-limited secret）更适合多租户 SaaS 场景。

**denied-peer-ip** ：防止攻击者利用你的 TURN 服务器扫描内网或发起 SSRF 攻击，生产环境必须配置。

### 创建日志目录并启动服务
    
    
    # 创建日志目录并设置权限
    sudo mkdir -p /var/log/turnserver
    sudo chown turnserver:turnserver /var/log/turnserver
    
    # 启用 coturn 服务（默认被禁用）
    sudo sed -i 's/#TURNSERVER_ENABLED=1/TURNSERVER_ENABLED=1/' /etc/default/coturn
    
    # 启动并设为开机自启
    sudo systemctl enable coturn
    sudo systemctl start coturn
    
    # 查看状态
    sudo systemctl status coturn

### 验证服务是否正常

启动后需要确认端口监听和日志输出都正常： 
    
    
    # 确认 3478 端口已在监听
    sudo netstat -tuln | grep 3478
    
    # 实时查看日志
    sudo tail -f /var/log/turnserver/turnserver.log
    
    # 或通过 journalctl
    sudo journalctl -u coturn -f

**防火墙提醒** ：确保服务器的 3478（UDP/TCP）、5349（TLS）以及 min-port ~ max-port 范围内的 UDP 端口都已放行。云服务商的安全组和本机 iptables/nftables 都要检查。

### 客户端接入：iceServers 配置

coturn 部署完成后，在 WebRTC 客户端的 `RTCPeerConnection` 配置中指定 ICE 服务器即可： 
    
    
    const peerConnection = new RTCPeerConnection({
      iceServers: [
        // STUN：发现公网映射地址
        { urls: "stun:turn.example.com:3478" },
        // TURN：直连失败时的中继
        {
          urls: "turn:turn.example.com:3478",
          username: "webrtc",
          credential: "YourStrongPassword"
        },
        // TURNS：TLS 加密的 TURN（推荐生产环境）
        {
          urls: "turns:turn.example.com:5349",
          username: "webrtc",
          credential: "YourStrongPassword"
        }
      ]
    });

排障清单

如果客户端无法通过 TURN 连通，按以下顺序排查：

  1. **端口是否开放** ：`nc -uvz turn.example.com 3478` 测试 UDP 可达性。
  2. **external-ip 是否正确** ：必须是服务器的真实公网 IP，不能是内网地址。
  3. **fingerprint 是否启用** ：浏览器对没有指纹的 TURN 响应会直接丢弃。
  4. **用户名密码是否匹配** ：客户端 credential 必须与 turnserver.conf 中的 user 完全一致。
  5. **日志是否有 Allocate 请求** ：如果日志里完全没有客户端请求，问题在网络层而非应用层。

第五章

DTLS/SRTP 与 DataChannel

WebRTC 媒体默认加密。DTLS（Datagram Transport Layer Security）在 UDP 上完成安全握手，并导出 SRTP（Secure RTP）所需密钥；后续音视频包走 SRTP 加密传输。DataChannel 则通常基于 SCTP over DTLS，用来传实时数据、控制消息、白板事件或游戏状态。 

**排障抓手** ：ICE connected 只代表网络路径通了，不代表媒体能正常播放。还要看 DTLS 是否完成、SRTP 是否有包、RTP timestamp 是否推进、解码器是否收到关键帧。

## Sources

  1. WebRTC project. [Real-time communication for the web](https://webrtc.org/).
  2. RFC 8445. [Interactive Connectivity Establishment (ICE)](https://datatracker.ietf.org/doc/html/rfc8445).
  3. RFC 8839. [JavaScript Session Establishment Protocol](https://datatracker.ietf.org/doc/html/rfc8839).
  4. RFC 3550. [RTP: A Transport Protocol for Real-Time Applications](https://datatracker.ietf.org/doc/html/rfc3550).
  5. RFC 3711. [The Secure Real-time Transport Protocol](https://datatracker.ietf.org/doc/html/rfc3711).
  6. LiveKit Docs. [LiveKit SFU internals](https://docs.livekit.io/reference/internals/livekit-sfu/).
  7. mediasoup documentation. [mediasoup v3 docs](https://mediasoup.org/documentation/v3/).
  8. Janus WebRTC Server. [Official documentation](https://janus.conf.meetecho.com/docs/).
  9. coturn project. [coturn TURN server](https://github.com/coturn/coturn).
