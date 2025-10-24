<template>
  <div class="flex min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100">
    <Sidebar :isOpen="isOpen" @close="isOpen = false" />

    <div class="flex-1 flex flex-col md:ml-64">
      <Navbar @toggle-sidebar="isOpen = !isOpen" />

      <!-- Content -->
      <main class="w-full py-8 px-4 sm:px-6 lg:px-8">
        <div class="space-y-8 max-w-6xl ml-4">
          <!-- Header -->
          <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Orders</h1>
            <p class="mt-2 text-gray-600 dark:text-gray-400">Manage and track customer orders</p>
          </div>

          <!-- Orders Content -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
            <!-- Header with Export Button -->
            <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
              <div class="flex space-x-1 bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
                <button
                  v-for="tab in statusTabs"
                  :key="tab.key"
                  @click="activeTab = tab.key"
                  :class="[
                    'px-4 py-2 text-sm font-medium rounded-md transition-colors',
                    activeTab === tab.key
                      ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow-sm'
                      : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
                  ]"
                >
                  {{ tab.label }}
                  <span v-if="tab.count > 0" class="ml-2 px-2 py-0.5 text-xs bg-gray-200 dark:bg-gray-500 rounded-full">
                    {{ tab.count }}
                  </span>
                </button>
              </div>
              <button
                @click="exportToCSV"
                class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors flex items-center space-x-2"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                <span>Export CSV</span>
              </button>
            </div>

            <!-- Orders Table -->
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead class="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Order ID
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Date
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Customer
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Total
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Status
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  <tr v-for="order in filteredOrders" :key="order.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                      #{{ order.id }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                      {{ order.date }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                      {{ order.customer }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                      ₹{{ order.total.toLocaleString() }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span :class="[
                        'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                        getStatusClass(order.status)
                      ]">
                        {{ order.status }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div class="flex space-x-2">
                        <button
                          @click="viewOrder(order)"
                          class="text-blue-600 dark:text-blue-400 hover:text-blue-900 dark:hover:text-blue-300"
                        >
                          View
                        </button>
                        <button
                          @click="editOrder(order)"
                          class="text-green-600 dark:text-green-400 hover:text-green-900 dark:hover:text-green-300"
                        >
                          Edit
                        </button>
                        <button
                          @click="deleteOrder(order)"
                          class="text-red-600 dark:text-red-400 hover:text-red-900 dark:hover:text-red-300"
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Empty State -->
            <div v-if="filteredOrders.length === 0" class="text-center py-12">
              <div class="text-gray-400 dark:text-gray-500 mb-4">
                <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                </svg>
              </div>
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No orders found</h3>
              <p class="text-gray-500 dark:text-gray-400">No orders match the current filter</p>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- View Order Modal -->
    <div v-if="showViewModal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-96 overflow-y-auto">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Order Details</h3>
          <button @click="closeViewModal" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        <div class="px-6 py-4">
          <div v-if="selectedOrder" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm font-medium text-gray-500 dark:text-gray-400">Order ID</label>
                <p class="text-lg font-semibold text-gray-900 dark:text-white">#{{ selectedOrder.id }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500 dark:text-gray-400">Date</label>
                <p class="text-lg text-gray-900 dark:text-white">{{ selectedOrder.date }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500 dark:text-gray-400">Customer</label>
                <p class="text-lg text-gray-900 dark:text-white">{{ selectedOrder.customer }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500 dark:text-gray-400">Total</label>
                <p class="text-lg font-semibold text-gray-900 dark:text-white">₹{{ selectedOrder.total.toLocaleString() }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500 dark:text-gray-400">Status</label>
                <span :class="[
                  'inline-flex px-3 py-1 text-sm font-semibold rounded-full',
                  getStatusClass(selectedOrder.status)
                ]">
                  {{ selectedOrder.status }}
                </span>
              </div>
            </div>
            <div class="pt-4 border-t border-gray-200 dark:border-gray-700">
              <h4 class="text-md font-medium text-gray-900 dark:text-white mb-2">Order Items</h4>
              <div class="space-y-2">
                <div class="flex justify-between items-center py-2 border-b border-gray-100 dark:border-gray-700">
                  <span class="text-sm text-gray-600 dark:text-gray-300">Premium Dog Food x2</span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">₹1,200</span>
                </div>
                <div class="flex justify-between items-center py-2 border-b border-gray-100 dark:border-gray-700">
                  <span class="text-sm text-gray-600 dark:text-gray-300">Cat Scratching Post x1</span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">₹800</span>
                </div>
                <div class="flex justify-between items-center py-2">
                  <span class="text-sm text-gray-600 dark:text-gray-300">Shipping</span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">₹50</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Order Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Edit Order</h3>
          <button @click="closeEditModal" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        <div class="px-6 py-4">
          <div v-if="editingOrder" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Status</label>
              <select v-model="editingOrder.status" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
                <option value="processing">Processing</option>
                <option value="shipped">Shipped</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Customer</label>
              <input v-model="editingOrder.customer" type="text" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Total</label>
              <input v-model="editingOrder.total" type="number" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
            </div>
            <div class="flex space-x-3 pt-4">
              <button @click="saveOrder" class="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors">
                Save Changes
              </button>
              <button @click="closeEditModal" class="flex-1 bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-300 py-2 px-4 rounded-md hover:bg-gray-400 dark:hover:bg-gray-500 transition-colors">
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Delete Order</h3>
        </div>
        <div class="px-6 py-4">
          <p class="text-gray-600 dark:text-gray-400 mb-4">
            Are you sure you want to delete order #{{ orderToDelete?.id }}? This action cannot be undone.
          </p>
          <div class="flex space-x-3">
            <button @click="confirmDelete" class="flex-1 bg-red-600 text-white py-2 px-4 rounded-md hover:bg-red-700 focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors">
              Delete
            </button>
            <button @click="closeDeleteModal" class="flex-1 bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-300 py-2 px-4 rounded-md hover:bg-gray-400 dark:hover:bg-gray-500 transition-colors">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import Navbar from '@/components/Navbar.vue'

interface Order {
  id: string
  date: string
  customer: string
  total: number
  status: string
}

const isOpen = ref(false)
const activeTab = ref('all')

// Modal states
const showViewModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const selectedOrder = ref<Order | null>(null)
const editingOrder = ref<Order | null>(null)
const orderToDelete = ref<Order | null>(null)

// Status tabs
const statusTabs = ref([
  { key: 'all', label: 'All', count: 0 },
  { key: 'processing', label: 'Processing', count: 0 },
  { key: 'shipped', label: 'Shipped', count: 0 },
  { key: 'completed', label: 'Completed', count: 0 },
  { key: 'cancelled', label: 'Cancelled', count: 0 }
])

// Sample orders data
const orders = ref<Order[]>([
  {
    id: '1234',
    date: '2024-01-15',
    customer: 'John Doe',
    total: 2500,
    status: 'processing'
  },
  {
    id: '1235',
    date: '2024-01-14',
    customer: 'Jane Smith',
    total: 1800,
    status: 'shipped'
  },
  {
    id: '1236',
    date: '2024-01-13',
    customer: 'Mike Johnson',
    total: 3200,
    status: 'completed'
  },
  {
    id: '1237',
    date: '2024-01-12',
    customer: 'Sarah Wilson',
    total: 1500,
    status: 'cancelled'
  },
  {
    id: '1238',
    date: '2024-01-11',
    customer: 'David Brown',
    total: 2800,
    status: 'processing'
  },
  {
    id: '1239',
    date: '2024-01-10',
    customer: 'Lisa Davis',
    total: 2100,
    status: 'shipped'
  }
])

// Computed properties
const filteredOrders = computed(() => {
  if (activeTab.value === 'all') {
    return orders.value
  }
  return orders.value.filter(order => order.status === activeTab.value)
})

// Methods
const getStatusClass = (status: string) => {
  const classes = {
    processing: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300',
    shipped: 'bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300',
    completed: 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300',
    cancelled: 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300'
  }
  return classes[status as keyof typeof classes] || 'bg-gray-100 text-gray-800 dark:bg-gray-900/40 dark:text-gray-300'
}

// View Order functionality
const viewOrder = (order: Order) => {
  selectedOrder.value = order
  showViewModal.value = true
}

const closeViewModal = () => {
  showViewModal.value = false
  selectedOrder.value = null
}

// Edit Order functionality
const editOrder = (order: Order) => {
  editingOrder.value = { ...order }
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
  editingOrder.value = null
}

const saveOrder = () => {
  if (editingOrder.value) {
    const index = orders.value.findIndex(order => order.id === editingOrder.value!.id)
    if (index !== -1) {
      orders.value[index] = { ...editingOrder.value }
      updateTabCounts()
    }
  }
  closeEditModal()
}

// Delete Order functionality
const deleteOrder = (order: Order) => {
  orderToDelete.value = order
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  orderToDelete.value = null
}

const confirmDelete = () => {
  if (orderToDelete.value) {
    const index = orders.value.findIndex(order => order.id === orderToDelete.value!.id)
    if (index !== -1) {
      orders.value.splice(index, 1)
      updateTabCounts()
    }
  }
  closeDeleteModal()
}

// Export to CSV functionality
const exportToCSV = () => {
  const csvContent = [
    ['Order ID', 'Date', 'Customer', 'Total', 'Status'],
    ...filteredOrders.value.map(order => [
      order.id,
      order.date,
      order.customer,
      order.total,
      order.status
    ])
  ].map(row => row.join(',')).join('\n')

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.setAttribute('href', url)
  link.setAttribute('download', `orders_${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// Update tab counts
const updateTabCounts = () => {
  statusTabs.value.forEach(tab => {
    if (tab.key === 'all') {
      tab.count = orders.value.length
    } else {
      tab.count = orders.value.filter(order => order.status === tab.key).length
    }
  })
}

// Initialize tab counts
updateTabCounts()
</script>
