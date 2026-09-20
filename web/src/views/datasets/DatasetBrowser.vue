<template>
  <div class="dataset-page">
    <!-- L1: 数据集卡片列表 -->
    <n-card v-if="!currentDataset" title="数据集" size="small">
      <template #header-extra>
        <n-button size="tiny" quaternary @click="loadDatasets">刷新</n-button>
      </template>
      <n-spin :show="loading">
        <div v-if="datasets.length" class="ds-grid">
          <div v-for="d in datasets" :key="d.id" class="ds-card" @click="openDataset(d)">
            <n-icon size="28" color="#eab308"><folder-outline /></n-icon>
            <div class="ds-name">{{ d.name }}</div>
            <div class="ds-meta">{{ d.subdirs }} 子目录 · {{ d.files }} 文件</div>
            <div v-if="d.is_symlink" class="ds-symlink">→ 软链</div>
          </div>
        </div>
        <EmptyState v-else-if="!loading" description="暂无数据集。将数据集目录（或软链）放入 datasets/ 即可显示。" />
      </n-spin>
    </n-card>

    <!-- L2: 目录浏览 -->
    <n-card v-else size="small">
      <template #header>
        <div class="crumb">
          <a class="crumb-link" @click="backToList">数据集</a>
          <span class="crumb-sep">/</span>
          <a class="crumb-link" :class="{ current: !pathParts.length }" @click="navigateTo(-1)">
            {{ currentDataset.name }}
          </a>
          <template v-for="(part, i) in pathParts" :key="i">
            <span class="crumb-sep">/</span>
            <a class="crumb-link" :class="{ current: i === pathParts.length - 1 }" @click="navigateTo(i)">
              {{ part }}
            </a>
          </template>
        </div>
      </template>
      <template #header-extra>
        <span class="total-hint">共 {{ browseData.total }} 项</span>
        <n-button size="tiny" quaternary style="margin-left: 8px" @click="loadBrowse">刷新</n-button>
      </template>

      <n-spin :show="browsing">
        <div v-if="browseData.items.length" class="browse-grid">
          <div v-for="item in browseData.items" :key="item.path" class="browse-item" @click="openItem(item)">
            <div class="item-thumb">
              <n-icon v-if="item.is_dir" size="30" color="#eab308"><folder-outline /></n-icon>
              <img v-else-if="item.is_image" :src="fileUrl(item.path)" class="item-cover" loading="lazy" />
              <template v-else-if="item.is_video">
                <img :src="thumbUrl(item.path)" class="item-cover" loading="lazy" @error="onThumbError" />
                <span class="play-overlay">▶</span>
              </template>
              <n-icon v-else size="26" color="#71717a"><document-outline /></n-icon>
            </div>
            <div class="item-name" :title="item.name">{{ item.name }}</div>
            <div v-if="!item.is_dir" class="item-size">{{ formatSize(item.size) }}</div>
          </div>
        </div>
        <EmptyState v-else-if="!browsing" description="空目录" />

        <n-pagination
          v-if="browseData.pages > 1"
          v-model:page="page"
          :page-count="browseData.pages"
          :page-size="pageSize"
          size="small"
          style="margin-top: 12px; justify-content: center"
          @update:page="loadBrowse"
        />
      </n-spin>
    </n-card>

    <!-- L3: 预览 modal -->
    <n-modal v-model:show="previewShow" preset="card" :title="previewItem?.name" style="max-width: 800px">
      <img
        v-if="previewItem?.is_image"
        :src="fileUrl(previewItem.path)"
        style="max-width: 100%; max-height: 70vh; display: block; margin: 0 auto"
      />
      <video
        v-else-if="previewItem?.is_video"
        :src="fileUrl(previewItem.path)"
        controls
        preload="none"
        playsinline
        style="width: 100%; max-height: 70vh; background: #000"
      />
      <div v-else class="no-preview">此文件类型暂不支持预览</div>
    </n-modal>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { NCard, NSpin, NButton, NIcon, NPagination, NModal } from 'naive-ui'
import { FolderOutline, DocumentOutline } from '@vicons/ionicons5'
import EmptyState from '../../components/common/EmptyState.vue'
import { listDatasets, browseDataset, getThumbUrl, getFileUrl } from '../../api/datasets'

