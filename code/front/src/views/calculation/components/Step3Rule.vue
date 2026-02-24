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

      <!-- A. Loading State (Optimized) -->
      <div v-if="loading" class="loading-container">
        <!-- AI Brain / Pulse Effect -->
        <div class="ai-processing-visual">
          <div class="core-circle">
            <el-icon>
              <Cpu />
            </el-icon>
          </div>
          <div class="ring r1"></div>
          <div class="ring r2"></div>
          <div class="ring r3"></div>
        </div>

        <!-- Progress Bar & Text -->
        <div class="progress-section">
          <h3 class="loading-title">{{ loadingPhaseText }}</h3>
          <el-progress :percentage="loadingPercentage" :stroke-width="10" striped striped-flow :duration="20"
            :color="customColors" />
          <p class="loading-detail">{{ loadingDetailText }}</p>
        </div>
      </div>

      <!-- B. Rule Visualization Area -->
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

                    <!-- 使用独立组件 (请确保已正确引入 StepCard 组件) -->
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

      <!-- C. Empty State (Optimized) -->
      <div v-else class="empty-state">
        <div class="empty-content">
          <div class="empty-icon-wrapper">
            <el-icon class="empty-icon">
              <MagicStick />
            </el-icon>
            <div class="icon-glow"></div>
          </div>
          <h3 class="empty-title">Ready to Generate Rule</h3>
          <p class="empty-desc">
            Click the button below to start the AI-driven rule generation process.<br>
            The system will analyze the question and construct a logical pipeline.
          </p>
          <el-button type="primary" size="large" round class="generate-btn" @click="regenerateRule" :loading="loading">
            <el-icon class="el-icon--left">
              <MagicStick />
            </el-icon>
            Generate Rule
          </el-button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, onUnmounted } from 'vue';
import { ElMessage } from 'element-plus';
import {
  Collection, BottomLeft, Operation, VideoPlay,
  MagicStick, ArrowDown, Cpu
} from '@element-plus/icons-vue';
// 假设你有一个 request 工具，如果没有，可以用 axios 代替
// import request from '@/utils/request'; 
// import { mockRule } from '@/stores/mockData'; // 移除 Mock 数据引用
import StepCard from './StepCard.vue';
// import axios from 'axios'; // 示例：使用 axios
import { srge_api } from '@/api/index';
// === 1. Props 定义完善 ===
// 必须包含调用 API 所需的所有字段
const props = defineProps<{
  formData: {
    question: string;
    formula: string; // 对应 knowledge
    clinicalText: string;
    rule: string;
  }
}>();

// === 2. API 定义 (建议移至单独文件) ===
// const api = {
//   ruleGenerate: (data: { question: string, knowledge: string, text: string }) => {
//     // 替换为你的真实请求路径
//     // return request.post('/rule/generate', data);
//     return axios.post('/api/rule/generate', data); 
//   }
// };

const loading = ref(false);
const loadingPercentage = ref(0);
const loadingPhaseText = ref('Initializing AI Model...');
const loadingDetailText = ref('Connecting to knowledge base...');
const activeRuleSections = ref<string[]>([]);
let progressTimer: number | null = null;

// === 3. 计算属性：解析 Rule ===
const ruleData = computed(() => {
  try {
    // 后端如果直接返回 Object，这里需要判断一下
    if (typeof props.formData.rule === 'object') {
        return props.formData.rule;
    }
    return props.formData.rule ? JSON.parse(props.formData.rule) : null;
  } catch (e) {
    console.error("JSON Parse Error:", e);
    return null;
  }
});

// Progress Bar Colors
const customColors = [
  { color: '#f56c6c', percentage: 20 },
  { color: '#e6a23c', percentage: 40 },
  { color: '#5cb87a', percentage: 60 },
  { color: '#1989fa', percentage: 80 },
  { color: '#6f7ad3', percentage: 100 },
];

onMounted(() => {
  // 如果已经有规则数据，直接显示
  if (props.formData.rule) {
    activeRuleSections.value = ['meta', 'input', 'steps', 'output'];
  } else {
    // 如果没有数据，自动触发一次生成 (可选)
    // regenerateRule();
    console.log("Page Loaded")
  }
});

onUnmounted(() => {
  if (progressTimer) clearInterval(progressTimer);
});

