// ============================================================
// HIDDEN_KEYS —— 菜单 / 功能隐藏配置（唯一控制点）
//
// 用法：把要隐藏的 key 加进下面数组即可。只影响入口显示，
//       路由保留可直接 URL 访问；删除 key 即恢复，完全可逆。
//
// 可用 key（与 MainLayout.vue menuOptions 同步维护）：
//
// [分组] 隐藏整个分组及其全部子项
//   'management'   项目管理（项目树/团队/报告/任务/里程碑/会议/文档）
//   'papers'       论文搜集
//   'training'     训练体系
//   'evaluation'   评测体系
//
// [菜单项] 隐藏单个菜单项（完整路由 path）
//   '/'                       首页
//   '/management/projects'    项目树
//   '/management/team'        团队成员
//   '/management/reports'     报告
//   '/management/tasks'       任务看板
//   '/management/milestones'  里程碑
//   '/management/meetings'    会议纪要
//   '/management/docs'        文档
//   '/papers/list'            论文列表
//   '/papers/config'          数据源配置
//   '/datasets'               数据集
//   '/training/run'           训练运行
//   '/training/results'       训练结果
//   '/training/models'        模型配置
//   '/training/datasets'      数据集配置
//   '/training/configs'       训练配置
//   '/evaluation/run'         评测运行
//   '/evaluation/speedrun'    Speed Run
//   '/evaluation/results'     评测结果
//   '/evaluation/outputs'     查看输出
//   '/evaluation/models'      模型管理
//   '/evaluation/datasets'    数据集管理
//   '/evaluation/configs'     评测配置
//
// [报告类型] 隐藏报告页内的单个类型 tab（页面级粒度，非菜单项）
//   'reports:daily'     日报
//   'reports:weekly'    周报
//   'reports:monthly'   月报
//
// 注意：分组内叶子全部被隐藏时，分组自动消失，无需重复配置分组 key。
// ============================================================

export const HIDDEN_KEYS = [
  '/management/team',       // 团队成员（协作类模块，本项目不需要）
  '/management/reports',    // 报告（日报/周报/月报）
  '/management/milestones', // 里程碑
  '/management/meetings',   // 会议纪要
]

/**
 * 按 hiddenKeys 过滤菜单树。
 * 规则：叶子 key 命中 → 摘除；分组 key 命中 → 摘整组；
 *       分组未命中但过滤后 children 为空 → 摘整组。
 * 不修改入参，返回新数组。
 */
export function filterHidden(items, hiddenKeys) {
  const hidden = new Set(hiddenKeys)
  const out = []
  for (const item of items) {
    if (hidden.has(item.key)) continue
    if (Array.isArray(item.children)) {
      const children = item.children.filter(c => !hidden.has(c.key))
      if (!children.length) continue
      out.push({ ...item, children })
    } else {
      out.push(item)
    }
  }
  return out
}
