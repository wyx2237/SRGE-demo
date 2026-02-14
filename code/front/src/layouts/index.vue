<template>
  <div class="layout-container">
    <MenuView v-if="!menuStore.isMobile" class="menu-view" />

    <el-container class="right-content-container">
      <el-header class="header">
        <HeaderView />
      </el-header>
      <!-- <Transition name="fade-slide" mode="out-in">
        <TabsView v-if="themeStore.showTabs" />
      </Transition> -->

      <el-scrollbar>
        <el-main class="main">
          <RouterView v-slot="{ Component, route }">
            <Transition name="fade-slide" mode="out-in">
              <KeepAlive :include="tabsStore.tabs.map((tab) => tab.path as string)">
                <component :is="Component" :key="route.path" />
              </KeepAlive>
            </Transition>
          </RouterView>
        </el-main>
      </el-scrollbar>
    </el-container>

    <!-- 移动端菜单抽屉 -->
    <el-drawer
      v-model="menuStore.isMobileMenuOpen"
      :direction="'ltr'"
      :with-header="false"
      :size="220"
      class="mobile-menu-drawer"
    >
      <MenuView />
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import HeaderView from '@/layouts/header.vue'
import MenuView from '@/layouts/menu.vue'
import TabsView from '@/layouts/TabsView.vue'
import { useMenuStore } from '@/stores/menu'
import { useThemeStore } from '@/stores/theme'
import { useTabsStore } from '@/stores/tabs'

defineOptions({ name: 'LayoutView' })

const menuStore = useMenuStore()
const themeStore = useThemeStore()
const tabsStore = useTabsStore()
</script>

<style scoped lang="scss">
.layout-container {
  width: 100%;
  height: 100vh;
  display: flex; /* Enable flexbox for side-by-side layout */
}
.menu-view {
  flex-shrink: 0; /* Prevent sidebar from shrinking */
}

.right-content-container {
  flex-grow: 1; /* Allow content area to take remaining space */
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
  min-height: calc(100vh - 50px - 2.5rem); /* Adjust based on header and tabs height */
  display: flex;
  flex-direction: column;
}

:deep(.mobile-menu-drawer) {
  .el-drawer__body {
    padding: 0;
  }
}
</style>


