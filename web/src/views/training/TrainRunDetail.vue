<template>
  <div class="run-detail">
    <n-card size="small">
      <template #header>
        <n-space align="center" size="small">
          <n-button size="small" quaternary @click="$router.push('/training/results')">← 返回</n-button>
          <h3>{{ run?.id || '运行详情' }}</h3>
          <n-tag v-if="run" :type="statusType" size="small" :bordered="false">{{ run.status }}</n-tag>
          <n-tag v-if="isRunning" type="info" size="small" :bordered="false">实时刷新中…</n-tag>
        </n-space>
      </template>
      <template #header-extra>
        <n-button size="small" :loading="loading" @click="load">刷新</n-button>
      </template>

      <n-spin :show="loading">
        <div v-if="run">
          <n-descriptions :column="4" size="small" label-placement="left" bordered>
            <n-descriptions-item label="模型">{{ run.model || '-' }}</n-descriptions-item>
            <n-descriptions-item label="数据集">{{ run.dataset || '-' }}</n-descriptions-item>
            <n-descriptions-item label="epochs">{{ run.epochs ?? '-' }}</n-descriptions-item>
            <n-descriptions-item label="lr">{{ fmt(run.lr) }}</n-descriptions-item>
            <n-descriptions-item label="batch_size">{{ run.batch_size ?? '-' }}</n-descriptions-item>
            <n-descriptions-item label="device">{{ run.device || '-' }}</n-descriptions-item>
            <n-descriptions-item label="开始">{{ fmtTime(run.started_at) }}</n-descriptions-item>
            <n-descriptions-item label="模式">{{ runMode }}</n-descriptions-item>
            <n-descriptions-item v-if="run.final_loss != null" label="final_loss">{{ fmt(run.final_loss) }}</n-descriptions-item>
            <n-descriptions-item v-if="run.best_metric != null" label="best_metric">{{ fmt(run.best_metric) }}</n-descriptions-item>
          </n-descriptions>

          <div v-if="run.checkpoint_path || run.best_checkpoint_path" class="cp-block">
            <div class="block-title">Checkpoint</div>
            <n-space size="small">
              <n-tag v-if="run.checkpoint_path" size="small" :bordered="false">latest: {{ run.checkpoint_path }}</n-tag>
              <n-tag v-if="run.best_checkpoint_path" size="small" type="success" :bordered="false">best: {{ run.best_checkpoint_path }}</n-tag>
            </n-space>
          </div>
        </div>
        <EmptyState v-else-if="!loading" description="run 不存在，或 results/training/metrics.json 中没有这条记录。" />
      </n-spin>
    </n-card>

    <!-- 曲线区：loss / 其它指标（自动发现）/ lr -->
    <n-card v-if="lossChart || metricChart || lrChart" size="small" title="训练曲线" class="mt">
      <div v-if="lossChart" class="chart-block">
        <div class="chart-title">Loss</div>
        <v-chart class="chart" :option="lossChart" autoresize />
      </div>
      <div v-if="metricChart" class="chart-block">
        <div class="chart-title">指标</div>
        <v-chart class="chart" :option="metricChart" autoresize />
      </div>
      <div v-if="lrChart" class="chart-block">
        <div class="chart-title">Learning Rate</div>
        <v-chart class="chart" :option="lrChart" autoresize />
      </div>
    </n-card>

    <!-- 可视化样本：按 epoch 分组，组内左右切换 -->
    <n-card v-for="group in visGroups" :key="group.epoch" size="small" class="mt">
      <template #header>
        <span>
          Epoch {{ group.epoch }}
          <span v-if="correctCount(group) !== null" :class="{ 'vis-all-ok': correctCount(group) === group.samples.length }">
            ({{ correctCount(group) }}/{{ group.samples.length }} correct)
          </span>
          <span v-else class="vis-count">（{{ group.samples.length }} 个样本）</span>
        </span>
      </template>

      <div class="vis-row">
        <button class="vis-nav" :disabled="(visIndex[group.epoch] || 0) === 0" @click="switchVis(group, -1)">◀</button>
        <div v-if="currentSample(group)" class="vis-main">
          <img :src="getVisSampleUrl(currentSample(group).url)" class="vis-img" loading="lazy" />
          <div class="vis-info">
            <span v-if="currentSample(group).correct != null" :class="currentSample(group).correct ? 'vis-ok' : 'vis-err'">
              {{ currentSample(group).correct ? 'OK' : 'WRONG' }}
            </span>
            <span v-if="currentSample(group).gt_label != null" class="vis-dim">GT: {{ currentSample(group).gt_label }}</span>
            <span v-if="currentSample(group).pred_label != null" class="vis-dim">
              pred: {{ currentSample(group).pred_label }}<template v-if="currentSample(group).score != null"> ({{ currentSample(group).score }})</template>
            </span>
            <span class="vis-idx">{{ (visIndex[group.epoch] || 0) + 1 }}/{{ group.samples.length }}</span>
          </div>
        </div>
        <button class="vis-nav" :disabled="(visIndex[group.epoch] || 0) >= group.samples.length - 1" @click="switchVis(group, 1)">▶</button>
      </div>
      <div class="vis-thumbs">
        <div
          v-for="(s, i) in group.samples"
          :key="s.url"
          class="vis-thumb"
          :class="{ active: i === (visIndex[group.epoch] || 0) }"
          @click="visIndex[group.epoch] = i"
        >
          <img :src="getVisSampleUrl(s.url)" loading="lazy" />
        </div>
      </div>
    </n-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { NCard, NSpin, NSpace, NButton, NTag, NDescriptions, NDescriptionsItem } from 'naive-ui'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent, DataZoomComponent } from 'echarts/components'
