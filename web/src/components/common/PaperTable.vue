<template>
  <div class="paper-table">
    <n-data-table
      :columns="columns"
      :data="rows"
      :pagination="{ pageSize: 20 }"
      :row-key="(row) => row.key"
      :scroll-x="1100"
      size="small"
      striped
    />
  </div>
</template>

<script setup>
import { computed, h } from 'vue'
import { useRouter } from 'vue-router'
import { NDataTable, NTag, NButton } from 'naive-ui'

const props = defineProps({
  papers: { type: Array, default: () => [] },
})

const router = useRouter()

const METHOD_FAMILY_COLORS = {
  'lip-sync': 'blue',
  '2d-talking-head': 'cyan',
  'motion-space-diffusion': 'purple',
  '3d-avatar': 'green',
  'diffusion-foundation': 'magenta',
  'streaming-realtime': 'orange',
  'action-generation': 'gold',
  'identity': 'red',
  'agent-system': 'teal',
  'engineering': 'default',
  'evaluation': 'lime',
  'stylized': 'pink',
  'survey': 'default',
}

// 一篇文章可含多条 qa：每条 qa 展开为一行，论文级字段随行携带。
const rows = computed(() => {
  const out = []
  for (const p of props.papers || []) {
    const qas = Array.isArray(p.qa) && p.qa.length ? p.qa : [{ question: '', answer: '' }]
    qas.forEach((qa, idx) => {
      out.push({
        key: `${p.id}#${idx}`,
        seq: p.seq,
        title: p.title || p.title_zh || p.id,
        title_zh: p.title_zh || '',
        id: p.id,
        institution: p.institution || '',
        venue: p.venue || '',
        year: p.year ?? null,
        method_family: p.method_family || '',
        question: qa.question || '',
        answer: qa.answer || '',
        derives_from: Array.isArray(p.derives_from) ? p.derives_from : [],
        note: p.note || '',
        note_type: p.note_type || '',
        blog_url: p.blog_url || '',
      })
    })
  }
  return out
})

function internalDocUrl(slug) {
  return `/management/docs/${slug.split('/').map(encodeURIComponent).join('/')}`
}

function openDoc(slug) {
  router.push(internalDocUrl(slug))
}

function linkButton(label, onClick, title) {
  return h(
    NButton,
    { size: 'tiny', quaternary: true, type: 'primary', title, onClick },
    { default: () => label },
  )
}

const columns = [
  {
    title: '#',
    key: 'seq',
    width: 52,
    sorter: (a, b) => (a.seq || 0) - (b.seq || 0),
  },
  {
    title: '论文',
    key: 'title',
    width: 260,
    ellipsis: { tooltip: true },
    sorter: (a, b) => String(a.title).localeCompare(String(b.title)),
    render: (row) => {
      if (row.blog_url) {
        return h(
          'a',
          { href: row.blog_url, target: '_blank', rel: 'noopener', title: row.title_zh },
          row.title,
        )
      }
      return row.title
    },
  },
  {
    title: '发布机构',
    key: 'institution',
    width: 180,
    ellipsis: { tooltip: true },
    sorter: (a, b) => String(a.institution).localeCompare(String(b.institution)),
    render: (row) => row.institution || '未标注',
  },
  {
    title: '发表',
    key: 'year',
    width: 150,
    ellipsis: { tooltip: true },
    sorter: (a, b) => (a.year || 0) - (b.year || 0),
    render: (row) => [row.venue, row.year].filter(Boolean).join(' · ') || '未标注',
  },
  {
    title: '方法族',
    key: 'method_family',
    width: 150,
    filterOptions: [...new Set(rows.value.map((r) => r.method_family).filter(Boolean))]
      .map((v) => ({ label: v, value: v })),
    filter: (value, row) => row.method_family === value,
    render: (row) =>
      row.method_family
        ? h(NTag, { size: 'small', bordered: false, type: METHOD_FAMILY_COLORS[row.method_family] || 'default' }, { default: () => row.method_family })
        : '',
  },
  {
    title: '提出的问题',
    key: 'question',
    width: 300,
    ellipsis: { tooltip: true },
    render: (row) => row.question || '—',
  },
  {
    title: '解法',
    key: 'answer',
    width: 360,
    ellipsis: { tooltip: true },
    render: (row) => row.answer || '—',
  },
  {
    title: '继承自',
    key: 'derives_from',
    width: 180,
    render: (row) => (row.derives_from.length ? row.derives_from.join('、') : '—'),
  },
  {
    title: '笔记',
    key: 'note',
    width: 130,
    render: (row) => {
      const links = []
      if (row.note_type === 'doc' && row.note) {
        links.push(linkButton('详读', () => openDoc(row.note), row.note))
      } else if (row.note) {
        links.push(
          h('a', { href: row.note, target: '_blank', rel: 'noopener' }, '笔记'),
        )
      }
      if (row.blog_url) {
        links.push(h('a', { href: row.blog_url, target: '_blank', rel: 'noopener', class: 'paper-link-gap' }, '博客'))
      }
      return links.length ? links : '未建'
    },
  },
]
</script>

<style scoped lang="scss">
.paper-table {
  margin: 16px 0;
}

:deep(.paper-link-gap) {
  margin-left: 8px;
  color: var(--color-primary);
}
</style>
