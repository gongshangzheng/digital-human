## Context

`论文笔记/` 已有 22 篇，绝大多数是**生成模型**（流式 portrait / 视频生成加速 / 分词器）。本篇是其中**第二篇"工具型"论文**（第一篇是 `face-vid2vid` 那类表示层工作、更准确说本篇是**重建/跟踪**类）：它不生成任何画面，只输出**几何线索与 FLAME 参数**，被别的模型当监督信号或驱动信号用。

它的价值集中在三点：

- **它是 PerformRecast 的监督来源**：PerformRecast 用 Pixel3DMM 跟踪的 49 个显式 3D 关键点做 FLAME Loss，才敢丢掉 LivePortrait 的四项辅助损失与第二训练阶段；
- **成本极低且数据全公开**：2×A6000 / 3 天（batch 40），论文把它当作卖点并与 Sapiens 对比；
- **它的第三条局限正好是我们的判据**：§6 明说基于优化的方法无法完美区分 identity 与 expression 参数，需要专门设计的先验。

素材：`.cache/article-note/pixel3dmm/`（HTML 254 KB 含全部题注、PDF、6 张原图）。本地 arXiv 版本为 **v1（2025-05-01）**，abs 页无后续版本；**ICLR 2026 的会议信息来自博客 `uika-2026`，arXiv 上没有标注**，笔记须如实区分。

## Goals / Non-Goals

**Goals：**

- 产出 10 节骨架的 `pixel3dmm.md` + sidecar，讲清"**先学像素级几何线索 → 再优化 FLAME**"的两段式与两条用法（单图拟合 / 单目视频跟踪）。
- 把三处**容易被二手引用带错**的事实写死：骨干是 **DINOv2**、主干**未冻结**（lr 降 10×）、**DPT 头被实验否掉**。
- 登记成本与数据规模：976K 图 / 1000+ 身份、IC-Light 光照增广、2×A6000 × 3 天、拟合 500 步 ≈ 30 秒。
- 第 8 节写与数字人的接口：它是 tracking/监督来源而非生成模型；成本门槛对我们有利；§6 第三条局限接进第七章判据；我们评测框架已有 `driving_mode: pixel3dmm`。
- 保留 5 张原图，每图配图题与正文解读。

**Non-Goals：**

- 不复现、不做本地实验；不宣称它已用于我们的生产链路（只有评测框架接入这一条事实）。
- 不修改第七章正文（另一个 change）。
- 不逐格抄录 Tab.2/3/4/5 的全部数字——主结果给结论与关键列，其余引用表号。
- 不把博客 `uika-2026` 的对照（Pixel3DMM 在头发边界不如 UIKA 平滑）写成**本篇论文的结论**。

## 1. 论文速览

| 项 | 值 |
|---|---|
| 标题 | Pixel3DMM: Versatile Screen-Space Priors for Single-Image 3D Face Reconstruction |
| 作者 | Simon Giebenhain、Tobias Kirschstein（TUM）、Martin Rünz（Synthesia）、Lourdes Agapito（UCL）、Matthias Nießner（TUM） |
| 单位 | 慕尼黑工业大学（TUM）、Synthesia、伦敦大学学院（UCL） |
| venue / 年份 | arXiv `2505.00615`（**仅 v1**，2025-05-01）；博客 `uika-2026` 记为 **ICLR 2026**（arXiv 无对应标注，笔记须注明来源） |
| 项目页 | https://simongiebenhain.github.io/pixel3dmm |
| 代码仓库 | 论文正文与 abs 页**未见代码链接**（项目页存在） |
| papers 库 | 未入库（frontmatter 只写 `arxiv_id`） |
| 素材 | `.cache/article-note/pixel3dmm/`（HTML 正文、PDF、6 张原图） |

## 2. 一句话价值主张（≤100 字）

不直接回归 3DMM 参数，而是先用两个 ViT 预测**逐像素法向与 UV 坐标**（screen-space prior），再拿这些线索**约束 FLAME 参数的优化**：双流 ViT 建在 **DINOv2** 特征上（主干 lr 降 10×、不冻结），用 **1000+ 身份 / 976K 图像**（NPHM + FaceScape + Ava256 对齐 FLAME 拓扑）训练，**2×A6000 训 3 天**；在自建基准的 posed 几何精度上超出最强基线 **15% 以上**。

## 3. 笔记结构大纲

### 3.1 目标文档架构（全文落点）

新建 `management/docs/论文笔记/pixel3dmm.md`，10 节骨架；`order` 取**当前最大 +10**（实施前用 `docs_order.py list` 复核——并行会话仍在持续新增）：

