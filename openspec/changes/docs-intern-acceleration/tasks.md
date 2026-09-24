# Tasks: docs-intern-acceleration

## 1. 资料整理（先于动笔，产物需确认）

- [x] 1.1 确认第一手 15+ 模型 SpeedRun / Formal Eval 数据位置；取到则抄录，取不到则该节标"待补"
- [x] 1.2 研读《视频生成训练与推理加速专题》与博客成稿 `video-gen-acceleration`，提取十个工作、四类成本、训练费光谱、本地候选（LIA-X decoder 蒸馏 333ms/帧）与两版侧重差异
- [x] 1.3 研读《digital-human-realtime-gpu-comparison》，提取三指标定义与关系、延迟链三段量级、30+ 模型分路线表（含来源分级与实测行）
- [x] 1.4 研读《CyberVerse 工程专题》与《Ditto 实时化与 TensorRT 加速复盘》，提取瓶颈基线、优化全景三档、编码链路耗时拆解
- [x] 1.5 从 CyberVerse `tasks.json` 提取首帧与开口相关项（t15/t16/t20/t25）的数字与结论
- [x] 1.6 研读《digital-human-engineering-benchmark》《hardware-assessment》，提取 A10 结论表与 LiveAct 结论修正（显存 vs 主机内存、Ampere 无 FP8）
- [x] 1.7 汇总数据表 + 术语表 + 证据强度 + 适用边界 + 待补清单，**在对话中提交审核，不写入仓库**

## 2. 搬迁与写作（1.x 全部确认后启动）

- [x] 2.1 写 `management/docs/数字人概述/数字人加速.md`（见 design 的 8 节大纲 + 3 张图），数字全部溯源整理产物
- [x] 2.2 从《数字人行业全景》删除已迁出的四节并留链接；从《工程设计》删除已迁出的部分并留链接（两篇的 change 同步更新）
- [x] 2.3 自查：结构契约对齐、无编造数字、无越界、无出处标注、无死链；openspec validate 通过并提交

## 3. 生成侧加速的笔记链接（待办）

- [x] 3.1 十篇笔记建成后，已在正文《生成侧加速》四个方向把 10 个工作名替换为文档链接（fpsattention / blade / nar / flashar / latent-spatial-memory / worldattention / zipar / dax / turbodiffusion / inferix）
