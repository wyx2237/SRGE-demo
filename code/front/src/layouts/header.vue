<template>
  <div class="header-container">
    <div class="header-left">
      <el-tooltip :content="menuStore.isMobile ? 'expand menu' : 'collapse menu'" placement="bottom" effect="dark">
        <div class="action-btn" @click="handleMenuToggle">
          <el-icon>
            <component
              :is="
                menuStore.isMobile
                  ? menuStore.iconComponents['HOutline:Bars3CenterLeftIcon']
                  : menuStore.isCollapse
                    ? menuStore.iconComponents['HOutline:Bars3BottomRightIcon']
                    : menuStore.iconComponents['HOutline:Bars3BottomLeftIcon']
              "
            />
          </el-icon>
        </div>
      </el-tooltip>
      <BreadcrumbView :showIcon="true"/>
    </div>

    <div class="header-right">
      <el-tooltip :content="themeStore.themeMode === 'dark' ? 'light mode' : 'dark mode'" placement="bottom" effect="dark">
        <div class="action-btn" @click="toggleTheme">
          <el-icon>
            <component
              :is="
                themeStore.themeMode === 'dark'
                  ? menuStore.iconComponents['HOutline:SunIcon']
                  : menuStore.iconComponents['HOutline:MoonIcon']
              "
            />
          </el-icon>
        </div>
      </el-tooltip>

      <el-dropdown>
        <div class="user-chip">
          <el-avatar :size="28" style="background: var(--el-color-primary)">D</el-avatar>
          <span class="user-name">Doctor</span>
          <el-icon><component :is="menuStore.iconComponents['HOutline:ChevronDownIcon']" /></el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="logout">logout</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMenuStore } from '@/stores/menu'
import { useThemeStore } from '@/stores/theme'
import BreadcrumbView from '@/layouts/Breadcrumb.vue'

defineOptions({ name: 'HeaderView' })

const menuStore = useMenuStore()
const themeStore = useThemeStore()
const route = useRoute()
const router = useRouter()


const handleMenuToggle = () => {
  if (menuStore.isMobile) {
    menuStore.toggleMobileMenu()
  } else {
    menuStore.toggleCollapse()
  }
}

const toggleTheme = () => {
  themeStore.toggleThemeMode(themeStore.themeMode === 'dark' ? 'light' : 'dark')
}

const logout = async () => {
  localStorage.removeItem('token')
  await router.replace({ name: 'login' })
}
</script>

<style scoped lang="scss">
.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.page-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--el-text-color-primary);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.action-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--el-text-color-regular);
  background: transparent;

  &:hover {
    background: var(--el-fill-color-light);
    color: var(--el-color-primary);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    animation: jello;
    animation-duration: 1s;
  }

  .el-icon {
    font-size: 1.25rem;
  }
}

.user-chip {
  height: 36px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 12px 0 6px;
  border-radius: 10px;
  border: 1px solid var(--el-border-color-lighter);
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    border-color: var(--el-color-primary-light-7);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
  }
}

.user-name {
  font-size: 0.9rem;
  color: var(--el-text-color-primary);
  font-weight: 600;
}
</style>


