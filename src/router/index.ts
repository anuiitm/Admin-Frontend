import { createRouter, createWebHistory, NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
import Login from '@/views/Login.vue'
import Dashboard from '@/views/Dashboard.vue'
import Settings from '@/views/Settings.vue'
import Orders from '@/views/Orders.vue'
import Products from '@/views/Products.vue'
import Inventory from '@/views/Inventory.vue'
import Promo from '@/views/Promo.vue'
import Customers from '@/views/Customers.vue'
import Analysis from '@/views/Analysis.vue'
import FAQ from '@/views/FAQ.vue'

export const isAuthenticated = (): boolean => {
	return localStorage.getItem('auth_token') !== null
}

const routes = [
	{ path: '/', redirect: '/dashboard' },
	{ path: '/login', name: 'login', component: Login, meta: { public: true } },
	{ path: '/dashboard', name: 'dashboard', component: Dashboard, meta: { requiresAuth: true } },
	{ path: '/settings', name: 'settings', component: Settings, meta: { requiresAuth: true } },
	{ path: '/orders', name: 'orders', component: Orders, meta: { requiresAuth: true } },
	{ path: '/products', name: 'products', component: Products, meta: { requiresAuth: true } },
	{ path: '/inventory', name: 'inventory', component: Inventory, meta: { requiresAuth: true } },
	{ path: '/promo', name: 'promo', component: Promo, meta: { requiresAuth: true } },
	{ path: '/customers', name: 'customers', component: Customers, meta: { requiresAuth: true } },
	{ path: '/analysis', name: 'analysis', component: Analysis, meta: { requiresAuth: true } },
	{ path: '/faq', name: 'faq', component: FAQ, meta: { requiresAuth: true } },
]

const router = createRouter({
	history: createWebHistory(),
	routes,
})

router.beforeEach((to: RouteLocationNormalized, _from: RouteLocationNormalized, next: NavigationGuardNext) => {
	if (to.meta.public) return next()
	if (to.meta.requiresAuth && !isAuthenticated()) return next({ name: 'login' })
	return next()
})

export default router