import EmptyState from '../../components/common/EmptyState.vue'
import { getTrainRunDetail, listVisSamples, getVisSampleUrl } from '../../api/training'

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, LegendComponent, DataZoomComponent])

const route = useRoute()
const runId = route.params.run_id
const loading = ref(false)
const run = ref(null)
const visGroups = ref([])
const visIndex = reactive({})
let pollTimer = null

const RUNNING = ['running', 'started']
const isRunning = computed(() => RUNNING.includes(run.value?.status))
const statusType = computed(() => {
  const s = run.value?.status
  if (s === 'completed') return 'success'
  if (s === 'error' || s === 'failed') return 'error'
  return 'info'
})
const runMode = computed(() => {
  const r = run.value
  if (!r) return '-'
  if (r.pretrained) return 'pretrained finetune'
  if (r.load_from) return `load_from ${r.load_from}`
  if (r.resumed_at) return 'resume'
  if (r.from_scratch) return 'from scratch'
  return 'default'
})

function fmt(v) { return (v == null || isNaN(v)) ? '-' : Number(v).toFixed(4) }
function fmtTime(t) { return t ? String(t).replace('T', ' ').slice(0, 19) : '-' }

function currentSample(group) { return group.samples[visIndex[group.epoch] || 0] }
function correctCount(group) {
  const judged = group.samples.filter(s => s.correct != null)
  return judged.length ? judged.filter(s => s.correct).length : null
}
function switchVis(group, dir) {
  const i = visIndex[group.epoch] || 0
  visIndex[group.epoch] = Math.max(0, Math.min(group.samples.length - 1, i + dir))
}

// 曲线基座：loss_series 数据驱动，不假设指标名（分类 acc / 率失真 psnr-bpp 通吃）
const series = computed(() => run.value?.loss_series || [])
const epochs = computed(() => series.value.map(p => p.epoch))
const ZOOM = [{ type: 'inside' }, { type: 'slider', height: 16, bottom: 8 }]

function baseOption(names, yName, extra = {}) {
  return {
    tooltip: { trigger: 'axis' },
    legend: { data: names, top: 0 },
    grid: { top: 30, left: 55, right: 20, bottom: 40 },
    xAxis: { type: 'category', data: epochs.value, name: 'epoch' },
    yAxis: { type: 'value', name: yName, ...extra },
    dataZoom: ZOOM,
    series: names.map(name => ({
      name, type: 'line', smooth: true, showSymbol: true, symbolSize: 5,
      data: series.value.map(p => p[name] ?? null),
    })),
  }
}

