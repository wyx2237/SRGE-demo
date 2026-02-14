import { createRouter, createWebHistory } from 'vue-router'
import NProgress from 'nprogress'
import { useTabsStore } from '@/stores/tabs'
import { useMenuStore } from '@/stores/menu'

NProgress.configure({
  easing: 'ease',
  speed: 500,
  showSpinner: false,
  trickleSpeed: 200,
  minimum: 0.3,
})

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/login/index.vue'),
      meta: { public: true },
    },
    {
      path: '/',
      name: 'layout',
      component: () => import('@/layouts/index.vue'),
      redirect: '/dashboard',
      children: [
        {
          path: '/dashboard',
          name: 'DashboardView',
          component: () => import('@/views/dashboard/index.vue'),
          meta: { title: 'Dashboard' },
        },
        // {
        //   path: '/calculation/old',
        //   name: 'CalculationView-old',
        //   component: () => import('@/views/calculation/index.vue'),
        //   meta: { title: 'Calculation' },
        // },
        {
          path: '/calculation',
          name: 'CalculationView',
          component: () => import('@/views/calculation/main.vue'),
          meta: { title: 'Medical Calculation' },
        },
        {
          path: '/rule-generation',
          name: 'RuleGenerationView',
          component: () => import('@/views/rule-generation/index.vue'),
          meta: { title: 'Rule Generation' },
        },
        {
          path: '/atomic-tool',
          name: 'AtomicToolView',
          component: () => import('@/views/atomic-tool/index.vue'),
          meta: { title: 'Atomic Tool' },
        },
        {
          path: '/cases',
          name: 'CasesView',
          component: () => import('@/views/cases/index.vue'),
          meta: { title: 'Cases' },
        },
        {
          path: '/config',
          name: 'ConfigView',
          component: () => import('@/views/config/index.vue'),
          meta: { title: 'Config' },
        },
      ],
    },
    {
      path: '/:pathMatch(.*)*',
      name: '404',
      component: () => import('@/views/exception/404.vue'),
      meta: { public: true },
    },
  ],
})

router.beforeEach((to) => {
  NProgress.start()

  const token = localStorage.getItem('token')
  if (to.meta?.public) return true
  if (!token) return { name: 'login' }

  // Add tab to tabsStore
  if (to.meta?.title) {
    const tabsStore = useTabsStore()
    const menuStore = useMenuStore()

    let icon = to.meta.icon as string | undefined
    if (!icon) {
      // Try to find icon from menuList if not present in route meta
      const menuItem = menuStore.menuList.find(item => item.path === to.path)
      if (menuItem) {
        icon = menuItem.icon
      }
    }

    tabsStore.addTab({
      path: to.path,
      title: to.meta.title as string,
      icon: icon,
      closable: true,
    })
  }
  return true
})

router.afterEach(() => {
  NProgress.done()
})

export default router
