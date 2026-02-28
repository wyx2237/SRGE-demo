<template>
  <div class="calculation-page-wrapper">

    <!-- 1. Top Navigation: Steps Indicator -->
    <div class="steps-header">
      <el-steps :active="activeStep" finish-status="success" align-center class="custom-steps">
        <el-step title="EMR Input" description="Input Clinical Text" />
        <el-step title="Question Confirmation" description="Confirm Calcualtion Question" />
        <el-step title="Rule Generation" description="Generate Structured Rule" />
        <el-step title="Calculation Execution" description="Execute Medical Calculation " />
      </el-steps>
    </div>

    <!-- 2. Main Content Area -->
    <div class="main-content">
      <transition name="fade-slide" mode="out-in">
        <component 
          :is="currentStepComponent" 
          :formData="pipelineData" 
          ref="stepRef" 
          @open-library="openDialog"
          @confirmed="handleStep2Confirmation"
          @execution-complete="handleStep4Execution"
          class="step-component-wrapper" 
          key="component" 
        />
      </transition>

      <!-- 3. Actions Bar -->
      <div class="footer-actions-block">
        <div class="footer-inner-panel">
          <!-- Left: Switch Text -->
          <div class="action-group left">
            <!-- <el-button v-if="activeStep === 0 && pipelineData.clinicalText" @click="openDialog" link type="primary"
              class="link-btn">
              <el-icon class="el-icon--left">
                <Switch />
              </el-icon>
              Switch Case
            </el-button> -->
          </div>

          <!-- Center: Navigation -->
          <div class="action-group center">
            <el-button v-if="activeStep === 1 || activeStep === 3" @click="prevStep" round class="nav-btn secondary" :icon="ArrowLeft">
              Back
            </el-button>

            <el-button v-if="activeStep < 3" type="primary" @click="nextStep" round class="nav-btn primary-gradient"
              :disabled="!canProceed">
              <span>Next Step</span>
              <el-icon class="el-icon--right">
                <ArrowRight />
              </el-icon>
            </el-button>

            <el-button v-if="activeStep === 3" type="success"
              @click="resetPipeline"
              :disabled="!step4Executed"
              round
              class="nav-btn success-gradient">
              <el-icon class="el-icon--left">
                <RefreshRight />
              </el-icon>
              Finish & Reset
            </el-button>
          </div>
          <div class="action-group right"></div>
        </div>
      </div>
    </div>

    <!-- Dialog -->
    <el-dialog v-model="showCaseDialog" :title="dialogTitle" width="850px" destroy-on-close align-center
      class="custom-dialog">

      <!-- Table for Step 0: EMR Text Selection -->
      <el-table v-if="activeStep === 0" :data="clinicalCases" stripe style="width: 100%" @row-click="selectCase"
        class="resource-table">
        <el-table-column label="EMR Texts" min-width="400">
          <template #default="{ row }">
            <div class="text-preview">
              <el-tag size="small" effect="plain" class="id-tag">{{ row.id }}</el-tag>
              <span class="content">{{ row.clinicalText }}</span>
            </div>
          </template>
        </el-table-column>
        
        <!-- 【修改点 1：调整宽度并添加下载按钮】 -->
        <el-table-column label="Action" width="160" align="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <!-- 下载按钮：使用 @click.stop 阻止触发 selectCase -->
              <el-button 
                type="info" 
                link 
                :icon="Download" 
                @click.stop="downloadCaseText(row)"
                title="Download Text"
              >
                Save
              </el-button>
              <el-button size="small" type="primary" plain round>Load</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- Table for Step 1: Question Selection -->
      <el-table v-if="activeStep === 1" :data="knowledgeCases" stripe style="width: 100%" @row-click="selectCase"
        class="resource-table">
        <el-table-column prop="question" label="Medical Calculation Question" min-width="400">
          <template #default="{ row }">
            <span class="question-text">{{ row.question }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Action" width="100" align="right">
          <template #default>
            <el-button size="small" type="primary" plain round>Select</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted } from 'vue';
import { useRoute } from 'vue-router';
// 【修改点 2：引入 Download 图标】
import { ArrowRight, ArrowLeft, Switch, RefreshRight, Download } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';

// --- 1. 导入数据源 ---
import { CaseMap } from '@/stores/test/caseMap';

defineOptions({ name: 'CalculationMainView' })

