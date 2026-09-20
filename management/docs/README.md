# 文档体系

> 本目录是 Digital Human 仓库的文档总入口。所有文档**夹内平铺、禁止嵌套**。
> 写作流程受 `openspec` 管控：先建 change → 审大纲（design）→ 出素材 → 审素材 → 才动笔（详见下文规则）。

## 目录

| 目录/文件 | 内容 | 说明 |
|-----------|------|------|
| `实习复盘/` | 实习工作复盘与领域文档（正文） | 每篇一个单篇 change 实施 |
| `论文笔记/` | 数字人论文/模型统一笔记库 | 一篇一个论文/模型，历史精读在 papers 库 |
| `knowledge/` | 外部信息源复制件（InternWiki / 博客精选） | 单层平铺，上游冻结；索引见 `knowledge/README.md` |
| `api-design-conventions.md` | 接口设计约定 | 脚手架自带 |
| `git-workflow.md` | Git 工作流 | 脚手架自带 |

## 实习复盘/ 计划清单

| # | 文档 | 单篇 change | 状态 |
|---|------|-------------|------|
| 1 | 数字人介绍与技术路线.md | `docs-intern-intro` | 大纲待审 |
| 2 | CyberVerse框架.md | `docs-intern-cyberverse` | 大纲待补审 |
| 3 | 数字人身份.md | `docs-intern-identity` | 待启动 |
| 4 | 数字人动作.md | `docs-intern-motion` | 待启动 |
| 5 | 工程改进.md | `docs-intern-engineering` | 待启动 |
| 6 | 数字人行业全景.md | `docs-intern-industry` | 待启动 |
| 7 | 总结.md（总览+发文方向） | `docs-intern-summary` | 待启动 |

## 论文笔记/ 计划清单

`avatar-forcing.md` / `ditto.md` / `liveact.md` / `omnimate.md` / `talker-t2av.md`
（统一模板：论文层 + 可选工程层；技术路线总纲在 `实习复盘/数字人介绍与技术路线.md`，不在此夹）

## 写作与审核规则

1. **统一骨架**（内容文档）：为什么重要 → 现行做法（信息总结）→ 我们的工作 → 可能的改进方向
2. **审核闸门**（依据 doc-writing skill）：
   - 建单篇 change → design.md **内嵌完整大纲**（到二级标题 + 每节表达什么）
   - **用户审大纲** → 通过后进入「资料整理」
   - 整理结果**在对话中提交审核，不写入仓库**（只审证据与口径）
   - **用户审素材** → 通过后才写正文
3. **位置规则**：仓库里只放文章正文（`实习复盘/`、`论文笔记/`）；计划留在 `openspec/changes/<change>/`；**素材不落仓库**；外部复制件进 `knowledge/`
4. **数据诚实**：不编造数字；没把握的地方用文字写明（如「推测」「尚无实测」），不使用标注符号体系
5. **正文不写出处**：不写 `knowledge/xxx.md`、不写"《X》原文："、不标来源日期与 commit；出处只留在 change 的整理环节。二手信息用自然语言说明其性质即可
6. **文档间链接**：职责边界用相对链接（"详见《数字人身份》"），这是结构分工，不是出处

## 与 openspec 的关系

体系级总 change：`openspec/changes/internship-work-review-docs`（登记表与结构契约的唯一权威）。
