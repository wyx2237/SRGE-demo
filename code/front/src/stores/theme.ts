import { defineStore } from 'pinia'
import { useDark, useToggle } from '@vueuse/core'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const isDark = useDark()
  const toggleDark = useToggle(isDark)

  const themeMode = ref<'light' | 'dark'>(
    (localStorage.getItem('themeMode') as 'light' | 'dark') || 'light',
  )

  const toggleThemeMode = (newVal: 'light' | 'dark') => {
    themeMode.value = newVal
    toggleDark(newVal === 'dark')
    localStorage.setItem('themeMode', newVal)
  }

  const primaryColorOptions = [
    { value: '#8B5CF6', name: '紫色' },
    { value: '#10B981', name: '绿色' },
    { value: '#F59E0B', name: '橙色' },
    { value: '#EF4444', name: '红色' },
    { value: '#6366F1', name: '靛蓝' },
    { value: '#1677FF', name: '蓝色' },
    { value: '#0EA5E9', name: '天蓝' },
    { value: '#00BCD4', name: '青色' },
    { value: '#909399', name: '灰色' },
  ]

  const setPrimaryColor = (color: string) => {
    const root = document.documentElement
    root.style.setProperty('--el-color-primary', color)
    root.style.setProperty('--el-color-primary-light-3', `color-mix(in srgb, ${color} 70%, white)`)
    root.style.setProperty('--el-color-primary-light-5', `color-mix(in srgb, ${color} 50%, white)`)
    root.style.setProperty('--el-color-primary-light-7', `color-mix(in srgb, ${color} 30%, white)`)
    root.style.setProperty('--el-color-primary-light-8', `color-mix(in srgb, ${color} 20%, white)`)
    root.style.setProperty('--el-color-primary-light-9', `color-mix(in srgb, ${color} 10%, white)`)
    root.style.setProperty('--el-color-primary-dark-2', `color-mix(in srgb, ${color} 80%, black)`)
  }

  const primaryColor = ref(localStorage.getItem('theme-color-primary') || '#8B5CF6')
  setPrimaryColor(primaryColor.value)

  const togglePrimaryColor = (colorValue: string) => {
    primaryColor.value = colorValue
    localStorage.setItem('theme-color-primary', colorValue)
    setPrimaryColor(colorValue)
  }

  const showLogo = ref(JSON.parse(localStorage.getItem('showLogo') || 'true'))
  const toggleShowLogo = (value: boolean) => {
    showLogo.value = value
    localStorage.setItem('showLogo', JSON.stringify(showLogo.value))
  }

  const showTabs = ref(JSON.parse(localStorage.getItem('showTabs') || 'true'))
  const toggleShowTabs = (value: boolean) => {
    showTabs.value = value
    localStorage.setItem('showTabs', JSON.stringify(showTabs.value))
  }

  return {
    themeMode,
    primaryColor,
    primaryColorOptions,
    showLogo,
    toggleThemeMode,
    togglePrimaryColor,
    toggleShowLogo,
    showTabs,
    toggleShowTabs,
  }
})


