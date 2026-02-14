<template>
  <div class="step-content-wrapper">
    <div class="modern-card">
      
      <!-- 1. Header Area -->
      <div class="card-header-flex">
        <div class="header-left">
          <div class="step-badge">STEP 04</div>
          <h2 class="title">Calculation Execution</h2>
          <p class="subtitle">
            Parse clinical text, extract variables, and execute the rule logic.
          </p>
        </div>
        
        <div class="header-right">
          <div v-if="hasExecuted" class="reset-btn-wrapper">
            <el-tooltip 
              raw-content
              content="<div>Reset Execution: Clears the current execution results<br/>and returns to the initial state. You can re-execute<br/>the calculation or modify previous steps.</div>"
              placement="bottom"
              effect="dark"
            >
              <el-icon class="help-icon-before-reset"><QuestionFilled /></el-icon>
            </el-tooltip>
            <el-button 
              link 
              type="primary" 
              class="reset-btn"
              @click="resetState" 
            >
              <el-icon class="el-icon--left"><RefreshLeft /></el-icon>
              Reset Execution
            </el-button>
          </div>
        </div>
      </div>

      <!-- 2. Initial State (Ready to Execute) -->
      <div v-if="!hasExecuted" class="initial-state-container">
        <div class="state-icon-wrapper">
          <div class="pulse-ring"></div>
          <el-icon><Cpu /></el-icon>
        </div>
        <h3>Ready for Medical Calculation</h3>
        <p>The engine is ready to parse the clinical text and execute the structured rule logic defined in previous steps.</p>
        
        <div class="execute-btn-wrapper">
          <el-tooltip 
            raw-content
            content="<div>Execute Medical Calculation Engine: Click this button<br/>to start executing the structured rule. The system will parse<br/>clinical text, extract variables, execute calculation logic<br/>step by step, and generate the final result.</div>"
            placement="top"
            effect="dark"
          >
            <el-icon class="help-icon-before-execute"><QuestionFilled /></el-icon>
          </el-tooltip>
          <el-button 
            type="primary" 
            size="large" 
            :loading="extracting" 
            @click="executeEngine" 
            round 
            class="execute-btn"
          >
            <el-icon class="el-icon--left"><VideoPlay /></el-icon>
            Calculation Execution
          </el-button>
        </div>
      </div>

      <!-- 3. Execution Result View -->
      <div v-else class="execution-view">
        
        <!-- A. Source Text Highlighting (New Feature) -->
        <div class="section-container source-text-section">
          <div class="section-header clickable" @click="isTextExpanded = !isTextExpanded">
            <div class="title-group">
              <el-icon><Document /></el-icon>
              <span>Source Text Analysis</span>
              <el-tag size="small" effect="plain" round class="status-tag">Parsed</el-tag>
              <el-tooltip 
                raw-content
                content="<div>Source Text Analysis: Displays the original clinical text<br/>with highlighted extracted entities (variable values).<br/>You can click to expand/collapse to view the complete clinical text.<br/>Highlighted portions indicate successfully extracted parameters.</div>"
                placement="top"
                effect="dark"
              >
                <el-icon class="help-icon-in-section" @click.stop><QuestionFilled /></el-icon>
              </el-tooltip>
            </div>
            <div class="toggle-icon">
              <span class="toggle-label">{{ isTextExpanded ? 'Collapse' : 'Expand' }}</span>
              <el-icon :class="{ 'is-rotated': isTextExpanded }"><ArrowDown /></el-icon>
            </div>
          </div>
          
          <el-collapse-transition>
            <div v-show="isTextExpanded" class="source-body">
              <div class="text-content" v-html="highlightedHtml"></div>
              <div class="legend-bar">
                <div class="legend-item">
                  <span class="dot highlight"></span>
                  <span>Extracted Entity</span>
                </div>
              </div>
            </div>
          </el-collapse-transition>
        </div>

        <div class="split-layout">
          
          <!-- B. Parameters Table -->
          <div class="left-panel">
            <div class="section-title">
              <el-icon><Files /></el-icon> Parameter Extraction
              <el-tooltip 
                raw-content
                content="<div>Parameter Extraction: Displays all variables and their values<br/>extracted from clinical text. Includes variable names, original<br/>text fragments, and parsed numerical values. These parameters<br/>will be used in subsequent calculation steps.</div>"
                placement="top"
                effect="dark"
              >
                <el-icon class="help-icon"><QuestionFilled /></el-icon>
              </el-tooltip>
            </div>
            <div class="table-card">
              <el-table :data="extractedParams" :border="false" class="modern-table">
                <el-table-column prop="name" label="Variable">
                  <template #default="{ row }">
                    <span class="code-text primary">{{ row.name }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="rawValue" label="Source Fragment">
                  <template #default="{ row }">
                    <span class="source-fragment">"{{ row.rawValue }}"</span>
                  </template>
                </el-table-column>
                <el-table-column prop="value" label="Value" width="100">
                  <template #default="{ row }">
                    <span class="value-text">{{ row.value }}</span>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </div>

          <!-- C. Medical Calculation Trace -->
          <div class="right-panel">
            <div class="section-title">
              <el-icon><Operation /></el-icon> Execution Trace
              <el-tooltip 
                raw-content
                content="<div>Execution Trace: Displays each step of rule execution,<br/>including step name, category, calculation logic, and output results.<br/>You can view the complete calculation process and understand<br/>how each step transforms inputs into outputs.</div>"
                placement="top"
                effect="dark"
              >
                <el-icon class="help-icon"><QuestionFilled /></el-icon>
              </el-tooltip>
            </div>
            <div class="trace-container">
              <el-timeline>
                <el-timeline-item
                  v-for="(step, index) in executionSteps"
                  :key="index"
                  :type="step.type"
                  :color="step.color"
                  :hollow="true"
                  hide-timestamp
                  class="custom-timeline-item"
                >
                  <div class="trace-card">
                    <div class="trace-header">
                      <span class="step-name">{{ step.stepName }}</span>
                      <el-tag size="small" :type="step.tagType" effect="light" class="step-tag">{{ step.category }}</el-tag>
                    </div>
                    <div class="trace-body">
                      <div class="logic-row">
                        <span class="label">Logic:</span>
                        <code class="logic-code">{{ step.logic }}</code>
                      </div>
                      <div class="result-row">
                        <span class="label">Output:</span>
                        <span class="result-value">{{ step.result }}</span>
                        <span class="result-var">({{ step.outputName }})</span>
                      </div>
                    </div>
                  </div>
                </el-timeline-item>
              </el-timeline>
            </div>
          </div>
          
        </div>

        <!-- D. Final Result Panel -->
        <div class="final-result-wrapper">
          <div class="result-card">
            <div class="result-label-wrapper">
              <div class="result-label">FINAL MEDICAL CALCULATION RESULT</div>
              <el-tooltip 
                raw-content
                content="<div>Final Medical Calculation Result: Displays the final output value<br/>after the entire rule execution. This is the final medical metric<br/>calculated based on structured rules and extracted parameters,<br/>which can be used for clinical decision-making.</div>"
                placement="top"
                effect="dark"
              >
                <el-icon class="help-icon-in-result"><QuestionFilled /></el-icon>
              </el-tooltip>
            </div>
            <div class="result-value-group">
              <span class="value">{{ finalResult }}</span>
              <span class="unit">mL/min</span>
            </div>
            <div class="result-info">
              <el-tag effect="dark" type="success" round>Creatinine Clearance</el-tag>
              <span class="divider">|</span>
              <span class="rule-name">Cockcroft-Gault Formula</span>
            </div>
          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { Files, Cpu, Operation, VideoPlay, RefreshLeft, Document, ArrowDown, QuestionFilled } from '@element-plus/icons-vue';
import { mockClinicalText } from '@/stores/mockData';

// --- 类型定义 ---
interface ParamItem {
  name: string;
  rawValue: string;
  value: string | number;
}

interface StepItem {
  stepId: string;
  stepName: string;
  category: string;
  logic: string;
  outputName: string;
  result: string;
  type: 'primary' | 'success' | 'warning' | 'info';
  color?: string;
  tagType: '' | 'success' | 'warning' | 'info' | 'danger';
}

// --- 状态 ---
const hasExecuted = ref(false);
const extracting = ref(false);
const finalResult = ref<string | null>(null);
const extractedParams = ref<ParamItem[]>([]);
const executionSteps = ref<StepItem[]>([]);
const isTextExpanded = ref(false);

// --- 计算属性：高亮 HTML ---
const highlightedHtml = computed(() => {
  if (!mockClinicalText) return '';
  let html = mockClinicalText;
  
  extractedParams.value.forEach(param => {
    if (param.rawValue) {
      // 简单替换，实际项目建议使用更严谨的 NLP 索引切分
      const regex = new RegExp(`(${escapeRegExp(param.rawValue)})`, 'gi');
      html = html.replace(regex, `<span class="highlight-mark" title="${param.name}: ${param.value}">$1</span>`);
    }
  });
  return html.replace(/\n/g, '<br>');
});

function escapeRegExp(string: string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// --- Actions ---
const resetState = () => {
  hasExecuted.value = false;
  finalResult.value = null;
  extractedParams.value = [];
  executionSteps.value = [];
  isTextExpanded.value = false;
};

const executeEngine = () => {
  extracting.value = true;
  setTimeout(() => {
    hasExecuted.value = true;
    isTextExpanded.value = true; // 自动展开原文
    
    // Mock Data
    extractedParams.value = [
      { name: 'age', rawValue: '58-year-old', value: 58 },
      { name: 'gender', rawValue: 'male', value: 'male' },
      { name: 'height_m', rawValue: '178 cm', value: 1.78 },
      { name: 'actual_weight', rawValue: '95 kg', value: 95.0 },
      { name: 'serum_creatinine', rawValue: '1.2 mg/dL', value: 1.2 }
    ];

    executionSteps.value = [
      { 
        stepId: '1', stepName: 'Calc BMI', category: 'Formula',
        logic: 'weight / height² = 95 / 1.78²', outputName: 'bmi', result: '29.98', 
        type: 'primary', tagType: ''
      },
      { 
        stepId: '2', stepName: 'Weight Cat', category: 'Logic',
        logic: 'BMI 29.98 ≥ 25 (Overweight)', outputName: 'category', result: '"Overweight"', 
        type: 'warning', color: '#f59e0b', tagType: 'warning'
      },
      { 
        stepId: '3', stepName: 'Calc IBW', category: 'Formula',
        logic: '50 + 2.3 * (height_in - 60)', outputName: 'ibw', result: '73.18', 
        type: 'info', tagType: 'info'
      },
      { 
        stepId: '4', stepName: 'Calc ABW', category: 'Formula',
        logic: 'IBW + 0.4 * (Actual - IBW)', outputName: 'abw', result: '81.91', 
        type: 'info', tagType: 'info'
      },
      { 
        stepId: '5', stepName: 'Sel Weight', category: 'Condition',
        logic: 'Overweight → Use ABW', outputName: 'selected_weight', result: '81.91', 
        type: 'success', color: '#10b981', tagType: 'success'
      },
      { 
        stepId: '6', stepName: 'Calc CrCl', category: 'Final',
        logic: 'Cockcroft-Gault Formula', outputName: 'crcl', result: '77.74', 
        type: 'primary', tagType: ''
      }
    ];
    
    finalResult.value = `77.74`;
    extracting.value = false;
  }, 1500);
};
</script>

<style scoped lang="scss">
/* 全局容器 (继承之前的风格) */
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
  min-height: 500px;
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
    .title { font-size: 1.75rem; font-weight: 800; color: #0f172a; margin: 0 0 8px 0; }
    .subtitle { font-size: 1rem; color: #64748b; margin: 0; }
  }
  
  .reset-btn-wrapper {
    display: flex;
    align-items: center;
    gap: 8px;
    .help-icon-before-reset {
      color: var(--el-text-color-placeholder);
      font-size: 0.95rem;
      cursor: help;
      transition: color 0.2s;
      &:hover {
        color: #2563eb;
      }
    }
  }
  .reset-btn { font-weight: 600; color: var(--el-text-color-secondary); &:hover { color: #2563eb; } }
}

/* 2. Initial State */
.initial-state-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  
  .state-icon-wrapper {
    position: relative;
    width: 80px;
    height: 80px;
    background: var(--el-color-primary-light-9);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    color: var(--el-color-primary);
    margin-bottom: 24px;
    
    .pulse-ring {
      position: absolute;
      width: 100%;
      height: 100%;
      border-radius: 50%;
      border: 2px solid #3b82f6;
      animation: pulse 2s infinite;
      opacity: 0;
    }
  }
  
  h3 { font-size: 1.5rem; color: var(--el-text-color-primary); margin: 0 0 12px 0; }
  p { color: var(--el-text-color-secondary); margin-bottom: 40px; max-width: 500px; text-align: center; line-height: 1.6; }
  
  .execute-btn-wrapper {
    display: flex;
    align-items: center;
    gap: 12px;
    .help-icon-before-execute {
      color: var(--el-text-color-placeholder);
      font-size: 1rem;
      cursor: help;
      transition: color 0.2s;
      &:hover {
        color: #2563eb;
      }
    }
  }
  
  .execute-btn {
    padding: 24px 48px;
    font-size: 1.1rem;
    font-weight: 700;
    box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
    transition: transform 0.2s;
    &:hover { transform: translateY(-2px); }
  }
}

/* 3. Execution View - Source Text */
.source-text-section {
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 32px;
  
  .section-header {
    background: #f8fafc;
    padding: 12px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #e2e8f0;
    transition: background 0.2s;
    
    &.clickable:hover { background: #f1f5f9; }
    
    .title-group {
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 600;
      color: #334155;
      .status-tag { border-color: #cbd5e1; color: #64748b; }
      .help-icon-in-section {
        color: #94a3b8;
        font-size: 0.9rem;
        cursor: help;
        transition: color 0.2s;
        &:hover {
          color: #2563eb;
        }
      }
    }
    
    .toggle-icon {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.85rem;
      color: #94a3b8;
      .is-rotated { transform: rotate(180deg); }
    }
  }
  
  .source-body {
    background: #fff;
    .text-content {
      padding: 24px;
      font-family: 'Georgia', serif;
      font-size: 1.05rem;
      line-height: 1.8;
      color: #1e293b;
      
      :deep(.highlight-mark) {
        background-color: #fef3c7; /* Amber-100 */
        border-bottom: 2px solid #f59e0b; /* Amber-500 */
        color: #92400e;
        padding: 0 4px;
        border-radius: 2px;
        font-weight: 600;
        cursor: help;
        transition: background-color 0.2s;
        &:hover { background-color: #fde68a; }
      }
    }
    .legend-bar {
      border-top: 1px dashed #e2e8f0;
      padding: 8px 24px;
      background: #fafafa;
      .legend-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.75rem;
        color: #64748b;
        .dot { width: 8px; height: 8px; border-radius: 2px; }
        .dot.highlight { background: #fef3c7; border: 1px solid #f59e0b; }
      }
    }
  }
}

/* 4. Split Layout (Params + Trace) */
.split-layout {
  display: flex;
  gap: 32px;
  margin-bottom: 40px;
  
  .left-panel { flex: 4; }
  .right-panel { flex: 5; }
  
  .section-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.95rem;
    font-weight: 700;
    color: #475569;
    margin-bottom: 16px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    .help-icon {
      color: #94a3b8;
      font-size: 0.85rem;
      cursor: help;
      transition: color 0.2s;
      margin-left: 4px;
      &:hover {
        color: #3b82f6;
      }
    }
  }
}

/* Table Card */
.table-card {
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
}

.modern-table {
  :deep(th.el-table__cell) { background: #f8fafc; font-size: 0.8rem; text-transform: uppercase; }
  .code-text { font-family: 'Consolas', monospace; font-weight: 600; font-size: 0.9rem; }
  .code-text.primary { color: #2563eb; }
  .source-fragment { font-style: italic; color: #64748b; font-size: 0.9rem; }
  .value-text { font-weight: 700; color: #1e293b; }
}

/* Trace Timeline */
.trace-container {
  max-height: 400px;
  overflow-y: auto;
  padding-right: 10px;
  
  .trace-card {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 4px;
    
    .trace-header {
      background: #f8fafc;
      padding: 8px 12px;
      border-bottom: 1px solid #f1f5f9;
      display: flex;
      justify-content: space-between;
      align-items: center;
      .step-name { font-weight: 700; font-size: 0.85rem; color: #334155; }
      .step-tag { font-weight: 600; border: none; }
    }
    
    .trace-body {
      padding: 10px 12px;
      font-size: 0.85rem;
      
      .logic-row { margin-bottom: 6px; display: flex; gap: 8px; color: #64748b; }
      .logic-code { font-family: 'Consolas', monospace; color: #475569; background: #f1f5f9; padding: 0 4px; border-radius: 4px; }
      
      .result-row {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #059669;
        font-weight: 600;
        background: #ecfdf5;
        padding: 6px 8px;
        border-radius: 4px;
        
        .result-value { font-weight: 800; font-size: 1rem; }
        .result-var { font-weight: 400; font-size: 0.8rem; opacity: 0.8; }
      }
    }
  }
}

/* 5. Final Result Panel */
.final-result-wrapper {
  margin-top: 20px;
  
  .result-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 16px;
    padding: 32px;
    text-align: center;
    color: #fff;
    box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.1), 0 10px 10px -5px rgba(15, 23, 42, 0.04);
    
    .result-label-wrapper {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      margin-bottom: 16px;
      .result-label {
        font-size: 0.85rem;
        font-weight: 700;
        color: #94a3b8;
        letter-spacing: 2px;
      }
      .help-icon-in-result {
        color: #94a3b8;
        font-size: 0.9rem;
        cursor: help;
        transition: color 0.2s;
        &:hover {
          color: #38bdf8;
        }
      }
    }
    
    .result-value-group {
      display: flex;
      align-items: baseline;
      justify-content: center;
      gap: 12px;
      margin-bottom: 24px;
      
      .value { font-size: 4rem; font-weight: 800; line-height: 1; color: #38bdf8; text-shadow: 0 0 20px rgba(56, 189, 248, 0.3); }
      .unit { font-size: 1.5rem; color: #94a3b8; font-weight: 600; }
    }
    
    .result-info {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 16px;
      font-size: 0.9rem;
      color: #cbd5e1;
      .divider { color: #475569; }
    }
  }
}

@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
@keyframes pulse { 0% { transform: scale(0.95); opacity: 0.5; } 100% { transform: scale(1.5); opacity: 0; } }

/* Mobile Adaption */
@media (max-width: 900px) {
  .split-layout { flex-direction: column; }
}
</style>