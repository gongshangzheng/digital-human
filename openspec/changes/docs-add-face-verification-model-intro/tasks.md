## 1. 设计确认与素材核实

- [x] 1.1 ✅ 已确认（见 design.md `## Resolved Decisions`）：仅人脸、slug `face-verification-models.md`、压缩《数字人身份》重复解释、第 5 节标题不冠"ArcFace 之后"、§6 只留 ☆ 6 篇。
- [x] 1.2 ✅ 已探测：`PROXY_OFF`（VPN 未连）；已用 OpenAlex 直连 + Semantic Scholar 完成白名单核实，结果与素材获取状态写入 design.md Decision 4。待 VPN 可用时补核实 OpenS2V-Nexus 与需全文支撑的公式/数值。
- [x] 1.3 ✅ 已核实损失谱系组（FaceNet / NormFace / SphereFace / CosFace / ArcFace / Center Loss，含 DOI + arXiv）；ArcFace 公式链取自本地博客深读页（`arcface-2018.html`）。
- [x] 1.4 ✅ 已核实自适应改进组（CurricularFace / MagFace / AdaFace / ElasticFace / UniFace / Fair Loss）并取到摘要原文。
- [x] 1.5 ✅ 已核实评测与边界组（LFW / MegaFace / IJB-C / MS-Celeb-1M / WebFace260M / Masked Face Challenge + 生成侧 ☆ 6 篇）；OpenS2V-Nexus 已决定不引用。
- [x] 1.6 ✅ 已在对话中提交素材摘要（问题设定 / 机制 / 代价与边界 / 拟用章节），用户确认口径"按你说的来"。

## 2. 技术介绍正文与元数据

- [x] 2.1 创建 `management/docs/技术介绍/face-verification-models.md`，补 `title` / `author` / `date` / `tags` / `summary` / `order: 20`。
- [x] 2.2 按 design 第 1、2 节写任务定义、开集设定、统一接口与评测指标 / 基准代际，附任务小表与 Mermaid 图。
- [x] 2.3 按 design 第 3 节写损失谱系与 ArcFace 公式（`L1→L2→L3` + 统一 `(m1,m2,m3)` 框架），配符号表、margin 族对照表与谱系图。
- [x] 2.4 按 design 第 4 节写数据、骨干与大规模分类器工程，给出"先看数据与骨干，再谈损失"的结论。
- [x] 2.5 按 design 第 5 节写"自适应 margin 与鲁棒性改进"（标题不冠"ArcFace 之后"；后继者的问题写进本节正文与结论），配方法对照表与谱系图。
- [x] 2.6 按 design 第 6 节写"作为数字人度量与损失时，人脸识别模型的边界"，给出四角色挪用图、失效机制表，只引 ☆ 6 篇，其余机制叙述指向库内文档；不复制项目实测数值。
- [x] 2.7 按 design 第 7、8 节写场景选型对照表与术语 / 符号表。
- [x] 2.8 创建同名 sidecar JSON，登记 `changelog` 与 `related`（数字人身份、identity-consistency、dpo）。

## 3. 既有文档收敛

- [x] 3.1 修改 `management/docs/数字人概述/数字人身份.md`：三族度量表的编码器枚举加链、Mermaid 节点与"借来的尺子"段落的通用解释压缩为链接（+7/-7 行），项目实测、数值、表格、图原样保留。
- [x] 3.2 无需更新 sidecar：`数字人概述/` 目录下所有文档均无同名 sidecar JSON，按现状不动。

## 4. 验证与交付

- [x] 4.1 校验 frontmatter 必填项齐全、sidecar JSON 合法（`json.load` 通过，`related` 为对象数组）。
- [x] 4.2 核验站内链接与锚点：4 个链接目标均存在，且全部出现在 `/api/management/docs` 列表里。
- [x] 4.3 检查公式定界符（189 个 `$`，无奇数行、无 `\(`/`\[`）、5 个 Mermaid 块围栏配对、标题层级不跳级。
- [x] 4.4 文档顺序工具确认 `技术介绍/` 为 10 → 20，无重复 order，未运行 `renumber`。
- [x] 4.5 经 FastAPI 校验：列表含 `技术介绍/face-verification-models`（order 20），详情接口 200、`sidecar.related` 三个 slug 全部解析成功；`数字人概述/数字人身份` 详情仍 200。
- [x] 4.6 运行 `openspec validate docs-add-face-verification-model-intro --strict` 通过；`git status` 仅含预期的三处改动。
