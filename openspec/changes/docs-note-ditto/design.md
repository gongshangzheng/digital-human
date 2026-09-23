## Context

`management/docs/论文笔记/` 目前只有 `avatar-forcing.md` 一篇。`ditto.md` 是清单里的下一篇，也是 `avatar-forcing.md` 的对照篇：两篇同属「运动空间 + 流式实时」，但锚定方式相反——Ditto 靠逐帧参考注册与渲染期外观、Avatar Forcing 靠块因果递归 latent。素材已就绪：`.cache/article-note/ditto/`（arXiv HTML v3 + PDF + 6 张原图 + 6 个确认 lane），`validate-analysis.py` 通过；papers 库条目为 `arxiv-2411.19509`。

## Goals / Non-Goals

**Goals：**

- 产出 10 节骨架的 `ditto.md` + 同名 sidecar，把论文机制、数字、可控性与流式链路讲清，并把我们的工程层裁决压缩进第 8 节。
- 用两处**代码级澄清**补论文与知识库都没有写清的事：265 维的真实构成、以及「66 是离散 bin 而非 66 个自由度」。
- 把三类口径边界写进正文而不是留给读者踩：三层 RTF 不可合并、长时归一化漂移不属 Ditto、前 3.2 秒音画错位仍未定因。

**Non-Goals：**

- 不复制 `数字化人概述/数字人身份`、`数字人加速` 的实验矩阵与数字（只做结论与链接）。
- 不写 Avatar Forcing 的漂移机制（属已归档的 `avatar-forcing.md`），只在第 8 节做一句对照。
- 不改代码、训练配置、推理参数；不新增知识库文档。
- 不补跑实验、不伪造未披露配置。

## 1. 论文速览

| 项 | 值 |
|---|---|
| 标题 | Ditto: Motion-Space Diffusion for Controllable Realtime Talking Head Synthesis |
| 作者 | Tianqi Li、Ruobing Zheng、Minghui Yang、Jingdong Chen、Ming Yang |
| 单位 | 蚂蚁集团（论文署名未在 HTML 正文给出，落笔前回 PDF 首页核对） |
| venue / 年份 | ACM MM 2025 |
| arXiv | `2411.19509`（HTML/PDF 均为 **v3**，PDF CreationDate 2025-05-01） |
| 代码仓库 | 论文声明开源；**我们接入的是 CyberVerse `models/ditto/`**（锚定 `4968280`） |
| papers 库 | `arxiv-2411.19509` |
| 素材 | `.cache/article-note/ditto/`（paper.txt 派生自 HTML v3、PDF、6 张原图、6 lane 分析） |

## 2. 一句话价值主张（≤100 字）

把扩散目标从冗余的 VAE latent 换到 LivePortrait 定义的 **265 维运动空间**，用条件 DiT 生成身份无关运动、再交给参考锚定的渲染器还原画面，从而同时拿到 **细粒度可控**（区域/幅度/注视/情绪）与 **单卡实时**（RTF 0.635 离线、0.895 在线、首帧 385ms）。

## 3. 笔记结构大纲

### 3.1 目标文档架构（全文落点）

新建单篇 `management/docs/论文笔记/ditto.md`，沿用 10 节骨架（口径同 `论文笔记/README.md` 与 `note-structure-template.md`），阅读顺序与落点如下：

