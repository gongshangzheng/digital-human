/**
 * 菜单可见性配置（单一配置点）
 *
 * 协作类管理模块在此隐藏：仅从导航菜单移除，路由与后端 API 保留
 * （URL 直达仍可用）。从数组中删除对应 key 即恢复显示。
 */
export const HIDDEN_MENU_KEYS = [
  '/management/team',       // 团队成员
  '/management/reports',    // 报告（日报/周报/月报）
  '/management/milestones', // 里程碑
  '/management/meetings',   // 会议纪要
]

export function isMenuHidden(key) {
  return HIDDEN_MENU_KEYS.includes(key)
}

/** 过滤菜单树：命中的 key 不显示；父级 children 被清空时父级也不显示 */
export function filterMenuOptions(options) {
  return options
    .map((opt) => {
      if (!opt.children) return opt
      return { ...opt, children: opt.children.filter((c) => !isMenuHidden(c.key)) }
    })
    .filter((opt) => !isMenuHidden(opt.key))
    .filter((opt) => !opt.children || opt.children.length > 0)
}
