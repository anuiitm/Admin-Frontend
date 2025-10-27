<template>
  <div class="flex min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100">
    <Sidebar :isOpen="isOpen" @close="isOpen = false" />

    <div class="flex-1 flex flex-col md:ml-64">
      <Navbar @toggle-sidebar="isOpen = !isOpen" />

      <!-- Content -->
      <main class="w-full py-8 px-4 sm:px-6 lg:px-8">
        <div class="space-y-8 max-w-6xl ml-4">
          <!-- Header -->
          <div class="mb-8 flex justify-between items-center">
            <div>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Customers</h1>
            <p class="mt-2 text-gray-600 dark:text-gray-400">Manage customer information and relationships</p>
            </div>
            <div>
              <button
                @click="exportCustomers"
                class="bg-green-600 text-white py-2 px-4 rounded-md shadow-sm hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900 transition-colors flex items-center"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                Export Customers
              </button>
            </div>
          </div>

          <!-- Customer Stats Cards -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
            <!-- Total Customers -->
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-blue-100 dark:bg-blue-900/40 rounded-md flex items-center justify-center">
                    <svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Total Customers</p>
                  <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ customers.length }}</p>
                </div>
              </div>
            </div>

            <!-- Active Customers -->
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-green-100 dark:bg-green-900/40 rounded-md flex items-center justify-center">
                    <svg class="w-5 h-5 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Active Customers</p>
                  <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ activeCustomersCount }}</p>
                </div>
              </div>
            </div>

            <!-- Total Revenue -->
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-yellow-100 dark:bg-yellow-900/40 rounded-md flex items-center justify-center">
                    <svg class="w-5 h-5 text-yellow-600 dark:text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Total Revenue</p>
                  <p class="text-2xl font-semibold text-gray-900 dark:text-white">₹{{ totalRevenue.toLocaleString() }}</p>
                </div>
              </div>
            </div>

            <!-- Average Order Value -->
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-purple-100 dark:bg-purple-900/40 rounded-md flex items-center justify-center">
                    <svg class="w-5 h-5 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Avg Order Value</p>
                  <p class="text-2xl font-semibold text-gray-900 dark:text-white">₹{{ averageOrderValue.toLocaleString() }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Customers Table -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
            <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Search Customers</label>
                  <input
                    v-model="searchQuery"
                    type="text"
                    placeholder="Search by name, email, location..."
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Status</label>
                  <select
                    v-model="selectedStatus"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900"
                  >
                    <option value="">All Status</option>
                    <option value="active">Active</option>
                    <option value="blocked">Blocked</option>
                  </select>
                </div>

              </div>

              <div class="flex justify-end">
                <button
                  @click="clearFilters"
                  class="px-4 py-2 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 transition-colors"
                >
                  Clear Filters
                </button>
              </div>
            </div>

            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead class="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      User ID
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Name
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Date Joined
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Location
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Total Spends
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Total Orders
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
                  <tr v-for="customer in filteredCustomers" :key="customer.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                      {{ customer.userId }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <div class="flex-shrink-0 h-10 w-10">
                          <div class="h-10 w-10 rounded-full bg-gray-300 dark:bg-gray-600 flex items-center justify-center">
                            <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
                              {{ customer.name.charAt(0).toUpperCase() }}
                            </span>
                          </div>
                        </div>
                        <div class="ml-4">
                          <div class="text-sm font-medium text-gray-900 dark:text-white">{{ customer.name }}</div>
                          <div class="text-sm text-gray-500 dark:text-gray-400">{{ customer.email }}</div>
                        </div>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                      {{ formatDate(customer.dateJoined) }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                      {{ customer.location }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                      ₹{{ customer.totalSpends.toLocaleString() }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                      {{ customer.totalOrders }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span :class="[
                        'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                        getStatusClass(customer.status)
                      ]">
                        {{ customer.status }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div class="flex space-x-2">
                        <button
                          @click="toggleBlock(customer)"
                          :class="[
                            'px-3 py-1 text-xs font-medium rounded-md transition-colors',
                            customer.status === 'active' 
                              ? 'bg-red-100 text-red-800 hover:bg-red-200 dark:bg-red-900/40 dark:text-red-300 dark:hover:bg-red-900/60'
                              : 'bg-green-100 text-green-800 hover:bg-green-200 dark:bg-green-900/40 dark:text-green-300 dark:hover:bg-green-900/60'
                          ]"
                        >
                          {{ customer.status === 'active' ? 'Block' : 'Unblock' }}
                        </button>
                        <button
                          @click="deleteCustomer(customer)"
                          class="px-3 py-1 text-xs font-medium rounded-md bg-red-100 text-red-800 hover:bg-red-200 dark:bg-red-900/40 dark:text-red-300 dark:hover:bg-red-900/60 transition-colors"
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-if="filteredCustomers.length === 0" class="text-center py-12">
                <div class="text-gray-400 dark:text-gray-500 mb-4">
                  <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                  </svg>
                </div>
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No customers found</h3>
              <p class="text-gray-500 dark:text-gray-400">No customers match the current filters</p>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Delete Customer</h3>
        </div>
        <div class="px-6 py-4">
          <p class="text-gray-600 dark:text-gray-400 mb-4">
            Are you sure you want to delete "{{ customerToDelete ? customerToDelete.name : '' }}"? This action cannot be undone.
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

interface Customer {
  id: string
  userId: string
  name: string
  email: string
  dateJoined: string
  location: string
  totalSpends: number
  totalOrders: number
  status: 'active' | 'blocked'
}

const isOpen = ref(false)
const showDeleteModal = ref(false)
const customerToDelete = ref<Customer | null>(null)

// Filter states
const searchQuery = ref('')
const selectedStatus = ref('')
const selectedLocation = ref('')

// Filter options
const locations = ref(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad'])

// Sample customers data
const customers = ref<Customer[]>([
  {
    id: '1',
    userId: 'CUST001',
    name: 'Rajesh Kumar',
    email: 'rajesh.kumar@email.com',
    dateJoined: '2023-01-15',
    location: 'Mumbai',
    totalSpends: 25000,
    totalOrders: 12,
    status: 'active'
  },
  {
    id: '2',
    userId: 'CUST002',
    name: 'Priya Sharma',
    email: 'priya.sharma@email.com',
    dateJoined: '2023-02-20',
    location: 'Delhi',
    totalSpends: 18000,
    totalOrders: 8,
    status: 'active'
  },
  {
    id: '3',
    userId: 'CUST003',
    name: 'Amit Patel',
    email: 'amit.patel@email.com',
    dateJoined: '2023-03-10',
    location: 'Bangalore',
    totalSpends: 32000,
    totalOrders: 15,
    status: 'active'
  },
  {
    id: '4',
    userId: 'CUST004',
    name: 'Sneha Reddy',
    email: 'sneha.reddy@email.com',
    dateJoined: '2023-01-05',
    location: 'Chennai',
    totalSpends: 12000,
    totalOrders: 6,
    status: 'blocked'
  },
  {
    id: '5',
    userId: 'CUST005',
    name: 'Vikram Singh',
    email: 'vikram.singh@email.com',
    dateJoined: '2023-04-12',
    location: 'Kolkata',
    totalSpends: 45000,
    totalOrders: 20,
    status: 'active'
  },
  {
    id: '6',
    userId: 'CUST006',
    name: 'Anita Desai',
    email: 'anita.desai@email.com',
    dateJoined: '2023-02-28',
    location: 'Hyderabad',
    totalSpends: 15000,
    totalOrders: 7,
    status: 'active'
  },
  {
    id: '7',
    userId: 'CUST007',
    name: 'Rohit Agarwal',
    email: 'rohit.agarwal@email.com',
    dateJoined: '2023-03-25',
    location: 'Pune',
    totalSpends: 8000,
    totalOrders: 4,
    status: 'blocked'
  },
  {
    id: '8',
    userId: 'CUST008',
    name: 'Kavita Joshi',
    email: 'kavita.joshi@email.com',
    dateJoined: '2023-01-30',
    location: 'Ahmedabad',
    totalSpends: 28000,
    totalOrders: 14,
    status: 'active'
  }
])

// Computed properties
const activeCustomersCount = computed(() => {
  return customers.value.filter(customer => customer.status === 'active').length
})

const totalRevenue = computed(() => {
  return customers.value.reduce((total, customer) => total + customer.totalSpends, 0)
})

const averageOrderValue = computed(() => {
  const totalOrders = customers.value.reduce((total, customer) => total + customer.totalOrders, 0)
  return totalOrders > 0 ? Math.round(totalRevenue.value / totalOrders) : 0
})

const filteredCustomers = computed(() => {
  let filtered = customers.value

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(customer => 
      customer.name.toLowerCase().includes(query) ||
      customer.email.toLowerCase().includes(query) ||
      customer.location.toLowerCase().includes(query) ||
      customer.userId.toLowerCase().includes(query)
    )
  }

  // Status filter
  if (selectedStatus.value) {
    filtered = filtered.filter(customer => customer.status === selectedStatus.value)
  }

  // Location filter
  if (selectedLocation.value) {
    filtered = filtered.filter(customer => customer.location === selectedLocation.value)
  }

  return filtered
})

// Methods
const getStatusClass = (status: string) => {
  const classes = {
    active: 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300',
    blocked: 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300'
  }
  return classes[status as keyof typeof classes] || 'bg-gray-100 text-gray-800 dark:bg-gray-900/40 dark:text-gray-300'
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedStatus.value = ''
  selectedLocation.value = ''
}

const toggleBlock = (customer: Customer) => {
  customer.status = customer.status === 'active' ? 'blocked' : 'active'
}

const deleteCustomer = (customer: Customer) => {
  customerToDelete.value = customer
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  customerToDelete.value = null
}

const confirmDelete = () => {
  if (customerToDelete.value) {
    const index = customers.value.findIndex(customer => customer.id === customerToDelete.value!.id)
    if (index !== -1) {
      customers.value.splice(index, 1)
    }
  }
  closeDeleteModal()
}

const exportCustomers = () => {
  // Create CSV content
  const headers = ['User ID', 'Name', 'Email', 'Date Joined', 'Location', 'Total Spends', 'Total Orders', 'Status']
  const csvContent = [
    headers.join(','),
    ...customers.value.map(customer => [
      customer.userId,
      `"${customer.name}"`,
      `"${customer.email}"`,
      customer.dateJoined,
      `"${customer.location}"`,
      customer.totalSpends,
      customer.totalOrders,
      customer.status
    ].join(','))
  ].join('\n')

  // Create and download file
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.setAttribute('href', url)
  link.setAttribute('download', `customers_${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
</script>
