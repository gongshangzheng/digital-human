# menu-visibility（菜单/功能可见性配置）

## Purpose

通过集中配置的 hidden key 列表控制侧边栏菜单项与报告类型 tab 的显示/隐藏。隐藏只影响入口可见性，不删除路由，配置随时可逆（口径与上游 ProjFlow `menu-visibility` 一致）。本仓库以此替换手写的 `web/src/config/menu.js`。

## Requirements

### Requirement: 集中配置的隐藏列表

系统 SHALL 提供一个集中的前端常量配置（`HIDDEN_KEYS`，定义于 `web/src/config/hidden.js`），作为菜单与报告类型 tab 可见性的唯一控制点；列表为空时所有功能 SHALL 全部显示。

#### Scenario: 配置为空
- **WHEN** `HIDDEN_KEYS` 为空数组
- **THEN** 侧边栏显示全部分组与菜单项，报告页显示全部三个类型 tab，与无此功能时行为一致

### Requirement: 菜单项级隐藏

`HIDDEN_KEYS` 中的叶子 key（路由 path，如 `/management/reports`）命中时，对应菜单项 SHALL 不显示，但其路由 SHALL 保持注册——直接输入 URL 仍可访问。

#### Scenario: 隐藏单个菜单项
- **WHEN** 配置含 `/management/reports`
- **THEN** 侧边栏不显示「报告」菜单项，其余菜单不受影响
- **THEN** 浏览器直接访问 `/management/reports` 仍正常渲染

### Requirement: 分组级隐藏

`HIDDEN_KEYS` 中的分组 key（如 `evaluation`）命中时，该分组及其全部子项 SHALL 不显示；分组未直接命中但其全部叶子被逐项隐藏时，该分组也 SHALL 自动隐藏；仍有可见叶子的分组 SHALL 正常显示。

#### Scenario: 隐藏整个分组
- **WHEN** 配置含 `evaluation`
- **THEN** 侧边栏不显示「评测体系」分组及其全部子项

#### Scenario: 组内叶子全部隐藏
- **WHEN** 配置同时含 `/papers/list` 与 `/papers/config`
- **THEN** 「论文搜集」分组整体不显示

#### Scenario: 组内叶子部分隐藏
- **WHEN** 配置仅含 `/papers/config`
- **THEN** 「论文搜集」分组显示，其下仅显示「论文列表」

### Requirement: 报告类型级隐藏

`HIDDEN_KEYS` 中的报告类型 key（`reports:daily` / `reports:weekly` / `reports:monthly`）命中时，报告页对应类型 tab SHALL 不显示；被隐藏类型的数据与详情路由 SHALL 不受影响。当前激活类型被隐藏时，页面 SHALL 自动切换到第一个可见类型。

#### Scenario: 隐藏日报
- **WHEN** 配置含 `reports:daily`
- **THEN** 报告页仅显示「周报」「月报」tab，默认展示周报
- **THEN** 直接访问日报详情路由仍正常渲染

#### Scenario: 当前类型被隐藏
- **WHEN** 用户停留在日报 tab，随后配置隐藏 `reports:daily` 并刷新
- **THEN** 页面自动落在第一个可见类型（周报），不报错

### Requirement: 可逆性

从 `HIDDEN_KEYS` 移除任一 key 后，对应功能 SHALL 无需其他操作即在菜单/tab 中恢复显示。

#### Scenario: 移除 key 恢复显示
- **WHEN** 从 `HIDDEN_KEYS` 删除 `/management/reports` 并刷新
- **THEN** 「报告」菜单项重新出现在侧边栏
