<template>
  <div class="calculation-page-wrapper">

    <!-- 1. Top Navigation: Steps Indicator -->
    <div class="steps-header">
      <el-steps :active="activeStep" finish-status="success" align-center class="custom-steps">
        <el-step title="EMR Input" description="Input Clinical Text" />
        <el-step title="Question Selection" description="Select Calcualtion Question" />
        <el-step title="Rule Generation" description="Generate Structured Rule" />
        <el-step title="Calculation Execution" description="Execute Medical Calculation " />
      </el-steps>
    </div>

    <!-- 2. Main Content Area -->
    <div class="main-content">
      <transition name="fade-slide" mode="out-in">

        <!-- Scenario A: Empty State (Step 0 & No Data) -->
        <div v-if="activeStep === 0 && !pipelineData.clinicalText" class="empty-state-container" key="empty">
          <div class="empty-content">
            <div class="icon-box">
              <el-icon>
                <Collection />
              </el-icon>
            </div>
            <h3>EMR Input</h3>
            <p>Please select a sample EMR from the library to initialize the medical calculation pipeline.</p>
            <el-button type="primary" size="large" round @click="openDialog" class="action-btn">
              Load EMR Text
            </el-button>
          </div>
        </div>

        <!-- Scenario B: Dynamic Step Component -->
        <component v-else :is="currentStepComponent" :formData="pipelineData" ref="stepRef" @open-library="openDialog"
          class="step-component-wrapper" key="component" />
      </transition>

      <!-- 3. Actions Bar -->
      <div class="footer-actions-block">
        <div class="footer-inner-panel">

          <!-- Left: Switch Text -->
          <div class="action-group left">
            <el-button v-if="activeStep === 0 && pipelineData.clinicalText" @click="openDialog" link type="primary"
              class="link-btn">
              <el-icon class="el-icon--left">
                <Switch />
              </el-icon>
              Switch Case
            </el-button>
          </div>

          <!-- Center: Navigation -->
          <div class="action-group center">
            <el-button v-if="activeStep > 0" @click="prevStep" round class="nav-btn secondary" :icon="ArrowLeft">
              Back
            </el-button>

            <el-button v-if="activeStep < 3" type="primary" @click="nextStep" round class="nav-btn primary-gradient"
              :disabled="!canProceed">
              <span>Next Step</span>
              <el-icon class="el-icon--right">
                <ArrowRight />
              </el-icon>
            </el-button>

            <el-button v-if="activeStep === 3" type="success" @click="resetPipeline" round
              class="nav-btn success-gradient">
              <el-icon class="el-icon--left">
                <RefreshRight />
              </el-icon>
              Finish & Reset
            </el-button>
          </div>

          <!-- Right: Spacer -->
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
        <el-table-column label="Action" width="100" align="right">
          <template #default>
            <el-button size="small" type="primary" plain round>Load</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Table for Step 1: Question Selection -->
      <!-- 修改点：移除了 Standard Formula 列 -->
      <el-table v-if="activeStep === 1" :data="knowledgeCases" stripe style="width: 100%" @row-click="selectCase"
        class="resource-table">
        <el-table-column prop="question" label="Medical Calculation Question" min-width="400">
          <template #default="{ row }">
            <span class="question-text">{{ row.question }}</span>
          </template>
        </el-table-column>
        <!-- 已移除 Formula 列 -->
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
import { ArrowRight, ArrowLeft, Collection, Switch, RefreshRight } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';

defineOptions({ name: 'CalculationMainView' })

// Import child components
import Step1Context from './components/Step1Context.vue';
import Step2Formula from './components/Step2Formula.vue';
import Step3Rule from './components/Step3Rule.vue';
import Step4Result from './components/Step4Result.vue';

const route = useRoute();
const activeStep = ref(0);
const showCaseDialog = ref(false);

const pipelineData = reactive({
  question: '',
  formula: '',
  clinicalText: '',
  rule: ''
});

type ClinicalCase = { id: string; clinicalText: string }
// 修改点：类型定义从 formula 改为 description
type KnowledgeCase = { question: string; description: string }

