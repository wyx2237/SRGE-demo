<template>
  <div class="page">
    <el-row :gutter="16" class="top">
      <!-- Left: Clinical Text -->
      <el-col :xs="24" :lg="12">
        <el-card shadow="never" class="panel">
          <template #header>
            <div class="panel-header">
              <div class="panel-title">Clinical Text</div>
            </div>
          </template>

          <div class="block">
            <el-upload
              accept=".txt"
              :auto-upload="false"
              :show-file-list="false"
              :on-change="handleTxtChange"
            >
              <el-button>Upload a .txt</el-button>
            </el-upload>
          </div>

          <el-input
            v-model="clinicalText"
            type="textarea"
            :rows="10"
            placeholder="Enter..."
          />
        </el-card>
      </el-col>

      <!-- Right: Rule Select -->
      <el-col :xs="24" :lg="12">
        <el-card shadow="never" class="panel">
          <template #header>
            <div class="panel-header">
              <div class="panel-title">Rule Select</div>
            </div>
          </template>

          <el-tabs v-model="activeTab" class="tabs">
            <el-tab-pane label="Tab1" name="tab1" />
            <el-tab-pane label="Tab2" name="tab2" />
          </el-tabs>

          <div v-if="activeTab === 'tab1'" class="tab-panel">
            <div class="block">
              <el-button type="primary" class="full" @click="handleRuleAction">
                Select a Rule
              </el-button>
            </div>
          </div>

          <div v-else class="tab-panel">
          <div class="block">
            <el-input v-model="problemText" placeholder="输入一段问题描述的文本" />
          </div>

          <div class="block">
            <el-button type="primary" class="full" @click="handleRuleAction">
                生成 Rule
            </el-button>
            </div>
          </div>

          <el-input
            v-model="ruleText"
            type="textarea"
            :rows="8"
            placeholder="展示 Rule"
          />

          <div class="block">
            <el-button type="primary" plain class="full" @click="handleRuleAction">
              {{ activeTab === 'tab1' ? 'Select a Rule' : '生成 Rule' }}
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Center Run -->
    <div class="run-row">
      <el-button type="primary" size="large" @click="run" :disabled="!canRun">
        Run
      </el-button>
    </div>

    <!-- Bottom: Final Answer + Context -->
    <el-card shadow="never" class="bottom">
      <div class="bottom-rows">
        <div class="bottom-row">
          <div class="label-chip">Final Answer</div>
          <el-input v-model="finalAnswer" type="textarea" :rows="3" placeholder="最终答案..." />
        </div>
        <div class="bottom-row">
          <div class="label-chip">Context</div>
          <el-input v-model="contextText" type="textarea" :rows="6" placeholder="计算过程、中间变量" />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { UploadFile, UploadFiles, UploadProps } from 'element-plus'
import { ElMessage } from 'element-plus'

defineOptions({ name: 'CalculationView' })

const activeTab = ref<'tab1' | 'tab2'>('tab1')

const clinicalText = ref('')
const problemText = ref('')
const ruleText = ref('')

const finalAnswer = ref('')
const contextText = ref('')

const canRun = computed(() => clinicalText.value.trim() && ruleText.value.trim())

const handleTxtChange: UploadProps['onChange'] = async (uploadFile: UploadFile, _uploadFiles: UploadFiles) => {
  const raw = uploadFile.raw
  if (!raw) return
  if (!raw.name.toLowerCase().endsWith('.txt')) {
    ElMessage.warning('请选择 .txt 文件')
    return
  }
  const text = await raw.text()
  clinicalText.value = text
  ElMessage.success('已加载文本')
}

const handleRuleAction = () => {
  if (activeTab.value === 'tab1') {
    // demo: 选择一段 rule
    ruleText.value = JSON.stringify(
      {
        mode: 'select',
        selected: 'rule_template_01',
        rule: {
          template: 'atomic_tool_chain',
          steps: ['extract', 'normalize', 'calculate', 'format'],
        },
      },
      null,
      2,
    )
    ElMessage.success('已选择 Rule（demo）')
    return
  }

  if (!problemText.value.trim()) {
    ElMessage.warning('请先输入问题描述')
    return
  }

    // demo: 生成一段 rule
    ruleText.value = JSON.stringify(
      {
        mode: 'generate',
        input: problemText.value.trim(),
        rule: {
          if: [{ field: 'x', op: '>', value: 0 }],
          then: [{ action: 'compute', expr: 'y = f(x)' }],
        },
      },
      null,
      2,
    )
    ElMessage.success('已生成 Rule（demo）')
}

const run = () => {
  if (!canRun.value) {
    ElMessage.warning('请先准备 Clinical Text 与 Rule')
    return
  }

  // demo: 用当前输入拼一个输出
  finalAnswer.value = '运行成功（demo）：已根据 Rule 对文本进行计算并生成答案。'
  contextText.value = [
    'Inputs:',
    `- clinicalText length: ${clinicalText.value.length}`,
    `- problem: ${problemText.value.trim() || '(empty)'}`,
    '',
    'Intermediate:',
    '- parsed_entities: {...}',
    '- variables: { x: 1, y: 2 }',
    '',
    'Rule:',
    ruleText.value.slice(0, 400) + (ruleText.value.length > 400 ? '…' : ''),
  ].join('\n')
  ElMessage.success('Run 完成（demo）')
}
</script>

<style scoped lang="scss">
.page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.panel {
  border-radius: 16px;
  border: 1px solid var(--el-border-color-lighter);
  height: 100%;

  :deep(.el-card__header) {
    padding: 12px 14px;
  }

  :deep(.el-card__body) {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 14px;
  }
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.panel-title {
  font-weight: 800;
  font-size: 15px;
}

.block {
  margin-bottom: 12px;
}

.full {
  width: 100%;
}

.tab-panel {
  display: flex;
  flex-direction: column;
}

.run-row {
  display: flex;
  justify-content: center;
  margin-top: -4px;
}

.bottom {
  border-radius: 16px;
  border: 1px solid var(--el-border-color-lighter);
  background: var(--el-fill-color-lighter);
  padding: 14px;
}

.bottom-rows {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.bottom-row {
  display: grid;
  grid-template-columns: 180px 1fr;
  gap: 14px;
  align-items: stretch; /* 关键：让左侧跟随右侧高度 */
}

.label-chip {
  border-radius: 12px;
  border: 1px solid var(--el-border-color-lighter);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: var(--el-text-color-primary);
  background: var(--el-fill-color-light);
  height: 100%;
  min-height: 44px;
}

@media (max-width: 960px) {
  .bottom-row {
    grid-template-columns: 1fr;
  }
}
</style>


