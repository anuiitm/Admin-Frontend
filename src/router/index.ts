import { createRouter, createWebHistory, NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
import Login from '@/views/Login.vue'
import Dashboard from '@/views/Dashboard.vue'
// import Settings from '@/views/Settings.vue'

export const isAuthenticated = (): boolean => {
	return localStorage.getItem('auth_token') !== null
}

const routes = [
	{ path: '/', redirect: '/dashboard' },
	{ path: '/login', name: 'login', component: Login, meta: { public: true } },
	{ path: '/dashboard', name: 'dashboard', component: Dashboard, meta: { requiresAuth: true } },
	// { path: '/settings', name: 'settings', component: Settings, meta: { requiresAuth: true } },
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

