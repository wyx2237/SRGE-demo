<template>
  <div class="header-section">
    <div class="welcome-banner">
      <h2>👋 Welcome Back, Doctor</h2>
      <p class="subtitle">这里是临床计算规则引擎控制台，系统运行状态良好。</p>
    </div>
    
    <el-row :gutter="20">
      <el-col :xs="24" :sm="12" :md="6" v-for="(item, index) in statItems" :key="index">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon-wrapper" :class="item.colorClass">
            <el-icon><component :is="item.icon" /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-label">{{ item.label }}</div>
            <div class="stat-number">
              {{ item.value }}
              <span v-if="item.trend" class="trend-tag" :class="item.trend > 0 ? 'up' : 'down'">
                <el-icon><component :is="item.trend > 0 ? 'Top' : 'Bottom'" /></el-icon>
                {{ Math.abs(item.trend) }}%
              </span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { Odometer, Files, TrendCharts, EditPen, Top, Bottom } from '@element-plus/icons-vue'

const statItems = [
  { 
    label: '今日生成规则', 
    value: '24', 
    trend: 12, 
    icon: EditPen, 
    colorClass: 'bg-blue' 
  },
  { 
    label: '执行成功率', 
    value: '98.5%', 
    trend: 0.5, 
    icon: Odometer, 
    colorClass: 'bg-green' 
  },
  { 
    label: '待人工审核', 
    value: '5', 
    trend: -2, 
    icon: Files, 
    colorClass: 'bg-orange' 
  },
  { 
    label: 'API 调用量', 
    value: '1.2k', 
    trend: 18, 
    icon: TrendCharts, 
    colorClass: 'bg-purple' 
  },
]
</script>

<style scoped lang="scss">
.header-section {
  .welcome-banner {
    margin-bottom: 20px;
    h2 {
      margin: 0;
      font-size: 24px;
      color: var(--el-text-color-primary);
    }
    .subtitle {
      margin: 8px 0 0;
      color: var(--el-text-color-secondary);
      font-size: 14px;
    }
  }
}

.stat-card {
  border-radius: 12px;
  border: none;
  box-shadow: 0 4px 16px rgba(0,0,0,0.04);
  margin-bottom: 16px;
  
  :deep(.el-card__body) {
    display: flex;
    align-items: center;
    padding: 20px;
  }
}

.stat-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  font-size: 24px;
  
  &.bg-blue { background: #ecf5ff; color: #409EFF; }
  &.bg-green { background: #f0f9eb; color: #67C23A; }
  &.bg-orange { background: #fdf6ec; color: #E6A23C; }
  &.bg-purple { background: #f4f4f5; color: #909399; }
}

.stat-content {
  flex: 1;
  .stat-label {
    font-size: 13px;
    color: var(--el-text-color-secondary);
  }
  .stat-number {
    font-size: 24px;
    font-weight: 700;
    margin-top: 4px;
    display: flex;
    align-items: center;
    gap: 8px;
    
    .trend-tag {
      font-size: 12px;
      font-weight: normal;
      display: flex;
      align-items: center;
      padding: 2px 6px;
      border-radius: 4px;
      
      &.up { background: #f0f9eb; color: #67C23A; }
      &.down { background: #fef0f0; color: #F56C6C; }
    }
  }
}
</style>