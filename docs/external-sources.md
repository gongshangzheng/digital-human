# 外部代码源与信息源登记表

> 登记先于引用：任何外部源被本仓库引用或索引之前，必须先在此登记。
> 锚定 commit 保证后续外部源演进后引用仍可复现（`git -C <本机路径> show <hash>:<path>`）。

| 源 | 远端 | 本机路径 | 用途 | 引入方式 | 锚定 commit | 状态 |
|----|------|----------|------|----------|-------------|------|
| CyberVerse | github.com/gongshangzheng/CyberVerse | `~/code/CyberVerse` | 实时数字人 Agent 框架优化 fork：avatarforcing / ditto / flash_head / MuseTalk / SoulX-LiveAct 模型插件、流式管线、设计文档 | 独立 clone（不 vendoring） | `4968280b109aa2e31d463bc7cfae1959d3dfa215`（2026-08-04） | active |
| ProjFlow | `~/code/ProjFlow`（上游脚手架） | `~/code/ProjFlow` | 共享脚手架上游：management / papers / evaluation 三模块 + FastAPI + Vue3 | rsync 拷贝派生（本仓库即下游） | 拷贝时工作树快照 | active |
| 博客 | gongshangzheng.github.io | `~/gongshangzheng.github.io` | 数字人论文精读 / 工程解读 / survey / arxiv-digest（~156 篇，导入 `papers/data/`） | 只读提取（元数据 JSON） | 导出时快照 | active |
| InternWiki | `~/code/InternWiki` | `~/code/InternWiki` | 数字人知识库（tangwen 26 篇 + junjiawang voice-agent 系列），复制到 `management/docs/knowledge/internwiki/` | Markdown 复制 | 复制时快照 | active |

## CyberVerse 关键索引路径（锚定 `4968280`）

**模型插件**（Avatar 抽象：`inference/plugins/avatar/base.py`）
- `models/avatarforcing/` — LIA 系 flow matching 运动隐空间生成，双向听说（streaming_avatarforcing.py、af_agent.py、pasteback_utils.py）
- `models/ditto/` — HuBERT→LMDM→六级渲染，TRT fp16（stream_pipeline_online.py + core/）
- `models/flash_head/`、`models/MuseTalk/`、`models/SoulX-LiveAct/`

**设计文档**（`management/docs/`，6 篇）
- `avatarforcing-design.md` — AvatarForcing 设计总纲（身份/动作/合成三段架构、双音频 CFG、anchor guidance）
- `ditto-design.md` — Ditto 设计总纲（三层流式、TRT 加速、RTF 3→0.9）
- `streaming-pipeline.md` — 流式管线
- `paste-back-compositing.md` — 贴回合成
- `silent-avatar-feed-gate.md` — 静音喂料闸门
- `avatar-rtf-latency-over-time.md` — RTF 延迟时序基准

**管理体系**
- `management/projects/digital-human/` — dh-eval 评测框架任务树（t1–t11：Web UI ProjFlow 架构迁移、模型评测集成、Ditto TRT 实时化等）
- `management/team/`（tangwen、guanmu）

**服务架构**：inference gRPC :50051 / Go orchestrator :8080 / TURN :8443 / 前端 :5173，运行于远程 GPU 服务器，本地仅编辑（详见其 AGENTS.md）

## 维护规则

- 外部源引入方式：独立 clone（推荐）/ git submodule / vendored（附 commit），统一存专用目录，禁止与自有代码混层
- 被索引的关键内容随登记表锚定 commit；外部源显著演进时更新本表
- 上游（ProjFlow/InternWiki/博客）在资产进入本仓库后视为冻结历史源，演进在本仓库进行
