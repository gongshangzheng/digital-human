## 1. 规范

- [x] 1.1 `specs/docs-page-content/spec.md`：MODIFIED「用 `order` 字段显式表达阅读顺序」——加「步长 10、留插入空间、插入不重排既有文档」约定 + 「在两篇之间插入新文档」scenario + 示例改 10/20
- [ ] 1.2 `openspec validate docs-order-tooling --strict` 通过

## 2. 脚本实现 `scripts/docs_order.py`

- [ ] 2.1 骨架：`argparse` 三子命令 `list` / `insert` / `renumber`，模块 docstring 写清用法（与 `scripts/import_papers.py` 风格一致）；stdlib only，Python 3.9 兼容（不用 `str | None`）
- [ ] 2.2 frontmatter 行级读写：解析出 `order:` 所在行与当前值；写入时保留其余字节（D2）；无该字段时插到 `title:` 之后
- [ ] 2.3 排序基准与后端同源：`order → id → date 降序 → slug`（注释指向 `server/routers/management.py:_doc_sort_key`）
- [ ] 2.4 `list`：输出 表格（order / title / slug）+ 相邻空位数 + 可插入槽位；重复 order 标出并以非零码退出（D6）
- [ ] 2.5 `insert`：`--after/--before/--index/--order` 定位置；有整数空位取中点、无空位位移后续（D4）；`--shift` 强制位移；缺省追加到末尾
- [ ] 2.6 `insert --create`：文件不存在时生成最小 frontmatter（title/author/date/tags/order/summary + 标题行）（D7）；`--author` 可覆盖
- [ ] 2.7 `renumber`：按当前顺序整体重排为 `--step`（默认 10）/`--start`（默认 10）
- [ ] 2.8 全局：默认 dry-run，`--apply` 落盘（D3）；写盘后逐文件 `yaml.safe_load` 校验，失败则回滚该文件并报错
- [ ] 2.9 `--force`：仅在显式指定时允许在重复 order 存在时写入

## 3. 应用约定

- [ ] 3.1 对 `management/docs/数字人概述/` 跑 `renumber --apply`：`1–8 → 10–80`（阅读顺序不变）
- [ ] 3.2 `list` 复查：8 篇为 10–80、无重复、每对相邻之间有 9 个空位

## 4. 验证

- [ ] 4.1 临时目录演练：`--create` 插入到两篇之间 → dry-run 与 apply 各一次，确认空位路径不触碰其它文件
- [ ] 4.2 临时目录演练：把空位填满（10/11 或连续插入）→ 确认走位移路径且结果规整为 10 步长
- [ ] 4.3 幂等：`renumber --apply` 连续跑两次，第二次无任何改动
- [ ] 4.4 重复 order：手工造一个重复值 → `list` 报错且退出码非零；`--apply` 被拒绝
- [ ] 4.5 顺序一致性：脚本 `list` 的顺序 == `GET /api/management/docs` 中该分组的顺序
- [ ] 4.6 回滚可用：`renumber --step 1 --start 1` 的 dry-run 输出与预期一致（不实际执行）
- [ ] 4.7 `python3 -m py_compile scripts/docs_order.py` 通过

## 5. 提交

- [ ] 5.1 提交（`feat(docs): order 改为 10 步长 + scripts/docs_order.py 插入/重排工具`）
- [ ] 5.2 归档 change（把 delta 同步进 `openspec/specs/docs-page-content/`）
