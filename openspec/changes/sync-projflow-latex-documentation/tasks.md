## 1. 规划与规格

- [x] 1.1 创建 `docs-math` capability delta，并记录 `docs-page-content` 的数学职责迁移和 `repository-agent-skills` 的统一入口契约
- [x] 1.2 严格验证 change 规划 artifacts，并确认不修改由 `docs-order-tooling` 维护的主 `docs-page-content` spec

## 2. Markdown 数学渲染

- [x] 2.1 在 `web/package.json` 与锁文件添加直接 KaTeX / markdown-it 插件依赖
- [x] 2.2 在现有 Markdown 渲染器中注册 KaTeX、载入样式，并保持原始 HTML 禁用、链接、图片和 Mermaid 行为不变
- [x] 2.3 为行内数学增加美元符号守卫，使金额等普通文本不被误判，同时保持非法公式的可见降级

## 3. 文档写作 skills

- [x] 3.1 新增本仓库裁剪后的 project-scoped `documentation` skill 和 Mermaid 公式速查，保留本仓库目录、sidecar、资产和 namespace 约定
- [x] 3.2 更新 `article-note` 的公式写作、分析和校验规则，使其与 KaTeX 语法一致
- [x] 3.3 移除重叠的 project-scoped `doc-writing` skill

## 4. 验证

- [x] 4.1 执行针对性 Markdown 数学检查，覆盖行内/块级公式、表格、金额、代码围栏、非法公式和 HTML 安全边界
- [x] 4.2 运行 `npm run build` 与本 change 的严格 OpenSpec 验证，并核对工作区未暂存文件
