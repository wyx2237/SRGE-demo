<template>
  <div class="sidebar-wrapper" :class="{ 'is-collapsed': menuStore.isCollapse }"
    :style="{ backgroundColor: menuBackgroundColor }">
    
    <!-- 1. 顶部 Logo 区域 (使用新组件) -->
    <div class="logo-header" v-if="themeStore.showLogo" @click="handleLogoClick">
      <!-- 传递折叠状态给子组件 -->
      <Logo :collapsed="menuStore.isCollapse" />
    </div>

    <!-- 2. 滚动菜单区域 -->
    <el-scrollbar class="menu-scrollbar">
      <el-menu 
        :default-active="activeMenu" 
        :collapse="menuStore.isCollapse" 
        :background-color="menuBackgroundColor"
        :text-color="menuTextColor" 
        :active-text-color="menuActiveTextColor" 
        :collapse-transition="false"
        :mode="menuMode" 
        @select="navigation" 
        class="custom-menu"
      >
        <!-- 这里的 MenuItem 保持不变 -->
        <MenuItem v-for="item in menuStore.menuList" :key="item.path" :item="item" />
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MenuItem from '@/layouts/menuItem.vue'
import Logo from '@/components/Logo.vue' // 引入新组件
import { useMenuStore } from '@/stores/menu'
import { useThemeStore } from '@/stores/theme'

defineOptions({ name: 'MenuView' })

const menuStore = useMenuStore()
const themeStore = useThemeStore()
const route = useRoute()
const router = useRouter()

const activeMenu = computed(() => route.path)
const menuMode = computed(() => 'vertical')

// Use Element Plus theme vars to keep dark/light consistent.
const menuBackgroundColor = computed(() => 'var(--el-bg-color)')
const menuTextColor = computed(() => 'var(--el-text-color-regular)')
const menuActiveTextColor = computed(() => themeStore.primaryColor)

const navigation = (key: string) => {
  router.push(key)
  if (menuStore.isMobile && menuStore.isMobileMenuOpen) {
    menuStore.isMobileMenuOpen = false
  }
}

const handleLogoClick = () => {
  router.push('/')
}
</script>

<style scoped lang="scss">
/* 
Sidebar 容器逻辑保持不变 
*/
.sidebar-wrapper {
  height: 100vh;
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--el-border-color-lighter);
  width: 240px;
  transition: width 0.3s cubic-bezier(0.2, 0, 0, 1), background-color 0.3s;

  &.is-collapsed {
    width: 64px;

    &.mobile {
      width: 0;
    }
  }
}

/* 
Logo Header 容器
现在的样式很简单，只负责定高和光标，内部布局由 Logo.vue 接管 
*/
.logo-header {
  height: 64px;
  cursor: pointer;
  /* 确保 Logo 组件可以撑满高度 */
  display: flex;
  align-items: center;
  justify-content: flex-start;
  
  /* 给一个悬停效果 */
  &:hover {
    background-color: var(--el-fill-color-light);
  }
}

.menu-scrollbar {
  flex: 1;
}

.custom-menu {
  border-right: none !important;
  width: 100%;

  &:not(.el-menu--collapse) {
    padding: 8px;
  }
}

/* MenuItem 样式 (保持你的原样) */
:deep(.el-menu-item),
:deep(.el-sub-menu__title) {
  height: 50px;
  line-height: 50px;
  border-radius: 8px;
  margin-bottom: 4px;

  .el-icon {
    font-size: 18px;
    margin-right: 12px;
    transition: margin 0.3s;
  }

  &:hover {
    background-color: var(--el-fill-color-light) !important;
    color: var(--el-color-primary) !important;

    .el-icon {
      color: var(--el-color-primary);
    }
  }

  &.is-active {
    background-color: var(--el-color-primary-light-9) !important;
    color: var(--el-color-primary) !important;
    font-weight: 600;

    html.dark & {
      background-color: var(--el-color-primary-light-8) !important;
    }
  }
}

/* 折叠态样式覆盖 */
.el-menu--collapse {
  padding: 4px 0;

  :deep(.el-menu-item),
  :deep(.el-sub-menu__title) {
    padding: 0 !important;
    margin: 4px 0;
    justify-content: center;
    border-radius: 0;

    .el-icon {
      margin: 0;
    }

    span {
      display: none;
      visibility: hidden;
    }
  }
}
</style>