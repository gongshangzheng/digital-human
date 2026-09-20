# Design: docs-intern-intro（含待审核大纲）

## Context

- 伞 change 登记表 #1；统一写作骨架（为什么重要 → 现行做法 → 我们的工作 → 改进方向）。
- 目标读者：**自己**（回顾 + 后续推进素材 + 发文选题依据）。
- 定位：**数字人领域入门与路线总览**（教科书视角）；与《数字人行业全景》分工——后者写产业/产品/实测，本文写原理与流派。
- 正文目标路径：`management/docs/实习复盘/数字人介绍与技术路线.md`

## Goals / Non-Goals

**Goals：** 说清"数字人是什么、为什么重要、几条路线怎么做、优缺点、怎么评、我们为何这么选"。
**Non-Goals：** 不写我们的工程/实验细节（链各篇）；不写竞品与实测横评（《数字人行业全景》）。

---

## 【待审核】正文大纲（到二级标题）

### 一、`## 数字人是什么`
- 表达内容：两层划分（数字人模型 vs 数字人系统）；一句话定义；"三个判断问题"（表现质量/表现范围/工程性能）表；常见任务名（换嘴配音/talking head/3D avatar）
- 论证/结论：方案评价先问三问题，任务名不等于路线
- 素材：knowledge/《数字人基础》§一/§二、《5分钟认识数字人》

### 二、`## 为什么重要`
- 表达内容：产品价值（面对面交互临场感）；落地形态（面试官数字人等）；技术价值（多模态集成试炼场）；关键约束（实时性决定可用性）
- 论证/结论：数字人是"可见对话"的载体，实时性是可用性门槛
- 事实分级：产品/技术价值标【待验证·判断】，落地形态【已验证】

### 三、`## 技术路线版图`
- 3.0 `> 框架说明`：**两条轴**——「生成方式」（模型直接预测什么）×「渲染/资产后端」（画面靠什么落地）；两轴可自由组合，不是互斥路线（引《数字人基础》原文）
- **完整路线清单**（依据 `digital-human-avatar-survey` 表 2 的六条 taxonomy + `数字人渲染器专题` §二的 renderer 光谱）：

| # | 路线 | 核心表示 | 代表工作 | 优势 / 限制 |
|---|------|---------|---------|------------|
| 1 | 2D talking-head / latent inpainting | landmarks、mask、latent | MuseTalk、SadTalker | 简单快、生态成熟 / 身体手势弱、3D 一致性弱 |
| 2 | 结构化动作策略 | SMPL-X、FLAME、MANO、VQ motion token | EMAGE、Audio2Photoreal、EMO2 | 可解释可控、动作可单独评估 / 仍需 renderer |
| 3 | 动作扩散 + 快速渲染器 | 低维 motion + warping GAN/renderer | ChatAnyone；**Ditto、Avatar Forcing（我们的主线）** | 实时性强、工程闭环清晰 / 画面自由度低于整帧大模型 |
| 4 | 视频基座模型适配 | video latent、DiT/MM-DiT、ReferenceNet、LoRA | OmniAvatar、HunyuanVideo-Avatar、wan-streamer | 全画幅表达强 / 训练推理重、资产不可复用 |
| 5 | **3D 资产驱动** | 3DGS 高斯 / NeRF 场 / **mesh + blendshape·FLAME rig** | 5a 学习式：GaussianTalker、UIKA、FlexAvatar；**5b 参数化装配式：FLAME/ARKit blendshape + 游戏引擎渲染（工业实时角色，Audio2Face 类）** | 身份可复用、渲染可控 / 注册难、训练成本高、极端动作风险 |
| 6 | 掩码局部多人控制 | face mask + localized cross-attention | HunyuanVideo-Avatar | 可指定说话人 / 依赖 mask |

