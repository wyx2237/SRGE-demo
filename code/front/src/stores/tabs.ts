import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface TabItem {
  path: string
  title: string
  icon?: string
  closable: boolean
}

export const useTabsStore = defineStore('tabs', () => {
  const activePath = ref('/dashboard') // Default active path
  const tabs = ref<TabItem[]>([
    // Use the same icon key as in menuStore for Dashboard
    { path: '/dashboard', title: 'Dashboard', closable: false, icon: 'HOutline:HomeIcon' },
  ])

  const addTab = (tab: TabItem) => {
    if (!tabs.value.some((t) => t.path === tab.path)) {
      tabs.value.push(tab)
    }
    activePath.value = tab.path
  }

  // const removeTab = (path: string) => {
  //   if (tabs.value.length === 1 && tabs.value[0].path === path) {
  //     // Don't remove the last tab if it's the current one
  //     return
  //   }

  //   const index = tabs.value.findIndex((t) => t.path === path)
  //   if (index !== -1) {
  //     tabs.value.splice(index, 1)
  //     if (activePath.value === path) {
  //       // If the closed tab was active, activate the next or previous one
  //       activePath.value = tabs.value[Math.max(0, index - 1)].path
  //     }
  //   }
  // }

  const closeOtherTabs = (path: string) => {
    tabs.value = tabs.value.filter(tab => tab.path === path || !tab.closable)
    activePath.value = path
  }

  const closeAllTabs = () => {
    tabs.value = tabs.value.filter(tab => !tab.closable)
    activePath.value = tabs.value[0]?.path || '/dashboard'
  }

  const closeRightTabs = (path: string) => {
    const index = tabs.value.findIndex((t) => t.path === path)
    if (index !== -1) {
      tabs.value = tabs.value.slice(0, index + 1).filter(tab => tab.path === path || !tab.closable)
      activePath.value = path
    }
  }

  const closeLeftTabs = (path: string) => {
    const index = tabs.value.findIndex((t) => t.path === path)
    if (index !== -1) {
      tabs.value = tabs.value.slice(index).filter(tab => tab.path === path || !tab.closable)
      activePath.value = path
    }
  }

  return {
    activePath,
    tabs,
    addTab,
    // removeTab,
    closeOtherTabs,
    closeAllTabs,
    closeRightTabs,
    closeLeftTabs,
  }
})