// === 4. 核心逻辑：生成规则 ===
const regenerateRule = async () => {
  // 防止重复点击
  if (loading.value) return;
  
  loading.value = true;
  loadingPercentage.value = 0;
  activeRuleSections.value = []; // 清空展示区

  // 启动模拟进度条（为了视觉效果，让用户知道在运行）
  startFakeProgress();
  console.log('props.formData')
  console.log(props.formData)
  try {
    // 构造请求参数
    const payload = {
      question: props.formData.question,
      knowledge: props.formData.formula, // 注意：你的前文将 description 赋值给了 formula
      text: props.formData.clinicalText
    };

    // --- 发起真实的 API 请求 ---
    // const res = await api.ruleGenerate(payload);
    const generatedRule = await srge_api.ruleGenerate(payload);
    console.log(generatedRule)
    // 假设后端返回结构是 { data: { rule: { ... } } }
    // 根据你的实际响应结构调整


    if (generatedRule) {
      // 成功获取：瞬间拉满进度条
      loadingPercentage.value = 100;
      loadingPhaseText.value = 'Finalizing Structure...';
      
      // 稍微延迟一下以展示 100% 状态，然后渲染数据
      setTimeout(() => {
        // 更新父组件数据 (注意：props.formData 是响应式对象，直接修改属性是 Vue 允许的)
        // 统一存储为字符串格式，或者根据你的需求存储对象
        props.formData.rule = typeof generatedRule === 'string' 
          ? generatedRule 
          : JSON.stringify(generatedRule, null, 2);

        loading.value = false;
        activeRuleSections.value = ['meta', 'input', 'steps', 'output'];
        ElMessage.success('Rule generated successfully');
      }, 600);
    } else {
      throw new Error('Empty rule data returned');
    }

  } catch (error) {
    console.error(error);
    loading.value = false;
    loadingPhaseText.value = 'Generation Failed';
    loadingDetailText.value = 'Please check network or input data';
    ElMessage.error('Failed to generate rule. Please try again.');
  } finally {
    if (progressTimer) clearInterval(progressTimer);
  }
};

// 模拟进度条动画（只走到 90%，剩下的 10% 等 API 返回）
const startFakeProgress = () => {
  if (progressTimer) clearInterval(progressTimer);
  
  loadingPercentage.value = 0;
  
  progressTimer = setInterval(() => {
    if (loadingPercentage.value < 90) {
      // 前期快，后期慢
      const increment = loadingPercentage.value < 50 ? 2 : 1;
      loadingPercentage.value += increment;
      updateLoadingText(loadingPercentage.value);
    }
  }, 100); // 每 100ms 更新一次
};

// 根据进度更新文案
const updateLoadingText = (progress: number) => {
  if (progress < 20) {
    loadingPhaseText.value = 'Parsing Clinical Question...';
    loadingDetailText.value = 'Identifying key medical entities and variables';
  } else if (progress < 50) {
    loadingPhaseText.value = 'Retrieving Atomic Tools...';
    loadingDetailText.value = 'Matching logic with available calculation units';
  } else if (progress < 80) {
    loadingPhaseText.value = 'Constructing Logic Pipeline...';
    loadingDetailText.value = 'Linking inputs, formulas, and conditions';
  } else {
    loadingPhaseText.value = 'Validating Consistency...';
    loadingDetailText.value = 'Waiting for server response...';
  }
};

const getCategoryColor = (category: string) => {
  const map: Record<string, string> = {
    ThresholdMapping: '#3b82f6', // Blue
    ConditionEvaluation: '#f59e0b', // Orange
    FormulaCalculation: '#8b5cf6', // Purple
    StatisticalAggregation: '#10b981', // Green
    Preprocessing: '#64748b' // Gray
  };
  return map[category] || '#3b82f6';
};
</script>
<style scoped lang="scss">
/* 全局容器 */
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
  min-height: 500px;
  /* Increased height for better centering */
}

/* 1. Header */
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