const datasets = ref([])
const loading = ref(false)
const currentDataset = ref(null)
const currentPath = ref('')
const browsing = ref(false)
const page = ref(1)
const pageSize = 20
const browseData = reactive({ items: [], total: 0, page: 1, size: pageSize, pages: 0 })

const previewShow = ref(false)
const previewItem = ref(null)

const pathParts = computed(() => (currentPath.value ? currentPath.value.split('/') : []))

const thumbUrl = (path) => getThumbUrl(currentDataset.value.id, path)
const fileUrl = (path) => getFileUrl(currentDataset.value.id, path)

async function loadDatasets() {
  loading.value = true
  try {
    datasets.value = await listDatasets()
  } catch {
    datasets.value = []
  }
  loading.value = false
}

async function loadBrowse() {
  browsing.value = true
  try {
    const d = await browseDataset(currentDataset.value.id, {
      path: currentPath.value, page: page.value, size: pageSize,
    })
    Object.assign(browseData, d)
  } catch {
    Object.assign(browseData, { items: [], total: 0, pages: 0 })
  }
  browsing.value = false
}

function openDataset(d) {
  currentDataset.value = d
  currentPath.value = ''
  page.value = 1
  loadBrowse()
}

function backToList() {
  currentDataset.value = null
  currentPath.value = ''
}

function navigateTo(idx) {
  currentPath.value = idx < 0 ? '' : pathParts.value.slice(0, idx + 1).join('/')
  page.value = 1
  loadBrowse()
}

function openItem(item) {
  if (item.is_dir) {
    currentPath.value = item.path
    page.value = 1
    loadBrowse()
  } else {
    previewItem.value = item
    previewShow.value = true
  }
}

function onThumbError(e) {
  e.target.style.display = 'none'
}

function formatSize(bytes) {
  if (!bytes) return '0 B'
  const units = ['B', 'KB', 'MB', 'GB']
  let i = 0
  let v = bytes
  while (v >= 1024 && i < units.length - 1) { v /= 1024; i++ }
  return `${v.toFixed(i ? 1 : 0)} ${units[i]}`
}

onMounted(loadDatasets)
</script>

<style scoped lang="scss">
.dataset-page { padding: 4px 8px; }

// L1 数据集卡片
.ds-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
}
.ds-card {
  padding: 16px 12px;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background: var(--color-card);
  cursor: pointer;
  text-align: center;
  transition: all 0.15s;
  &:hover { border-color: var(--color-primary); background: var(--color-hover); }
  .ds-name { margin-top: 8px; font-size: 13px; font-weight: 600; color: var(--color-text); word-break: break-all; }
  .ds-meta { margin-top: 4px; font-size: 11px; color: var(--color-text-dim); }
  .ds-symlink { margin-top: 2px; font-size: 10px; font-style: italic; color: var(--color-text-dim); }
}

// 面包屑
.crumb { display: flex; align-items: center; flex-wrap: wrap; gap: 4px; font-size: 13px; }
.crumb-link {
  cursor: pointer; color: var(--color-text-secondary);
  &:hover { color: var(--color-primary); }
  &.current { color: var(--color-text); font-weight: 600; cursor: default; }
}
.crumb-sep { color: var(--color-text-dim); }
.total-hint { font-size: 12px; color: var(--color-text-dim); }

// L2 浏览网格
.browse-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 10px;
}
.browse-item {
  border: 1px solid var(--color-border);
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  background: var(--color-card);
  transition: border-color 0.15s;
  &:hover { border-color: var(--color-primary); }
}
.item-thumb {
  position: relative;
  height: 100px;
  display: flex; align-items: center; justify-content: center;
  background: var(--color-elevated);
  overflow: hidden;
}
.item-cover { width: 100%; height: 100%; object-fit: cover; }
.play-overlay {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
  font-size: 22px; color: rgba(255, 255, 255, 0.85);
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6);
  pointer-events: none;
}
.item-name {
  padding: 6px 8px 2px; font-size: 12px; color: var(--color-text);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.item-size { padding: 0 8px 6px; font-size: 10px; color: var(--color-text-dim); }
.no-preview { padding: 32px; text-align: center; color: var(--color-text-dim); }
</style>
