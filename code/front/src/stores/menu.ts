import { defineStore } from 'pinia'
import * as ElIcons from '@element-plus/icons-vue'
import * as HeroOutlineIcons from '@heroicons/vue/24/outline'
import * as HeroSolidIcons from '@heroicons/vue/24/solid'
import { useWindowSize } from '@vueuse/core'
import { computed, markRaw, ref, watchEffect } from 'vue'
import type { Component } from 'vue'
import type { IMenuItem } from '@/types/menu'

export const useMenuStore = defineStore('menu', () => {
  // el-icon 图标映射
  const elIcons: Record<string, Component> = {}
  Object.keys(ElIcons).forEach((key) => {
    elIcons[`Element:${key}`] = ElIcons[key as keyof typeof ElIcons] as Component
  })
  // heroicons outline 图标映射
  const heroOutlineIcons: Record<string, Component> = {}
  Object.keys(HeroOutlineIcons).forEach((key) => {
    heroOutlineIcons[`HOutline:${key}`] = HeroOutlineIcons[key as keyof typeof HeroOutlineIcons] as Component
  })
  // heroicons solid 图标映射
  const heroSolidIcons: Record<string, Component> = {}
  Object.keys(HeroSolidIcons).forEach((key) => {
    heroSolidIcons[`HSolid:${key}`] = HeroSolidIcons[key as keyof typeof HeroSolidIcons] as Component
  })

  const iconComponents: Record<string, Component> = markRaw({
    ...elIcons,
    ...heroOutlineIcons,
    ...heroSolidIcons,
  })

  const isCollapse = ref(false)
  const toggleCollapse = () => {
    isCollapse.value = !isCollapse.value
  }

  const { width } = useWindowSize()
  const isMobile = computed(() => width.value < 992)

  watchEffect(() => {
    if (isMobile.value) isCollapse.value = false
  })

  const isMobileMenuOpen = ref(false)
  const toggleMobileMenu = () => {
    isMobileMenuOpen.value = !isMobileMenuOpen.value
  }

  // 先用静态菜单（后续你接后端/权限时再替换成动态加载）
  const menuList = ref<IMenuItem[]>([
    {
      id: 'm-dashboard',
      title: 'Dashboard',
      path: '/dashboard',
      icon: 'HOutline:HomeIcon',
      type: 'menu',
      parentId: '',
      order: 1,
      status: 'active',
      permission: '',
    },
    {
      id: 'm-calculation',
      title: 'Medical Calculation',
      path: '/calculation',
      icon: 'HOutline:CalculatorIcon',
      type: 'menu',
      parentId: '',
      order: 2,
      status: 'active',
      permission: '',
    },
    {
      id: 'm-atomic-tool',
      title: 'Tool Template',
      path: '/atomic-tool',
      icon: 'HOutline:WrenchScrewdriverIcon',
      type: 'menu',
      parentId: '',
      order: 3,
      status: 'active',
      permission: '',
    },
    // Hidden menu items
    // {
    //   id: 'm-calculation-v2',
    //   title: 'Calculation v2',
    //   path: '/calculation/v2',
    //   icon: 'HOutline:CalculatorIcon',
    //   type: 'menu',
    //   parentId: '',
    //   order: 4,
    //   status: 'active',
    //   permission: '',
    // },
    // {
    //   id: 'm-rule-generation',
    //   title: 'Rule Generation',
    //   path: '/rule-generation',
    //   icon: 'HOutline:SparklesIcon',
    //   type: 'menu',
    //   parentId: '',
    //   order: 5,
    //   status: 'active',
    //   permission: '',
    // },
    // {
    //   id: 'm-cases',
    //   title: 'Cases',
    //   path: '/cases',
    //   icon: 'HOutline:DocumentTextIcon',
    //   type: 'menu',
    //   parentId: '',
    //   order: 8,
    //   status: 'active',
    //   permission: '',
    // },
    // {
    //   id: 'm-config',
    //   title: 'Config',
    //   path: '/config',
    //   icon: 'HOutline:Cog6ToothIcon',
    //   type: 'menu',
    //   parentId: '',
    //   order: 7,
    //   status: 'active',
    //   permission: '',
    // },
  ])

  return {
    iconComponents,
    menuList,
    isCollapse,
    isMobileMenuOpen,
    isMobile,
    toggleCollapse,
    toggleMobileMenu,
  }
})