/* --- Optimized Loading State --- */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  animation: fadeIn 0.5s ease-out;

  /* AI Processing Visual (Pulse Rings) */
  .ai-processing-visual {
    position: relative;
    width: 100px;
    height: 100px;
    margin-bottom: 40px;
    display: flex;
    align-items: center;
    justify-content: center;

    .core-circle {
      width: 60px;
      height: 60px;
      background: linear-gradient(135deg, #2563eb, #3b82f6);
      border-radius: 50%;
      z-index: 10;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 28px;
      box-shadow: 0 0 20px rgba(37, 99, 235, 0.5);
    }

    .ring {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      border-radius: 50%;
      border: 2px solid #3b82f6;
      opacity: 0;

      &.r1 {
        width: 60px;
        height: 60px;
        animation: pulseRing 2s infinite;
        animation-delay: 0s;
      }

      &.r2 {
        width: 60px;
        height: 60px;
        animation: pulseRing 2s infinite;
        animation-delay: 0.6s;
      }

      &.r3 {
        width: 60px;
        height: 60px;
        animation: pulseRing 2s infinite;
        animation-delay: 1.2s;
      }
    }
  }

  .progress-section {
    width: 100%;
    max-width: 400px;
    text-align: center;

    .loading-title {
      font-size: 1.2rem;
      color: #1e293b;
      margin-bottom: 16px;
      font-weight: 700;
      min-height: 1.5em;
      /* Prevent layout shift */
    }

    .loading-detail {
      margin-top: 16px;
      color: #64748b;
      font-size: 0.9rem;
      min-height: 1.4em;
    }
  }
}

/* --- Optimized Empty State --- */
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: 40px;

  .empty-content {
    text-align: center;
    max-width: 450px;

    .empty-icon-wrapper {
      position: relative;
      width: 90px;
      height: 90px;
      margin: 0 auto 30px;
      display: flex;
      align-items: center;
      justify-content: center;

      .empty-icon {
        font-size: 60px;
        color: #8b5cf6;
        /* Violet */
        z-index: 2;
        animation: float 3s ease-in-out infinite;
      }

      .icon-glow {
        position: absolute;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(139, 92, 246, 0.2) 0%, rgba(255, 255, 255, 0) 70%);
        border-radius: 50%;
        animation: glow 3s ease-in-out infinite;
      }
    }

    .empty-title {
      font-size: 1.6rem;
      font-weight: 800;
      color: #1e293b;
      margin: 0 0 16px 0;
    }

    .empty-desc {
      font-size: 1rem;
      color: #64748b;
      line-height: 1.6;
      margin: 0 0 40px 0;
    }

    .generate-btn {
      padding: 18px 40px;
      /* Bigger button */
      font-size: 1.1rem;
      font-weight: 700;
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      /* Vivid Gradient */
      border: none;
      box-shadow: 0 10px 20px -5px rgba(99, 102, 241, 0.4);
      background-size: 200% auto;
      transition: all 0.3s ease;

      &:hover {
        background-position: right center;
        transform: translateY(-3px);
        box-shadow: 0 15px 25px -5px rgba(99, 102, 241, 0.5);
      }

      &:active {
        transform: translateY(-1px);
      }

      :deep(.el-icon) {
        font-size: 1.2em;
        margin-right: 8px;
      }
    }
  }
}

/* Animations */
@keyframes pulseRing {
  0% {
    transform: translate(-50%, -50%) scale(0.8);
    opacity: 0.8;
    border-width: 3px;
  }

  100% {
    transform: translate(-50%, -50%) scale(2.2);
    opacity: 0;
    border-width: 0px;
  }
}

@keyframes float {

  0%,
  100% {
    transform: translateY(0px);
  }

  50% {
    transform: translateY(-10px);
  }
}

@keyframes glow {

  0%,
  100% {
    transform: scale(1);
    opacity: 0.5;
  }

  50% {
    transform: scale(1.2);
    opacity: 0.8;
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

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

/* --- Collapse & Content Styles (Kept largely the same as requested, ensuring compatibility) --- */
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

    .ml-2 {
      margin-left: 8px;
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

.panel-body {
  padding: 24px;
  background: #fff;
  border-top: 1px solid #f1f5f9;

  &.bg-gray {
    background: #fcfcfc;
  }
}

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
  
  /* --- 新增：高度限制与滚动 --- */
  max-height: 1200px;       /* 限制最大高度 */
  overflow-y: auto;        /* 内容超出时显示垂直滚动条 */
  padding-right: 14px;     /* 增加右侧内边距，防止滚动条遮挡内容 */

  /* 美化滚动条 (Webkit内核浏览器) */
  &::-webkit-scrollbar {
    width: 6px;
  }
  &::-webkit-scrollbar-thumb {
    background-color: #cbd5e1;
    border-radius: 3px;
  }
  &::-webkit-scrollbar-track {
    background-color: #f1f5f9;
  }
}
</style>