| 节 | 标题 | 承载什么 | 配图/公式/图 | 字数 |
|---|---|---|---|---|
| 0 | 论文信息 | 元信息表 + 「与我们接入的 CyberVerse 版本」说明 | 表格 | 150 |
| 1 | 一句话总结 | 价值主张 + 4 条贡献（换空间 / 可控制 / 实时 / 解耦） | 列表 | 200 |
| 2 | 问题与动机 | 论文两条 critical issues：**控制缺失** 与 **推理慢**；VASA-1 的隐式表示不支持控制 + 源码未公开 | 对照小表 | 500 |
| 3 | 方法精析 | 3.1 运动空间（$\mathbf{m}$ 不含 $\mathbf{c}$、式(1)(2)(3)）；3.2 条件 DiT 与 ECS/ICS；3.3 训练三策略与损失式(4)(5)(6)；3.4 可控性（21×3 探针、区域/幅度、gaze 修正） | 图 1 `framework`、图 2 `dit`、图 3 `bs`、Mermaid 主链路、式(1)(2)(3)(6) | 1300 |
| 4 | 训练与实现细节 | 十项配置披露表；**训练与推理的参考条件取法差异**单独标出；265 维构成表 | 配置表 + 265 维表 + `265 = 1 + 66×3 + 3 + 63` | 700 |
| 5 | 推理与系统链路 | 三模块流式优化（HuBERT KV cache 0.4s、segment-wise fusion 中心加权、50→10 步、TensorRT、FFmpeg）；**三层 RTF 口径对照表** | Mermaid 时序 + 表 5/6 + 口径对照表 | 600 |
| 6 | 实验与结果 | 表 1（Talk9）、表 2（HDTF100）、表 3（盲测）、表 4（消融）+ 定性结论；gaze 消融 | 图 4 `comp_2`、图 5 `res`、图 6 `gaze_correction` + 四张表 | 1000 |
| 7 | 相关工作与定位 | GAN→EMO→EchoMimic/Hallo/Loopy 与 VASA-1 两条脉络；四轴定位表 | 定位表 | 400 |
| 8 | 局限与启发 | 论文局限（naturalness 偏弱及归因、依赖 LivePortrait 组件）+ 我们的实测（唇动隔离、3.2 秒错位未定因、`fix_kp_cond` 回锚机制）+ 可操作启发 | 「论文局限 vs 我们结论」对照表 | 600 |
| 9 | 术语与符号表 | 术语表 + 符号表 + 三处符号冲突说明 | 两张表 | — |
| 10 | 相关文档 | 知识库精读三篇 + 数字人身份/动作/加速 + papers 条目 | 链接列表 | — |

**跨文件触点**（唯一一处）：`论文笔记/README.md` 现有清单里 `ditto.md` 状态由「待写」改为「已完成」。

### 3.2 逐节要点与素材来源

| 节 | 要点（只写有据可查的） | 素材来源 | 缺料替代 |
|---|---|---|---|
| 2 | 两条 critical issues 的原文依据；VASA-1「motion-appearance 解耦空间 + DiT」为何被当作起点、它的两点不足 | `citation.md` 1/4；`methodology.md` A | 无缺口 |
| 3.1 | Motion Extractor 四项输出与形状；$\mathbf{m}=\{\boldsymbol{\delta},\mathbf{R},\mathbf{t}\}$ 为何 identity-agnostic；式(1)(2) 只差运动项 ⇒ 身份钉在渲染入口；式(3) renderer 学 warp 场 | `methodology.md` B | $K$ 论文未给，用 §3.2.3 的 21 点反推并注明 |
| 3.2 | 四个条件信号各自解决什么；ECS 走 cross-attention、ICS 与噪声拼接；$\mathbf{C}$ 五分量 | `methodology.md` C | 无缺口 |
| 3.3 | flip 的真实动机（头朝向偏置，不是普通增强）；自适应权重的分组+epoch 差+softmax；lipsync 选 ckpt；$\mathcal{L}_d/\mathcal{L}_t/\mathcal{L}_{ini}$ 三项作用 | `methodology.md` D | 三项权重系数论文未披露 ⇒ 写「等权相加，未披露系数」 |
| 3.4 | 63 维=21×3；第 34 维右眼、第 58 维张嘴（≈ARKit jaw open）；区域/幅度控制；gaze 的模板视频 + $\boldsymbol{\delta_e}=\mathcal{K}(\mathbf{R_e})$ + $\boldsymbol{\delta}_{correct}$ | `methodology.md` E；图 `bs` | 逐维语义表未给全 ⇒ 只写论文点名的两维 |
| 4 | 50h/330 identities/均 150s；8×A100、batch 1024、Adan、1e-4、wd 0.02、500 epochs；25fps；$L=80$ 帧；训练期 $m_{ref}$ 取前一帧、$c_{ref}$ 取同 clip 随机帧 vs 推理期都取源图；**265 维构成** | `experiment.md` 4.1；`code-analysis.md` C1 | 机时/种子未披露 ⇒ 写「未披露」 |
| 5 | 三个模块的单步耗时与 RTF；offline/online × 头/全身的 RTF 与 FFD；online 为何需要更长重叠；三层口径的对象与硬件 | `methodology.md` F；`experiment.md` 表 5/6；`code-analysis.md` C3 | Table 1 与 Table 6 环境不可断言同一 ⇒ 并列不合并 |
| 6 | 表 1–4 全量数字 + 粗体/下划线含义；GT 行不参与排名；表 2 的 † 与表 3 的 10 人 20 clips | `experiment.md` 全表 | 补充材料未获取 ⇒ 正文不引补充视频证据 |
| 7 | 四轴定位表；VASA-1 无公开代码 ⇒ 无同协议数值 | `citation.md` 4 | 引用号到条目的完整映射需回 PDF References 核对 |
| 8 | naturalness 48.7% vs Hallo2 59.3% + 作者归因；唇动隔离 v1→v2→kp 修复与 LSE 表；外观类 LoRA 已否决；闭嘴源 LatentSync；前 3.2 秒错位未定因；`fix_kp_cond` 默认关闭 | `experiment.md` 表 3；`code-analysis.md` C4/C5/C6 | 跨素材与人工判定未完成 ⇒ 明写边界 |
| 9 | 术语表 + 符号表 + 三处冲突（$K$ 一符两义、$L$ 与 $\mathcal{L}$、论文 $\mathbf{m}$ vs 部署命名） | `terminology.md` | 无缺口 |

