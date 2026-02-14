<!-- src/components/Logo.vue -->
<template>
  <div class="app-logo" :class="{ 'collapsed': collapsed, 'is-large': large }">
    <!-- 图标部分 -->
    <div class="logo-icon">
      <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <!-- 这里定义两个渐变：
               1. sidebarLogoGradient: 用于侧边栏 (Primary Color)
               2. heroLogoGradient: 用于 Dashboard (Blue -> Cyan) 
          -->
          <linearGradient id="sidebarLogoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="var(--el-color-primary)" />
            <stop offset="100%" stop-color="#06b6d4" />
          </linearGradient>
          
          <linearGradient id="heroLogoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#2563eb" />
            <stop offset="100%" stop-color="#06b6d4" />
          </linearGradient>
        </defs>

        <!-- 动态切换 fill 和 stroke 的 URL -->
        <g :fill="large ? 'url(#heroLogoGradient)' : 'url(#sidebarLogoGradient)'"
           :stroke="large ? 'url(#heroLogoGradient)' : 'url(#sidebarLogoGradient)'">
           
           <path d="M50 5 L93.3 30 V80 L50 105 L6.7 80 V30 Z" stroke="none" opacity="0.1"/>
           <path d="M50 10 L89 32.5 V77.5 L50 100 L11 77.5 V32.5 Z" fill="none" stroke-width="8" stroke-linejoin="round"/>
           <rect x="42" y="30" width="16" height="50" rx="4" stroke="none" />
           <rect x="25" y="47" width="50" height="16" rx="4" stroke="none" />
           <circle cx="50" cy="55" r="10" fill="var(--el-bg-color)" stroke="none" />
           
           <!-- 中心点颜色逻辑：普通模式用 Primary，大号模式用深蓝 -->
           <circle cx="50" cy="55" r="5" :fill="large ? '#2563eb' : 'var(--el-color-primary)'" stroke="none" />
        </g>
      </svg>
    </div>

    <!-- 文字部分 -->
    <Transition name="fade-slide">
      <h1 v-show="!collapsed" class="logo-title">SRGE</h1>
    </Transition>
  </div>
</template>

<script setup lang="ts">
defineProps({
  // 控制侧边栏折叠
  collapsed: {
    type: Boolean,
    default: false
  },
  // 控制是否为 Dashboard 大号模式
  large: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped lang="scss">
.app-logo {
  display: flex;
  align-items: center;
  height: 100%;
  width: 100%;
  overflow: hidden;
  transition: all 0.3s;
  
  /* 默认侧边栏模式：左对齐，有内边距 */
  padding-left: 20px; 

  /* --- 状态 1: 侧边栏折叠 --- */
  &.collapsed {
    padding-left: 0;
    justify-content: center;
    .logo-icon { width: 32px; height: 32px; }
  }

  /* --- 状态 2: Dashboard 大号模式 --- */
  &.is-large {
    padding-left: 0;
    justify-content: center; /* 居中对齐 */
    gap: 16px; /* 图标和文字的间距 */

    /* 大图标尺寸 */
    .logo-icon {
      width: 80px; 
      height: 80px;
      /* 增强投影 */
      filter: drop-shadow(0 10px 15px rgba(37, 99, 235, 0.2));
    }

    /* 大文字样式 */
    .logo-title {
      margin: 0; /* 清除默认 margin */
      font-size: 48px; /* 3rem */
      font-weight: 900;
      letter-spacing: -2px; /* 紧凑设计 */
      /* 使用 Hero 渐变色 */
      background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
  }
}

/* 通用图标样式 */
.logo-icon {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  transition: all 0.3s cubic-bezier(0.2, 0, 0, 1);
  
  svg {
    width: 100%;
    height: 100%;
    display: block; /* 消除 SVG 底部空隙 */
  }
}

/* 通用文字样式 (侧边栏默认) */
.logo-title {
  margin: 0 0 0 12px;
  font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
  font-weight: 900;
  font-size: 22px;
  letter-spacing: -0.5px;
  color: var(--el-text-color-primary);
  white-space: nowrap;
  
  /* 侧边栏文字渐变 */
  background: linear-gradient(135deg, var(--el-text-color-primary) 0%, var(--el-text-color-regular) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* 进出动画 */
.fade-slide-enter-active {
  transition: all 0.3s ease-out;
  transition-delay: 0.1s;
}
.fade-slide-leave-active {
  transition: all 0.1s ease-in;
}
.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}
</style>