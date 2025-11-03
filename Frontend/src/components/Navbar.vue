<template>
    <header
        class="flex items-center justify-between bg-white dark:bg-gray-800 p-4 shadow-md"
    >
        <button @click="$emit('toggle-sidebar')" class="md:hidden p-2 rounded bg-gray-200 dark:bg-gray-800 text-gray-800 dark:text-white hover:bg-gray-300 dark:hover:bg-gray-700 transition-colors"> ☰ </button>
        <div class="flex items-center w-full max-w-3xl">
            <div class="flex items-center w-full space-x-2">
                <!-- Search Entity Dropdown -->
                <select
                    v-model="searchEntity"
                    class="w-32 h-10 px-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900 text-sm"
                >
                    <option value="all">All</option>
                    <option value="products">Products</option>
                    <option value="customers">Customers</option>
                    <option value="orders">Orders</option>
                </select>
                
                <!-- Search Input -->
                <input
                    v-model="searchQuery"
                    @keyup.enter="handleSearch"
                    type="text"
                    :placeholder="getSearchPlaceholder()"
                    class="w-[55%] h-10 px-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900"
                />
                
                <!-- Search Button -->
                <button 
                    @click="handleSearch" 
                    class="w-20 h-10 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200 flex items-center justify-center"
                >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                </button>
            </div>
        </div>

        <div class="flex items-center gap-4">
            <!-- Notifications Dropdown -->
            <div class="relative">
                <button 
                    @click="toggleNotifications" 
                    class="p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-300 transition-colors relative"
                >
                    🔔
                    <span v-if="unreadCount > 0" class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">{{ unreadCount }}</span>
                </button>
                
                <!-- Notification Dropdown -->
                <div 
                    v-if="showNotifications" 
                    class="absolute right-0 mt-2 w-80 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-50"
                >
                    <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Notifications</h3>
                    </div>
                    <div class="max-h-64 overflow-y-auto">
                        <div v-for="notification in notifications" :key="notification.id" 
                             class="px-4 py-3 border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer"
                             :class="{ 'bg-blue-50 dark:bg-blue-900/20': !notification.read }"
                             @click="markAsRead(notification.id)">
                            <div class="flex items-start space-x-3">
                                <div class="flex-shrink-0">
                                    <div class="w-2 h-2 bg-blue-500 rounded-full mt-2" v-if="!notification.read"></div>
                                </div>
                                <div class="flex-1 min-w-0">
                                    <p class="text-sm font-medium text-gray-900 dark:text-white">{{ notification.title }}</p>
                                    <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ notification.message }}</p>
                                    <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">{{ notification.time }}</p>
                                </div>
                            </div>
                        </div>
                        <div v-if="notifications.length === 0" class="px-4 py-8 text-center">
                            <p class="text-gray-500 dark:text-gray-400">No notifications</p>
                        </div>
                    </div>
                    <div class="px-4 py-3 border-t border-gray-200 dark:border-gray-700">
                        <button 
                            @click="markAllAsRead" 
                            class="text-sm text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300"
                            v-if="unreadCount > 0"
                        >
                            Mark all as read
                        </button>
                    </div>
                </div>
            </div>
            
            <button @click="goSettings" class="p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-300 transition-colors">⚙️</button>
            <ThemeToggle />
            <button
                @click="logout"
                class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm"
            > Logout </button>
        </div>
    </header>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ThemeToggle from '@/components/ThemeToggle.vue'
import { useApi } from '@/composables/useApi'

const searchQuery = ref('')
const searchEntity = ref('all')
const router = useRouter()

function handleSearch() {
  if (searchQuery.value.trim()) {
    router.push({ 
      name: 'SearchResults', 
      query: { 
        q: searchQuery.value,
        entity: searchEntity.value
      } 
    })
  }
}

function getSearchPlaceholder() {
  const placeholders = {
    all: 'Search products, customers, orders...',
    products: 'Search products by name, SKU, category...',
    customers: 'Search customers by name, email, location...',
    orders: 'Search orders by ID, customer, status...'
  }
  return placeholders[searchEntity.value as keyof typeof placeholders] || placeholders.all
}

const showNotifications = ref(false)
const notifications = ref<{ id: number; title: string; message: string; time: string; read: boolean }[]>([])
const api = useApi()

// Computed properties
const unreadCount = computed(() => {
    return notifications.value.filter(n => !n.read).length
})

// Methods
function toggleNotifications() {
    showNotifications.value = !showNotifications.value
}

async function markAsRead(id: number) {
    try { await api.post(`/notifications/${id}/read`, {}) } catch (e) { /* noop */ }
    const n = notifications.value.find(n => n.id === id)
    if (n) n.read = true
}

function markAllAsRead() {
    notifications.value.forEach(n => { n.read = true })
}

function logout() {
    localStorage.removeItem('auth_token')
    router.push({ name: 'login' })
}

function goSettings() {
    router.push('/settings')
}

// Close notifications when clicking outside
document.addEventListener('click', (event) => {
    const target = event.target as HTMLElement
    if (!target.closest('.relative')) {
        showNotifications.value = false
    }
})

onMounted(async () => {
  try {
    const data = await api.get<any[]>(`/notifications`)
    notifications.value = data.map(d => ({ id: Number(d.notification_id), title: d.title, message: d.message, time: new Date(d.created_at).toLocaleString(), read: d.is_read }))
  } catch (e) { /* noop */ }
})
</script>