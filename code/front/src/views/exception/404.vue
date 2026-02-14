<template>
  <div class="wrap">
    <el-result icon="warning" title="404" sub-title="页面不存在">
      <template #extra>
        <el-button type="primary" @click="$router.replace('/dashboard')">返回首页</el-button>
      </template>
    </el-result>
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: 'NotFoundView' })
</script>

<style scoped>
.wrap {
  min-height: calc(100vh - 100px);
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>