| 节 | 标题 | 承载什么 | 配图/公式/表 | 字数 |
|---|---|---|---|---|
| 0 | 论文信息 | 元信息表 + 「arXiv 仅 v1 / ICLR 2026 来自博客」说明 + 「papers 库未入库」 | 表格 | 180 |
| 1 | 一句话总结 | 价值主张 + 4 条贡献（逐像素几何先验 / UV 查表式 2D 顶点损失 / 单目视频跟踪 / posed+neutral 双任务基准） | 列表 + 图 1 | 260 |
| 2 | 问题与动机 | 单图 3D 人脸重建的两条路线（端到端回归 vs 优化式）与作者的两段式选择 | 图 1 + 路线对照 | 600 |
| 3 | 方法精析 | 3.1 学习像素级对齐几何线索（架构 / 数据准备与配比 / 光照增广 / 训练目标）；3.2 单图 FLAME 拟合（参数集 / 2D 顶点损失 / 法向损失 / 优化）；3.3 单目视频跟踪（冻结项 / 批量 / 时序平滑） | 图 2 + Mermaid ×2 + 式 3/4–8/9 | ≥1500 |
| 4 | 训练与实现细节 | 数据、配比、优化器、lr、batch、硬件、步数、拟合耗时、未披露项 | 10 项配置披露表 | 700 |
| 5 | 推理与系统链路 | 两段式推理（前向预测 → 拟合 500 步 ≈ 30 s）；视频跟踪的冻结与批量策略；与我们评测框架 `driving_mode` 的接点 | Mermaid 时序 | 600 |
| 6 | 实验与结果 | 自建基准（posed / neutral）、协议（Chamfer / NC / R2.5）、主结果（>15%）、既有基准（FaceScape / NoW）、法向估计、拟合消融 | 图 3、图 4、图 5 + 表格 | 1200 |
| 7 | 相关工作与定位 | 前馈 FLAME 回归器（DECA / EMOCA / MICA）与优化式方法；DINO 特征用于稠密预测；与 UIKA / FlexAvatar / PerformRecast 的关系 | 谱系表 | 500 |
| 8 | 局限与启发 | 论文三条局限 + 我们的口径（成本低 / 非生成模型而是监督来源 / driving_mode 已接入 / 与第七章判据的接口） | 「论文局限 vs 我们结论」表 | 900 |
| 9 | 术语与符号表 | 术语 + 符号 + 四处易错命名 | 两张表 | — |
| 10 | 相关文档 | performrecast、face-vid2vid、liveportrait、3dgs 研究、第七章 | 链接列表 | — |

**跨文件触点**（唯一一处）：`论文笔记/README.md` 中 `pixel3dmm.md` 状态改「已完成」。

### 3.2 逐节要点与素材来源

