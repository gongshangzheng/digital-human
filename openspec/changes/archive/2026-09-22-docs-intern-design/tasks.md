# Tasks: docs-intern-design

## 1. 资料整理（先于动笔，产物需确认）

- [x] 1.1 研读《CyberVerse 工程专题》§一–§五，抄录瓶颈基线表、音频缺口前后对照表、会话回收时间线、性能尝试表、未采纳方案表
- [x] 1.2 研读《Ditto 实时化与 TensorRT 加速复盘》，提取优化全景（生产基线 / 已验证未默认 / 已回退）与"为什么不是 TRT 单点胜利"
- [x] 1.3 从 tasks.json 提取 t1–t25 的描述与进展要点，按主题归类（首帧与开口 / 打断与收声 / 待机与静默 / 画质与流畅 / 会话与内存 / 编码与链路）
- [x] 1.4 研读《Ditto 改动实践》与《视频生成训练与推理加速专题》，提取 PasteBack 两条路径（AF 裁剪框+alpha / Ditto 仿射）与贴回指标（p95 67.3→12.7ms、RTF 0.698→0.588、TTFF 1.39→1.18s、像素 max diff=0）
- [x] 1.5 汇总数据表 + 术语表 + 证据强度 + 适用边界 + 未采纳清单 + 待补清单，**在对话中提交审核，不写入仓库**

## 2. 动笔写作（1.x 全部确认后启动）

- [x] 2.1 写 `management/docs/实习复盘/工程改进.md`（见 design 的 11 节大纲 + 3 张 mermaid 图），数字全部溯源整理产物
- [x] 2.2 自查：结构契约对齐、无编造数字、无越界（系统通论归《CyberVerse框架》）、无出处标注、无死链；openspec validate 通过并提交

## 3. 补写 PasteBack 小节（本轮新增）

- [x] 3.1 explore 贴回代码与修复笔记：`pasteback_utils.py`、`model.py` 的矩阵构造与裁剪入口、Ditto 的 `putback`/`source2info`/`avatar_registrar`、`avatarforcing-pasteback-fluctuation.md`
- [x] 3.2 按 design 第七节改写《工程改进》的 PasteBack 小节：完整链路六阶段 + 三轮修复 + 与 Ditto 的对照 + 参数 + 指标；配一张链路图
- [x] 3.3 自查：无出处路径（代码路径只留 change）、数字溯源、与《数字人加速》边界不重叠（贴回属画质/正确性，速度数字只保留 p95 与前后的性能路径描述）
