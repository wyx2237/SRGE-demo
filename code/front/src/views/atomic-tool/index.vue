<template>
  <div class="atomic-library-container">
    
    <!-- 顶部标题区域 (无变化) -->
    <div class="library-header">
      <div class="header-left">
        <!-- <div class="brand-badge">ATOMIC LIBRARY</div> -->
        <h1 class="main-title">Atomic Tool Template Library</h1>
        <p class="sub-title">Standardized component repository for logic construction</p>
      </div>
      <div class="header-right">
        <div class="stat-box">
          <span class="stat-num">{{ tools.length }}</span>
          <span class="stat-label">Templates Available</span>
        </div>
      </div>
    </div>

    <!-- 列表内容区域 -->
    <div class="tool-list-wrapper">
      <el-collapse v-model="activeNames" accordion class="custom-collapse">
        <el-collapse-item 
          v-for="(tool, index) in tools" 
          :key="tool.id" 
          :name="tool.id"
          class="tool-item"
        >
          <!-- 1. 卡片标题栏 (Header) -->
          <template #title>
            <div class="card-header-flex">
              
              <!-- 区域1：大图标 -->
              <div class="section-icon">
                <div class="icon-wrapper" :class="getColorClass(index)">
                  <el-icon :size="32"><Tools /></el-icon>
                </div>
              </div>

              <!-- 区域2：核心信息 -->
              <div class="section-info">
                <div class="info-row-top">
                  <span class="tool-name">{{ tool.general_info.Name }}</span>
                  <span class="tool-tag">ATOMIC</span>
                </div>
                <div class="info-row-bottom">
                  {{ tool.general_info.Description }}
                </div>
              </div>

              <!-- 区域3：元数据 (自定义的展开按钮) -->
              <div class="section-meta">
                <span class="detail-label">DETAILS</span>
                <div class="arrow-circle">
                  <el-icon class="arrow-icon"><ArrowDown /></el-icon>
                </div>
              </div>

            </div>
          </template>

          <!-- 2. 卡片详情内容 (Body) (无变化) -->
          <div class="tool-detail-body">
            <div class="body-panel left-panel">
              <div class="panel-header">
                <el-icon><Connection /></el-icon>
                <span>Logic Specification</span>
              </div>
              <div class="io-flow-chart">
                <div class="flow-node input">
                  <span class="node-label">INPUT</span>
                  <div class="node-content">{{ tool.flow_info.Input }}</div>
                </div>
                <div class="flow-arrow">
                  <div class="line"></div>
                  <el-icon><ArrowDown /></el-icon>
                </div>
                <div class="flow-node output">
                  <span class="node-label">OUTPUT</span>
                  <div class="node-content">{{ tool.flow_info.Output }}</div>
                </div>
              </div>
              <div class="full-desc">
                <strong>Description:</strong> {{ tool.general_info.Description }}
              </div>
            </div>
            <div class="body-panel right-panel">
              <div class="panel-header dark-header">
                <div class="ph-left">
                  <el-icon><Cpu /></el-icon> Implementation
                </div>
                <div class="ph-right">
                  <span class="lang-badge">PYTHON</span>
                </div>
              </div>
              <div class="code-container">
                <pre><code>{{ tool.code_info.Logic }}</code></pre>
              </div>
            </div>
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { atomicTools } from '@/stores/mockData'
import { Tools, Connection, ArrowDown, Cpu } from '@element-plus/icons-vue'

defineOptions({ name: 'AtomicToolView' })

const activeNames = ref('')
const tools = ref(atomicTools)

const getColorClass = (index: number) => {
  const colors = ['blue', 'green', 'purple', 'orange', 'cyan', 'indigo']
  return colors[index % colors.length]
}
</script>

<style scoped lang="scss">
/* --- 1. 全局容器 --- */
.atomic-library-container {
  min-height: 100vh;
  background-color: var(--el-bg-color-page);
  padding: 40px;
  display: flex;
  flex-direction: column;
  gap: 30px;
  box-sizing: border-box;
  font-family: 'Inter', -apple-system, sans-serif;
}

/* --- 2. 页面顶部 Header --- */
.library-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding-bottom: 20px;
  border-bottom: 2px solid var(--el-border-color-lighter);

  .header-left {
    .brand-badge {
      font-size: 0.75rem;
      font-weight: 800;
      color: #0ea5e9;
      letter-spacing: 2px;
      margin-bottom: 8px;
    }
    .main-title {
      font-size: 2.5rem;
      font-weight: 800;
      color: var(--el-text-color-primary);
      margin: 0;
      line-height: 1.1;
    }
    .sub-title {
      color: var(--el-text-color-secondary);
      margin: 8px 0 0 0;
      font-size: 1rem;
    }
  }

  .header-right {
    .stat-box {
      text-align: right;
      .stat-num {
        display: block;
        font-size: 3rem;
        font-weight: 700;
        color: var(--el-text-color-primary);
        line-height: 1;
      }
      .stat-label {
        color: var(--el-text-color-placeholder);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
      }
    }
  }
}

/* --- 3. 列表样式 --- */
.tool-list-wrapper {
  width: 100%;
}

.custom-collapse {
  border: none;
  display: flex;
  flex-direction: column;
  gap: 24px;

  .tool-item {
    background-color: var(--el-bg-color);
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--el-border-color-lighter);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    transition: transform 0.2s ease, box-shadow 0.2s ease;

    &:hover {
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
      transform: translateY(-2px);
    }

    /* 
       核心修改：隐藏 Element Plus 默认的箭头 
       注意：这里使用 display: none 强制隐藏
    */
    :deep(.el-collapse-item__arrow) {
      display: none !important;
    }

    :deep(.el-collapse-item__header) {
      height: auto; 
      line-height: normal;
      background-color: var(--el-bg-color) !important; 
      padding: 0;
      border-bottom: 1px solid var(--el-border-color-lighter);
    }
    
    :deep(.el-collapse-item__wrap) {
      background-color: var(--el-bg-color) !important; 
      border-bottom: none;
    }
    :deep(.el-collapse-item__content) {
      padding: 0;
    }
  }
}

