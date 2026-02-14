<template>
  <div class="rule-detail-container">
    <el-card shadow="never" class="canvas-card" :body-style="{ padding: 0, height: '100%' }">
      
      <!-- 1. 详情页头部 -->
      <div class="detail-header">
        <el-page-header @back="$emit('back')">
          <template #content>
            <span class="detail-title"> {{ rule.name }} </span>
            <el-tag size="small" :type="getStatusType(rule.status)" style="margin-left: 10px">
              {{ rule.status }}
            </el-tag>
          </template>
          <template #extra>
            <el-button-group>
              <!-- 修正点：使用 :icon 绑定组件对象 -->
              <el-button :icon="Edit" round>编辑</el-button>
              <el-button :icon="VideoPlay" type="success" round>测试执行</el-button>
            </el-button-group>
          </template>
        </el-page-header>
      </div>

      <!-- 2. 画布与属性面板容器 -->
      <div class="canvas-container">
        
        <!-- 左侧：模拟画布区域 -->
        <div class="canvas-area">
          <div class="placeholder-node start-node">Start</div>
          <div class="connector"></div>
          <div class="placeholder-node logic-node">
            <!-- 修正点：确保 Cpu 组件已导入 -->
            <el-icon :size="20"><Cpu /></el-icon>
            <span>Logic Computation</span>
          </div>
          <div class="connector"></div>
          <div class="placeholder-node end-node">Output: {{ rule.id }}</div>
          
          <div class="canvas-watermark">Graphical Workflow Viewer</div>
        </div>

        <!-- 右侧：属性面板 -->
        <div class="properties-panel">
          <h4>Rule Properties</h4>
          <div class="prop-item">
            <label>ID</label>
            <span>{{ rule.id }}</span>
          </div>
          <div class="prop-item">
            <label>Version</label>
            <span>v{{ rule.version }}</span>
          </div>
          <div class="prop-item">
            <label>Last Updated</label>
            <span>{{ rule.updatedAt }}</span>
          </div>
          <div class="prop-item">
            <label>Complexity</label>
            <el-rate v-model="mockRate" disabled size="small" />
          </div>
          <el-divider />
          <p class="desc">该规则通过自然语言处理生成，并通过逻辑引擎验证。</p>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
// 确保引入了所有用到的图标
import { Cpu, Edit, VideoPlay } from '@element-plus/icons-vue'

const props = defineProps<{
  rule: {
    id: string
    name: string
    status: string
    updatedAt: string
    version: string
  }
}>()

const emit = defineEmits(['back'])
const mockRate = ref(4)

const getStatusType = (status: string) => {
  switch (status) {
    case 'Active': return 'success'
    case 'Testing': return 'warning'
    case 'Draft': return 'info'
    default: return ''
  }
}
</script>

<style scoped lang="scss">
.rule-detail-container {
  height: 100%;
  min-height: 500px;
  display: flex;
  flex-direction: column;
}

.canvas-card {
  flex: 1;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  /* Card 会自动处理背景色，无需手动设置 */
}

.detail-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-light);
  /* --- 修复点：头部背景色 --- */
  background: var(--el-bg-color); 
}

.detail-title {
  font-weight: 700;
  font-size: 16px;
  color: var(--el-text-color-primary); /* 文字颜色 */
}

.canvas-container {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.canvas-area {
  flex: 1;
  /* --- 修复点：画布背景色 --- */
  background-color: var(--el-fill-color-light); /* 浅灰/深灰背景 */
  
  /* 网格线颜色也需要调整为变量 */
  background-image: 
    linear-gradient(var(--el-border-color-lighter) 1px, transparent 1px),
    linear-gradient(90deg, var(--el-border-color-lighter) 1px, transparent 1px);
  background-size: 20px 20px;
  
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.canvas-watermark {
  position: absolute;
  bottom: 20px;
  right: 20px;
  font-size: 24px;
  font-weight: 900;
  color: var(--el-text-color-placeholder); /* 水印颜色 */
  opacity: 0.2;
  pointer-events: none;
}

.placeholder-node {
  padding: 12px 24px;
  border-radius: 8px;
  
  /* --- 修复点：节点背景色 --- */
  background: var(--el-bg-color-overlay);
  
  border: 2px solid;
  font-weight: bold;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 8px;
  z-index: 2;
  
  &.start-node { border-color: #67C23A; color: #67C23A; }
  &.logic-node { border-color: #409EFF; color: #409EFF; padding: 20px 40px;}
  &.end-node { border-color: #F56C6C; color: #F56C6C; }
}

.connector {
  width: 2px;
  height: 40px;
  background: var(--el-border-color-darker); /* 连接线颜色 */
}

.properties-panel {
  width: 280px;
  /* --- 修复点：属性面板背景色 --- */
  background: var(--el-bg-color);
  border-left: 1px solid var(--el-border-color-light);
  padding: 20px;
  
  h4 {
    margin: 0 0 20px 0;
    color: var(--el-text-color-primary);
  }

  .prop-item {
    margin-bottom: 16px;
    label {
      display: block;
      font-size: 12px;
      color: var(--el-text-color-secondary);
      margin-bottom: 4px;
    }
    span {
      font-size: 14px;
      font-weight: 500;
      color: var(--el-text-color-regular);
      font-family: monospace;
    }
  }
  
  .desc {
    font-size: 12px;
    color: var(--el-text-color-secondary);
    line-height: 1.6;
  }
}
</style>