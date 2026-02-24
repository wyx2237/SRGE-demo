<template>
  <div class="step-content-wrapper">
    <div class="modern-card">

      <!-- 1. 头部区域 (Flex布局：左侧文字，右侧按钮) -->
      <div class="card-header-flex">
        <div class="header-left">
          <div class="step-badge">STEP 02</div>
          <h2 class="title">Question Input</h2>
          <p class="subtitle">
            Input a medical calculation question and its complete description. 
            <span class="recommend-highlight">
            Or select a question example from `Question Examples` and the system will automatically reatrieve the complete description.
            </span>
          </p>
        </div>

        <div class="header-right">
          <el-button type="primary" plain round class="library-btn" @click="$emit('open-library')">
            <el-icon class="el-icon--left">
              <Collection />
            </el-icon>
            Question Examples
          </el-button>
        </div>
      </div>

      <!-- 2. 表单区域 -->
      <el-form :model="formData" label-position="top" class="modern-form">

        <!-- 问题输入 -->
        <el-form-item required>
          <template #label>
            <span class="custom-label">MEDICAL CALCULATION QUESTION</span>
          </template>
          <el-input v-model="formData.question"
            placeholder="e.g. Calculate the patient's BMI index based on recent vitals" clearable
            class="custom-input" />
        </el-form-item>

        <!-- 公式/知识输入 -->
        <el-form-item required>
          <template #label>
            <span class="custom-label">COMPLETE DESCRIPTION (FORMULA / LOGIC)</span>
          </template>
          <el-input v-model="formData.formula" type="textarea" :rows="5" resize="none" class="custom-textarea"
            placeholder="Example: BMI = weight (kg) / (height (m) ^ 2). If height is in cm, convert to meters first." />
        </el-form-item>

      </el-form>

    </div>
  </div>
</template>

<script setup lang="ts">
import { Collection } from '@element-plus/icons-vue'

defineProps<{
  formData: {
    question: string;
    formula: string;
  }
}>();

const emit = defineEmits(['open-library']);
</script>

<style scoped lang="scss">
/* 容器 */
.step-content-wrapper {
  width: 100%;
  margin: 0;
  font-family: 'Inter', -apple-system, sans-serif;
  animation: slideUp 0.6s cubic-bezier(0.2, 0.8, 0.2, 1);
}

/* 现代卡片风格 */
.modern-card {
  background: var(--el-bg-color);
  border-radius: 20px;
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.05),
    0 10px 15px -3px rgba(0, 0, 0, 0.05);
  border: 1px solid var(--el-border-color-lighter);
  padding: 40px;
  box-sizing: border-box;
  width: 100%;
}

/* 1. Header Flex 布局 */
.card-header-flex {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  /* 顶部对齐 */
  margin-bottom: 40px;
  gap: 20px;

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
      color: var(--el-text-color-primary);
      margin: 0 0 8px 0;
      letter-spacing: -0.5px;
    }

    .subtitle {
      font-size: 1rem;
      color: var(--el-text-color-secondary);
      margin: 0;
      line-height: 1.5;
    }
  }

.recommend-highlight {
  color: #0ea5e9;
  font-weight: 700;
}

  /* 按钮样式优化 */
  .header-right {
    .library-btn {
      border-color: var(--el-border-color-lighter);
      background-color: var(--el-fill-color-lighter);
      color: var(--el-text-color-regular);
      font-weight: 600;
      padding: 18px 24px;
      /* 更大的点击区域 */
      transition: all 0.2s ease;

      &:hover {
        background-color: var(--el-color-primary-light-9);
        border-color: var(--el-color-primary-light-7);
        color: #2563eb;
        transform: translateY(-1px);
      }
    }
  }
}

/* 2. Form 样式优化 */
.modern-form {
  .custom-label {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--el-text-color-regular);
    letter-spacing: 0.5px;
    text-transform: uppercase;
    white-space: nowrap;
    /* keep asterisk and label text on the same line */
  }

  /* 通用 Input/Textarea 样式混合 */
  @mixin modern-input-style {
    background-color: var(--el-fill-color-light);
    border: 1px solid var(--el-border-color);
    border-radius: 12px;
    font-size: 1rem;
    color: var(--el-text-color-primary);
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
      box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1);
    }
  }

  /* 应用到 Textarea */
  :deep(.custom-textarea .el-textarea__inner) {
    @include modern-input-style;
    padding: 16px;
    line-height: 1.7;
  }

  /* 应用到 Input */
  :deep(.custom-input .el-input__wrapper) {
    @include modern-input-style;
    padding: 4px 16px;
    /* 调整内边距适应高度 */
    height: 48px;
    /* 增加高度更现代 */

    /* 修复 Element Plus input wrapper 的 focus 样式 */
    &.is-focus {
      box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1) !important;
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
  .card-header-flex {
    flex-direction: column;
    align-items: flex-start;

    .header-right {
      width: 100%;

      .library-btn {
        width: 100%;
      }
    }
  }

  .modern-card {
    padding: 24px;
  }

  .title {
    font-size: 1.5rem;
  }
}
</style>