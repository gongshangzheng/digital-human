<template>
  <div class="speedrun-page">
    <n-card size="small">
      <template #header>
        <div class="toolbar">
          <span class="page-title">Speed Run</span>
          <n-select
            v-model:value="filterModel" :options="modelOptions" placeholder="模型"
            size="small" clearable filterable style="width: 180px"
          />
          <n-select
            v-model:value="filterVideo" :options="videoOptions" placeholder="视频"
            size="small" clearable filterable style="width: 200px"
          />
          <n-tag v-if="accuracy !== null" size="small" :type="accuracy >= 0.5 ? 'success' : 'warning'" :bordered="false">
            准确率 {{ (accuracy * 100).toFixed(0) }}%
          </n-tag>
        </div>
      </template>
      <template #header-extra>
        <n-tag size="small" :type="status.running ? 'info' : 'success'" :bordered="false">
          {{ status.running ? `运行中 · 已出 ${status.results_count} 条` : `共 ${filteredResults.length} 条` }}
        </n-tag>
        <n-button size="tiny" quaternary style="margin-left: 8px" @click="loadAll">刷新</n-button>
      </template>

      <n-spin :show="loading">
        <n-grid v-if="pagedResults.length" cols="3 600:2 900:3 1200:4" :x-gap="12" :y-gap="12" responsive="screen">
          <n-grid-item v-for="r in pagedResults" :key="r.id">
            <div class="video-card" @click="playVideo(r)">
              <div class="thumb">
                <img v-if="r.cover_image" :src="getSpeedrunOutputUrl(r.cover_image)" class="cover-img" loading="lazy" />
                <n-icon v-else size="36"><play-circle-outline /></n-icon>
                <span class="play-overlay">▶</span>
                <span v-if="r.correct === true" class="badge correct">✓</span>
                <span v-else-if="r.correct === false" class="badge wrong">✗</span>
                <span v-else class="badge na">—</span>
              </div>
              <div class="card-body">
                <div class="row model">{{ r.model_id }}</div>
                <div class="row pred">
                  {{ r.metrics?.top1_label || '—' }}
                  <em v-if="r.metrics?.top1_score != null">{{ Number(r.metrics.top1_score).toFixed(2) }}</em>
                </div>
                <div class="row stats">{{ statsLine(r) }}</div>
                <div class="row video-name">{{ r.video }}</div>
              </div>
            </div>
          </n-grid-item>
        </n-grid>
        <EmptyState
          v-else-if="!loading"
          description="暂无 Speed Run 结果。下游库跑批后 results/speedrun/results.json 会出现在这里。"
        />

        <n-pagination
          v-if="filteredResults.length > pageSize"
          v-model:page="page"
          :page-count="pageCount"
          :page-size="pageSize"
          size="small"
          style="margin-top: 12px; justify-content: center"
        />
      </n-spin>
    </n-card>

    <VideoModal v-model:show="modalShow" :title="modalTitle" :src="modalSrc" />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { NCard, NSpin, NButton, NIcon, NTag, NSelect, NGrid, NGridItem, NPagination } from 'naive-ui'
import { PlayCircleOutline } from '@vicons/ionicons5'
import EmptyState from '../../components/common/EmptyState.vue'
import VideoModal from '../../components/common/VideoModal.vue'
import { getSpeedrunResults, getSpeedrunStatus, getSpeedrunOutputUrl } from '../../api/evaluation'

const results = ref([])
const status = ref({ running: false, results_count: 0 })
const loading = ref(false)

const filterModel = ref(null)
const filterVideo = ref(null)

const page = ref(1)
const pageSize = 20

const modalShow = ref(false)
const modalTitle = ref('')
const modalSrc = ref('')

const modelOptions = computed(() =>
  [...new Set(results.value.map(r => r.model_id))].map(v => ({ label: v, value: v })))
const videoOptions = computed(() =>
  [...new Set(results.value.map(r => r.video))].map(v => ({ label: v, value: v })))

