// 主内容滚动位置记忆（用于长文页刷新后回到原阅读位置）
//
// 背景：ProjFlow 的页面滚动不在 window 上，而由 MainLayout 的 `app-content`
// （naive-ui n-scrollbar）内部的 `.n-scrollbar-container` 承载。本模块负责：
//   - 定位该容器（容错、可降级）
//   - 会话级（sessionStorage）读写滚动位置
//   - 内容渲染完成后恢复位置，并做一次延迟校正
//
// 所有存储访问与容器查找失败均静默降级，不影响页面渲染。

const KEY_PREFIX = 'doc-scroll:'

function getStorage() {
  try {
    return typeof window === 'undefined' ? null : window.sessionStorage
  } catch {
    return null // 隐私模式 / 禁用 storage
  }
}

/** 定位主内容滚动容器；找不到返回 null。 */
export function findScrollContainer() {
  if (typeof document === 'undefined') return null
  return (
    document.querySelector('.app-content .n-scrollbar-container') ||
    document.querySelector('.n-scrollbar-container') ||
    null
  )
}

/** 读取某 key 记录的位置；无记录或异常返回 null。 */
export function readScrollPosition(key) {
  const storage = getStorage()
  if (!storage || !key) return null
  try {
    const raw = storage.getItem(KEY_PREFIX + key)
    if (raw === null) return null
    const n = Number.parseInt(raw, 10)
    return Number.isFinite(n) ? n : null
  } catch {
    return null
  }
}

/** 写入位置；异常静默忽略。 */
export function saveScrollPosition(key, top) {
  const storage = getStorage()
  if (!storage || !key) return
  try {
    storage.setItem(KEY_PREFIX + key, String(Math.max(0, Math.round(top))))
  } catch {
    /* 配额或 privacy 限制：静默降级 */
  }
}

/**
 * 给滚动容器挂上「节流保存」监听。
 *
 * 位置始终记录在 key 所属的那篇文档下：路由切换时先由 noteRouteChange()
 * 结算旧文档位置，再切换到新 key，避免切换瞬间的滚动事件把旧位置写到新键。
 *
 * @param {HTMLElement|null} el 滚动容器
 * @param {() => string} getKey 返回当前 key（如 route.path）
 * @param {{ delay?: number }} [options]
 * @returns {{ commit: Function, noteRouteChange: Function, dispose: Function }}
 */
export function attachScrollMemory(el, getKey, { delay = 150 } = {}) {
  let key = typeof getKey === 'function' ? getKey() : ''
  let lastTop = el ? el.scrollTop : 0
  let timer = null

  function flush() {
    if (timer) {
      clearTimeout(timer)
      timer = null
    }
    saveScrollPosition(key, lastTop)
  }

  function onScroll() {
    if (!el) return
    lastTop = el.scrollTop
    if (timer) return
    timer = setTimeout(() => {
      timer = null
      saveScrollPosition(key, lastTop)
    }, delay)
  }

  if (el) el.addEventListener('scroll', onScroll, { passive: true })

  return {
    /** 结算旧文档位置并切到新 key；同时把位置基准重置为顶部。 */
    noteRouteChange(nextKey) {
      flush()
      key = nextKey || ''
      lastTop = 0
    },
    /** 立即把当前位置落盘。 */
    commit: flush,
    /** 解绑监听并落盘最后一次位置。 */
    dispose() {
      if (el) el.removeEventListener('scroll', onScroll)
      flush()
    },
  }
}

/**
 * 等内容就绪后恢复滚动位置，并在 settleDelay 后校正一次
 * （吸收图片 / Mermaid 异步渲染引起的高度变化）。
 *
 * @param {string} key 记录键（通常 route.path）
 * @param {() => boolean} isReady 内容是否已渲染完成
 * @param {{ tries?: number, interval?: number, settleDelay?: number }} [options]
 */
export function restoreAfterRender(key, isReady, { tries = 16, interval = 60, settleDelay = 150 } = {}) {
  const target = readScrollPosition(key)
  if (target === null || target <= 0) return

  let attempt = 0
  const apply = () => {
    const el = findScrollContainer()
    if (!el) return
    el.scrollTop = target
    // 内容后续长高（图片/Mermaid）会让位置前移，延迟再校正一次
    setTimeout(() => {
      const again = findScrollContainer()
      if (again) again.scrollTop = target
    }, settleDelay)
  }

  const tick = () => {
    if (typeof isReady !== 'function' || isReady()) {
      apply()
      return
    }
    if (++attempt >= tries) return // 超时放弃，静默降级
    setTimeout(tick, interval)
  }

  tick()
}

/**
 * 恢复该 key 的位置；无记录（或记录为顶部）时显式回到顶部。
 * 用于文档切换：访问过的文档恢复原位，首次访问的从顶部开始。
 */
export function restoreOrReset(key, isReady, options) {
  const target = readScrollPosition(key)
  if (target !== null && target > 0) {
    restoreAfterRender(key, isReady, options)
    return
  }
  const el = findScrollContainer()
  if (el) el.scrollTop = 0
}
