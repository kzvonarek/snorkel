import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/',          name: 'Overview',    component: () => import('@/views/OverviewView.vue') },
  { path: '/projects',  name: 'Projects',    component: () => import('@/views/ProjectsView.vue') },
  { path: '/connect',   name: 'Connect',     component: () => import('@/views/ConnectDataView.vue') },
  { path: '/personas',  name: 'Personas',    component: () => import('@/views/PersonasView.vue') },
  { path: '/market',    name: 'Market',      component: () => import('@/views/MarketView.vue') },
  { path: '/products',  name: 'Products',    component: () => import('@/views/ProductsView.vue') },
  { path: '/sandbox',   name: 'Sandbox',     component: () => import('@/views/SandboxView.vue') },
  { path: '/swarm',     name: 'Swarm',       component: () => import('@/views/SwarmView.vue') },
  { path: '/results',   name: 'Results',     component: () => import('@/views/ResultsView.vue') },
  { path: '/report',    name: 'Report',      component: () => import('@/views/ReportView.vue') },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
