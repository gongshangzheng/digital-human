---
title: "数字人工程解读（四）：实时数字人模型推理 Benchmark 汇总"
description: "汇总 CyberVerse、OpenAvatarChat 与 LiveAct 官方仓库在 A10 上实测的实时数字人推理数据：推理 FPS、显存占用、主机内存约束与 nvidia-smi 消耗百分比。持续更新。"
date: 2026-06-16T16:26:19
created_at: 2026-06-16T16:26:19
updated_at: 2026-09-03T13:52:39
tags: [数字人, Benchmark, 推理速度, 显存, LiteAvatar, FlashHead, CyberVerse, OpenAvatarChat]
aliases: ["categories/AI/数字人/数字人工程解读"]
sub_id: 40
toc: true
mathjax: false
---

> 来源：博客 gongshangzheng.github.io `src/pages/digital-human-engineering-benchmark.html`，html2text 转换复制于 2026-09-20。原文：https://gongshangzheng.github.io/digital-human-engineering-benchmark.html

**本页定位** ：这是"数字人工程解读系列"的实验数据汇总页。表格记录各开源实时数字人工程在真实 GPU 上跑出的推理 FPS、显存占用与消耗百分比，供选型与排障参考。数据来源有四类：系列文章中的实测日志、用户提供的 nvidia-smi 截图、digital_human 项目在 A10 上的冒烟实测日志，以及对官方仓库的源码核查（用于区分"源码可确认"与"实测已验证"）。未公开、未实测的数据一律标"—"或"待补充"，不做猜测。

Benchmark

实时数字人模型推理数据

模型 | 效果（视频） | 推理速度（FPS） | 显存占用 | 显存消耗（nvidia-smi）  
---|---|---|---|---  
**LiteAvatar**  
OpenAvatarChat · A10 | 待补充 | 25.19 | 7507 MiB / 23028 MiB | ≈32.5%（三进程合计 7488 MiB）  
**[LAM](lam-2025.html)**  
OpenAvatarChat · A10 | 待补充 | 30（arkit_face 30帧/秒） | 1725 MiB / 23028 MiB | ≈7.5%（单进程 1716 MiB）  
**[SoulX-FlashHead](paper-soulx-flashhead.html)-1_3B Lite**  
CyberVerse · A10 · wav2vec2-base-960h | 待补充 | ≈46.7（24帧/0.514s） | 待补充 | 待补充  
**FlashHead 1.3B Pro**  
CyberVerse · A10 | 待补充 | ≈4.8（28帧/5.82s, 512×512） | 7839 MiB / 23028 MiB | ≈34.0%（GPU-Util 100%, 148W/150W）  
**FlashHead 1.3B Pro**  
CyberVerse · A10 · 55.8s 长音频 · GPU 非独占 | — | 1.4（1114帧/801.4s）  
RTF ≈14.4×，与训练/打分分时共享 | 峰值 9.9 GiB / 23028 MiB | ≈43%（GPU-Util、功耗未采）  
**LiveAct 18B**  
官方仓库 generate.py · A10 · 512×512 · bf16 + offload 三件套 | — | 0.8–0.9  
37.6s/迭代，42/42 完成 | 峰值 10.4 GiB / 23028 MiB  
主机内存峰值 113 GiB / 125 GiB | ≈46%（GPU-Util、功耗未采）  
**LiveAct 18B**  
官方仓库 generate.py · A10 · 416×720 · bf16 + offload 三件套 | — | 0.67  
47.4s/迭代，43/43 完成，RTF ≈47.5× | 峰值 11.7 GiB / 23028 MiB  
主机内存峰值 118 GiB / 125 GiB | ≈52%（GPU-Util、功耗未采）  
**LiveAct 18B**  
官方仓库自报 · 2× H100 · FP8 | — | 20（实时） | 未披露 | —  
**LiveAct 18B**  
官方仓库自报 · 单张 RTX 5090 · FP8 + offload | — | 6 | 未披露 | —  
**LiveAct 18B**  
CyberVerse · RTX PRO 6000（源码报告） | 待补充 | 20 | 待补充 | 待补充  
  
_注：除特别标注外，所有 FPS 数据均在**单张 NVIDIA A10（24GB）** 上测得。FPS 列为 Avatar 模型本身的视频帧生成速度，不含 ASR/LLM/TTS/WebRTC 等链路开销。"待补充"表示该条目尚未在当前实验中采集到对应数据。_

### LiveAct 18B 在 A10 上：瓶颈是主机内存，不是显存

本页早期版本把 LiveAct 记成"不可用（OOM / 超时）· >23028 MiB"。这个结论已经被 2026-09 的两次完整跑通推翻 #liveact-a10-smoke-run9-2026-09-01# #liveact-a10-smoke-run11b-2026-09-02#：512×512 跑完 42/42 迭代、416×720 跑完 43/43 迭代，都产出了完整的 55.5 秒带音轨视频。

