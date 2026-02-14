<template>
  <div class="step-content-wrapper">
    <div class="modern-card">

      <!-- 1. Header Area -->
      <div class="card-header-flex">
        <div class="header-left">
          <div class="step-badge">STEP 03</div>
          <h2 class="title">Rule Generation</h2>
          <p class="subtitle">
            AI-driven transformation of textual questions into executable structured rules.
          </p>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner">
          <div class="spinner-ring"></div>
          <el-icon class="spinner-icon">
            <MagicStick />
          </el-icon>
        </div>
        <p class="loading-text">Analyzing question and generating rule...</p>
      </div>

      <!-- Rule Visualization Area -->
      <div v-else-if="ruleData" class="rule-visualizer">

        <!-- Custom Collapse -->
        <el-collapse v-model="activeRuleSections" class="custom-collapse">

          <!-- 1) Meta Info -->
          <el-collapse-item name="meta">
            <template #title>
              <div class="collapse-header-content" :class="{ 'is-active': activeRuleSections.includes('meta') }">
                <div class="header-main">
                  <div class="icon-box blue"><el-icon>
                      <Collection />
                    </el-icon></div>
                  <span class="header-title">Meta Info</span>
                </div>
                <transition name="fade">
                  <div v-if="!activeRuleSections.includes('meta')" class="header-summary">
                    <el-tag type="success" size="small" effect="plain" round>Name</el-tag>
                    <el-tag type="success" size="small" effect="plain" round>Description</el-tag>
                    <span class="divider">|</span>
                    <span class="summary-text-light">Click to view details</span>
                  </div>
                </transition>
                <div class="header-toggle"><el-icon class="toggle-icon">
                    <ArrowDown />
                  </el-icon></div>
              </div>
            </template>
            <div class="panel-body">
              <div class="meta-card">
                <div class="meta-content">
                  <div class="meta-title-row">
                    <h3>{{ ruleData.name }}</h3>
                  </div>
                  <p class="meta-desc">{{ ruleData.description }}</p>
                </div>
              </div>
            </div>
          </el-collapse-item>

          <!-- 2) Input Info -->
          <el-collapse-item name="input">
            <template #title>
              <div class="collapse-header-content" :class="{ 'is-active': activeRuleSections.includes('input') }">
                <div class="header-main">
                  <div class="icon-box purple"><el-icon>
                      <BottomLeft />
                    </el-icon></div>
                  <span class="header-title">Input Info</span>
                </div>
                <transition name="fade">
                  <div v-if="!activeRuleSections.includes('input')" class="header-summary">
                    <el-tag size="small" effect="plain" round>{{ ruleData.inputs.length }} Variables</el-tag>
                    <span class="divider">|</span>
                    <span class="summary-text-light">Click to view details</span>
                  </div>
                </transition>
                <div class="header-toggle"><el-icon class="toggle-icon">
                    <ArrowDown />
                  </el-icon></div>
              </div>
            </template>
            <div class="panel-body">
              <div class="table-wrapper">
                <el-table :data="ruleData.inputs" :border="false" class="modern-table">
                  <el-table-column prop="input_name" label="Variable Name" width="240">
                    <template #default="{ row }">
                      <div class="code-pill primary">{{ row.input_name }}</div>
                    </template>
                  </el-table-column>
                  <el-table-column prop="input_type" label="Type" width="120">
                    <template #default="{ row }">
                      <span class="type-text">{{ row.input_type }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column prop="input_desc" label="Description" />
                </el-table>
              </div>
            </div>
          </el-collapse-item>

          <!-- 3) Steps Info -->
          <el-collapse-item name="steps">
            <template #title>
              <div class="collapse-header-content" :class="{ 'is-active': activeRuleSections.includes('steps') }">
                <div class="header-main">
                  <div class="icon-box orange"><el-icon>
                      <Operation />
                    </el-icon></div>
                  <span class="header-title">Steps Info</span>
                </div>
                <transition name="fade">
                  <div v-if="!activeRuleSections.includes('steps')" class="header-summary">
                    <el-tag type="warning" size="small" effect="plain" round>{{ ruleData.steps.length }} Steps</el-tag>
                    <span class="divider">|</span>
                    <span class="summary-text-light">Click to view details</span>
                  </div>
                </transition>
                <div class="header-toggle"><el-icon class="toggle-icon">
                    <ArrowDown />
                  </el-icon></div>
              </div>
            </template>

            <div class="panel-body bg-gray">
              <div class="timeline-container">
                <el-timeline>
                  <el-timeline-item v-for="(step, index) in ruleData.steps" :key="step.step_id"
                    :color="getCategoryColor(step.category)" :timestamp="`Step ${step.step_id}`" placement="top"
                    hide-timestamp class="custom-timeline-item">

                    <!-- 使用独立组件，只需传入 step 数据 -->
                    <StepCard :step="step" />

                  </el-timeline-item>
                </el-timeline>
              </div>
            </div>
          </el-collapse-item>

          <!-- 4) Output Info -->
          <el-collapse-item name="output">
            <template #title>
              <div class="collapse-header-content" :class="{ 'is-active': activeRuleSections.includes('output') }">
                <div class="header-main">
                  <div class="icon-box green"><el-icon>
                      <VideoPlay />
                    </el-icon></div>
                  <span class="header-title">Output Info</span>
                </div>
                <transition name="fade">
                  <div v-if="!activeRuleSections.includes('output')" class="header-summary">
                    <el-tag type="success" size="small" effect="plain" round>1 Return</el-tag>
                    <span class="divider">|</span>
                    <span class="summary-text-light">Click to view details</span>
                  </div>
                </transition>
                <div class="header-toggle"><el-icon class="toggle-icon">
                    <ArrowDown />
                  </el-icon></div>
              </div>
            </template>
            <div class="panel-body">
              <div class="table-wrapper">
                <el-table :data="[ruleData.output]" :border="false" class="modern-table">
                  <el-table-column prop="output_name" label="Output Name" width="240">
                    <template #default="{ row }">
                      <div class="code-pill success">{{ row.output_name }}</div>
                    </template>
                  </el-table-column>
                  <el-table-column prop="output_type" label="Type" width="120">
                    <template #default="{ row }">
                      <span class="type-text">{{ row.output_type }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column prop="output_desc" label="Description" />
                </el-table>
              </div>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <div class="empty-content">
          <el-icon class="empty-icon">
            <MagicStick />
          </el-icon>
          <h3 class="empty-title">Ready to Generate Rule</h3>
          <p class="empty-desc">Click the button below to start AI-driven rule generation...</p>
          <el-button type="primary" size="large" round class="generate-btn" @click="regenerateRule" :loading="loading">
            <el-icon class="el-icon--left">
              <MagicStick />
            </el-icon>
            Rule Generation
          </el-button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { ElMessage } from 'element-plus';
import {
  Collection, BottomLeft, Operation, VideoPlay,
  Tools, Aim, MagicStick, ArrowDown
} from '@element-plus/icons-vue';
import { mockRule } from '@/stores/mockData';
import StepCard from './StepCard.vue';

const props = defineProps<{
  formData: {
    rule: string;
  }
}>();

const loading = ref(false);
const activeRuleSections = ref<string[]>([]);

const ruleData = computed(() => {
  try {
    return props.formData.rule ? JSON.parse(props.formData.rule) : null;
  } catch (e) {
    return null;
  }
});

onMounted(() => {
  if (props.formData.rule) {
    activeRuleSections.value = ['meta'];
  }
});

const regenerateRule = () => {
  loading.value = true;
  setTimeout(() => {
    const newRule = JSON.parse(JSON.stringify(mockRule));
    props.formData.rule = JSON.stringify(newRule, null, 2);
    loading.value = false;
    activeRuleSections.value = ['meta', 'input', 'steps', 'output'];
    ElMessage.success('Rule generated successfully');
  }, 1500);
};

const getCategoryColor = (category: string) => {
  const map: Record<string, string> = {
    FormulaCalculation: '#3b82f6',
    DiscreteValueMapping: '#8b5cf6',
    ConditionEvaluation: '#f59e0b',
    Preprocessing: '#64748b'
  };
  return map[category] || '#3b82f6';
};
</script>

<style scoped lang="scss">
/* 全局容器 (保持不变) */
.step-content-wrapper {
  width: 100%;
  font-family: 'Inter', -apple-system, sans-serif;
  animation: slideUp 0.6s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.modern-card {
  background: var(--el-bg-color);
  border-radius: 20px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 10px 15px -3px rgba(0, 0, 0, 0.05);
  border: 1px solid var(--el-border-color-lighter);
  padding: 40px;
  box-sizing: border-box;
  width: 100%;
  position: relative;
  min-height: 400px;
}

/* 1. Header (保持不变) */
.card-header-flex {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;

  .header-left {
    .step-badge {
      display: inline-block;
      font-size: 0.75rem;
      font-weight: 800;
      color: #2563eb;
      background: #eff6ff;
      padding: 6px 12px;
      border-radius: 30px;
      letter-spacing: 1px;
      margin-bottom: 16px;
    }

    .title {
      font-size: 1.75rem;
      font-weight: 800;
      color: #0f172a;
      margin: 0 0 8px 0;
    }

    .subtitle {
      font-size: 1rem;
      color: #64748b;
      margin: 0;
    }
  }
}

/* --- Custom Collapse Styling (保持不变) --- */
.custom-collapse {
  border: none;
  display: flex;
  flex-direction: column;
  gap: 16px;

  :deep(.el-collapse-item) {
    border: 1px solid var(--el-border-color-lighter);
    border-radius: 12px;
    overflow: hidden;
    transition: all 0.3s ease;

    &.is-active {
      border-color: #bfdbfe;
      box-shadow: 0 4px 12px rgba(59, 130, 246, 0.08);
    }
  }

  :deep(.el-collapse-item__arrow) {
    display: none;
  }

  :deep(.el-collapse-item__header) {
    height: auto;
    line-height: normal;
    background: transparent;
    padding: 0;
    border: none;
    font-size: 1rem;
    color: inherit;
    display: block;
  }

  :deep(.el-collapse-item__wrap) {
    border: none;
    background: transparent;
  }

  :deep(.el-collapse-item__content) {
    padding: 0;
  }
}

/* Custom Header Content (保持不变) */
.collapse-header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: #f8fafc;
  cursor: pointer;
  transition: background-color 0.3s ease;

  &.is-active {
    background: #eff6ff;

    .header-toggle {
      background: #3b82f6;
      color: #fff;
      transform: rotate(180deg);
    }
  }

  &:hover:not(.is-active) {
    background: #f1f5f9;
  }

  .header-main {
    display: flex;
    align-items: center;
    gap: 12px;

    .icon-box {
      width: 36px;
      height: 36px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;

      &.blue {
        background: #dbeafe;
        color: #1e40af;
      }

      &.purple {
        background: #f3e8ff;
        color: #6b21a8;
      }

      &.orange {
        background: #ffedd5;
        color: #9a3412;
      }

      &.green {
        background: #dcfce7;
        color: #166534;
      }
    }

    .header-title {
      font-weight: 700;
      color: #334155;
      font-size: 1rem;
    }
  }

  .header-summary {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 12px;
    margin-right: 20px;
    font-size: 0.85rem;
    color: #64748b;

    .divider {
      color: #cbd5e1;
      font-size: 0.8rem;
    }

    .summary-text-light {
      opacity: 0.7;
      font-size: 0.8rem;
    }
  }

  .header-toggle {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #e2e8f0;
    color: #64748b;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }
}

/* Panel Body Content */
.panel-body {
  padding: 24px;
  background: #fff;
  border-top: 1px solid #f1f5f9;

  &.bg-gray {
    background: #fcfcfc;
  }
}

/* Meta & Table Styles (保持不变) */
.meta-card {
  .meta-title-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;

    h3 {
      margin: 0;
      font-size: 1.25rem;
      color: #1e293b;
    }
  }

  .meta-desc {
    margin: 0;
    color: #64748b;
    line-height: 1.6;
  }
}

.table-wrapper {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

.modern-table {
  :deep(th.el-table__cell) {
    background: #f8fafc !important;
    color: #64748b;
    font-weight: 600;
    font-size: 0.85rem;
    text-transform: uppercase;
  }

  .code-pill {
    font-family: 'Consolas', monospace;
    font-size: 0.9rem;
    padding: 4px 8px;
    border-radius: 6px;
    font-weight: 600;
    display: inline-block;

    &.primary {
      background: #eff6ff;
      color: #2563eb;
    }

    &.success {
      background: #ecfdf5;
      color: #059669;
    }
  }

  .type-text {
    color: #64748b;
    font-size: 0.9rem;
    font-weight: 500;
    background: #f1f5f9;
    padding: 2px 8px;
    border-radius: 4px;
  }
}

/* Timeline Styles (Modified) */
.timeline-container {
  padding: 0 10px;
}


@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>