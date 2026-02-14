<template>
  <div class="page">
    <el-card shadow="never" class="panel">
      <template #header>
        <div class="panel-header">
          <div class="panel-title">Config</div>
        </div>
      </template>

      <div class="config-container">
        <div class="config-item">
          <div class="label-chip">模型URL</div>
          <el-input v-model="modelUrl" placeholder="" />
        </div>
        <div class="config-item">
          <div class="label-chip">模型API KEY</div>
          <el-input v-model="modelApiKey" type="password" show-password placeholder="" />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineOptions({ name: 'ConfigView' })

const modelUrl = ref('')
const modelApiKey = ref('')
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

.config-container {
  display: flex;
  flex-direction: column;
  gap: 15px; /* Adjust as needed for spacing between items */
}

.config-item {
  display: grid;
  grid-template-columns: 180px 1fr; /* Label takes 180px, input takes rest */
  gap: 14px;
  align-items: center;
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
  min-height: 44px; /* Ensure consistent height with input */
}

@media (max-width: 960px) {
  .config-item {
    grid-template-columns: 1fr; /* Stack label and input on small screens */
  }
}
</style>


