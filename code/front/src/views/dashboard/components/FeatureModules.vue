<template>
  <div class="section-container">
    <h3 class="section-title">
      <el-icon><Menu /></el-icon> 功能模块
    </h3>
    <el-row :gutter="20">
      <el-col :xs="24" :sm="12" :md="12" :lg="6" v-for="mod in modules" :key="mod.title">
        <el-card 
          class="module-card" 
          shadow="hover" 
          @click="$router.push(mod.path)"
        >
          <div class="module-header">
            <div class="module-icon" :style="{ background: mod.bgColor }">
              <el-icon :style="{ color: mod.iconColor }"><component :is="mod.icon" /></el-icon>
            </div>
            <div class="module-arrow">
              <el-icon><Right /></el-icon>
            </div>
          </div>
          <div class="module-body">
            <h4>{{ mod.title }}</h4>
            <p>{{ mod.desc }}</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { Menu, Right, Cpu, Files, DataLine, Setting } from '@element-plus/icons-vue'

const modules = [
  {
    title: '计算实验室',
    desc: '4步流程向导，从文本到计算结果的完整演示。',
    path: '/calculation',
    icon: Cpu,
    bgColor: '#ecf5ff',
    iconColor: '#409EFF'
  },
  {
    title: '规则库管理',
    desc: '查看、编辑和管理已生成的结构化规则。',
    path: '/rules',
    icon: Files,
    bgColor: '#f0f9eb',
    iconColor: '#67C23A'
  },
  {
    title: '统计报表',
    desc: '系统使用情况与计算准确率分析。',
    path: '/statistics',
    icon: DataLine,
    bgColor: '#fdf6ec',
    iconColor: '#E6A23C'
  },
  {
    title: '系统设置',
    desc: 'API 密钥配置与计算引擎参数调整。',
    path: '/settings',
    icon: Setting,
    bgColor: '#f4f4f5',
    iconColor: '#909399'
  }
]
</script>

<style scoped lang="scss">
.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  font-size: 18px;
  color: var(--el-text-color-primary);
}

.module-card {
  cursor: pointer;
  border-radius: 12px;
  border: 1px solid transparent;
  transition: all 0.3s;
  margin-bottom: 16px;
  
  /* 固定高度与Flex布局 */
  height: 180px; 
  display: flex;
  flex-direction: column;
  box-sizing: border-box;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    border-color: var(--el-color-primary-light-7);
    
    .module-arrow {
      opacity: 1;
      transform: translateX(0);
    }
  }

  :deep(.el-card__body) {
    flex: 1;
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 20px;
  }
  
  .module-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 16px;
    flex-shrink: 0;
    
    .module-icon {
      width: 44px;
      height: 44px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
    }
    
    .module-arrow {
      opacity: 0;
      transform: translateX(-10px);
      transition: all 0.3s;
      color: var(--el-text-color-placeholder);
      margin-top: 4px;
    }
  }
  
  .module-body {
    flex: 1;
    display: flex;
    flex-direction: column;
    
    h4 {
      margin: 0 0 8px;
      font-size: 16px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    p {
      margin: 0;
      font-size: 13px;
      color: var(--el-text-color-secondary);
      line-height: 1.5;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
  }
}
</style>