import Step1Context from './components/Step1Context.vue';
import Step2Formula from './components/Step2Formula.vue';
import Step3Rule from './components/Step3Rule.vue';
import Step4Result from './components/Step4Result.vue';

const route = useRoute();
const activeStep = ref(0);
const showCaseDialog = ref(false);

const selectedCaseId = ref<string>('');

const pipelineData = reactive({
  question: '',
  formula: '',
  clinicalText: '',
  rule: ''
});

type ClinicalCase = { id: string; clinicalText: string }
type KnowledgeCase = { question: string; description: string }

// --- 3. 生成 Clinical Cases (Step 0 列表) ---
const clinicalCases = computed<ClinicalCase[]>(() => {
  return Object.entries(CaseMap).map(([key, value]: [string, any]) => ({
    id: key,
    clinicalText: value.text
  }));
});

// --- 4. 生成 Knowledge Cases (Step 1 列表) ---
const knowledgeCases = computed<KnowledgeCase[]>(() => {
  if (!selectedCaseId.value || !CaseMap[selectedCaseId.value as keyof typeof CaseMap]) {
    return [];
  }
  const questions = CaseMap[selectedCaseId.value as keyof typeof CaseMap].questions;
  return questions.map((item: any) => ({
    question: item.question,
    description: item.formula 
  }));
});

const currentStepComponent = computed(() => {
  switch (activeStep.value) {
    case 0: return Step1Context;
    case 1: return Step2Formula;
    case 2: return Step3Rule;
    case 3: return Step4Result;
    default: return Step1Context;
  }
});

const dialogTitle = computed(() => activeStep.value === 0 ? 'Select EMR Text Source' : 'Select Medical Calculation Question');

// 新增状态：Step 2 是否已确认
const step2Confirmed = ref(false);

// 处理 Step 2 的确认事件
const handleStep2Confirmation = (status: boolean) => {
  step2Confirmed.value = status;
};

// 新增状态：Step 4 是否已执行
const step4Executed = ref(false);

// 处理 Step 4 的完成事件
const handleStep4Execution = (status: boolean) => {
  step4Executed.value = status;
};

const canProceed = computed(() => {
  if (activeStep.value === 0) return pipelineData.clinicalText.trim() !== '';
  if (activeStep.value === 1) {
    // Step 1 (Question Selection) 的通过条件：
    // 1. 问题和公式不为空 (原有逻辑)
    // 2. AND 必须已经点击了 Confirm 按钮 (新增逻辑)
    const hasData = pipelineData.question.trim() !== '' && pipelineData.formula.trim() !== '';
    return hasData && step2Confirmed.value;
  }
  if (activeStep.value === 2) return !!pipelineData.rule;
  return true;
});

const openDialog = () => { showCaseDialog.value = true; }

// 【修改点 3：添加下载功能函数】
const downloadCaseText = (row: ClinicalCase) => {
  try {
    // 1. 创建 Blob 对象
    const blob = new Blob([row.clinicalText], { type: 'text/plain;charset=utf-8' });
    
    // 2. 创建临时下载链接
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    
    // 3. 设置文件名 (例如: Case_101.txt)
    link.download = `Case_${row.id}.txt`;
    
    // 4. 触发下载并清理
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    ElMessage.success(`Downloaded ${row.id} successfully`);
  } catch (error) {
    ElMessage.error('Failed to download file');
    console.error(error);
  }
};

const selectCase = (row: ClinicalCase | KnowledgeCase) => {
  if (activeStep.value === 0) {
    const emrRow = row as ClinicalCase;
    selectedCaseId.value = emrRow.id; 
    pipelineData.clinicalText = emrRow.clinicalText;
    pipelineData.question = '';
    pipelineData.formula = '';
    ElMessage.success(`EMR text loaded (${emrRow.id})`);
  } else if (activeStep.value === 1) {
    const knowledgeRow = row as KnowledgeCase;
    pipelineData.question = knowledgeRow.question;
    pipelineData.formula = knowledgeRow.description;
    ElMessage.success('Question selected');
  }
  showCaseDialog.value = false;
};

const nextStep = () => { if (activeStep.value < 3) activeStep.value++; };
const prevStep = () => { if (activeStep.value > 0) activeStep.value--; };

