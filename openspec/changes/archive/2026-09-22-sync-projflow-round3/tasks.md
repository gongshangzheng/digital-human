## 1. 后端：文档图片静态端点

- [x] 1.1 `server/main.py`：引入 `StaticFiles` 与 `MANAGEMENT_DIR`，挂载 `/api/management/docs-assets` → `management/docs/_assets`（`os.makedirs` + `check_dir=False`）
- [x] 1.2 `server/routers/management.py`：`get_docs()` 的 `os.walk` 跳过我下划线前缀目录（`dirs[:] = [d for d in dirs if not d.startswith('_')]`），并更新 docstring
- [x] 1.3 冒烟：启动后端，`GET /api/health` 正常；`GET /api/management/docs` 仍返回既有文档

## 2. 前端：figure 渲染与样式

- [x] 2.1 `web/src/components/common/MarkdownRenderer.vue`：覆写 `image` 规则（`<img loading="lazy">`），并按上游实现加「整段单图 → `<figure>` + `<figcaption>`」的 `paragraph_open/close` 包装（保留既有 heading / fence / 链接改写 / 锚点接管）
- [x] 2.2 `web/src/styles/index.scss`：`.markdown-body` 下新增 `figure` / `figure img` / `figcaption` / `img` 规则
- [x] 2.3 冒烟：含图文档渲染出 `figure` + `figcaption`；无 alt 图为裸 `img`；任务列表、Mermaid、文内锚点不受影响

## 3. 目录与 skill 联动

- [x] 3.1 新增 `management/docs/_assets/.gitkeep`
- [x] 3.2 `.agents/skills/article-note/SKILL.md`：前置条件改为「文档图片端点已就绪」，恢复标准 `figures.py publish` 流程
- [x] 3.3 端到端验证：用 `figures.py` 发布一张测试图到 `_assets/`，`GET /api/management/docs-assets/...` 200，再从文档渲染确认；验证后清理测试图

## 4. 文档列表排序链收敛（上游 `644fed0`）

> 本仓库已有等价排序链，本组只做「常量位置」收敛，不改排序行为。

- [x] 4.1 `server/config.py` 新增 `DOCS_FOLDER_ORDER = ['实习复盘', '论文笔记', 'knowledge']`，沿用本仓库 config 既有的「下游库可覆盖」注释惯例
- [x] 4.2 `server/routers/management.py`：删除本地 `_DOCS_FOLDER_ORDER`，改从 `server.config` 导入 `DOCS_FOLDER_ORDER`，`_doc_sort_key` 引用公开常量
- [x] 4.3 与上游逐行核对：`_doc_number` / `_doc_date_ordinal` / `_doc_sort_key` 与上游 `644fed0` 一致（收敛后残余差异应仅为 `import json` 行位置与一行本地 sidecar 注释，不再有常量来源差异）
- [x] 4.4 文内锚点接管：确认本仓库 `MarkdownRenderer.vue` 的 `#` 分支与上游 `644fed0` 一致（仅核对，不改代码）
- [x] 4.5 冒烟：重启后端，`GET /api/management/docs` 顺序为 实习复盘 → 论文笔记 → knowledge，且连续请求一致

## 5. 登记与校验

- [x] 5.1 上游同步记录写入本 change（本轮含 `e505269` 图片能力 / `4a3b964` 文档根目录唯一 / `644fed0` 锚点 + 排序链）
- [x] 5.2 硬验收：与上游 HEAD 逐字节比对，`MarkdownRenderer.vue` 与 `index.scss` 的 diff 必须为空（此项比冒烟更强）
  ```bash
  U=~/code/ProjFlow
  diff <(git -C $U show HEAD:web/src/components/common/MarkdownRenderer.vue) web/src/components/common/MarkdownRenderer.vue
  diff <(git -C $U show HEAD:web/src/styles/index.scss) web/src/styles/index.scss
  ```
- [x] 5.3 `openspec validate sync-projflow-round3 --strict` 通过
- [x] 5.4 提交（`[shared] feat: pick 上游文档图片能力 + 排序常量收敛到 config`）