const filteredResults = computed(() => results.value.filter(r =>
  (!filterModel.value || r.model_id === filterModel.value) &&
  (!filterVideo.value || r.video === filterVideo.value)))

const pageCount = computed(() => Math.ceil(filteredResults.value.length / pageSize))
const pagedResults = computed(() => {
  const start = (page.value - 1) * pageSize
  return filteredResults.value.slice(start, start + pageSize)
})
watch([filterModel, filterVideo], () => { page.value = 1 })

const accuracy = computed(() => {
  const judged = filteredResults.value.filter(r => r.correct === true || r.correct === false)
  if (!judged.length) return null
  return judged.filter(r => r.correct).length / judged.length
})

function statsLine(r) {
  const parts = []
  if (r.gpu_mem_mb != null) parts.push(`${r.gpu_mem_mb}MB`)
  if (r.elapsed_s != null) parts.push(`${r.elapsed_s}s`)
  if (r.gpu_avg_util != null) parts.push(`${r.gpu_avg_util}%`)
  if (r.rtf != null) parts.push(`RTF ${r.rtf}`)
  return parts.join(' · ') || '—'
}

function playVideo(r) {
  modalTitle.value = `${r.model_id} · ${r.video}`
  modalSrc.value = r.output_video ? getSpeedrunOutputUrl(r.output_video) : ''
  modalShow.value = true
}

async function loadAll() {
  loading.value = true
  try {
    const [res, st] = await Promise.all([getSpeedrunResults(), getSpeedrunStatus()])
    results.value = res.results || []
    status.value = st
  } catch { /* 保持旧数据 */ }
  loading.value = false
}

let pollTimer = null
function startPollingIfRunning() {
  if (pollTimer) return
  pollTimer = setInterval(async () => {
    try {
      const st = await getSpeedrunStatus()
      status.value = st
      if (st.running) {
        const res = await getSpeedrunResults()
        results.value = res.results || []
      } else if (results.value.length) {
        clearInterval(pollTimer)
        pollTimer = null
      }
    } catch { /* 轮询失败忽略 */ }
  }, 3000)
}

onMounted(async () => {
  await loadAll()
  if (status.value.running) startPollingIfRunning()
})
onUnmounted(() => { if (pollTimer) clearInterval(pollTimer) })
</script>

<style scoped lang="scss">
.speedrun-page { padding: 4px 8px; }

.toolbar { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.page-title { font-size: 15px; font-weight: 600; }

.video-card {
  border: 1px solid var(--color-border);
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  background: var(--color-card);
  transition: border-color 0.15s;
  &:hover { border-color: var(--color-primary); }
}

.thumb {
  position: relative;
  height: 120px;
  display: flex; align-items: center; justify-content: center;
  background: #000;
  color: rgba(255, 255, 255, 0.9);
  overflow: hidden;

  .cover-img { width: 100%; height: 100%; object-fit: cover; }
  .play-overlay {
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    font-size: 28px; color: rgba(255, 255, 255, 0.8);
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6);
    pointer-events: none;
  }
  .badge {
    position: absolute; top: 6px; left: 8px;
    width: 22px; height: 22px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    color: #fff; font-size: 12px;
    &.correct { background: #22c55e; }
    &.wrong { background: #ef4444; }
    &.na { background: #71717a; }
  }
}

.card-body {
  padding: 8px 10px;
  .row {
    font-size: 12px; line-height: 1.6;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  .model { font-weight: 600; color: var(--color-text); }
  .pred {
    color: var(--color-text-secondary);
    em { font-style: normal; color: var(--color-text-dim); margin-left: 4px; font-variant-numeric: tabular-nums; }
  }
  .stats { color: var(--color-text-dim); font-variant-numeric: tabular-nums; }
  .video-name { color: var(--color-text-dim); font-style: italic; font-size: 10px; }
}
</style>