| 节 | 要点 | 素材来源 | 缺料替代 |
|---|---|---|---|
| 2 | 端到端回归丢细节、优化式需要好的先验；作者选择"**先用网络给出像素级线索、再用线索约束优化**"的两段式 | HTML Abstract、§1、Fig 2 题注 | 无缺口 |
| 3.1 | 两个 ViT（法向 / UV）建在 **DINOv2** 上；头 = 4 个 transformer block + 3 次上卷积（32²→256²）+ 线性层，unpatchify 到 512²×c（$c=3$ 法向、$c=2$ UV）；主干**不冻结**、**lr 降 10×**；训练目标是最直白的逐像素 L2 + 前掩码（式 3） | §3.1.1、§3.1.3 | — |
| 3.1 数据 | NPHM（470×23×40 = 376K）、FaceScape（350×20×50 = 350K）、Ava256（每人 50 个最分散表情 ×20 相机 = 250K，**无高保真几何、只监督 UV 网络**）；合计 1000+ 身份 / 976K 图；FaceScape/Ava256 用 **IC-Light** 做光照增广 | §3.1.2 两个小标题 | — |
| 3.2 | 优化量：FLAME identity(300)/expression(100)/jaw/头姿 + 相机 R/t/焦距/主点（式 4/5）；**2D 顶点损失**：分割掩码去掉背景/眼球/口腔 → 用模板 UV 在预测 UV 图上最近邻查表得 $p^*_v$（式 6）→ 带 $\delta_{uv}$ 阈值指示函数的 2D 距离（式 7）；法向损失 $\mathcal{L}_n$；优化细节与权重 | §3.2.1、§3.2.2、式 6–8 | 式 8 的完整形式与权重须对照 PDF |
| 3.3 | 扩到整段视频：首帧估初值后**冻结 identity、焦距、主点**；先逐帧顺序优化，再批量（$B=\min(T,16)$）优化；加**时序平滑项**（式 9，作用于表情/下颌/头姿/平移） | §3.3、式 9 | — |
| 4 | 两网络各自训练；Adam、batch 40、lr 1e-4（头）/1e-5（主干）、**2×A6000 × 3 天**；拟合 500 步、**≈30 秒（未优化实现）**、$\lambda_{uv}=2000$、$\lambda_n=200$、$\lambda_{id}=0.15$、$\lambda_{ex}=0.01$、lr_id 0.001、lr_ex 0.003；训练总 GPU 小时**未披露** | §5.1 | 未披露项写「未披露」 |
| 5 | 两段式：前向预测法向/UV → 优化 FLAME 参数（单图 30 s；视频含批量与平滑）；与 `3dgs-methods-research` 里 `driving_mode: pixel3dmm`（依赖 `easy-pixel3dmm` + `pytorch3d` + `nvdiffrast`）对应 | §3.2/§3.3、`knowledge/3dgs-methods-research.md` | 我们侧接入细节只引用，不展开 |
| 6 | 自建基准：**posed**（保真度）与 **neutral**（形状/表情解耦）双任务，首个同时评测两者；GT 来自 NeRSemble（COLMAP）；协议：对齐+分割去非面部 → 单向 Chamfer L1/L2、法向余弦 NC、R2.5；主结论 posed 超最强基线 **>15%**；既有基准 FaceScape / NoW；法向估计；拟合消融 | §4.1/§4.2、§5.1–5.7、Tab.1–5 | Tab.2/3/4/5 数值写作时回填 |
| 7 | 两条路线对照；DINO 特征用于稠密预测；与 UIKA（同配方但改边界平滑）、FlexAvatar（用其估 FLAME）、PerformRecast（用其做显式监督）的关系 | §2、博客页对照（标明来源） | 引用文献只点名 |
| 8 | 论文局限：① 先验网络**不能利用多视角**（未来可借鉴 DUSt3R / RollingDepth）；② 若要训大规模 3DMM 条件生成模型，需要更快重建 → 可把逐像素预测器**蒸馏成前馈 3DMM 预测器**；③ **基于优化的方法无法完美区分 identity 与 expression，需要专门设计的先验**。我们的口径：成本低（A6000 级可训、数据全公开）、它是监督/驱动来源而非生成模型、评测框架已接入、第 ③ 条与第七章判据同轴 | §6、`knowledge/3dgs-methods-research.md` | 无本地实测 ⇒ 只做接口说明 |
| 9 | 术语/符号 + 四处易错（**DINOv2 非 DINOv3**；主干**未冻结**；**不用 DPT 头**；screen-space prior ≠ 参数空间先验；posed ≠ neutral） | §3/§4 | — |

## 4. 口径与取舍

- **D1 骨干与头必须写对**：**DINOv2 ViT-Base + 轻量头**，主干**不冻结而是 lr 降 10×**；论文明确说 DPT 头只增加耗时、不提升下游重建，Sapiens-300M 骨干同样"高成本无收益"。这是最容易从二手引用带错的一处（博客 UIKA 页描述的 frozen DINOv3 + DPT head 是 **UIKA 自己的**配方）。
- **D2 会议信息标注来源**：arXiv 上**只有 v1（2025-05-01）**、无会议标注；"ICLR 2026"来自博客，正文须写明"博客记为 ICLR 2026，arXiv 未标注"。
- **D3 与 UIKA 的对照不写成本篇结论**：那个"头发边界不如 UIKA 平滑"是博客页的对照评测，不是本文结论，引用时标注来源。
- **D4 成本口径**：只写论文给的"2×A6000 × 3 天"与"拟合 500 步 ≈ 30 秒（未优化实现）"，**不折算**其他卡型；训练总 GPU 小时论文未给。
- **D5 R2.5 与 Chamfer 的定义要写全**：R2.5 = GT 点到最近网格面 ≤2.5mm 的比例；Chamfer 是**单向**（GT → 预测网格面）。
- **D6 数据可用性**：三个数据集公开，但**代码未见链接** → 复现需自己实现；这一点要写在「已知证据与代价」里。
- **可选省略**：法向估计那一节只给结论与表号，不展开其指标口径细节。

## 5. 图表公式清单

**图片**（发布到 `management/docs/_assets/pixel3dmm/`，WebP，最长边 ≤1600px、单图 ≤500KB）

