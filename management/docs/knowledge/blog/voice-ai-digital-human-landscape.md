---
title: "数字人系列（十）：实时语音 AI 与数字人产业图谱"
description: "从语音模型、推理框架、数字人视频、Agent 平台到云与算力，五层拆解实时数字人/语音 AI 的产业地图与竞合关系。"
date: 2026-06-05T10:54:41
created_at: 2026-06-05T10:54:41
updated_at: 2026-07-08T11:33:03
tags: ["数字人", "语音AI", "TTS", "推理框架", "产业图谱", "Boson", "SGLang"]
aliases: ["categories/AI/数字人"]
sub_id: 100
hero_title: "实时语音 AI 与数字人产业图谱"
mathjax: true
---

> 来源：博客 gongshangzheng.github.io `src/pages/voice-ai-digital-human-landscape.html`，html2text 转换复制于 2026-09-20。原文：https://gongshangzheng.github.io/voice-ai-digital-human-landscape.html

5技术栈层

30+公司 / 项目

2条路线博弈

1张产业地图

系列位置

序章：这一篇画的是一张「市场地图」

这是数字人系列的第十篇，也是产业图谱篇。前面九篇我们一直在做「向下钻」的事情：从换嘴、运动空间、3DGS/NeRF、扩散基模、整帧生成、流式蒸馏一路讲到算力选型、训练资源、推理资源和 Benchmark。再结合 [CyberVerse 这套能把论文拼成可对话产品的源码](cyberverse-realtime-digital-human-agent.html)，这一篇换一个视角，做一次「向上看」——把支撑实时数字人和语音 AI 的整条产业链摊开，画一张**市场地图** ，看看每一层站着哪些公司、它们靠什么吃饭、彼此之间在抢什么。 之所以现在做这件事，是因为 2026 年上半年出现了一个标志性信号：Boson AI 在 2026-06-04 发布了 **Higgs Audio v3 TTS** ，不仅开放了模型权重，还明确说「可以用 SGLang-Omni 来服务」，而 SGLang-Omni 社区随即把它和 Fish Audio S2 Pro、Qwen3-Omni 一起做了推理优化。#Boson-Higgs-v3# #SGLang-Omni# 这件事把「模型层」和「推理层」的协同关系摆到了台面上——它不是孤立事件，而是整条产业链正在重新组织的一个缩影。所以这一篇不讲单个模型怎么训练，而讲**整张图怎么拼、谁和谁在博弈** 。 

**读法提示** ：本文按「五层技术栈」自下而上展开，每层给一张公司卡片表 + 一段竞合点评，最后用三组关系把整张图串起来，并给一份按场景的选型建议。如果你只关心某一层，可以直接跳到对应章节。

### 先看整张图：五层技术栈