显存裕度接近一半，主机内存才是真约束 

两次实测的**显存峰值只有 10.4 GiB（512×512）和 11.7 GiB（416×720）** ，22.5 GiB 的 A10 还剩一半以上。真正卡住部署的是主机内存：LiveAct 走官方消费级 offload 三件套（`--block_offload` / `--t5_cpu` / `--offload_cache`）把主干、T5 和 KV cache 全卸到 CPU，代价是主机内存稳态占用约 85–90 GiB——主干 37.8 GiB（`low_cpu_mem_usage=False` 全量驻 CPU）+ bf16 KV cache 35.2 GiB（3 去噪步 × 40 层，512² 下 `kv_cache_tokens=1024×14`）+ T5 11.4 GiB + CLIP ≈5 GiB #liveact-repo-source-read-2026-08-31#。换到 416×720，KV cache 涨到 40.2 GiB，与实测 118 GiB 峰值吻合。

此前几次中止**全部是同机其它任务挤爆主机内存** 触发的 cgroup OOM-killer 或自设看门狗击杀，不是 GPU 侧 OOM——其中一次 dmesg 记录到 anon-rss 73.5 GiB + bf16 KV 35 GiB ≈108 GiB，当时机器正被 LoRA 训练（19 GiB 显存）和打分任务占用 #liveact-a10-smoke-run9-2026-09-01#。所以正确口径是：**整机独占 + 可用主机内存 ≥110 GiB** ，125 GiB 的机器放得下，但不能只看启动时刻的内存快照。

另外两条路确实走不通：不加 offload 直接 bf16 全量装载约 36 GiB > 24 GiB，单卡塞不进；A10 是 Ampere，没有 FP8 硬件，`--fp8_gemm` / `--fp8_kv_cache` 都用不上——实测 `--fp8_kv_cache` 与 `torch.compile` 的 Triton 后端在 Ampere 上直接报 `ValueError: type fp8e4nv not supported in this architecture`，本想用 FP8 把 KV 砍半到 ≈17.6 GiB 的方案因此作废 #liveact-repo-source-read-2026-08-31#。官方 GUI 的 `demo.py` 还会**无条件** 调 `enable_fp8_gemm`，在 A10 上必挂，只能走 `generate.py` 且不带任何 `--fp8_*`。

这两次实测的唇同步质量不能用来横比 

两次都跑在 `--audio_cfg 1.0` \+ `--size 512*512`，而官方单卡 eval 口径是 `--audio_cfg 1.7` \+ `480*832`。`audio_cfg=1.0` 会让 `generate.py` 的音频 CFG 分支被**完全跳过** ，等于关掉音频引导 #liveact-a10-smoke-run11b-2026-09-02#。因此这批产物只能回答"放不放得下、跑不跑得通、多快"，唇同步质量不可与其它模型对比。

1.7 口径在 A10 上**没有验证过** ，而且大概率验证不了：`audio_cfg > 1.0` 会再分配一套等量 null-audio KV cache，bf16 下主机内存直接翻倍，而独占时峰值已经到 113 GiB / 125 GiB，没有余量。

**速度定位** ：0.8–0.9 FPS 意味着 55.5 秒视频要跑约 39 分钟墙钟（含 2.5 分钟加载）。同素材对照下，小它一个数量级的 FlashHead Pro 1.3B 是 1.4 FPS / RTF ≈14.4×，而且当时 GPU 还在与训练和打分分时共享 #flashhead-pro-a10-control-2026-08-31#——LiveAct 在 A10 上不但没有大模型的质量红利，速度还更慢，只适合离线评测。根因是架构而非工程：官方 20 FPS 实时是 2×H100 + FP8 的成绩，单卡 5090 + FP8 + offload 是 6 FPS，A10 的 bf16 算力约为 H100 的 1/16，而能救它的那些内核（FP8 矩阵乘、FP8 稀疏注意力）在 Ampere 上根本不存在 #liveact-repo-source-read-2026-08-31#。