- 注：**Blendshape/FLAME 作为动作表示的深度内容在《数字人动作》**，这里只作为资产接口与后端出现，一句话 + 链接，不展开
- 补充：**渲染后端视角**（`数字人渲染器专题` §二）——2D warping renderer（Ditto/LivePortrait、LIA-X、FLOAT/AF decoder）、FLAME/3DMM、NeRF/3DGS 专人资产、**ARKit/blendshape/game engine**、视频级后处理（Wav2Lip/LatentSync，非完整 renderer）
- 论证/结论：路线分野在「中间表示 + 渲染后端」；同一任务可由多条路线完成；**「操控 3D 模型」（参数化/rigged + 引擎渲染）是独立且工业成熟的一条路线**，与 5a 学习式资产区分（5b 资产为手工/标准接口，5a 需训练）
- 素材：`digital-human-avatar-survey` 表 2、`数字人渲染器专题` §二/§三、`动作空间专题` 表示谱系

### 四、`## 数字人系统与实时性（现行做法）`
- 表达内容：级联四组件；三种架构（级联/端到端/混合，含 A2-LLM 535ms、级联 3.2s）；两条工程战线（传输层 WebRTC；推理层流式分块）+ 轻量技巧；Agent 能力
- 论证/结论：系统延迟由排队与分块决定，不是单纯模型速度
- 引用：链《CyberVerse框架》看落地形态

### 五、`## 评价口径`
- 表达内容：五大指标族表（唇同步/身份漂移/画质/时序/效率）；"论文 FPS ≠ 产品 SLA"
- 论证/结论：指标各有适用域，身份度量有边界（链《数字人身份》）
- 引用：链《数字人身份》

### 六、`## 我们的选择与理由`
- 表达内容：调研时间线（06-08 启动 → 06-22 选型）；选型结论（GAGAvatar/UIKA 前馈式）；最终体系（CyberVerse + AvatarForcing/Ditto）
- 论证/结论：动作空间便于实时化与控制；前馈式 3D 建 avatar 成本低
- 引用：实测支撑链《数字人行业全景》

### 七、`## 开放问题与改进方向`
- 表达内容：手部+身体统一框架缺位；扩散实时化；身份度量标准化；3D GS 前馈化硬件门槛；【待补】测得的 RTF/显存与延迟数据
- 论证/结论：领域空白即后续选题空间

---

## 【待审核】关键决策点

1. **框架表述**：(A) 两轴为主 + 六条路线清单（survey 口径）【已按 explore 更新】 / (B) 精简为 3–4 条常用路线 / (C) 其他分法 —— 请选
2. **5b rigged mesh 路线证据薄**：工业实时角色（Audio2Face 类）我们没实测 —— 保留为路线介绍（标【待验证】+来源），还是删除？
2. 是否保留 `## 数字人系统与实时性` 与 `## 评价口径` 两节（它们与《CyberVerse框架》《数字人身份》部分交叉，也可压缩为一句+链接）

## 整理清单（动笔前必须完成）

| 来源 | 提取物 | 状态 |
|------|--------|------|
| knowledge/《数字人基础》《5分钟认识数字人》 | 两层划分、分析轴、生成方式三分类、架构、评价口径 | ✅ |
| knowledge/《3dgs-methods-research》 | FlexAvatar 等方法与 VFHQ-Test 指标、A10 可行性 | ✅ |
| knowledge/ 三篇 survey | 分类体系差异、领域挑战、模型线索 | ✅ |
| papers 库 | 按类抽代表模型清单（slug + 一句话） | ✅ |
| knowledge/《project-README》 | 选型结论与时间线 | ✅ |

## Decisions

- **D1 路线框架**：待用户定稿（见决策点 1）；未定稿前不写正文第三节
- **D2 素材留 change、正文进 docs**：整理产物 `openspec/changes/docs-intern-intro/整理-数字人介绍与技术路线.md`（不进 docs）；正文 `management/docs/实习复盘/数字人介绍与技术路线.md`

## Risks / Trade-offs

- [三路线被误读为互斥] → 正文显式说明组合关系
- [路线优缺点缺一手证据] → 优先引 knowledge 表格与 papers 指标，缺的标【待补】

## Open Questions

见"关键决策点"1、2。
