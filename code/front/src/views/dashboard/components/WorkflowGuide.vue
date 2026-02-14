<template>
  <el-card shadow="never" class="guide-card">
    <template #header>
      <div class="card-header">
        <span><el-icon><Guide /></el-icon> 规则引擎工作流</span>
      </div>
    </template>
    
    <div class="content-wrapper">
      <div class="steps-area">
        <el-steps :active="1" align-center finish-status="success">
          <el-step title="知识录入" description="输入公式与问题定义" />
          <el-step title="上下文解析" description="提供临床病历文本" />
          <el-step title="规则生成" description="AI 结构化与验证" />
          <el-step title="执行计算" description="参数抽取与结果输出" />
        </el-steps>
      </div>
      
      <div class="action-area">
        <el-button type="primary" round size="large" @click="$router.push('/calculation')">
          开始一次新计算
        </el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { Guide } from '@element-plus/icons-vue'
</script>

<style scoped lang="scss">
.guide-card {
  border-radius: 12px;
  
  .card-header {
    display: flex;
    align-items: center;
    gap: 6px;
    font-weight: 600;
  }

  .content-wrapper {
    padding: 10px 0;
    text-align: center;
  }

  .steps-area {
    margin-bottom: 30px;
    padding: 0 20px;
  }
}
</style>