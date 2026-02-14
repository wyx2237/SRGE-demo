<template>
  <div class="step-content-wrapper">
    <!-- 自定义卡片容器 -->
    <div class="modern-card">

      <!-- 1. 头部区域 -->
      <div class="card-header">
        <!-- 修改点：改为 STEP 01 -->
        <div class="step-badge">STEP 01</div>
        <h2 class="title">EMR Input</h2>
        <p class="subtitle">
          Input the unstructured EMR(Electronic Medical Record) text containing relevant patient parameters.
        </p>
      </div>

      <!-- 2. 提示区域 -->
      <div class="info-alert-box">
        <div class="alert-icon">
          <el-icon>
            <InfoFilled />
          </el-icon>
        </div>
        <div class="alert-content">
          <strong>Guidance:</strong> Ensure the text includes all necessary variables (e.g., demographics, lab results)
          required for the target medical calculation.
        </div>
      </div>

      <!-- 3. 表单区域 -->
      <el-form :model="formData" label-position="top" class="modern-form">
        <el-form-item required>
          <template #label>
            <span class="custom-label">EMR TEXT SOURCE</span>
          </template>

          <el-input v-model="formData.clinicalText" type="textarea" :rows="8" resize="none" class="custom-textarea"
            placeholder="Example: The patient is a 45-year-old male presenting with severe fatigue. Current weight is 82 kg, height 178 cm. Serum creatinine levels recorded at 1.2 mg/dL..." />
        </el-form-item>
      </el-form>

    </div>
  </div>
</template>

<script setup lang="ts">
import { InfoFilled } from '@element-plus/icons-vue'

defineProps<{
  formData: {
    clinicalText: string;
  }
}>();
</script>

<style scoped lang="scss">
/* 容器调整 */
.step-content-wrapper {
  /* 修改点：设置宽度为 100%，移除 max-width 限制 */
  width: 100%;
  margin: 0;
  font-family: 'Inter', -apple-system, sans-serif;
  animation: slideUp 0.6s cubic-bezier(0.2, 0.8, 0.2, 1);
}

/* 现代卡片风格 */
.modern-card {
  background: var(--el-bg-color);
  border-radius: 20px;
  /* 柔和阴影 */
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.05),
    0 10px 15px -3px rgba(0, 0, 0, 0.05);
  border: 1px solid var(--el-border-color-lighter);
  /* theme border */
  padding: 40px;
  box-sizing: border-box;
  width: 100%;
  /* 确保卡片撑满 wrapper */
}

/* 1. Header 样式 */
.card-header {
  margin-bottom: 32px;

  .step-badge {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 800;
    color: #2563eb;
    /* Primary Blue */
    background: #eff6ff;
    /* Blue-50 */
    padding: 6px 12px;
    border-radius: 30px;
    letter-spacing: 1px;
    margin-bottom: 16px;
  }

  .title {
    font-size: 1.75rem;
    font-weight: 800;
    color: var(--el-text-color-primary);
    margin: 0 0 8px 0;
    letter-spacing: -0.5px;
  }

  .subtitle {
    font-size: 1rem;
    color: var(--el-text-color-secondary);
    /* follow theme */
    margin: 0;
    line-height: 1.5;
  }
}

/* 2. 自定义 Alert 样式 */
.info-alert-box {
  display: flex;
  gap: 16px;
  background-color: var(--el-fill-color-lighter);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 32px;
  align-items: flex-start;

  .alert-icon {
    color: #0ea5e9;
    /* Sky-500 */
    font-size: 20px;
    padding-top: 2px;
  }

  .alert-content {
    font-size: 0.9rem;
    color: var(--el-text-color-regular);
    line-height: 1.6;

    strong {
      color: var(--el-text-color-primary);
      font-weight: 700;
    }
  }
}

/* 3. Form 样式优化 */
.modern-form {
  .custom-label {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--el-text-color-regular);
    /* theme text */
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }

  /* 深度选择器修改 el-input */
  :deep(.custom-textarea .el-textarea__inner) {
    background-color: var(--el-fill-color-light);
    /* subtle background */
    border: 1px solid var(--el-border-color);
    border-radius: 12px;
    padding: 16px;
    font-size: 1rem;
    color: var(--el-text-color-primary);
    line-height: 1.7;
    font-family: 'Inter', -apple-system, sans-serif;
    transition: all 0.2s ease;
    box-shadow: none;

    &::placeholder {
      color: var(--el-text-color-placeholder);
      font-weight: 400;
    }

    &:hover {
      border-color: var(--el-border-color-hover, var(--el-border-color));
    }

    &:focus {
      background-color: #ffffff;
      border-color: #2563eb;
      /* Primary Blue */
      box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1);
    }
  }
}

/* 动画 */
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

/* 移动端适配 */
@media (max-width: 600px) {
  .modern-card {
    padding: 24px;
  }

  .card-header .title {
    font-size: 1.5rem;
  }
}
</style>