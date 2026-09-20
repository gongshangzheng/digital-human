# 知识库索引

> 数字人知识库：从外部信息源**复制**而来（复制即声明本仓库为演进主体，上游冻结为历史源）。
> 外部源登记见 [docs/external-sources.md](../../../docs/external-sources.md)。

## internwiki/ — InternWiki 数字人知识库

来源：`~/code/InternWiki` @ commit `91b683b`（2026-09-20 复制）
原路径前缀：`apps/web/content/interns/tangwen/docs/` 与 `apps/web/content/interns/junjiawang/docs/`

| 目录/文件 | 内容 | 作者 |
|-----------|------|------|
| `基础/` | 数字人基础、动作空间专题、数字人渲染器专题 | tangwen |
| `模型精读/` | AvatarForcing 精读 ×2、Ditto 精读、Talker-T2AV 精读 | tangwen |
| `工程与评测/` | CyberVerse 工程专题、Ditto 实时化 TRT 复盘、音画同步、评测指标、数据集整理、视频生成加速、模型探索复盘、Talker-T2AV 接入 | tangwen |
| `快速导读/` | 5 分钟系列：认识数字人、声音变口型、单图推理、实时为何难 | tangwen |
| `微调与实践/` | Ditto 改动实践、AvatarForcing 微调实践、微调策略专题 | tangwen |
| `project-notes/` | 数字人项目 README、tasks.json、3DGS 方法调研、硬件评估 | tangwen |
| `voice-agent-web-*.md`（7 篇） | 语音 Agent Web 端：架构、数字人、MCP/RAG、会话生命周期、鉴权、前后端契约、badcase | junjiawang |

## blog/ — 博客精选文档（survey / 工程解读）

来源：`~/gongshangzheng.github.io` @ commit `3e7da698`（2026-09-20 html2text 转换复制，脚本 `scripts/copy_blog_knowledge.py`）
论文单篇精读不入知识库——已在 papers 库索引（带 blog_url）。

| 文件 | 内容 |
|------|------|
| `digital-human-survey-map.md` | 综述地图：四篇综述内容级对比 + 12 条新模型线索 |
| `digital-human-avatar-survey.md` | 数字人 Avatar 综述 |
| `realtime-digital-human-survey.md` | 实时数字人综述 |
| `gfvc-survey-2023.md` | GFVC 人脸视频编码综述 |
| `digital-human-engineering-benchmark.md` | 工程基准 |
| `digital-human-training-inference-benchmark.md` | 训练推理基准 |
| `digital-human-realtime-gpu-comparison.md` | 实时方案 GPU 对比 |
| `digital-human-streaming-distillation.md` | 流式蒸馏 |
| `digital-human-identity-consistency.md` | 身份一致性 |
| `cyberverse-realtime-digital-human-agent.md` | CyberVerse 实时数字人 Agent |
| `cyberverse-flashhead-lite-experiment.md` | FlashHead Lite 实验 |
| `realtime-communication-*.md`（5 篇） | 实时通信系列：Hub/媒体管线/服务端架构/WebRTC/网络基础 |
| `tool-augmented-digital-human.md` | 工具增强数字人 |
| `voice-ai-digital-human-landscape.md` | 语音 AI 数字人全景 |

## 相关但未复制

- 博客 `raw/` 论文源文件（LaTeX/图）：登记不复制（见 openspec change `init-project-from-projflow` design Open Questions）
- CyberVerse `management/docs/` 6 篇设计总纲：随 CyberVerse 仓库就地阅读（锚定 `4968280`，见 external-sources.md），不复制
