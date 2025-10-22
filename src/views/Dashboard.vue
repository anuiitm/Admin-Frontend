<template>
	<div class="flex min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100">
    	<Sidebar :isOpen="isOpen" @close="isOpen = false" />

    	<div class="flex-1 flex flex-col md:ml-64">
      		<Navbar @toggle-sidebar="isOpen = !isOpen" />

				<!-- Content -->
				<main class="max-w-7xl mx-1 px-1 sm:px-6 lg:px-8 py-6">
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
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import Navbar from '@/components/Navbar.vue'

const isOpen = ref(false)
const router = useRouter()

const cards = ref([
	{ title: 'Revenue', value: '$12,340', delta: '+8% from last week', badge: 'Live', badgeClass: 'bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300' },
	{ title: 'Orders', value: '238', delta: '+3% from last week', badge: 'Today', badgeClass: 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300' },
	{ title: 'Customers', value: '1,024', delta: '+1% from last week', badge: 'All', badgeClass: 'bg-gray-100 text-gray-700 dark:bg-gray-900/50 dark:text-gray-300' },
	{ title: 'Inventory', value: '342', delta: '-2% restock soon', badge: 'Watch', badgeClass: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/40 dark:text-yellow-300' },
])

const products = ref(['Premium Dog Food', 'Cat Scratching Post', 'Aquarium Set', 'Bird Cage'])

</script>

<style scoped>
</style>

