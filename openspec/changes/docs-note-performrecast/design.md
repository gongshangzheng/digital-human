## Context

`论文笔记/` 的隐式关键点主线现状：`face-vid2vid`（3D 隐式关键点 + 三项分解）→ `liveportrait`（可缩放运动变换 + stitching/retargeting + 265D 运动空间）→ 下游 `ditto`、`avatar-forcing`（把 265D 空间当扩散/流式输入）。**PerformRecast 直接改这条链的表示层**：指出 LivePortrait 的关键点变换运算顺序（先乘 $R$ 再加 $\delta$）与 FLAME 前向（先塑形再旋转）不一致，导致表情形变混入头姿，无法「只改表情」。

素材齐全：arXiv HTML 全文（`2603.19731v1`）+ 博客精读（仅 Replacement 模式）+ 9 张原图。论文的训练超参与 benchmark 细节在**附录**（arXiv HTML supplementary），正文只给方法与主表。

本篇属**纯论文层笔记 + 与 LivePortrait/扩散路线的对照**：没有我们的接入实测，CyberVerse 也无该模型目录，因此第 8 节写「与既有笔记的谱系对照 + 论文缺口」，不写「接入状态」。

## Goals / Non-Goals

**Goals：**

- 产出 10 节骨架的 `performrecast.md` + sidecar，讲清「公式一致性 → 解耦」这一核心机制，以及 49 点显式关键点监督、BAM 分区监督、两推理模式。
- 完整登记 Table 1（**Replacement 与 Enhancement 两列**）、Table 2（肖像动画 self/cross）、Table 3（MEAD）与消融，逐格照录。
- 训练配置披露按 10 项表列全（数据/规模/预处理/初始化/batch/lr/优化器/步数/硬件/复现），正文与附录分别标来源，未披露项写「未披露」。
- 第 8 节承担与 `liveportrait`、`face-vid2vid` 的谱系对照，并点出「GAN 生成上限（牙齿模糊）」与扩散路线的边界。
- 保留 6 张能替代文字的原图，每图有图题与正文解读。

**Non-Goals：**

- 不写接入与部署（无本地实测、无对应代码目录）。
- 不把博客口径当作论文口径：博客只登 Replacement 列，Enhancement 列、附录超参以论文为准。
- 不补跑实验；不把「6 FPS」写成已在我们硬件复现的性能。
- 不改代码、训练配置与推理参数。

## 1. 论文速览

| 项 | 值 |
|---|---|
| 标题 | PerformRecast: Expression and Head Pose Disentanglement for Portrait Video Editing |
| 作者 | Jiadong Liang、Bojun Xiong、Jie Tian、Hua Li、Xiao Long、Yong Zheng、Huan Fu |
| 单位 | HUJING Digital Media & Entertainment Group（虎鲸文娱） |
| venue / 年份 | CVPR 2026（博客登记；arXiv 正文未声明，写作时标口径） |
| arXiv | `2603.19731v1` |
| 项目页 / 代码 | https://github.com/youku-aigc/PerformRecast（论文称开源代码与数据） |
| papers 库 | **未入库**（frontmatter 只写 `arxiv_id`，不写 `papers_id`） |
| 素材 | `.cache/article-note/performrecast/`（`paper.txt`、`blog.txt`、`raw/facts.md`、`raw/figures/` 9 张原图） |

## 2. 一句话价值主张（≤100 字）

把 warping 类肖像动画的关键点变换公式改成与 FLAME 一致（先加表情再乘头姿），从而继承 3DMM 的**表情/头姿解耦**；再用 Pixel3DMM 跟踪的 **49 个显式 3D 关键点**做 FLAME Loss 替掉 4 项辅助损失与第二训练阶段，并用 **BAM** 分区监督修好面部边界错位；支持「只换表情」的 Replacement 与「叠加表情增量」的 Enhancement 两种推理模式。

## 3. 笔记结构大纲

### 3.1 目标文档架构（全文落点）

新建 `management/docs/论文笔记/performrecast.md`，沿用 10 节骨架：