const resetPipeline = () => {
  ElMessage.success('Pipeline reset successfully');
  activeStep.value = 0;
  selectedCaseId.value = '';
  pipelineData.question = '';
  pipelineData.formula = '';
  pipelineData.clinicalText = '';
  pipelineData.rule = '';
  // 新增：重置 Step 2 确认状态
  step2Confirmed.value = false;
  // 新增：重置 Step 4 执行状态
  step4Executed.value = false;
};

onMounted(() => {
  if (route.query.question) {
    pipelineData.question = route.query.question as string;
    pipelineData.formula = route.query.formula as string || '';
    if (route.query.clinicalText) pipelineData.clinicalText = route.query.clinicalText as string;
  }
});
</script>

<style scoped lang="scss">
/* --- 1. Global Wrapper --- */
.calculation-page-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-height: 100vh;
  background-color: rgb(227, 239, 255);
  font-family: 'Inter', -apple-system, sans-serif;
}

/* ... 保持原有样式不变 ... */
/* 为了节省篇幅，省略未修改的样式部分，实际代码中请保留原有的样式 */
/* ... */

.steps-header {
  padding: 30px 40px;
  background: var(--el-bg-color);
  border-bottom: 1px solid var(--el-border-color-lighter);
  margin-bottom: 30px;

  .custom-steps {
    max-width: 900px;
    margin: 0 auto;

    :deep(.el-step__title) {
      font-weight: 700;
      font-size: 0.95rem;
      color: var(--el-text-color-secondary);

      &.is-process {
        color: #2563eb;
      }

      &.is-finish {
        color: #059669;
      }
    }

    :deep(.el-step__head.is-process) {
      .el-step__line {
        background-color: #bfdbfe;
      }

      .el-step__icon {
        border-color: #2563eb;
        color: #2563eb;
        background: #eff6ff;
      }
    }

    :deep(.el-step__description) {
      display: none;
    }
  }
}

.main-content {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px 40px 20px;
  box-sizing: border-box;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.footer-actions-block {
  width: 100%;
  margin-top: 24px;
  display: flex;
  justify-content: center;
}

.footer-inner-panel {
  width: 100%;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 16px;
  padding: 16px 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: space-between;

  .action-group {
    flex: 1;
    display: flex;
    align-items: center;

    &.center {
      justify-content: center;
      gap: 16px;
    }

    &.right {
      justify-content: flex-end;
    }

    &.left {
      justify-content: flex-start;
    }
  }
}

.link-btn {
  font-weight: 600;
  font-size: 0.9rem;

  &:hover {
    text-decoration: underline;
  }
}

.nav-btn {
  height: 44px;
  padding: 0 28px;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;

  :deep(span) {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  &.secondary {
    background: #f1f5f9;
    color: #475569;

    &:hover {
      background: #e2e8f0;
      color: #1e293b;
    }
  }

  &.primary-gradient {
    background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
    box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3), 0 2px 4px -1px rgba(37, 99, 235, 0.1);
    color: white;

    &:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
      background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
    }

    &:disabled {
      background: #94a3b8;
      box-shadow: none;
      cursor: not-allowed;
    }
  }

  &.success-gradient {
    background: linear-gradient(135deg, #059669 0%, #10b981 100%);
    box-shadow: 0 4px 6px -1px rgba(5, 150, 105, 0.3);
    color: white;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 15px -3px rgba(5, 150, 105, 0.4);
    }

    &:disabled {
      background: #94a3b8;
      box-shadow: none;
      cursor: not-allowed;
    }
  }
}

.resource-table {
  .text-preview {
    display: flex;
    flex-direction: column;
    gap: 6px;

    .id-tag {
      width: fit-content;
      background: #f1f5f9;
      border: none;
      color: #64748b;
    }

    .content {
      font-family: 'Georgia', serif;
      font-size: 0.9rem;
      color: #334155;
      line-height: 1.5;
      
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 3;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }

  .question-text {
    font-weight: 600;
    color: var(--el-text-color-primary);
    font-size: 1rem;
  }
}

/* 【修改点 4：新增样式，用于按钮组布局】 */
.action-buttons {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
}

@media (max-width: 768px) {
  .steps-header {
    padding: 20px;
  }

  .custom-steps :deep(.el-step__description) {
    display: none;
  }

  .footer-inner-panel {
    flex-direction: column;
    gap: 10px;
    padding: 16px;
    height: auto;
  }

  .action-group {
    width: 100%;
    justify-content: center !important;
  }
}
</style>