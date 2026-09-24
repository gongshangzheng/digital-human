## Why

`docs-intern-acceleration` 的最后一个任务（3.1）要求：等《数字人加速》里点名的**生成侧加速十个工作**各自有笔记后，把正文中的工作名替换为文档链接。目前这十篇一篇未写，是 `internship-work-review-docs` 3.1 验收（论文笔记齐备）与 `docs-intern-acceleration` 收口的共同阻塞项。十篇的素材已经在 `knowledge/视频生成训练与推理加速专题.md` 汇总（含证据等级），但缺正式笔记。

## What Changes

- 新增 **10 篇笔记**到 `management/docs/论文笔记/`：`fpsattention`、`blade`、`latent-spatial-memory`、`zipar`、`nar`、`flashar`、`turbodiffusion`、`inferix`（8 篇论文）+ `worldattention`、`dax`（2 篇仓库/技术报告类）
- 每篇配 sidecar；有论文原图的发布到 `management/docs/_assets/<slug>/`
- 回补链接：《数字人加速》「生成侧加速」四方向里把工作名替换为文档链接（即 `docs-intern-acceleration` 3.1）
- 更新 `论文笔记/README.md` 清单状态；同步伞 change 2.14 与 `docs-intern-acceleration` 3.1

## Capabilities

### New Capabilities
（无——纯文档 change，`.openspec.yaml` 置 `skip_specs: true`）

### Modified Capabilities
（无）

## Impact

- 新增 10 篇笔记 + 10 个 sidecar + 若干图片目录
- `数字人加速.md` 生成侧加速小节新增 10 处链接
- 不涉及渲染器、构建与后端接口
