## Why

LIA-X 是「外观特征 + flow-warp decoder」这族方法的代表（《数字人身份》86 用它作例），也是《数字人加速》里现成的 decoder 蒸馏候选——论文 512²、bf16、batch=1 下约 333ms/帧，是我们当时 T2AV 链路的速度瓶颈。但笔记库里没有这一篇，概述中的点名叫法无法跳转，读者读不到"线性导航 + 稀疏运动字典"这套机制到底是什么。

## What Changes

- 新增 `management/docs/论文笔记/lia-x.md`：按 10 节骨架成文，含论文原图（5 张，其一句义控制需拼接三面板）、公式（2–3 个）、术语与符号表
- 新增 sidecar `management/docs/论文笔记/lia-x.json`
- 发布采用图到 `management/docs/_assets/lia-x/`（WebP，单图 ≤500KB、单篇 ≤5MB）
- 链接回补：把概述中的点名叫法换成文档链接（《数字人身份》86、《数字人加速》83；仅替换链接，不改数字与结论）
- 不修改其它笔记与概述正文

## Capabilities

### New Capabilities
（无——纯文档 change，`.openspec.yaml` 置 `skip_specs: true`）

### Modified Capabilities
（无）

## Impact

- 新增 1 篇笔记 + 1 个 sidecar + 1 个图片目录
- 《数字人身份》《数字人加速》新增站内链接
- 不涉及渲染器、构建与后端接口
