# Tasks: docs-inline-anchor-links

## 1. 前端接管文内锚点

- [x] 1.1 `MarkdownRenderer.handleClick` 增加 `#` 分支：`preventDefault` + `getElementById(decodeURIComponent(href.slice(1)))` + `scrollIntoView({ behavior: 'smooth', block: 'start' })`
- [x] 1.2 验证：`/management/docs/实习复盘/数字人身份` 里 4 处文内引用能平滑跳到目标小节；URL 不变；右侧 TOC 行为不变；外部链接与 `[[slug]]` 跨文档链接不受影响

## 2. 收尾

- [x] 2.1 复查 skill《文档内链接》三条规范（heading 链接 / 标题不用冒号 / slug 规则）与实际实现一致
- [x] 2.2 `openspec validate docs-inline-anchor-links` 通过并提交
