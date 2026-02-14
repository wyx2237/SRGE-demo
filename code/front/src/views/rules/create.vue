<template>
  <el-row :gutter="16">
    <el-col :xs="24" :lg="14">
      <el-card shadow="never">
        <template #header>
          <div class="header">
            <div class="title">新建规则</div>
            <el-tag type="info">Demo</el-tag>
          </div>
        </template>

        <el-form :model="form" label-width="92px" class="form">
          <el-form-item label="规则名称">
            <el-input v-model="form.name" placeholder="例如：订单金额>1000需要二级审批" />
          </el-form-item>

          <el-form-item label="规则类型">
            <el-select v-model="form.type" placeholder="请选择">
              <el-option label="审批" value="审批" />
              <el-option label="安全" value="安全" />
              <el-option label="营销" value="营销" />
            </el-select>
          </el-form-item>

          <el-form-item label="输入文本">
            <el-input
              v-model="form.text"
              type="textarea"
              :rows="8"
              placeholder="粘贴自然语言描述，系统将尝试生成可执行规则结构…"
            />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="generate">生成</el-button>
            <el-button @click="reset">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-col>

    <el-col :xs="24" :lg="10">
      <el-card shadow="never">
        <template #header>
          <div class="header">
            <div class="title">生成结果（预览）</div>
            <el-button type="success" :disabled="!result" @click="publish">发布</el-button>
          </div>
        </template>

        <el-empty v-if="!result" description="点击“生成”后在这里查看结构化规则" />

        <div v-else class="result">
          <pre>{{ result }}</pre>
        </div>
      </el-card>
    </el-col>
  </el-row>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'

defineOptions({ name: 'RulesCreateView' })

const form = reactive({
  name: '',
  type: '',
  text: '',
})

const result = ref('')

const generate = () => {
  if (!form.text.trim()) {
    ElMessage.warning('请先输入文本')
    return
  }
  result.value = JSON.stringify(
    {
      name: form.name || '未命名规则',
      type: form.type || '未分类',
      sourceText: form.text.trim(),
      rule: {
        if: [{ field: 'amount', op: '>', value: 1000 }],
        then: [{ action: 'require_approval', level: 2 }],
      },
    },
    null,
    2,
  )
  ElMessage.success('已生成（demo）')
}

const reset = () => {
  form.name = ''
  form.type = ''
  form.text = ''
  result.value = ''
}

const publish = () => {
  ElMessage.success('已发布（demo）')
}
</script>

<style scoped lang="scss">
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}
.title {
  font-weight: 800;
}
.form {
  padding-top: 8px;
}
.result {
  pre {
    margin: 0;
    padding: 12px;
    border-radius: 12px;
    background: var(--el-fill-color-lighter);
    border: 1px solid var(--el-border-color-lighter);
    color: var(--el-text-color-primary);
    font-size: 12px;
    line-height: 1.55;
    overflow: auto;
    max-height: 520px;
  }
}
</style>


