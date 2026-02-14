<template>
  <el-container class="left-mode-container">
    <MenuView v-if="!menuStore.isMobile" class="menu-view" />
    <el-container>
      <el-header class="header">
        <HeaderView />
      </el-header>

      <el-scrollbar>
        <el-main class="main">
          <RouterView v-slot="{ Component, route }">
            <Transition name="fade-slide" mode="out-in">
              <component :is="Component" :key="route.path" />
            </Transition>
          </RouterView>
        </el-main>
      </el-scrollbar>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import HeaderView from '@/layouts/header.vue'
import MenuView from '@/layouts/menu.vue'
import { useMenuStore } from '@/stores/menu'

defineOptions({ name: 'LeftMode' })

const menuStore = useMenuStore()
</script>

<style scoped lang="scss">
.left-mode-container {
  width: 100%;
  height: 100%;
}
.menu-view {
  flex-shrink: 0;
}

.header {
  height: 50px;
  background: var(--el-bg-color);
  border-bottom: 1px solid var(--el-border-color-lighter);
  padding-right: 0.25rem;
}

.main {
  background: var(--el-bg-color-page);
  padding: 1rem;
  position: relative;
  overflow-y: auto;
  overflow-x: hidden;
  min-height: calc(100vh - 50px);
  display: flex;
  flex-direction: column;
}
</style>


