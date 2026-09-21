# Tasks: docs-intern-industry

## 1. 资料整理（先于动笔，产物需确认）

- [ ] 1.1 确认第一手横评数据位置（digital_human 平台 / 远端 / 其他路径）；取到则抄录 15+ 模型指标表，取不到则明确记为待补
- [ ] 1.2 研读《digital-human-realtime-gpu-comparison》，提取 FPS/TTFF/RTF 定义与关系、延迟链分解、30+ 模型分路线对比表（标注来源类别与读表纪律）
- [ ] 1.3 研读《digital-human-engineering-benchmark》《hardware-assessment》，提取四个硬件层级、LiveAct 18B 主机内存瓶颈、A10 可行性结论
- [ ] 1.4 研读竞品与产品素材（LiveTalking 四层架构与商用、OpenAvatarChat/LiteAvatar/Ultralight、CyberVerse GPLv3 约束、产品侧五层技术栈与全双工语音 LLM）
- [ ] 1.5 研读《模型探索与未采纳实验复盘》，提取待复跑清单与证据等级定义
- [ ] 1.6 汇总数据表 + 术语表 + 证据强度 + 适用边界 + 待补清单，**在对话中提交审核，不写入仓库**

## 2. 动笔写作（1.x 全部确认后启动）

- [ ] 2.1 写 `management/docs/实习复盘/数字人行业全景.md`（见 design 的 9 节大纲 + 3 张 mermaid 图），数字全部溯源整理产物
- [ ] 2.2 自查：结构契约对齐、无编造数字、无越界（原理与流派归《数字人介绍与技术路线》）、无出处标注、无死链；openspec validate 通过并提交