### 数据来源

  * **LiteAvatar / A10** ：用户提供 2026-06-16 16:18 OpenAvatarChat 运行日志 + nvidia-smi 输出。#openavatarchat-a10-log-2026-06-16#
  * **LAM / A10** ：用户提供 2026-06-16 16:27 OpenAvatarChat LAM 推理日志 + nvidia-smi 输出。#openavatarchat-lam-a10-log-2026-06-16#
  * **FlashHead Lite** ：[[数字人工程解读（二）：CyberVerse 实验记录——FlashHead Lite + wav2vec2 的端到端耗时拆解]] 中的 Python Avatar 生成日志。#cyberverse-flashhead-experiment#
  * **FlashHead Pro / A10** ：用户提供 2026-06-16 17:35 CyberVerse FlashHead Pro 推理日志 + nvidia-smi 输出（A10, 512×512）。#cyberverse-flashhead-pro-a10-log-2026-06-16#
  * **LiveAct** ：[[数字人工程解读（一）：CyberVerse，把论文拼成一个能对话的实时数字人]] 第六章硬件 benchmark 表。#cyberverse-source-read#
  * **LiveAct / A10（512×512）** ：2026-09-01 04:02~04:41 官方仓库 `generate.py` 冒烟 run 9，机器独占，videoc1 首帧 + 55.8s audio_mid，42/42 迭代完成。日志 `smoke_run.log` \+ 每 10s 采样的 `mem_trace.log`。#liveact-a10-smoke-run9-2026-09-01#
  * **LiveAct / A10（416×720）** ：2026-09-02 13:01~13:45 冒烟 run 11b，机器独占，weishen 真人首帧 + 完整 audio_mid，43/43 迭代完成，含 `clamp(0,1)` 与 `quality=9` 两处清晰度补丁。#liveact-a10-smoke-run11b-2026-09-02#
  * **LiveAct 官方仓库源码核查** ：2026-08-31 clone `Soul-AILab/SoulX-LiveAct`（main）后逐行核查 `generate.py` / `demo.py` / `wan/modules/clip.py`，含显存账本、offload 开关语义、FP8 硬件门槛与官方速度参照。#liveact-repo-source-read-2026-08-31#
  * **FlashHead Pro / A10（55.8s 长音频）** ：2026-08-31 同素材对照，videoc1 + audio_mid，GPU0 与 LoRA 训练/打分分时共享。#flashhead-pro-a10-control-2026-08-31#

### 参考来源

  * OpenAvatarChat LiteAvatar A10 运行日志与 nvidia-smi 输出（2026-06-16 16:18）。用户提供原始数据。
  * OpenAvatarChat LAM A10 推理日志与 nvidia-smi 输出（2026-06-16 16:27）。用户提供原始数据。
  * CyberVerse 本地实验日志（2026-06-12）：SoulX-FlashHead-1_3B Lite + wav2vec2-base-960h Avatar 生成耗时。见 [数字人工程解读（二）](cyberverse-flashhead-lite-experiment.html)。
  * CyberVerse FlashHead 1.3B Pro A10 推理日志与 nvidia-smi 输出（2026-06-16 17:35）。用户提供原始数据，512×512 分辨率。
  * CyberVerse 源码解读（2026-06-05）：README 硬件 benchmark 表。见 [数字人工程解读（一）](cyberverse-realtime-digital-human-agent.html)。
  * LiveAct 18B 单张 A10 冒烟实测 run 9（2026-09-01 04:02~04:41，机器独占）：`generate.py --size 512*512 --block_offload --t5_cpu --offload_cache`，bf16 KV、无 FP8 开关，42/42 迭代，输出 55.5s / 1333 帧 @24fps 带音轨视频；显存峰值 10.4 GiB、主机内存峰值 113 GiB / 125 GiB、37.6s/迭代。含 dmesg OOM-killer 记录与每 10s 采样内存曲线。本项目原始实测日志。
  * LiveAct 18B 单张 A10 冒烟实测 run 11b（2026-09-02 13:01~13:45，机器独占，GPU1）：416×720 竖版 + `clamp(0,1)` \+ `export_to_video(quality=9)`，43/43 迭代，输出 55.5s @24fps / 15.1 Mbps 视频；显存峰值 11.7 GiB、主机内存峰值 118 GiB / 125 GiB（KV cache 40.2 GiB）、47.4s/迭代 ≈0.67 生成 FPS。同期记录 `--audio_cfg 1.0` 与官方 eval 口径 `1.7 + 480*832` 的复现保真度差异。本项目原始实测日志。
  * SoulX-LiveAct 官方仓库源码核查（2026-08-31，clone main 后逐行核查）：`generate.py:206` 默认 `torch_dtype=torch.bfloat16`、FP8 为可选开关、`demo.py:126` 无条件调 `enable_fp8_gemm`、消费级 offload 三件套语义、bf16 全量 ≈36 GiB 显存账本、Ampere 上 `--fp8_kv_cache` × `torch.compile` 冲突、官方速度参照（2×H100 FP8 = 20 FPS；单卡 5090 FP8+offload = 6 FPS）。[Soul-AILab/SoulX-LiveAct](https://github.com/Soul-AILab/SoulX-LiveAct)。
  * FlashHead 1.3B Pro 单张 A10 长音频对照实测（2026-08-31，videoc1 + 55.8s audio_mid，GPU0 与 LoRA 训练/打分分时共享，非独占）：1114 帧 / 55.7s 视频，推理 801.4s → 1.4 FPS、RTF 14.39，显存峰值 9.9 GiB。本项目原始实测日志。

[←上一篇 · 工程解读（二）FlashHead Lite 耗时拆解](cyberverse-flashhead-lite-experiment.html) [枢纽页数字人系列总目录](digital-human-hub.html)
