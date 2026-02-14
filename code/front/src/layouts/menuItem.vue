<template>
  <!-- 情况 1: 有子菜单 -->
  <el-sub-menu v-if="hasChildren" :index="item.id" class="custom-sub-menu">
    <template #title>
      <el-icon v-if="item.icon" class="menu-icon">
        <component :is="menuStore.iconComponents[item.icon]" />
      </el-icon>
      <span class="menu-title">{{ item.title }}</span>
    </template>
    <!-- 递归调用 -->
    <MenuItem v-for="child in item.children" :key="child.path" :item="child" />
  </el-sub-menu>

  <!-- 情况 2: 无子菜单 -->
  <el-menu-item v-else :index="item.path" class="custom-menu-item">
    <el-icon v-if="item.icon" class="menu-icon">
      <component :is="menuStore.iconComponents[item.icon]" />
    </el-icon>
    <span class="menu-title">{{ item.title }}</span>
  </el-menu-item>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { IMenuItem } from '@/types/menu'
import { useMenuStore } from '@/stores/menu'

defineOptions({ name: 'MenuItem' })

const props = defineProps<{ item: IMenuItem }>()

const menuStore = useMenuStore()

const hasChildren = computed(() => props.item.children && props.item.children.length > 0)
</script>

<style scoped lang="scss">
/* 通用变量 */
$border-radius: 8px;
$item-height: 48px;
$transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);

/* --- 1. 深度选择器覆盖 Element Plus 默认样式 --- */

/* 针对 el-menu-item 和 el-sub-menu 的标题区域 */
:deep(.el-menu-item),
:deep(.el-sub-menu__title) {
  height: $item-height;
  line-height: $item-height;
  border-radius: $border-radius;
  margin: 4px 8px; /* 上下4px，左右8px，形成悬浮感 */
  color: #64748b; /* Slate-500: 默认文字颜色 */
  transition: $transition;
  border: none; /* 移除默认边框 */
  
  /* 修复折叠时的 padding */
  &.el-tooltip__trigger {
    padding: 0 !important; /* 让图标居中 */
  }

  /* 悬停状态 */
  &:hover {
    background-color: #f1f5f9 !important; /* Slate-100 */
    color: #1e293b !important; /* Slate-900 */
    
    .menu-icon {
      color: #1e293b;
      transform: scale(1.1);
    }
  }
}

/* --- 2. 选中激活状态 (Active) --- */
:deep(.el-menu-item.is-active) {
  background-color: var(--el-color-primary-light-9) !important; /* 极淡的品牌色背景 */
  color: var(--el-color-primary) !important;
  font-weight: 600;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05); /* 微弱的阴影 */

  /* 选中时的左侧指示条 (可选，类似 Dashboard 的装饰) */
  &::before {
    content: "";
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    height: 20px;
    width: 3px;
    background-color: var(--el-color-primary);
    border-radius: 0 4px 4px 0;
    opacity: 0; /* 默认隐藏，如果喜欢左侧蓝条可以改为 1 */
    transition: opacity 0.3s;
  }
  
  .menu-icon {
    color: var(--el-color-primary); /* 图标跟随变色 */
  }
}

/* --- 3. 内部元素样式 --- */

.menu-icon {
  font-size: 18px;
  margin-right: 10px;
  vertical-align: middle;
  transition: transform 0.3s ease, color 0.3s ease;
  /* 确保图标不被挤压 */
  flex-shrink: 0; 
}

.menu-title {
  font-family: 'Inter', -apple-system, sans-serif;
  font-weight: 500;
  font-size: 0.95rem;
  letter-spacing: 0.2px;
  vertical-align: middle;
  
  /* 文字截断处理 */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1; /* 占据剩余空间 */
}

/* --- 4. 针对折叠菜单的特殊处理 --- */
/* 当菜单折叠时，隐藏文字，调整图标位置 */
:deep(.el-menu--collapse) {
  .menu-title {
    display: none;
    opacity: 0;
    width: 0;
  }
  
  .el-menu-item, 
  .el-sub-menu__title {
    margin: 4px 0; /* 折叠时左右不需要 margin */
    display: flex;
    justify-content: center;
    align-items: center;
    
    .menu-icon {
      margin-right: 0;
    }
    
    .el-sub-menu__icon-arrow {
      display: none; /* 折叠时隐藏右侧箭头 */
    }
  }
}
</style>