const lossChart = computed(() => {
  if (!series.value.some(p => p.loss != null)) return null
  return baseOption(['loss'], 'loss')
})

// 除 epoch/loss/lr 外的所有数值键自动成线
const metricKeys = computed(() => {
  const keys = new Set()
  for (const p of series.value) {
    for (const [k, v] of Object.entries(p)) {
      if (k === 'epoch' || k === 'loss' || k === 'lr') continue
      if (typeof v === 'number') keys.add(k)
    }
  }
  return [...keys]
})

const metricChart = computed(() => {
  if (!metricKeys.value.length) return null
  return baseOption(metricKeys.value, '指标')
})

const lrChart = computed(() => {
  if (!series.value.some(p => p.lr != null)) return null
  const opt = baseOption(['lr'], 'lr')
  opt.legend = undefined
  opt.grid.top = 10
  opt.series[0].showSymbol = false
  return opt
})

async function loadVis() {
  try {
    const d = await listVisSamples(runId)
    visGroups.value = d.groups || []
    visGroups.value.forEach(g => { if (visIndex[g.epoch] == null) visIndex[g.epoch] = 0 })
  } catch {
    visGroups.value = []
  }
}

async function load() {
  loading.value = true
  try { run.value = await getTrainRunDetail(runId) } catch { run.value = null }
  loading.value = false
  await loadVis()
  if (isRunning.value) startPoll()
  else stopPoll()
}

function startPoll() {
  if (pollTimer) return
  pollTimer = setInterval(async () => {
    try { run.value = await getTrainRunDetail(runId) } catch { /* 瞬时失败不中断轮询 */ }
    await loadVis()
    if (!isRunning.value) stopPoll()
  }, 3000)
}
function stopPoll() { if (pollTimer) { clearInterval(pollTimer); pollTimer = null } }

onMounted(load)
onUnmounted(stopPoll)
</script>

<style scoped lang="scss">
.run-detail { padding: 4px 8px; }
.mt { margin-top: 12px; }
h3 { margin: 0; font-size: 15px; font-weight: 600; }

.cp-block { margin-top: 12px; }
.block-title { font-size: 12px; font-weight: 600; color: var(--color-text-dim); margin-bottom: 6px; }

.chart-block { margin-bottom: 16px; &:last-child { margin-bottom: 0; } }
.chart-title { font-size: 13px; font-weight: 600; color: var(--color-text-secondary); margin-bottom: 4px; }
.chart { height: 200px; width: 100%; }

.vis-row { display: flex; align-items: center; gap: 12px; }
.vis-nav {
  flex-shrink: 0; width: 36px; height: 36px;
  border: none; border-radius: 6px; cursor: pointer; font-size: 14px;
  background: var(--color-elevated); color: var(--color-text-secondary);
  &:hover:not(:disabled) { background: var(--color-hover); color: var(--color-text); }
  &:disabled { opacity: 0.3; cursor: default; }
}
.vis-main { flex: 1; text-align: center; min-width: 0; }
.vis-img { max-width: 100%; max-height: 300px; border-radius: 6px; display: block; margin: 0 auto 8px; }
.vis-info {
  font-size: 12px; display: flex; justify-content: center; align-items: center; gap: 12px;
  .vis-ok { color: #22c55e; font-weight: 600; }
  .vis-err { color: #ef4444; font-weight: 600; }
  .vis-dim { color: var(--color-text-dim); }
  .vis-idx { color: var(--color-text-dim); margin-left: auto; font-variant-numeric: tabular-nums; }
}
.vis-all-ok { color: #22c55e; }
.vis-count { color: var(--color-text-dim); font-size: 12px; }
.vis-thumbs { display: flex; gap: 6px; margin-top: 10px; overflow-x: auto; }
.vis-thumb {
  flex-shrink: 0; width: 60px; height: 45px;
  border: 2px solid transparent; border-radius: 4px; overflow: hidden; cursor: pointer;
  &.active { border-color: var(--color-primary); }
  img { width: 100%; height: 100%; object-fit: cover; }
}
</style>