/* --- 4. 卡片头部布局 --- */
.card-header-flex {
  width: 100%;
  display: flex;
  align-items: stretch; 
  min-height: 100px;
}

.section-icon {
  width: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--el-fill-color-lighter); 
  border-right: 1px solid var(--el-border-color-lighter); 
  flex-shrink: 0;

  .icon-wrapper {
    width: 64px;
    height: 64px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    
    &.blue { background: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe; }
    &.green { background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
    &.purple { background: #f3e8ff; color: #6b21a8; border: 1px solid #e9d5ff; }
    &.orange { background: #ffedd5; color: #9a3412; border: 1px solid #fed7aa; }
    &.cyan { background: #cffafe; color: #155e75; border: 1px solid #a5f3fc; }
    &.indigo { background: #e0e7ff; color: #3730a3; border: 1px solid #c7d2fe; }
  }
}

.section-info {
  flex: 1;
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 8px;

  .info-row-top {
    display: flex;
    align-items: center;
    gap: 12px;
    
    .tool-name {
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--el-text-color-primary); 
    }
    .tool-tag {
      font-size: 0.7rem;
      font-weight: 700;
      background: #334155;
      color: #fff;
      padding: 2px 6px;
      border-radius: 4px;
    }
  }

  .info-row-bottom {
    font-size: 0.95rem;
    color: var(--el-text-color-secondary); 
    line-height: 1.5;
  }
}

.section-meta {
  width: 100px;
  border-left: 1px solid var(--el-border-color-lighter); 
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;
  background-color: var(--el-fill-color-blank);
  flex-shrink: 0;
  transition: background-color 0.2s;

  &:hover {
    background-color: var(--el-fill-color-lighter);
  }

  .detail-label {
    font-size: 0.65rem;
    font-weight: 800;
    color: var(--el-text-color-placeholder);
    letter-spacing: 1px;
    user-select: none;
  }

  .arrow-circle {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background-color: #e2e8f0;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;

    .arrow-icon {
      font-size: 1rem;
      color: #64748b;
      transition: transform 0.3s;
    }
  }
}

/* 箭头旋转动画 & 高亮 */
:deep(.el-collapse-item.is-active) {
  .arrow-icon {
    transform: rotate(180deg);
    color: #0f172a;
  }
  .arrow-circle {
    background-color: #cbd5e1;
  }
}

/* --- 5. 详情 Body --- */
.tool-detail-body {
  display: flex;
  border-top: 1px solid #e2e8f0; 
}

.body-panel {
  padding: 24px;
}

.left-panel {
  flex: 4;
  background-color: var(--el-bg-color);
  border-right: 1px solid var(--el-border-color-lighter);
  display: flex;
  flex-direction: column;

  .panel-header {
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--el-text-color-regular);
    text-transform: uppercase;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
}

.io-flow-chart {
  display: flex;
  flex-direction: column;
  gap: 0;
  margin-bottom: 20px;

  .flow-node {
    border: 1px solid var(--el-border-color-lighter);
    border-radius: 6px;
    padding: 12px 16px;
    position: relative;
    background: var(--el-bg-color);
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);

    .node-label {
      font-size: 0.7rem;
      font-weight: 800;
      color: var(--el-text-color-placeholder);
      display: block;
      margin-bottom: 4px;
    }
    .node-content {
      font-family: monospace;
      font-weight: 600;
      color: var(--el-text-color-primary);
      font-size: 1rem;
    }

    &.input { border-left: 4px solid #3b82f6; background: #eff6ff; }
    &.output { border-left: 4px solid #10b981; background: #ecfdf5; }
  }

  .flow-arrow {
    height: 30px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: var(--el-text-color-placeholder);
    .line { height: 100%; width: 1px; background: var(--el-border-color); }
  }
}

.full-desc {
  font-size: 0.9rem;
  color: var(--el-text-color-regular);
  line-height: 1.6;
  padding-top: 16px;
  border-top: 1px dashed var(--el-border-color-lighter);
}

.right-panel {
  flex: 5;
  background-color: #1e293b;
  color: #f1f5f9;
  padding: 0;
  display: flex;
  flex-direction: column;

  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 20px;
    background: #0f172a;
    border-bottom: 1px solid #334151;
    
    .ph-left {
      font-weight: 600;
      font-size: 0.9rem;
      display: flex;
      align-items: center;
      gap: 8px;
      color: #94a3b8;
    }
    .lang-badge {
      font-size: 0.7rem;
      background: #334155;
      padding: 2px 8px;
      border-radius: 4px;
      color: #e2e8f0;
      border: 1px solid #475569;
    }
  }

  .code-container {
    padding: 20px;
    overflow-x: auto;
    
    pre {
      margin: 0;
      code {
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 0.9rem;
        line-height: 1.7;
        color: #e2e8f0;
      }
    }
  }
}

@media (max-width: 768px) {
  .atomic-library-container { padding: 16px; }
  .card-header-flex { flex-wrap: wrap; }
  .section-icon { width: 80px; height: auto; border-right: none; border-bottom: 1px solid #f1f5f9;}
  .section-info { width: calc(100% - 80px); padding: 16px; }
  .section-meta { width: 100%; border-left: none; border-top: 1px solid #f1f5f9; flex-direction: row; padding: 10px 16px; }
}
</style>