## 4. 口径与取舍

- **D1 论文数字只来自表内**：表 1/2 的基线数字中带 † 的来自 Hallo2 论文，属跨来源；正文必须标注，不写成自跑。
- **D2 用户的工程层压成第 8 节**：完整实验矩阵（隔离演进全表、TRT 三层优化、编排层六项修复）留在 `knowledge/Ditto 改动实践.md`、`Ditto 实时化与 TensorRT 加速复盘.md` 与 `数字人概述/数字人加速.md`，本篇只留结论 + 链接。
- **D3 三层 RTF 必须带对象与硬件**：模型侧 0.635/0.895（A100+TRT）、生产端到端 ≈0.997、编排层 2.80→0.937，禁止合并成单一倍数。
- **D4 长时稳定性只写 Ditto 侧证据**：`fix_kp_cond=0` 默认 + 逐帧参考注册/贴回构成锚定；「头部逐渐放大的漂移」明确归属 Avatar Forcing 线，不写进本篇。
- **D5 naturalness 必须成对呈现**：写「视觉质量与唇同步最优」时必须同时给 naturalness 48.7% 与 Hallo2 59.3%。
- **D6 不写正文行号**：代码级事实只写文件与功能（如「部署侧在 `motion_stitch` 里用固定索引做唇/眼掩码」），避免随代码漂移失效。
- **D7 可选省略**：第 5 节的工程改造细节、第 7 节的 Loopy 单篇导读、补充材料视频证据均可省略或压成一句。

## 5. 图表公式清单

**图片**（发布到 `management/docs/_assets/ditto/`，WebP，最长边 ≤1600px、单图 ≤500KB、单篇 ≤5MB）

| 笔记图号 | 源文件 | 用在哪 | 论文图 | 发布前处理 |
|---|---|---|---|---|
| 图 1 | `framework.png` | §3 主链路（模块归属 ℳ/ℱ/𝒢/𝒯/ℋ） | Fig 1 | 缩到 1600 + WebP |
| 图 2 | `dit.png` | §3 条件 DiT 结构 | Fig 2 | 体积合规，仅转 WebP |
| 图 3 | `bs.png` | §3 可控性（逐维探针语义） | Fig 3 | 不缩放，压到 ≤500KB |
| 图 4 | `comp_2.png` | §6 定性对比（含伪影箭头） | Fig 5 | 缩到 1600 + WebP |
| 图 5 | `res.png` | §6 跨风格/尺度与可控性 | Fig 4 | 缩到 1600 + WebP（压缩比最高） |
| 图 6 | `gaze_correction.png` | §6 gaze 消融（§3 gaze 段回链） | Fig 6 | 缩到 1600 + WebP |

每图必须有图题与正文解读；正文图号按笔记出现顺序重排，不沿用论文编号。

**公式**（KaTeX `$$...$$` + 符号表）

