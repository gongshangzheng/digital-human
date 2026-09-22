// 文档取数来源切换层：开发走 FastAPI，生产静态托管走构建期 docs-data.json。
import {
  getDocList as apiDocList,
  getDocDetail as apiDocDetail,
} from './management'

const USE_STATIC = import.meta.env.PROD
const API_ASSET_PREFIX = '/api/management/docs-assets/'

function toStaticAssetUrls(content) {
  if (!content) return content
  return content.split(API_ASSET_PREFIX).join(`${import.meta.env.BASE_URL}docs-assets/`)
}

let staticCache = null

async function loadStaticData() {
  if (staticCache) return staticCache
  const url = `${import.meta.env.BASE_URL}docs-data.json`
  const response = await fetch(url, { cache: 'no-cache' })
  if (!response.ok) throw new Error(`无法加载文档静态数据 ${url}（HTTP ${response.status}）`)
  staticCache = await response.json()
  return staticCache
}

export async function getDocList() {
  if (!USE_STATIC) return apiDocList()
  const data = await loadStaticData()
  return data.docs || []
}

export async function getDocDetail(slug) {
  if (!USE_STATIC) return apiDocDetail(slug)
  const data = await loadStaticData()
  const doc = data.details?.[slug]
  if (!doc) throw new Error(`Doc not found: ${slug}`)
  return { ...doc, content: toStaticAssetUrls(doc.content) }
}
