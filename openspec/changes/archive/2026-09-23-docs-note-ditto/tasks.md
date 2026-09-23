## 1. 素材与结构（待用户审核）

- [x] 1.1 建工作区 `.cache/article-note/ditto/`；抓取 arXiv `2411.19509` HTML(v3) + PDF（source tarball 406 失败，已降级）
- [x] 1.2 下载 6 张论文原图并逐个 PIL 校验（两张首下截断，`curl -C -` 续传补齐）
- [x] 1.3 派生 `raw/sources/paper.txt`（HTML → 纯文本，公式保留 `$alttext$`），供各 lane 引用
- [x] 1.4 跑 4 个委派 lane（methodology / experiment / code-analysis / image-collection）+ 自写 2 个 lane（citation / terminology）
- [x] 1.5 写 `synthesis.md`；`validate-analysis.py` 通过（exit 0）
- [x] 1.6 填 `workspace.json` 的 `repository` 字段（CyberVerse `models/ditto` @4968280）
- [x] 1.7 写 change 的 proposal + design（含目标文档架构、10 节大纲、图表公式清单、待裁决项）
- [x] 1.8 **用户审核结构**（design 第 3、5、7 节）；确认后才进入第 2 组

## 2. 图片发布

- [x] 2.1 `figures.py inspect` 清点 6 张原图，确认尺寸/体积与 design 第 5 节一致
- [x] 2.2 图片可读性复核：本机模型不支持读图，无法目视；退化为浏览器解码校验（6 张全部 `naturalWidth > 0`、尺寸与源图一致）。**图内小字可读性仍待用户目视确认**
- [x] 2.3 `figures.py convert` 转 WebP：4 张缩到最长边 ≤1600px、压到单图 ≤500KB
- [x] 2.4 `figures.py publish` 到 `management/docs/_assets/ditto/`；回填体积并确认单篇合计 ≤5MB
- [x] 2.5 核对 `GET /api/management/docs-assets/ditto/<file>` 全部 200

## 3. 正文写作

- [x] 3.1 按 design §3.1 写第 0/1/2 节（元信息表、四条贡献、两条 critical issues + VASA-1 对照）
- [x] 3.2 写第 3 节：运动空间（式 1/2/3、$\mathbf{m}$ 不含 $\mathbf{c}$）→ 条件 DiT 与 ECS/ICS → 训练三策略与式(6) → 可控性（21×3、第 34/58 维、gaze 链路）；配图 1/2/3 与 Mermaid 主链路
- [x] 3.3 写第 4 节：十项配置披露表 + 265 维构成表 + 训练/推理参考条件差异；未披露项一律写「未披露」
- [x] 3.4 写第 5 节：三模块流式优化 + 表 5/6 + 三层 RTF 口径对照表（每行带对象与硬件）
- [x] 3.5 写第 6 节：表 1/2/3/4 全量数字 + † 与 10 人 20 clips 的口径说明 + 定性结论；配图 4/5/6
- [x] 3.6 写第 7 节：四轴定位表 + VASA-1「无同协议数值」声明
- [x] 3.7 写第 8 节：naturalness 成对呈现 + 唇动隔离演进结论 + 3.2 秒错位未定因 + `fix_kp_cond` 回锚机制 + 「论文局限 vs 我们结论」对照表
- [x] 3.8 写第 9/10 节（术语表、符号表、三处符号冲突、相关文档链接）
- [x] 3.9 写 sidecar `ditto.json`（`changelog` 记首次创建；`related` 用含 `slug`/`title` 的对象）

## 4. 交付物

- [x] 4.1 更新 `management/docs/论文笔记/README.md` 清单：`ditto.md` 状态改为已完成
- [x] 4.2 确认图片编号按笔记出现顺序重排（图 1–6），未沿用论文 Figure 编号

## 5. 校验与提交

- [x] 5.1 `validate-note.py` 通过（frontmatter / 标题层级 / 公式定界符 / 图片 URL / 图号连续 / sidecar / 内链）
- [x] 5.2 `check-delivery.py` 汇总通过
- [x] 5.3 浏览器实测：图片显示、Mermaid 渲染、内链与文内锚点可跳
- [x] 5.4 `openspec validate docs-note-ditto --strict` 通过
- [x] 5.5 提交（`docs(note): 新增 ditto 论文笔记 —— 运动空间扩散 + 可控性 + 流式实时`），只包含本篇相关文件