把实时数字人/语音 AI 拆开，从用户能看到的对话产品，到底层的 GPU，一共是五层。每一层都同时存在**开源/开放权重** 和**闭源商业平台** 两条路线在竞争，这是理解整张图的主线。 {{< mermaid >}} flowchart TB subgraph L4["L4 · Agent 平台 + 实时通信（拼装成可对话产品）"] direction LR A1["编排框架  
CyberVerse / Pipecat / LiveKit Agents"] A2["WebRTC 基础设施  
LiveKit / Daily.co"] A3["一站式语音 Agent  
Vapi / Retell"] end subgraph L3["L3 · 数字人视频（给声音配上脸）"] direction LR V1["说话头 / 唇形同步  
[LivePortrait](paper-liveportrait.html) / [MuseTalk](paper-musetalk.html) / SoulX"] V2["企业视频 / 全身  
HeyGen / Synthesia / Tavus / D-ID"] end subgraph L1["L1 · 语音模型（让机器开口说话）"] direction LR S1["可控 TTS / 声音克隆  
Boson / Fish / Qwen3-TTS / ElevenLabs"] S2["全双工语音 LLM  
OpenAI Realtime / Gemini Live / Seeduplex"] end subgraph L2["L2 · 推理框架（让模型跑得快又便宜）"] direction LR R1["通用 LLM serving  
SGLang / vLLM / TensorRT-LLM"] R2["多模态 / 语音 serving  
SGLang-Omni / NVIDIA Riva"] end subgraph L5["L5 · 云与算力（提供 GPU 燃料）"] direction LR C1["GPU 硬件  
NVIDIA H200 / B200 / GB200"] C2["推理云 / Serverless GPU  
Baseten / Fireworks / Modal"] end L4 --> L3 L4 --> L1 L3 --> L2 L1 --> L2 L2 --> L5 {{< /mermaid >}} 

_图 1：实时数字人/语音 AI 的五层技术栈。上层是用户可感知的产品，越往下越接近基础设施。一个完整的实时数字人产品，往往要把这五层各挑一个供应商拼起来。_

Layer 1 · Voice

语音模型层：让机器开口说话

这一层是数字人的「声带」。它又分两个子赛道：一是**可控 TTS / 声音克隆** （把文字变成有情绪、可定制音色的语音），二是**全双工语音 LLM** （边听边说、能被打断的端到端语音对话）。 

### 可控 TTS / 声音克隆

这个子赛道最热闹，开源和闭源打得难解难分。最新的信号是 Boson 的 Higgs Audio v3：它把 TTS 从「朗读文本」推进到「面向语音 Agent 的实时可控表达层」，强调 inline 标签控制情感、语速、停顿甚至音效，所谓 _speaks, not just reads_ 。#Boson-Higgs-v3# 

公司/项目| 定位| 主打产品| 开源状态| 关键数据  
---|---|---|---|---  
**Boson AI**|  面向 Voice Agent 的音频基础模型| Higgs Audio v3 TTS| 开放权重（研究/非商用，HF 可下）| 2026-06-04 发布，100+ 语言，零样本克隆，inline 情感控制，可用 SGLang-Omni 服务  
**Fish Audio**|  开源取向高性能多语 TTS| Fish Audio S2 Pro| 开放权重（Fish Research License，商用需授权）| 4B 参数，1000 万小时训练，80+ 语言，H200 上 RTF 0.195 / TTFA ~100ms，Seed-TTS 中文 WER 0.54%  
**阿里 Qwen3-TTS**|  开源低延迟流式 TTS| Qwen3-TTS-12Hz（0.6B/1.7B）| 开源（Apache-2.0）| 10 语言，端到端延迟低至 97ms，3 秒声音克隆  
**Resemble / Chatterbox**|  开源声音克隆模型家族| Chatterbox / Turbo / Multilingual| 开源（MIT）| Turbo 350M 低延迟，Multilingual 23+ 语言，5 秒克隆，盲测 63.75% 优于 ElevenLabs  
**ElevenLabs**|  商业 TTS 龙头| Eleven v3 / Conversational AI| 闭源 API| 2025-01 Series C $1.8 亿 / 估值 $33 亿，累计 $2.81 亿，70+ 语言，60%+ Fortune 500 采用  
**MiniMax**|  全球 AI foundation model 公司| MiniMax Audio / Speech 系列| 闭源 API/产品| 2022 成立，累计 2.12 亿用户，覆盖 200+ 国家，声音克隆 + 多语种  
**Cartesia**|  超低延迟流式 TTS 基础设施| Sonic / Sonic-3.5| 闭源 API| sub-90ms 延迟，40+ 语言，主打自然度第一  
**火山引擎豆包语音**|  字节系企业语音服务| Doubao Seed TTS/ASR/ICL 2.0| 闭源云服务| 超自然合成 + 声音复刻 + 多语种识别  
  
### 全双工语音 LLM

这个子赛道更接近「未来形态」——不是先转文字再合成语音，而是音频原生、能边听边说、能被自然打断。目前主要是大厂闭源在领跑。 

公司/项目| 产品| 特征| 开源状态  
---|---|---|---  
**OpenAI**|  GPT Realtime / Realtime API| 低延迟原生多模态 speech-to-speech| 闭源 API  
**Google DeepMind**|  Gemini 3.1 Flash Live / TTS| Live dialogue + 语音生成，SynthID 水印| 闭源 API  
**ByteDance Seed**|  Seeduplex| Native Full-Duplex Speech LLM，边听边说、干扰抑制| 闭源  
  
**竞合点评** ：可控 TTS 赛道的格局是「开放权重军团围攻闭源 API」——Boson、Fish、Qwen3-TTS、Chatterbox 用开放权重 + inline 可控性，正面挑战 ElevenLabs 的商业护城河；而全双工语音 LLM 因为训练成本极高，短期仍是 OpenAI/Google/字节的闭源天下。许可证是关键变量：真正宽松可商用的只有 Qwen3-TTS（Apache-2.0）和 Chatterbox（MIT），Boson 和 Fish 都是「研究免费、商用需授权」。

Layer 2 · Serving

推理框架层：让模型跑得快又便宜

模型训出来只是第一步，要在生产里以低延迟、高吞吐、可控成本跑起来，靠的是这一层。对实时数字人来说，这一层直接决定「能不能做到实时」。 

项目| 定位| 核心技术| 背后组织| 开源/许可证| 关键数据  
---|---|---|---|---|---  
**SGLang**|  高性能 LLM/多模态 serving| RadixAttention 前缀缓存、零开销调度、PD 分离| 非营利组织 LMSYS| 开源| 支撑全球 40 万+ GPU，被 xAI/AMD/NVIDIA/LinkedIn/Cursor/Oracle/Baseten 采用，获 a16z 开源资助，已加入 PyTorch 生态  
**SGLang-Omni**|  omni/多模态语音 serving 分支| 多阶段流水线编排| SGLang 社区| 开源| 为 Fish Audio S2 Pro、Qwen3-Omni 做优化，可服务 Boson Higgs Audio v3  
**vLLM**|  最主流开源 LLM 推理引擎| PagedAttention 分页 KV cache、连续批处理| UC Berkeley Sky Computing Lab 起源| 开源（Apache-2.0）| 2000+ 贡献者，支持 200+ 模型架构；主贡献方 Neural Magic 于 2025-01 被 Red Hat 收购  
**TensorRT-LLM**|  NVIDIA GPU 推理优化库| FP8/INT4 量化、张量并行、融合算子| NVIDIA| 开源（NVIDIA 许可）| 常配 Triton Inference Server、NIM 微服务使用  
**TGI**|  HuggingFace 模型推理服务器| 连续批处理、流式、张量并行| Hugging Face| 开源| 服务于 HF Inference Endpoints  
**LMDeploy**|  国产模型部署工具链| TurboMind 引擎、量化| 上海 AI Lab / InternLM| 开源| 与 InternLM/Qwen 生态结合  
**NVIDIA Riva**|  语音 AI 推理 SDK| ASR/TTS GPU 加速、流式| NVIDIA| SDK/容器（企业授权）| 是 NVIDIA ACE 数字人微服务的语音底座  
  
**竞合点评** ：通用 LLM serving 形成 **SGLang / vLLM / TensorRT-LLM** 三足鼎立——vLLM 靠 PagedAttention 成为事实标准且贡献者最广，SGLang 靠 RadixAttention 和大规模部署（40 万 GPU、被 xAI 采用）后来居上，TensorRT-LLM 则是 NVIDIA GPU 上的极致性能底座。值得注意的是 **SGLang-Omni** 这条多模态分支：它正在把推理框架从「文本 token 生成」延伸到「语音/全双工」，并主动去适配 Boson、Fish、Qwen 这些开放权重 TTS——这正是 L1 和 L2 协同的关键纽带。另一个信号是商业化路径：Neural Magic 被 Red Hat 收购，意味着开源推理引擎正在被企业级软件巨头收编。

Layer 3 · Avatar

数字人视频层：给声音配上一张脸

有了会说话的声音，还要有会动的脸甚至全身。这一层从「单图说话头」到「企业级全身视频」跨度很大，呈现出鲜明的「开源底层模型 vs 闭源商业平台」分化。 

公司/项目| 定位| 细分赛道| 开源状态| 关键数据  
---|---|---|---|---  
**Soul-AILab**|  实时流式数字人生成模型| 说话头 + 人体动画| 开源（权重在 HF/ModelScope）| [SoulX-FlashHead](paper-soulx-flashhead.html)-1.3B 实时流式说话头；[SoulX-LiveAct](paper-liveact.html) 在 2×H100/H200 上 20 FPS，RTX 5090 上 6 FPS  
**LivePortrait**|  高效肖像动画| 说话头 / 肖像驱动| 开源| 快手 KwaiVGI 出品，被快手/抖音/剪映/视频号采用  
**MuseTalk**|  实时唇形同步| 唇形同步 / 视频配音| 开源| 腾讯音乐 Lyra Lab 出品，V100 上 30fps+，权重/训练代码全开放  
**Synthesia**|  企业 AI 视频平台| 企业视频 / 全身| 闭源 SaaS| 2017 伦敦，2026-01 Series E $2 亿 / 估值 $40 亿，160+ 语言，90%+ Fortune 100 使用，240+ avatar，1M+ 用户  
**HeyGen**|  AI 视频/Avatar 生成平台| 企业视频 / Avatar| 闭源 SaaS/API| 2020 成立，Series A $6000 万 / 估值 >$5 亿，ARR 从 $100 万涨到 $3500 万+  
**Tavus**|  实时对话视频 Avatar / 人计算| 实时互动数字人 / API| 闭源 SaaS/API| 2020 成立，Series A $1800 万（传 Series B $4000 万），Phoenix-4/Raven-1/Sparrow-1 模型，客户含 Salesforce/Meta  
**D-ID**|  说话头像 / 数字人平台| 说话头 / 企业视频| 闭源平台/API| Series B $2500 万 / 累计 $4800 万，120+ 语言，Deep Nostalgia 累计近 1 亿次动画  
**商汤如影 / 腾讯云 / 阿里云**|  大厂企业级数字人平台| 直播 / 企业视频 / 互动| 闭源云服务| 商汤如影超级直播间称运营效率提升 7 倍；阿里云为通义实验室出品；腾讯云智能数智人多模态交互  
  
**竞合点评** ：这一层有一条非常清晰的**「开源中国队 vs 闭源海外队」** 分界线。底层开源模型几乎全是中国团队——快手 LivePortrait、腾讯音乐 MuseTalk、Soul AI Lab 的 SoulX 系列；而企业视频商业化的头部（Synthesia $40 亿估值、HeyGen、Tavus、D-ID）则由海外公司领跑。逻辑是：开源模型做**底座** ，闭源平台做**产品和服务** 。海外大厂用 SaaS 封装把模型能力卖给企业客户（培训、营销、客服），而中国团队更倾向开源模型 + 大厂云平台（商汤/腾讯/阿里）两条腿走路。

Layer 4 · Agent

Agent 平台 + 实时通信层：把零件拼成产品

前三层都是「零件」——声音、推理、脸。要变成一个用户能打电话、能视频对话的产品，需要这一层把它们串起来，并解决实时音视频传输（WebRTC）、对话编排、打断、工具调用等问题。 

公司/项目| 定位| 细分赛道| 开源状态| 关键数据  
---|---|---|---|---  
**CyberVerse**|  自托管开源数字人 Agent 框架| 编排 + 通信 + 数字人一体| 开源（GPLv3）| gRPC 微服务 + WebRTC + PersonaAgent/SubAgent + RAG + 可选 avatar，支持 LiveKit SFU；商用需注意 GPLv3 法务  
**Pipecat**|  开源实时语音/多模态 Agent 框架| Agent 编排| 开源（Python）| Daily.co 出品，transport 支持 Daily/LiveKit WebRTC，可做 multi-agent handoff  
**LiveKit**|  WebRTC 基础设施 + voice agent 栈| 基础设施 + 编排| 开源（server）+ Cloud| Series C Index 领投 $1 亿 / 估值 $10 亿；被 OpenAI ChatGPT Advanced Voice 官方采用；Agents 月下载 1M+  
**Daily.co**|  全球 WebRTC 实时音视频基础设施| WebRTC 基础设施| 商业（维护开源 Pipecat）| 2016 成立，Series B $4000 万 / 累计 $6000 万，13ms 首跳延迟，75+ 全球 PoP  
**Vapi**|  一站式企业语音 Agent 平台| 一站式语音 Agent| 闭源 SaaS| Series B $5000 万（Series A 由 BVP 领投 $2000 万），支撑 10 亿通话，75 万+ 开发者，<500ms 延迟  
**Retell AI**|  AI 电话 Agent / 呼叫中心自动化| 一站式语音 Agent| 闭源 SaaS| ~600ms 延迟，专有 turn-taking 模型，drag-and-drop agentic framework  
  
**竞合点评** ：这一层分三档。**LiveKit/Daily.co** 占据最底的实时通信基础设施，其中 LiveKit 已被 OpenAI Advanced Voice 官方架构采用，是这一层最强的节点；**CyberVerse/Pipecat/LiveKit Agents** 是开发者可自托管的编排框架，CyberVerse 更是把数字人 avatar 也整合进来的「一体化套件」；**Vapi/Retell** 则是面向业务客户的成品平台，把电话、合规、监控全封装好。选型逻辑很清楚：要可控/自托管选开源框架，要快速上线呼叫中心选 Vapi/Retell。

Layer 5 · Compute

云与算力层：提供 GPU 燃料

最底层是所有层的燃料。实时数字人对延迟极其敏感，GPU 选型和推理云的成本直接决定产品能不能跑、跑得起跑不起。 

公司/项目| 定位| 细分赛道| 关键数据  
---|---|---|---  
**NVIDIA**|  GPU 硬件 + 全栈推理软件| GPU 硬件 / 微服务| H200/B200/GB200 系列，Blackwell GB200 NVL72 LLM 推理对比 H100 达 30x；NIM 推理微服务、Triton；ACE + Riva + Audio2Face 构成完整数字人微服务链  
**Baseten**|  AI 推理云平台| 云推理平台| 洽谈 $10 亿融资 / 估值 $110 亿，NVIDIA 投资 $1.5 亿（前轮 $3 亿 / 估值 $50 亿）  
**Fireworks AI**|  AI 推理云平台| 云推理平台| Series C $2.5 亿 / 估值 $40 亿，Lightspeed/Index 领投  
**Modal Labs**|  Serverless GPU 平台| Serverless GPU| Series B $8700 万 / 估值 $11 亿，后续传 $3.55 亿 / 估值 $46.5 亿，营收 8 个月 5x 至 $3 亿  
**Together / Replicate / RunPod**|  开放模型推理云 / 模型托管| 云推理平台| 托管开源语音/数字人模型推理，按量付费  
**阿里云 / 火山引擎 / 腾讯云**|  中国侧 GPU 云与推理服务| 云推理平台| 提供 GPU 云 + 数字人/语音产品一体化（如阿里云 PAI）  
  
**竞合点评** ：NVIDIA 在这一层是绝对的霸主——既卖 GPU 硬件，又通过 NIM/Riva/ACE/Audio2Face 直接做到 L2-L3 的软件层，还反向投资 L5 的推理云（给 Baseten 投了 $1.5 亿）。这是一种**「算力霸主向上游全栈渗透」** 的打法。而 Baseten、Fireworks、Modal 这批推理云创业公司则在「让开放权重模型跑得更便宜」上卷成本（NVIDIA 官方称它们把单 token 成本压低多达 10x），融资估值都在数十亿美元量级，是这一轮 AI 基础设施热潮里最受资本追捧的一档。

Relations

三组关键竞合关系

把五层拼起来看，整张产业图里有三组最值得关注的博弈关系。 

### 关系一：模型层 ↔ 推理层的开源共生

Boson 把 Higgs v3 权重开放、并明确「可用 SGLang-Omni 服务」，SGLang-Omni 社区又主动为 Fish S2 Pro、Qwen3-Omni 做优化——**开放权重 TTS 与开源 omni 推理框架正在形成共生关系** 。这是对闭源 API（ElevenLabs、OpenAI Realtime）的一次集体反制：你卖 API，我开放权重 + 开源推理栈，让任何人都能自托管。本文开头那个「Boson + SGLang-Omni」的信号，本质上就是这条关系的最新一幕。 

### 关系二：开源中国队 vs 闭源海外队

在数字人视频层尤其明显：底层模型（SoulX、LivePortrait、MuseTalk）几乎全是中国团队开源，而企业视频商业化（Synthesia、HeyGen、Tavus）由海外公司领跑。**开源做底座，闭源做产品** ——这不是谁打败谁，而是产业链上下游的分工。中国团队用开源占据模型生态位，海外公司用 SaaS 占据企业客户和现金流。 

### 关系三：NVIDIA 的全栈渗透

NVIDIA 是唯一一家横跨多层的玩家：L5 卖 GPU（垄断），L2 做 TensorRT-LLM/Triton/NIM，L2-L3 做 Riva/ACE/Audio2Face 数字人微服务，还反向投资 L5 的推理云。**算力霸主正在沿着技术栈向上吃** ，把「卖铲子」变成「卖整条流水线」。 {{< mermaid >}} flowchart LR subgraph 开源阵营 B["Boson Higgs v3"] F["Fish S2 Pro"] Q["Qwen3-TTS"] SG["SGLang-Omni"] CN["SoulX/LivePortrait/MuseTalk"] end subgraph 闭源阵营 EL["ElevenLabs"] OAI["OpenAI Realtime"] SYN["Synthesia/HeyGen"] end subgraph 全栈玩家 NV["NVIDIA  
GPU+NIM+Riva+ACE"] end B -->|"权重开放, 可用其服务"| SG F -->|"被优化"| SG Q -->|"被优化"| SG SG -.->|"自托管反制"| EL SG -.->|"自托管反制"| OAI CN -.->|"开源底座 vs 闭源产品"| SYN NV -->|"全栈渗透 + 投资推理云"| SG NV -->|"提供 GPU 燃料"| EL {{< /mermaid >}} 

_图 2：三组竞合关系。开源阵营围绕 SGLang-Omni 形成共生反制闭源 API；中国开源模型与海外闭源产品形成上下游分工；NVIDIA 横跨全栈并向上渗透。_

Selection

按场景的选型建议

把整张图落到实际，给三类典型场景一份组合建议（仅供参考，许可证和成本须自行复核）。 

场景| L1 语音| L2 推理| L3 数字人视频| L4 编排| L5 算力  
---|---|---|---|---|---  
**完全自托管 / 数据敏感**|  Qwen3-TTS（Apache-2.0）| SGLang-Omni / vLLM| LivePortrait / MuseTalk| CyberVerse / Pipecat| 自建 H200 / Modal  
**快速上线企业语音 Agent**|  ElevenLabs / Cartesia| （平台托管）| HeyGen / D-ID（如需视频）| Vapi / Retell| （平台托管）  
**极致质量 / 全双工对话**|  OpenAI Realtime / Gemini Live| （厂商托管）| Tavus（实时互动）| LiveKit| 厂商云  
  
选型的三个判断锚点 

第一看**许可证** ：要商用就避开「研究/非商用」权重（Boson、Fish），优先 Apache-2.0（Qwen3-TTS）或 MIT（Chatterbox）；CyberVerse 是 GPLv3，商用务必法务确认。第二看**延迟预算** ：实时对话的体验由整条链路决定，不是单个模型的 FPS，TTS 的 TTFA、推理框架的调度、WebRTC 的网络延迟要一起算。第三看**自托管 vs 托管** ：要可控和数据安全就走开源自托管栈，要快和省心就用 Vapi/Retell/ElevenLabs 这类成品。

Wrap-up

系列收尾：从一篇 Survey 到一张产业图

这一篇是数字人系列的收尾。回看整个系列：我们从 Survey 序章 出发梳理了实时数字人的技术演进，中间几篇逐条拆解了换嘴、运动空间、3DGS/NeRF、扩散基模、整帧生成、流式蒸馏、算力选型、训练资源和 Benchmark，再到 [CyberVerse 源码解读](cyberverse-realtime-digital-human-agent.html) 看了一个真实系统怎么把论文拼成产品，最后用这一篇把视角拉到整条产业链。 如果说前面九篇回答的是「数字人**怎么做出来、怎么评估、怎么部署** 」，这一篇回答的是「数字人**这门生意长什么样** 」。两个视角合起来，才是一张完整的认知地图：往下能看到技术细节，往上能看到产业格局。技术会迭代，公司会起落，但这张五层栈的结构和「开源 vs 闭源」「模型 vs 推理 vs 产品」的博弈逻辑，在可见的未来都还会持续。 

[←上一篇 · 第九章训练、推理资源与 Benchmark](digital-human-training-inference-benchmark.html) [本文 · 第十章（收尾）实时语音 AI 与数字人产业图谱](voice-ai-digital-human-landscape.html) [系列目录数字人系列 Hub](digital-human-hub.html)

### 参考来源

  * Boson AI. Higgs Audio v3 TTS. [boson.ai/blog/higgs-audio-v3-tts](https://www.boson.ai/blog/higgs-audio-v3-tts)；模型权重 [bosonai/higgs-audio-v3-tts-4b](https://huggingface.co/bosonai/higgs-audio-v3-tts-4b)
  * SGLang. [github.com/sgl-project/sglang](https://github.com/sgl-project/sglang)；SGLang-Omni [github.com/sgl-project/sglang-omni](https://github.com/sgl-project/sglang-omni)
  * Fish Audio. Fish Speech / S2 Pro. [github.com/fishaudio/fish-speech](https://github.com/fishaudio/fish-speech)
  * Qwen Team. Qwen3-TTS. [github.com/QwenLM/Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS)
  * ElevenLabs. Series C. [elevenlabs.io/blog/series-c](https://elevenlabs.io/blog/series-c)
  * vLLM. [github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)；PagedAttention 论文 [arXiv:2309.06180](https://arxiv.org/abs/2309.06180)
  * Red Hat. Acquisition of Neural Magic (vLLM). [businesswire (2024-11)](https://www.businesswire.com/news/home/20241112030832/en/)
  * NVIDIA. Digital Human ACE Microservices (Riva/Audio2Face). [nvidianews](https://nvidianews.nvidia.com/news/digital-humans-ace-generative-ai-microservices)
  * NVIDIA. Blackwell Platform (GB200 NVL72). [nvidianews](https://nvidianews.nvidia.com/news/nvidia-blackwell-platform-arrives-to-power-a-new-era-of-computing)
  * Soul AI Lab. SoulX-FlashHead / SoulX-LiveAct. [soul-ailab.github.io](https://soul-ailab.github.io/soulx-flashhead/)；[github.com/Soul-AILab/SoulX-LiveAct](https://github.com/Soul-AILab/SoulX-LiveAct)
  * Synthesia. Series E ($200M / $4B). [synthesia.io](https://www.synthesia.io/post/series-e-200-million-4-billion-valuation-future-work)
  * HeyGen. Series A. [heygen.com/blog](https://www.heygen.com/blog/announcing-our-series-a)
  * Tavus. [tavus.io](https://www.tavus.io)；TechCrunch 报道 [techcrunch (2024-03)](https://techcrunch.com/2024/03/12/)
  * D-ID. Funding. [d-id.com/blog](https://www.d-id.com/blog/d-id-closes-25-million-funding-round/)
  * KwaiVGI (快手). LivePortrait. [github.com/KwaiVGI/LivePortrait](https://github.com/KwaiVGI/LivePortrait)
  * Tencent Music Lyra Lab. MuseTalk. [github.com/TMElyralab/MuseTalk](https://github.com/TMElyralab/MuseTalk)
  * CyberVerse. [github.com/dsd2077/CyberVerse](https://github.com/dsd2077/CyberVerse)
  * Pipecat (Daily.co). [github.com/pipecat-ai/pipecat](https://github.com/pipecat-ai/pipecat)
  * LiveKit. OpenAI partnership & Series C. [livekit.io/blog](https://livekit.io/blog/openai-livekit-partnership-advanced-voice-realtime-api)
  * Daily.co. Series B. [daily.co/blog](https://www.daily.co/blog/announcing-our-40m-series-b/)
  * Vapi. [vapi.ai](https://vapi.ai)；BVP 投资 [bvp.com](https://www.bvp.com/news/our-investment-in-vapi-the-voice-ai-developer-platform)
  * Retell AI. [retellai.com](https://www.retellai.com)
  * Baseten. NVIDIA investment. [WSJ](https://www.wsj.com/tech/ai/nvidia-invests-150-million-in-ai-inference-startup-baseten-fe7ede72)
  * Fireworks AI. Series C ($250M / $4B). [NVIDIA blog](https://blogs.nvidia.com/blog/inference-open-source-models-blackwell-reduce-cost-per-token/)
  * Modal Labs. Series B ($87M / $1.1B). [modal.com](https://modal.com/)