| 笔记图号 | 源文件（`.cache/article-note/pixel3dmm/raw/figures/`） | 用在哪 | 论文图 | 处理 |
|---|---|---|---|---|
| 图 1 | `media/p3dmm_teaser.jpg`（6144×2048，2.9 MB） | §1/§2 问题与动机 | Fig 1 | 缩到 ≤1600、转 WebP（**极宽条带，小字需目视**） |
| 图 2 | `pixel3dmm_method.png`（1598×644） | §3 方法总览（先验学习 + 测试时优化两段） | Fig 2 | 转 WebP |
| 图 3 | `media/most_expressive_images_5.jpg`（2048×1228） | §6 基准多样性 | Fig 3 | 缩到 ≤1600、转 WebP |
| 图 4 | `media/results_posed_...jpg`（4136×2034） | §6 posed 定性对比 | Fig 4 | 缩到 ≤1600、转 WebP |
| 图 5 | `media/results_neutral_...jpg`（4136×1062） | §6 neutral 定性对比（差异化点：解耦） | Fig 5 | 缩到 ≤1600、转 WebP |

> 备选：`pixel3dmm_normals.png`（Fig 6 法向估计）。**发布后需用户目视确认图 1、图 4 的小字可读性。**

**公式**（KaTeX `$$...$$` + 符号表）

1. 逐像素图像翻译训练目标 $\underset{\Psi_{\mathcal{M}}}{\arg\min}\sum_k\sum_{p\in M^k}\|f(I^k)_p-Y^k_p\|_2$（式 3）
2. FLAME 优化量 $\Omega_{\text{FLAME}}=\{\mathbf{z}_{\text{id}}\in\mathbb{R}^{300},\mathbf{z}_{\text{ex}}\in\mathbb{R}^{100},\theta\in\mathcal{SO}(3)\}$ 与相机量 $\Omega_{\text{cam}}$（式 4/5）
3. UV 最近邻查表 $p^*_v=\arg\min_{p\in P}\|T^{\text{uv}}_v-\mathcal{U}(I)_p\|$（式 6）
4. 2D 顶点损失 $\mathcal{L}_{\text{uv}}=\sum_{v\in V}\mathbb{1}_{\|T^{\text{uv}}_v-\mathcal{U}(I)_p\|<\delta_{\text{uv}}}\cdot|p^*_v-\pi(v)|$（式 7）
5. 时序平滑项 $\mathcal{L}_{\text{smooth}}^{\Phi}$（式 9）

**Mermaid**：两张——① 两段式推理（RGB → 法向/UV 预测 → FLAME 参数优化 → 网格）；② 单目视频跟踪（首帧初值 → 冻结 id/焦距/主点 → 逐帧顺序优化 → 批量 + 平滑项）。

**表格**：10 项配置披露表、数据集配比表、基准任务与协议表、主结果摘要表（posed / neutral）、「论文局限 vs 我们结论」表、术语表、符号表。

## 6. 引用关系

- `[[论文笔记/performrecast|PerformRecast 模型笔记]]`（**主要消费方**：用它做 49 点 FLAME Loss）
- `[[论文笔记/face-vid2vid|Face Vid2vid 模型笔记]]`、`[[论文笔记/liveportrait|LivePortrait 模型笔记]]`（同一条"隐式关键点/参数化表示"上下游）
- `[[knowledge/3dgs-methods-research|3DGS 方法调研]]`（我们这里的依赖与 `driving_mode: pixel3dmm` 就在其中）
- `[[数字人概述/数字人领域问题|数字人领域问题]]`（第七章：像素级/参数级跟踪作为"技术适用性"的一个候选）
- sidecar `related`：上述条目；`changelog` 记首次创建。**不含 `papers/` 条目**（未入库）。

## 7. 风险与待确认项

- [把 DINOv3 / DPT 头写成本篇的设计] → D1；§3.1.1 与 §9 各写一次。
- [把 ICLR 2026 写成 arXiv 标注] → D2。
- [把 UIKA 的对照写成本篇结论] → D3。
- [跨卡型折算成本] → D4。
- [Chamfer/R2.5 定义写残] → D5。
- [代码不可得却写成"可复现"] → D6；只写"数据公开、代码未见链接"。
- [图 1 极宽（6144×2048）缩放后小字不可读] → 发布后请用户目视；必要时按面板切分或改用 Fig 2/Fig 3 替代。
- [order 冲突] → 取当前最大 +10，实施前复核（并行会话持续新增笔记）。

## Migration Plan

1. 用户审核本 design（§3 结构、§4 的 D1–D6、§5 五张图与五条公式、§7 风险项）。
2. apply 阶段：5 张原图转 WebP 发布 → 写正文 → 写 sidecar → 改 `论文笔记/README.md` 一行。
3. 校验：`validate-note.py` / `validate-analysis.py` / `check-delivery.py` / 浏览器实测 / `docs_order.py list` / FastAPI 详情接口 / `openspec validate docs-note-pixel3dmm --strict`；任一不过则回退。
4. 完成后，第七章可考虑新增一条"像素级几何跟踪"的技术条目（属 `docs-dh-field-tech-applicability`，另行确认）。
