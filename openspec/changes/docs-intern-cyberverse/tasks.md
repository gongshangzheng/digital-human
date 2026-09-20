# Tasks: docs-intern-cyberverse

## 1. 资料整理（先于动笔，产物需确认）

- [ ] 1.1 读 CyberVerse README.zh-CN 与 AGENTS.md，提取定位、功能特性、端口表（50051/8080/8443/5173）与部署纪律
- [ ] 1.2 读 `inference/` 结构（core/plugins/services/rag/generated）与 AvatarPlugin 抽象，提取插件体系与接口
- [ ] 1.3 读 `server/internal/` 与 `proto/*.proto`，提取编排模块职责与七个 gRPC 接口
- [ ] 1.4 读 `models/` 五模型接入形态（插件路径），链论文笔记
- [ ] 1.5 读 knowledge/ 竞品框架三篇（open-avatar-chat-liteavatar / lite-avatar-source-code-analysis / ultralight-digital-human-source-read）+ cyberverse-realtime-digital-human-agent，整理框架版图对勘
- [ ] 1.6 从 management/projects/cyberverse/tasks.json 提取我们的改造任务（t1–t25）归类
- [ ] 1.7 汇总架构图 + 插件/模型清单 + 端口部署表 + 改造清单 + 竞品对勘，**在对话中提交审核，不写入仓库**

## 2. 动笔写作（1.x 确认后启动）

- [ ] 2.1 写 `management/docs/实习复盘/CyberVerse框架.md`（为什么需要框架 → 现行做法/版图 → 架构 → 模型接入 → 部署形态 → 我们的改造 → 改进方向）
- [ ] 2.2 自查：与《工程改进》边界（只列落点）、代码路径与 @4968280 实际结构一致；openspec validate 通过并提交
