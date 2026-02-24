<template>
  <div class="step-content-wrapper">
    <!-- 自定义卡片容器 -->
    <div class="modern-card">

      <!-- 1. 头部区域 -->
      <div class="card-header-flex">
        <div class="header-left">
          <div class="step-badge">STEP 01</div>
          <h2 class="title">EMR Input</h2>
          <p class="subtitle">
            Input the unstructured EMR (Electronic Medical Record) text.
            Type manually, upload a file, or select an example.
          </p>
        </div>

        <!-- 右侧按钮组 -->
        <div class="header-right">
          <!-- 上传文件按钮 -->
          <el-upload
            action="#"
            :auto-upload="false"
            :show-file-list="false"
            accept=".txt"
            :on-change="handleFileUpload"
            class="upload-demo"
          >
            <el-button plain round class="action-btn-secondary">
              <el-icon class="el-icon--left"><Upload /></el-icon>
              Upload .txt
            </el-button>
          </el-upload>

          <!-- 清空按钮 -->
          <el-button 
            plain 
            round 
            type="danger" 
            class="action-btn-danger" 
            @click="handleClear"
            :disabled="!formData.clinicalText"
          >
            <el-icon class="el-icon--left"><Delete /></el-icon>
            Clear
          </el-button>

          <!-- 分割线 (可选) -->
          <div class="divider-vertical"></div>

          <!-- 案例库按钮 -->
          <el-button type="primary" plain round class="library-btn" @click="$emit('open-library')">
            <el-icon class="el-icon--left"><Collection /></el-icon>
            EMR Examples
          </el-button>
        </div>
      </div>

      <!-- 2. 提示区域 -->
      <div class="info-alert-box">
        <div class="alert-icon">
          <el-icon><InfoFilled /></el-icon>
        </div>
        <div class="alert-content">
          <strong>Guidance:</strong> Ensure the text includes all necessary variables (e.g., demographics, lab results)
          required for the target medical calculation.
          <span class="recommend-highlight">It is highly recommended to select an example from `EMR Examples`.</span>
        </div>
      </div>

      <!-- 3. 表单区域 -->
      <el-form :model="formData" label-position="top" class="modern-form">
        <el-form-item required>
          <template #label>
            <span class="custom-label">EMR TEXT SOURCE</span>
          </template>

          <el-input 
            v-model="formData.clinicalText" 
            type="textarea" 
            :rows="8" 
            resize="none" 
            class="custom-textarea"
            placeholder="Example: The patient is a 45-year-old male presenting with severe fatigue..." 
          />
        </el-form-item>
      </el-form>

    </div>
  </div>
</template>

<script setup lang="ts">
import { InfoFilled, Collection, Upload, Delete } from '@element-plus/icons-vue'
import { ElMessage, type UploadFile } from 'element-plus'

const props = defineProps<{
  formData: {
    clinicalText: string;
  }
}>();

const emit = defineEmits(['open-library']);

// --- 1. 处理文件上传 (.txt) ---
const handleFileUpload = (uploadFile: UploadFile) => {
  const rawFile = uploadFile.raw;
  if (!rawFile) return;

  // 验证类型 (虽然 accept=".txt" 限制了选择，但最好再校验一下)
  if (rawFile.type !== 'text/plain') {
    ElMessage.error('Only .txt files are allowed');
    return;
  }

  // 使用 FileReader 读取文本内容
  const reader = new FileReader();
  reader.onload = (e) => {
    if (e.target?.result) {
      // 将读取到的文本赋值给 formData
      props.formData.clinicalText = e.target.result as string;
      ElMessage.success('File loaded successfully');
    }
  };
  reader.onerror = () => {
    ElMessage.error('Failed to read file');
  };
  reader.readAsText(rawFile);
};

// --- 2. 处理清空 ---
const handleClear = () => {
  props.formData.clinicalText = '';
  ElMessage.info('Text cleared');
};
</script>

<style scoped lang="scss">
/* 容器调整 */
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
  margin-bottom: 32px;
  gap: 20px;

  .header-left {
    flex: 1; /* 让左侧占据剩余空间，避免挤压 */
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

  /* 右侧按钮组区域 */
  .header-right {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-shrink: 0; /* 防止按钮被挤压换行 */

    /* 垂直分割线 */
    .divider-vertical {
      width: 1px;
      height: 24px;
      background-color: var(--el-border-color);
      margin: 0 4px;
    }

    /* 灰色次级按钮 (Upload) */
    .action-btn-secondary {
      border-color: var(--el-border-color-lighter);
      background-color: transparent;
      color: var(--el-text-color-regular);
      font-weight: 600;
      &:hover {
        background-color: var(--el-fill-color);
        color: var(--el-color-primary);
        border-color: var(--el-color-primary-light-5);
      }
    }

    /* 红色危险按钮 (Clear) */
    .action-btn-danger {
      font-weight: 600;
      /* 只有 hover 时才显现红色背景，平时保持低调 */
      background-color: transparent;
      border-color: var(--el-border-color-lighter);
      color: var(--el-color-danger);
      
      &:hover {
        background-color: var(--el-color-danger-light-9);
        border-color: var(--el-color-danger-light-5);
      }
      &:disabled {
        background-color: transparent;
        border-color: var(--el-border-color-lighter);
        color: var(--el-text-color-placeholder);
      }
    }

    /* 蓝色主按钮 (Examples) */
    .library-btn {
      border-color: var(--el-border-color-lighter);
      background-color: var(--el-fill-color-lighter);
      color: var(--el-text-color-regular);
      font-weight: 600;
      padding: 12px 20px;
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

    .recommend-highlight {
      color: #0ea5e9;
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
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }

  /* 深度选择器修改 el-input */
  :deep(.custom-textarea .el-textarea__inner) {
    background-color: var(--el-fill-color-light);
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
@media (max-width: 800px) {
  .card-header-flex {
    flex-direction: column;
    align-items: flex-start;

    .header-right {
      width: 100%;
      justify-content: flex-start;
      flex-wrap: wrap;
      
      .upload-demo {
        margin-right: 0;
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