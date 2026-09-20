# Design: sync-projflow-shared-updates

## Context

- 本仓库脚手架拷贝自 ProjFlow 工作树，但**拷贝点早于**上游若干 `[shared]` 提交，导致缺失特性 + 一个中文 slug 的可访问性 bug。
- 上游现状（`eb331fc`）：已实现 `HIDDEN_KEYS` 隐藏机制（`web/src/config/hidden.js`）、文档页 sidecar json、TOC 符号处理、左右侧栏收起、子目录折叠。
- 我们与之的差异（`diff` 核实）：
  - 我们手写 `web/src/config/menu.js`（上游为 `hidden.js`，含分组级与报告类型级隐藏）
  - 缺 sidecar：`server/routers/management.py` 少 9 行（读 `<slug>.json` 并返回 `sidecar`）
  - 缺 TOC 处理：`web/src/utils/markdown.js` 少 `.replace(/\*\*/g, '')`
  - 缺 DocPage 特性：收起侧栏 + sidecar 区块（约 246 行差异）
  - 中文 slug bug：`_SLUG_RE = ^[a-zA-Z0-9_/-]+$`（上游同 bug，两者都打不开中文名文档）
- 我们的既有定制必须保留：端口 8812/3212、digital-human 身份与 localStorage 键、`实习复盘/`+`论文笔记/` 目录。

## Goals / Non-Goals

**Goals：** 中文文档可打开；采用上游 `HIDDEN_KEYS` 机制（退役自写 menu.js）；补齐文档页 sidecar / 收起 / 折叠能力；全部可验证。
**Non-Goals：** 不引入上游与本仓库无关的模块（datasets 浏览、训练 run 详情、Speed Run 画廊等——我们已从拷贝点带上，如缺另行评估）；不改端口与目录结构；不重建 ProjFlow 的 openspec change 历史。

## Decisions

- **D1 逐文件对照移植，不用 git cherry-pick**：我们已改名/改端口/自定义菜单逻辑，cherry-pick 必冲突；改为按上游文件内容逐段移植（`diff` 定位后手工合并），保留我们的定制点。
- **D2 menu.js → hidden.js 迁移而非并存**：删除 `web/src/config/menu.js`，新增上游 `hidden.js`，把我们的隐藏集合（`/management/team`、`/management/reports`、`/management/milestones`、`/management/meetings`）迁入 `HIDDEN_KEYS`；`MainLayout.vue` 改用上游过滤逻辑；`Home.vue` 的 `isMenuHidden` 引用同步改到新模块。
- **D3 中文 slug 修复方式**：`_SLUG_RE` 放宽为允许 Unicode 单词字符（`\w` 含中文）+ 空格 + `_ / -`；新增 `_valid_doc_slug()` 显式拒绝空值与 `..` 路径段，继续走 `safe_resolve` 根约束。（实测 FastAPI/Starlette 已对路径参数解码，**无需额外 unquote**；额外解码反而会引入二次解码风险。）
- **D4 sidecar 只落机制不补内容**：本 change 实现 sidecar 读取与渲染；是否给现有文档加 `<slug>.json` 由文档类 change 决定。
- **D5 上游回灌**：中文 slug 修复与 hidden.js 采用经验按 `[shared]` 回灌 ProjFlow（作为本 change 的后续任务记录，不在本仓库实现上游改动）。

## Risks / Trade-offs

- [移植漏文件导致前端行为不一致] → 用 `diff -rq` 逐目录核对，前端 `vite build` + 文档页手测作为验收
- [放宽 slug 正则引入路径穿越] → 保留 `safe_resolve` 根目录约束，并加 `..` 显式拒绝与负向测试
- [迁移 menu.js 时隐藏集合漏项] → 迁移后核对四项目标隐藏项与分组自动隐藏行为
- [上游仍在演进] → 记录对照基准 commit `eb331fc`

## Migration Plan

1. 修复 slug 正则 → 验证中文文档接口 200
2. 引入 hidden.js、迁移隐藏集合、删 menu.js → 验证隐藏行为
3. 移植 server sidecar + markdown TOC + DocPage（收起/sidecar） → 构建 + 手测
4. `vite build`、接口冒烟、`npm run check`（若有）；回滚 = git revert 本 change 的提交

## Open Questions

- 上游的 `documentation` spec 中"文档登记表"与"结构级变更走单篇 Change"两条：本仓库已用体系级 change（`internship-work-review-docs`）承载，是否要额外落成 spec？（默认：不落，保持体系 change 为唯一权威）
