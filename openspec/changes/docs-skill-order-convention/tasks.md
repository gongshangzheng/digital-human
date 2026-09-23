## 1. skill 更新（.agents/skills/documentation/SKILL.md）

- [x] 1.1 §2 元数据段落按 design D1 改写：强制显式排序键、写明缺省回落（date 降序）、索引 README 需 frontmatter、排序链
- [x] 1.2 §2 的 frontmatter 示例保持 `order: 10`（与新措辞一致）
- [x] 1.3 §3 按 design D2 追加两点：新建/插入文档必须写 `order`；工具要求目录内 `.md` 均有合法 frontmatter，README 缺 frontmatter 时会失败及修复方式
- [x] 1.4 §6 交付检查按 design D3 增加「order 完整、无重复、与阅读顺序一致（用 `docs_order.py list` 复看）」
- [x] 1.6 按 design D6 修正 `.agents/skills/article-note/scripts/validate-note.py` 的 `ALLOWED_META`，加入 `order`
- [x] 1.5 通读改动后的 SKILL.md，确认未与 `docs-page-content` 既有契约冲突（10 步长、排序链、文件夹优先级）

## 2. 论文笔记落地

- [x] 2.1 `management/docs/论文笔记/avatar-forcing.md` 加 `order: 10`
- [x] 2.2 `management/docs/论文笔记/ditto.md` 加 `order: 20`
- [x] 2.3 `management/docs/论文笔记/README.md` 补最小 frontmatter（title/author/date/tags/summary，按 design D5；默认不写 order）

## 3. 校验

- [x] 3.1 `docs_order.py list management/docs/论文笔记` 输出显示 10/20、无重复、无缺 frontmatter 报错
- [x] 3.2 `GET /api/management/docs` 中 `论文笔记/` 目录内顺序为 avatar-forcing → ditto → README，且 README 标题显示为「论文笔记」而非裸 slug
- [x] 3.3 `validate-note.py` 对两篇笔记仍通过（frontmatter 未破坏必填字段）
- [x] 3.4 `openspec validate docs-skill-order-convention --strict` 通过
- [x] 3.5 提交（`docs(skill): 明确每个内容文件夹必须使用显式排序键，并让论文笔记用上 order`），只包含 skill 与论文笔记相关文件