// Mock Data
const clinicalCases: ClinicalCase[] = [
  { id: "CASE-001", clinicalText: "Patient is a 58-year-old male admitted for routine checkup. His height is 178 cm (approx 70 inches) and his actual body weight is 95 kg. Recent laboratory results indicate a Serum Creatinine level of 1.2 mg/dL." },
  { id: "CASE-002", clinicalText: "The patient is a 45-year-old female presenting with fatigue. Physical examination shows a height of 165 cm and a weight of 60 kg. Blood pressure is 120/80 mmHg." },
  { id: "CASE-003", clinicalText: "A 70-year-old female with a 10-year history of hypertension. No diabetes or heart failure. She had one TIA last year. Current medications include Lisinopril." }
];

// 修改点：数据字段从 formula 改为 description
const knowledgeCases: KnowledgeCase[] = [
  { question: "Calculate Creatinine Clearance (Cockcroft-Gault)", description: "((140 - Age) * Weight) / (72 * Scr) [* 0.85 if Female]" },
  { question: "Calculate Body Mass Index (BMI)", description: "BMI = weight_kg / (height_m * height_m)" },
  { question: "Estimate Glomerular Filtration Rate (eGFR)", description: "CKD-EPI Equation (2021)" },
  { question: "CHA2DS2-VASc Score Calculation", description: "Score = CHF + Hypertension + Age>=75(2) + Diabetes + Stroke(2) + Vascular + Age65-74 + Sex category" }
];

const currentStepComponent = computed(() => {
  switch (activeStep.value) {
    case 0: return Step1Context;
    case 1: return Step2Formula;
    case 2: return Step3Rule;
    case 3: return Step4Result;
    default: return Step1Context;
  }
});

// 修改点：标题修改为 Select Medical Calculation Question
const dialogTitle = computed(() => activeStep.value === 0 ? 'Select EMR Text Source' : 'Select Medical Calculation Question');

const canProceed = computed(() => {
  if (activeStep.value === 0) return pipelineData.clinicalText.trim() !== '';
  if (activeStep.value === 1) return pipelineData.question.trim() !== '' && pipelineData.formula.trim() !== '';
  if (activeStep.value === 2) return !!pipelineData.rule;
  return true;
});

const openDialog = () => { showCaseDialog.value = true; }

const selectCase = (row: ClinicalCase | KnowledgeCase) => {
  if (activeStep.value === 0) {
    pipelineData.clinicalText = (row as ClinicalCase).clinicalText;
    ElMessage.success('EMR text loaded successfully');
  } else if (activeStep.value === 1) {
    // 修改点：将 description 赋值给 formula，保持后端逻辑不变
    pipelineData.question = (row as KnowledgeCase).question;
    pipelineData.formula = (row as KnowledgeCase).description;
    ElMessage.success('Question selected');
  }
  showCaseDialog.value = false;
};

const nextStep = () => { if (activeStep.value < 3) activeStep.value++; };
const prevStep = () => { if (activeStep.value > 0) activeStep.value--; };

const resetPipeline = () => {
  ElMessage.success('Pipeline reset successfully');
  activeStep.value = 0;
  pipelineData.question = '';
  pipelineData.formula = '';
  pipelineData.clinicalText = '';
  pipelineData.rule = '';
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
  background-color: var(--el-bg-color-page);
  font-family: 'Inter', -apple-system, sans-serif;
}

/* --- 2. Top Steps Header --- */
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

/* --- 3. Main Content Area --- */
.main-content {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px 40px 20px;
  box-sizing: border-box;
}

/* Empty State */
.empty-state-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  background: var(--el-bg-color);
  border-radius: 20px;
  border: 1px dashed var(--el-border-color);

  .empty-content {
    text-align: center;
    max-width: 400px;

    .icon-box {
      width: 80px;
      height: 80px;
      background: var(--el-fill-color-lighter);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 40px;
      color: var(--el-text-color-placeholder);
      margin: 0 auto 24px;
    }

    h3 {
      margin: 0 0 12px 0;
      color: var(--el-text-color-primary);
      font-size: 1.25rem;
    }

    p {
      color: var(--el-text-color-secondary);
      margin-bottom: 32px;
      line-height: 1.6;
    }

    .action-btn {
      padding: 20px 32px;
      font-weight: 600;
      box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
    }
  }
}

/* Transition */
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

/* --- 4. Footer Actions --- */
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

/* --- Buttons Styling --- */
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
  }
}

/* Table in Dialog */
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
    }
  }

  .question-text {
    font-weight: 600;
    color: var(--el-text-color-primary);
    font-size: 1rem;
  }
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