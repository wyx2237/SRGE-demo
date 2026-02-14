<template>
  <el-card shadow="never" class="card-clear-mb">
    <template #header>
      <div class="header">
        <div class="title">规则列表</div>
        <div class="actions">
          <el-input v-model="keyword" placeholder="搜索规则名称" clearable style="width: 260px" />
          <el-button type="primary" @click="$router.push('/rules/create')">新建规则</el-button>
        </div>
      </div>
    </template>

    <el-table :data="filtered" stripe style="width: 100%">
      <el-table-column prop="name" label="名称" min-width="240">
        <template #default="{ row }">
          <div class="name">
            <span class="dot" />
            <span class="ellipsis-text">{{ row.name }}</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="type" label="类型" width="140" />
      <el-table-column prop="status" label="状态" width="140">
        <template #default="{ row }">
          <el-tag :type="row.status === '已发布' ? 'success' : 'warning'">{{ row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="updatedAt" label="更新时间" width="180" />
      <el-table-column label="操作" width="160" fixed="right">
        <template #default>
          <el-button link type="primary">查看</el-button>
          <el-button link type="primary">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

defineOptions({ name: 'RulesListView' })

const keyword = ref('')

const rows = ref([
  { name: '当订单金额 > 1000 时需要二级审批', type: '审批', status: '已发布', updatedAt: '2026-01-21 10:12' },
  { name: '用户连续 3 次登录失败则锁定 30 分钟', type: '安全', status: '草稿', updatedAt: '2026-01-20 18:40' },
  { name: '新客首单发放优惠券并推送消息', type: '营销', status: '已发布', updatedAt: '2026-01-19 09:05' },
])

const filtered = computed(() => {
  const k = keyword.value.trim().toLowerCase()
  if (!k) return rows.value
  return rows.value.filter((r) => r.name.toLowerCase().includes(k))
})
</script>

<style scoped lang="scss">
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}
.title {
  font-weight: 800;
}
.actions {
  display: flex;
  align-items: center;
  gap: 12px;
}
.name {
  display: flex;
  align-items: center;
  gap: 10px;
}
.dot {
  width: 8px;
  height: 8px;
  border-radius: 99px;
  background: var(--el-color-primary);
  flex-shrink: 0;
  box-shadow: 0 0 0 4px color-mix(in srgb, var(--el-color-primary) 18%, transparent);
}
</style>


