<template>
	
	<div class="flex min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100">
    	<Sidebar :isOpen="isOpen" @close="isOpen = false" />

    	<div class="flex-1 flex flex-col md:ml-64">
      		<Navbar @toggle-sidebar="isOpen = !isOpen" />

      <!-- Content -->
      <main class="w-full py-8 px-4 sm:px-6 lg:px-8">
        <div class="space-y-8 max-w-6xl ml-4">
				<div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
            <p class="mt-2 text-gray-600 dark:text-gray-400">Your application dashboard</p>
          </div>

					<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
						<div v-if="cards.length === 0" class="col-span-full text-sm text-gray-500 dark:text-gray-400">No metrics yet.</div>
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
							<div v-if="recentOrders.length === 0" class="text-sm text-gray-500 dark:text-gray-400 py-4">No recent orders.</div>
							<ul v-else class="mt-4 divide-y divide-gray-100 dark:divide-gray-700">
								<li v-for="o in recentOrders" :key="o.id" class="flex items-center justify-between py-3">
									<span class="text-sm text-gray-700 dark:text-gray-200">Order #{{ o.number }}</span>
									<span class="text-xs text-gray-500">{{ o.items }} items • ₹{{ o.total.toFixed(2) }}</span>
								</li>
							</ul>
						</section>
						<section class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 p-5 shadow-soft">
							<h2 class="text-sm font-medium text-gray-700 dark:text-gray-200">Top Products</h2>
							<div v-if="topProducts.length === 0" class="text-sm text-gray-500 dark:text-gray-400 py-4">No products data.</div>
							<ul v-else class="mt-4 space-y-3">
								<li v-for="p in topProducts" :key="p.name" class="flex items-center justify-between">
									<span class="text-sm text-gray-700 dark:text-gray-200">{{ p.name }}</span>
									<span class="text-xs text-gray-500">{{ p.sold }} sold</span>
								</li>
							</ul>
						</section>
					</div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import Navbar from '@/components/Navbar.vue'
import { useApi } from '@/composables/useApi'

const isOpen = ref(false)
const router = useRouter()
const api = useApi()

const cards = ref<any[]>([])
const recentOrders = ref<any[]>([])
const topProducts = ref<any[]>([])

onMounted(async () => {
    try {
        const summary = await api.get<{ total_sales: number; total_orders: number; total_customers: number; low_stock_products: number }>(`/dashboard/summary`)
        cards.value = [
            { title: 'Revenue', value: `₹${summary.total_sales.toLocaleString()}`, delta: '', badge: 'Live', badgeClass: 'bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300' },
            { title: 'Orders', value: `${summary.total_orders}`, delta: '', badge: 'All', badgeClass: 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300' },
            { title: 'Customers', value: `${summary.total_customers}`, delta: '', badge: 'All', badgeClass: 'bg-gray-100 text-gray-700 dark:bg-gray-900/50 dark:text-gray-300' },
            { title: 'Low Stock', value: `${summary.low_stock_products}`, delta: '', badge: 'Watch', badgeClass: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/40 dark:text-yellow-300' },
        ]
    } catch (e) { /* noop */ }

    try {
        const orders = await api.get<any[]>(`/orders`)
        recentOrders.value = orders.slice(0, 5).map((o: any) => ({ id: o.order_id, number: o.order_number, items: (o.items_count || 0), total: o.total_price }))
    } catch (e) { /* noop */ }

    try {
        const analytics = await api.get<any[]>(`/analysis/products`)
        topProducts.value = analytics.slice(0, 5).map(a => ({ name: `#${a.product_id}`, sold: a.total_orders }))
    } catch (e) { /* noop */ }
})
</script>

<style scoped>
</style>

