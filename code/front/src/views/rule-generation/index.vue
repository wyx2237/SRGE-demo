<template>
  <div class="page-container">

    <!-- 视图 1: 规则列表 -->
    <!-- 使用 v-if 和 v-else-if 确保同一时间只渲染一个视图 -->
    <div v-if="!showGraphicalDisplay" class="view-wrapper list-view">
      <el-card shadow="never" class="main-card">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <h2 class="title">规则库管理</h2>
              <el-tag type="info" round effect="plain">{{ rules.length }} Rules</el-tag>
            </div>
            <div class="header-right">
              <el-input v-model="searchQuery" placeholder="搜索规则名称或ID..." prefix-icon="Search" style="width: 240px"
                clearable />
              <el-button type="primary" icon="Plus">新建规则</el-button>
            </div>
          </div>
        </template>

        <div class="rule-list">
          <el-scrollbar max-height="calc(100vh - 200px)">
            <div v-for="rule in filteredRules" :key="rule.id" class="rule-item" @click="handleRuleClick(rule)">
              <div class="rule-icon">
                <el-icon :size="24" :color="getStatusColor(rule.status)">
                  <component :is="rule.icon" />
                </el-icon>
              </div>

              <div class="rule-info">
                <div class="rule-name">
                  {{ rule.name }}
                  <span class="rule-id">#{{ rule.id }}</span>
                </div>
                <div class="rule-meta">
                  最后更新: {{ rule.updatedAt }} · 版本: v{{ rule.version }}
                </div>
              </div>

              <div class="rule-status">
                <el-tag :type="getStatusType(rule.status)" size="small">
                  {{ rule.status }}
                </el-tag>
                <el-icon class="arrow-icon">
                  <ArrowRight />
                </el-icon>
              </div>
            </div>

            <el-empty v-if="filteredRules.length === 0" description="未找到匹配的规则" />
          </el-scrollbar>
        </div>
      </el-card>
    </div>

    <!-- 视图 2: 规则详情 (引入子组件) -->
    <div v-else-if="showGraphicalDisplay" class="view-wrapper detail-view">
      <!-- 只有当 selectedRule 存在时才渲染子组件，避免空指针报错 -->
      <RuleDetail v-if="selectedRule" :rule="selectedRule" @back="showGraphicalDisplay = false" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Search, Plus, ArrowRight, DataAnalysis, Operation, Connection, Cpu } from '@element-plus/icons-vue'
// 确保这里的路径是正确的！如果 components 文件夹在同级，这样写是对的
import RuleDetail from './components/RuleDetail.vue'

defineOptions({ name: 'RuleGenerationView' })

interface Rule {
  id: string
  name: string
  status: 'Active' | 'Draft' | 'Testing'
  updatedAt: string
  version: string
  icon: any
}

const showGraphicalDisplay = ref(false)
const searchQuery = ref('')
const selectedRule = ref<Rule | null>(null)

const rules = ref<Rule[]>([
  { id: 'R-1001', name: 'BMI 肥胖指数计算', status: 'Active', updatedAt: '2023-11-20 14:30', version: '2.1', icon: DataAnalysis },
  { id: 'R-1002', name: 'eGFR 肾小球滤过率', status: 'Active', updatedAt: '2023-11-19 09:15', version: '1.5', icon: Operation },
  { id: 'R-1003', name: 'CHA2DS2-VASc 评分', status: 'Testing', updatedAt: '2023-11-21 16:00', version: '0.9', icon: Connection },
  { id: 'R-1004', name: '糖尿病风险预测逻辑', status: 'Draft', updatedAt: '2023-11-18 11:20', version: '0.1', icon: Cpu },
  { id: 'R-1005', name: '儿童生长发育评估', status: 'Active', updatedAt: '2023-10-05 10:00', version: '3.0', icon: DataAnalysis },
])

const filteredRules = computed(() => {
  if (!searchQuery.value) return rules.value
  const query = searchQuery.value.toLowerCase()
  return rules.value.filter(r =>
    r.name.toLowerCase().includes(query) ||
    r.id.toLowerCase().includes(query)
  )
})

const handleRuleClick = (rule: Rule) => {
  selectedRule.value = rule
  showGraphicalDisplay.value = true
}

const getStatusType = (status: string) => {
  switch (status) {
    case 'Active': return 'success'
    case 'Testing': return 'warning'
    case 'Draft': return 'info'
    default: return ''
  }
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'Active': return '#67C23A'
    case 'Testing': return '#E6A23C'
    case 'Draft': return '#909399'
    default: return '#409EFF'
  }
}
</script>

<style scoped lang="scss">
.page-container {
  height: 100%;
  min-height: 600px;
  display: flex;
  flex-direction: column;
}

.view-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.main-card {
  flex: 1;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  /* 移除 main-card 可能存在的背景设置，让 Element 自动处理 */
}

/* 头部样式 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .header-left {
    display: flex;
    align-items: center;
    gap: 12px;

    .title {
      margin: 0;
      font-size: 18px;
      font-weight: 700;
      color: var(--el-text-color-primary);
      /* 使用变量 */
    }
  }

  .header-right {
    display: flex;
    gap: 12px;
  }
}

/* 列表项样式 */
.rule-list {
  padding: 10px 0;
  flex: 1;
}

.rule-item {
  display: flex;
  align-items: center;
  padding: 16px;
  margin-bottom: 12px;
  border-radius: 8px;

  /* --- 修复点：背景色改为变量 --- */
  background-color: var(--el-bg-color);
  /* 在暗黑模式下会自动变深色 */
  border: 1px solid var(--el-border-color);
  /* 使用标准边框变量 */

  transition: all 0.3s ease;
  cursor: pointer;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    border-color: var(--el-color-primary-light-5);
    transform: translateY(-2px);

    /* 悬停时背景稍微亮一点/不同一点 */
    background-color: var(--el-bg-color-overlay);

    .arrow-icon {
      transform: translateX(4px);
      color: var(--el-color-primary);
    }
  }

  .rule-icon {
    width: 40px;
    height: 40px;
    border-radius: 8px;

    /* --- 修复点：背景色变量 --- */
    background-color: var(--el-fill-color-light);
    /* Element 标准填充色 */

    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 16px;
  }

  .rule-info {
    flex: 1;

    .rule-name {
      font-weight: 600;
      font-size: 16px;
      color: var(--el-text-color-primary);
      /* 文字颜色变量 */
      margin-bottom: 4px;

      .rule-id {
        font-size: 12px;
        color: var(--el-text-color-placeholder);
        /* 占位符文字颜色变量 */
        font-weight: normal;
        margin-left: 8px;
        font-family: monospace;
      }
    }

    .rule-meta {
      font-size: 13px;
      color: var(--el-text-color-secondary);
      /* 次要文字颜色变量 */
    }
  }

  .rule-status {
    display: flex;
    align-items: center;
    gap: 16px;

    .arrow-icon {
      transition: all 0.3s;
      color: var(--el-text-color-placeholder);
    }
  }
}
</style>