| 节 | 标题 | 承载什么 | 配图/公式/表 | 字数 |
|---|---|---|---|---|
| 0 | 论文信息 | 元信息表 + 「papers 库未入库」说明 + venue 口径 | 表格 | 150 |
| 1 | 一句话总结 | 价值主张 + 4 条贡献（公式一致 / 显式监督 / BAM / 两模式 benchmark） | 列表 | 250 |
| 2 | 问题与动机 | 表情-only 编辑 vs 肖像动画的区别；LivePortrait 运算顺序导致的解耦困境；3DMM 的启示 | 图 1（teaser）+ 运算顺序对照 Mermaid | 600 |
| 3 | 方法精析 | 3.1 预备（LivePortrait 式 1 + Pixel3DMM 的 FLAME 参数）；3.2 FLAME 一致变换（式 2/3）与三组显式关键点 + FLAME Loss（式 4）；3.3 丢弃 4 项损失（式 5）；3.4 BAM 分区监督（式 7/8） | 图 2（框架）+ 图 3（BAM）+ 图 4（49 点）+ 式 1–5、7、8 | ≥1500 |
| 4 | 训练与实现细节 | 两阶段 Teacher-Student；10 项配置披露表；关键点加噪、$x_{d,self}$ 加速、mask 计算 | 披露表 + 表 | 700 |
| 5 | 推理与系统链路 | Replacement（式 6）/ Enhancement（式 9）/ 肖像动画三种推理；6 FPS 口径 | 图 5（两模式）+ Mermaid | 600 |
| 6 | 实验与结果 | MetaHuman benchmark 构建；Table 1（Replacement + Enhancement 两列 + 消融）；Table 2（self/cross）；Table 3（MEAD）；Table 4（与扩散对比）；失败案例 | 图 6（失败案例）+ 四张表 | 1200 |
| 7 | 相关工作与定位 | LivePortrait / Face Vid2vid 谱系；扩散类表情编辑的改造对照 | 谱系表 | 500 |
| 8 | 局限与启发 | 论文自认（GAN 生成上限、牙齿模糊）；与我们笔记的对照（表示层改动 vs 损失堆叠）；可操作启发 | 「论文缺口 vs 我们结论」表 | 800 |
| 9 | 术语与符号表 | 术语表 + 符号表（$x_c,R,\delta,s,t$、$V_c,V_{exp},V_{kp}$、$\theta$ 四关节） | 两张表 | — |
| 10 | 相关文档 | `face-vid2vid`、`liveportrait`、`ditto`、`数字人身份/动作`、`知识库` 相关 | 链接列表 | — |

**跨文件触点**：`论文笔记/README.md` 清单补一行 `performrecast.md`。

### 3.2 图片清单（待确认后转换发布）

| 文件 | 论文图 | 用途 | 转换 |
|---|---|---|---|
| `teaser.png` | Fig. 1 | 任务示意（编辑源视频 + 动画静态肖像） | 需转 WebP + 缩到 ≤1600px（现 1948px/4.2MB） |
| `ljd_method.png` | Fig. 2 | 框架总览 | 直接发布（247KB，1043×386，OK） |
| `teacher-student.png` | Fig. 3 | BAM 分区监督 | 直接发布（339KB，581×532，OK） |
| `keypoints.png` | Fig. 4 | 49 个显式 3D 关键点分布 | 需转 WebP（776KB） |
| `two_infer_modes.png` | Fig. 5 | Replacement / Enhancement 两模式 | 需转 WebP + 缩（2025px/2.0MB） |
| `limitation.png` | Fig. 10 | 牙齿区域模糊失败案例 | 直接发布（184KB，OK） |

### 3.3 公式清单（正文内联，均配符号表）

式 (1) LivePortrait 变换；式 (2) FLAME 前向；式 (3) 改进变换；式 (4) FLAME Loss；式 (5) 总损失；式 (6) Replacement 关键点；式 (7)(8) BAM 分区损失；式 (9) Enhancement 关键点。

## 4. 待决项（已定）

用户以「继续」确认按推荐落地：

| # | 事项 | 结论 |
|---|---|---|
| 1 | 表 1 列数 | **同时登记 Replacement 与 Enhancement 两列** |
| 2 | venue 口径 | **CVPR 2026（博客登记；arXiv 正文未声明）** |
| 3 | 图数量 | **6 张**（teaser / 框架 / BAM / 关键点 / 两模式 / 失败） |
| 4 | 第 8 节对照 | **只点 liveportrait / face-vid2vid** |

## 5. 素材与来源

- `.cache/article-note/performrecast/paper.txt`（arXiv HTML `2603.19731v1` 正文 + 附录）
- `.cache/article-note/performrecast/blog.txt`（博客精读 `paper-performrecast`）
- `.cache/article-note/performrecast/raw/facts.md`（事实索引 + 冲突 + 缺口）
- `.cache/article-note/performrecast/raw/figures/`（9 张原图）
- 提取日志：source tarball / PDF 均返回 406，HTML 成功（`raw/sources/extraction-log.md`）
