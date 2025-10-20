<template>
	<div class="min-h-screen bg-gray-50 dark:bg-gray-900">
		<!-- Top bar -->
		<header class="bg-white/80 dark:bg-gray-800/80 backdrop-blur border-b border-gray-200 dark:border-gray-700">
			<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
				<div class="flex items-center gap-3">
					<div class="w-8 h-8 rounded-lg bg-primary-600 text-white grid place-items-center">
						<svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
							<path d="M12 21c4 0 7-2.5 7-5.5 0-2-2.5-3.5-5-2-1-.5-2-.5-3 0-2.5-1.5-5 0-5 2 0 3 3 5.5 7 5.5Z" fill="currentColor"/>
						</svg>
					</div>
					<h1 class="font-semibold text-gray-900 dark:text-gray-100">Dashboard</h1>
				</div>
				<div class="flex items-center gap-4">
					<ThemeToggle />
					<button @click="logout" class="text-xs text-red-600 hover:text-red-700">Logout</button>
				</div>
			</div>
		</header>

		<!-- Content -->
		<main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
				<div v-for="card in cards" :key="card.title" class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 p-5 shadow-soft">
					<div class="flex items-center justify-between">
						<h3 class="text-sm text-gray-600 dark:text-gray-300">{{ card.title }}</h3>
						<span :class="['text-xs px-2 py-0.5 rounded-full', card.badgeClass]">{{ card.badge }}</span>
					</div>
					<p class="mt-2 text-3xl font-semibold text-gray-900 dark:text-gray-100">{{ card.value }}</p>
					<p class="mt-1 text-xs text-gray-500" v-if="card.delta">{{ card.delta }}</p>
				</div>
			</div>

			<div class="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-6">
				<section class="lg:col-span-2 bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 p-5 shadow-soft">
					<h2 class="text-sm font-medium text-gray-700 dark:text-gray-200">Recent Orders</h2>
					<ul class="mt-4 divide-y divide-gray-100 dark:divide-gray-700">
						<li v-for="order in 5" :key="order" class="flex items-center justify-between py-3">
							<span class="text-sm text-gray-700 dark:text-gray-200">Order #{{ 1000 + order }}</span>
							<span class="text-xs text-gray-500">2 items • ${{ (order*24).toFixed(2) }}</span>
						</li>
					</ul>
				</section>
				<section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 p-5 shadow-soft">
					<h2 class="text-sm font-medium text-gray-700 dark:text-gray-200">Top Products</h2>
					<ul class="mt-4 space-y-3">
						<li v-for="p in products" :key="p" class="flex items-center justify-between">
							<span class="text-sm text-gray-700 dark:text-gray-200">{{ p }}</span>
							<span class="text-xs text-gray-500">1,2k sold</span>
						</li>
					</ul>
				</section>
			</div>
		</main>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import ThemeToggle from '@/components/ThemeToggle.vue'

const router = useRouter()

const cards = ref([
	{ title: 'Revenue', value: '$12,340', delta: '+8% from last week', badge: 'Live', badgeClass: 'bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300' },
	{ title: 'Orders', value: '238', delta: '+3% from last week', badge: 'Today', badgeClass: 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300' },
	{ title: 'Customers', value: '1,024', delta: '+1% from last week', badge: 'All', badgeClass: 'bg-gray-100 text-gray-700 dark:bg-gray-900/50 dark:text-gray-300' },
	{ title: 'Inventory', value: '342', delta: '-2% restock soon', badge: 'Watch', badgeClass: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/40 dark:text-yellow-300' },
])

const products = ref(['Premium Dog Food', 'Cat Scratching Post', 'Aquarium Set', 'Bird Cage'])

function logout() {
	localStorage.removeItem('auth_token')
	router.push({ name: 'login' })
}
</script>

<style scoped>
</style>