1. $\mathbf{x_{ref}} = \mathbf{c_{ref}}\mathbf{R_{ref}} + \boldsymbol{\delta_{ref}} + \mathbf{t_{ref}}$（式 1）
2. $\hat{\mathbf{x}} = \mathbf{c_{ref}}\hat{\mathbf{R}} + \hat{\boldsymbol{\delta}} + \hat{\mathbf{t}}$（式 2）
3. $\hat{I} = \mathcal{G}(\mathbf{f_{ref}}, \mathbf{x_{ref}}, \hat{\mathbf{x}})$（式 3）
4. $\mathcal{L} = \mathcal{L}_d + \mathcal{L}_t + \mathcal{L}_{ini}$（式 6；$\mathcal{L}_t$ 含速度/加速度两项）
5. $265 = 1_{\text{scale}} + 66\times3_{\text{pitch/yaw/roll}} + 3_{\mathbf{t}} + 63_{\text{exp}}$（工程层等式，非论文公式，标注来源为部署代码）

**Mermaid**：主链路时序 1 张（音频 → HuBERT → DiT → $\hat{\mathbf{m}}$ → renderer → 帧，含流式切分与中心加权融合）；训练/推理参考条件差异可并入同一张的分支，不单独再画。

**表格**：十项配置披露表、265 维构成表、表 1–4（论文）、表 5/6（论文）、三层 RTF 口径对照表、四轴定位表、术语表、符号表、「论文局限 vs 我们结论」对照表。

## 6. 引用关系

- `[[knowledge/Ditto 模型精读|Ditto 模型精读]]`、`[[knowledge/Ditto 改动实践|Ditto 改动实践]]`、`[[knowledge/Ditto 实时化与 TensorRT 加速复盘|Ditto 实时化与 TensorRT 加速复盘]]`
- `[[knowledge/动作空间专题|动作空间专题]]`、`[[knowledge/音画同步专题|音画同步专题]]`、`[[knowledge/数据集整理专题|数据集整理专题]]`、`[[knowledge/评测指标专题|评测指标专题]]`
- `[[数字人概述/数字人身份|数字人身份]]`、`[[数字人概述/数字人动作|数字人动作]]`、`[[数字人概述/数字人加速|数字人加速]]`、`[[数字人概述/工程设计|工程设计]]`
- `[[论文笔记/avatar-forcing|Avatar Forcing 模型笔记]]`（第 8 节一句对照）
- sidecar `related`：`papers/arxiv-2411.19509`、上述 knowledge/数字人概述条目；`changelog` 记首次创建。

## 7. 风险与待确认项

**需用户裁决**

1. **视频源模式的 pose 来源口径冲突**：代码 `motion_stitch.py:319-325` 在 `is_image_flag=False` 时默认 `use_d_keys=("exp",)`（pitch/yaw/roll/t/kp/scale 逐帧取自源帧），而知识库两篇写「头动仍由 `x_d` 的逐帧 pose 承载」。三种处理方式：(a) 按代码写，并把知识库列为待修正；(b) 按知识库写，把代码默认值视为已变更；(c) 本篇**回避细节**，只写「视频源模式下外观与骨架取自源帧」，把冲突留在 change 记录里。**倾向 (c)**，因为它不阻塞笔记且不产生新的错误陈述。

**风险与处理**

- [naturalness 数字被写成「全面最优」] → D5 强制成对呈现，表格保留 Hallo2 的 59.3% 粗体。
- [三层 RTF 被合并] → D3 + 口径对照表，每行标对象与硬件。
- [把 AF 的漂移归因写到 Ditto] → D4，并在第 8 节写明该结论归属 Avatar Forcing 线。
- [`bs.png` 只有 730px 且是多面板，正文可能看不清] → 发布前目视复核；若不可读，改在正文只写论文点名的第 34/58 维，图退为佐证。
- [图片许可未核实] → 沿用 `avatar-forcing.md` 已确立的论文原图发布惯例，保持一致。
- [论文未披露项被填满] → 机时、随机种子、三项损失权重系数一律写「未披露」。
- [引用号→条目映射未核] → 第 7 节若要点名 Loopy 等，先回 PDF References 核对，否则不点名。

## Migration Plan

1. 用户审核本 design（尤其第 3 节架构、第 5 节配图、第 7 节待裁决项）。
2. apply 阶段：发布图片（`figures.py inspect/convert/publish`）→ 写正文 → 写 sidecar → 改 `论文笔记/README.md` 一行。
3. 校验：`validate-note.py`、`check-delivery.py`、锚点与内链实点、`openspec validate docs-note-ditto --strict`；任一不过则回退本次改动。
