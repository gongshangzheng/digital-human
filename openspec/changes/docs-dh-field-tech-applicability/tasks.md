## 1. 设计与素材确认

- [x] 1.1 确认现有六章结构，核实正文中"外来技术 → 数字人"模式已有的两处单条（面部解剖先验、身份一致性判别器），确认没有专门章节。
- [x] 1.2 核实第六章「跨域问题」的实际范围（数据分布 / 合规 / 复现），确认它不是技术适用性。
- [x] 1.3 定位 1D 视觉分词器的库内素材：博客 `titok-1d-visual-tokenizer-survey`（TiTok 263 篇引用整理 + ProgressiveDiTok 定位）、AdapTok 快读草稿、`discrete-tokenizers-survey`（VidTok/ElasticTok 所在），以及 `gvcc-zero-shot-video-compression`、`contour-video-compression-survey`。
- [x] 1.4 核实两篇技术实例的书目：**AdapTok** = arXiv `2505.17011`（`Learning Adaptive and Temporally Causal Video Tokenization in a 1D Latent Space`，代码 `VisionXLab/AdapTok`）；**VidTok** = arXiv `2412.13061`（`VidTok: A Versatile and Open-Source Video Tokenizer`）。两篇均已用 OpenAlex arXiv-DOI 反查确认。
- [x] 1.5 参照基线核实：`论文笔记/face-vid2vid.md` 已完成（单图提身份：隐式 3D 关键点 + 外观 + canonical 容积）。
- [x] 1.6 ✅ 已核实：用户给的 **TivTok** = arXiv `2606.17590`（`TivTok: Broadcasting Time-Invariant Tokens for Scalable Video Tokenization`，2026-06-16，清华 Weiliang Chen / Yueqi Duan 等）。早前按误听登记的 `vidtok.md` 已撤，不保留为对照。
- [x] 1.7 用户确认章标题采纳值（默认 `## 七、技术适用性`）。

## 2. 待读清单登记

- [x] 2.1 `论文笔记/README.md` 追加 `adaptok.md`（`arXiv:2505.17011`）与 `tivtok.md`（`arXiv:2606.17590`）两行，状态 `待写`；两行均注明"拟用于从视频提角色身份，见领域问题第七章"。
- [x] 2.2 未创建这两个 `.md` 正文文件（将来按 article-note 流程各开 change）。

## 3. 正文新增章节

- [x] 3.1 在「六、跨域问题」之后新增 `## 七、技术适用性`，章首写清组织方式与与 §四、§六 的分工。
- [x] 3.2 写入五维度评估结构，"已验证 / 我们的推断 / 未验证"三分列。
- [x] 3.3 写首条目 `### 1D 视觉分词器：能不能用视频 token 提身份`：技术三粒度（TiTok / AdapTok / TivTok）+ 参照基线 Face Vid2vid（单图提身份）。
- [x] 3.4 写表示与接口匹配表（维度 / 时序性 / 因果性 / 可控性 / 可比性逐项判定），点明"视频 token 把运动一起编码进来"这个双刃。
- [x] 3.5 写五条可检验判据：身份信息量（selective sensitivity）、身份—运动解耦度、与单图基线对照、与现成身份编码器的排序一致性、**TIV 的身份纯度（TivTok 专属）**。
- [x] 3.6 写预判（全部标"我们的推断，未验证"）：AdapTok 与 TivTok 各对准一个硬约束（流式与算力 / 身份—运动解耦）且互补；TivTok 的 TIV 身份纯度必须用判据 5 验证；"视频是否优于单图"必须由判据 3 回答，不能先验判断。
- [x] 3.7 用一段带过同技术的另两条路径（提动作 / 管线侧压缩），说明判据不同，不展开。
- [x] 3.8 章节收尾：点明本章存在的理由（同一技术、不同位置、不同判据）。

## 4. 元数据同步

- [x] 4.1 frontmatter `summary` 加入"技术适用性"。
- [x] 4.2 开头分类段追加一句技术适用性的归类口径。
- [x] 4.3 `tags` 默认不动。

## 5. 验证与交付

- [x] 5.1 章编号连续（七章）、标题层级无跳级、表格列数与分隔行一致。
- [x] 5.2 站内链接目标存在（含 `论文笔记/face-vid2vid`、`论文笔记/adaptok` 等将来条目按存在性决定是否链接）。
- [x] 5.3 确认与 §四/§六 无内容重复。
- [x] 5.4 确认所有预判带"我们的推断，未验证"标记。
- [x] 5.5 `openspec validate docs-dh-field-tech-applicability --strict`；FastAPI 详情接口确认文档可读、章数正确。
- [x] 5.6 提交 `docs(field-problems): 新增「技术适用性」章与视频 token 提身份条目`。

## 6. 长期演进（本 change 不归档）

- [x] 6.1 在 design 记录"不归档"与沿用既有六条长期演进约定。
- [ ] 6.2 后续每条新技术仍按同一流程：先在本 change 的 design 追加条目规格与引用白名单，再追加 tasks，用户确认后才写正文。
- [ ] 6.3 每轮补充完成后**不跑** `openspec-archive-change`。
