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
              <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Inventory</h1>
              <p class="mt-2 text-gray-600 dark:text-gray-400">Track and manage your inventory</p>
            </div>
            <div>
              <button
                @click="showUpdateModal = true"
                class="bg-blue-600 text-white py-2 px-4 rounded-md shadow-sm hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900 transition-colors flex items-center"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                </svg>
                Update Inventory
              </button>
            </div>
          </div>

          <!-- Inventory Stats Cards -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Total Inventory Value -->
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-blue-100 dark:bg-blue-900/40 rounded-md flex items-center justify-center">
                    <svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Total Inventory Value</p>
                  <p class="text-2xl font-semibold text-gray-900 dark:text-white">₹{{ totalInventoryValue.toLocaleString() }}</p>
                </div>
              </div>
            </div>

            <!-- Low Stock Items -->
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-yellow-100 dark:bg-yellow-900/40 rounded-md flex items-center justify-center">
                    <svg class="w-5 h-5 text-yellow-600 dark:text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Low Stock Items</p>
                  <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ lowStockCount }}</p>
                </div>
              </div>
            </div>

            <!-- Out of Stock Items -->
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-red-100 dark:bg-red-900/40 rounded-md flex items-center justify-center">
                    <svg class="w-5 h-5 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Out of Stock</p>
                  <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ outOfStockCount }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Inventory Table -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
            <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Search Products</label>
                  <input
                    v-model="searchQuery"
                    type="text"
                    placeholder="Search by name, SKU..."
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Stock Status</label>
                  <select
                    v-model="selectedStockStatus"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900"
                  >
                    <option value="">All Stock Status</option>
                    <option value="in-stock">In Stock</option>
                    <option value="low-stock">Low Stock</option>
                    <option value="out-of-stock">Out of Stock</option>
                  </select>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Pet Type</label>
                  <select
                    v-model="selectedPetType"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900"
                  >
                    <option value="">All Pet Types</option>
                    <option v-for="petType in petTypes" :key="petType" :value="petType">{{ petType }}</option>
                  </select>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Category</label>
                  <select
                    v-model="selectedCategory"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900"
                  >
                    <option value="">All Categories</option>
                    <option v-for="category in categories" :key="category" :value="category">{{ category }}</option>
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
                      Image
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Name
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      SKU
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Price
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Current Stock
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Category
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Pet Type
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Stock Status
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  <tr v-for="product in filteredProducts" :key="product.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <img :src="product.image" :alt="product.name" class="h-12 w-12 rounded-lg object-cover" />
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm font-medium text-gray-900 dark:text-white">{{ product.name }}</div>
                      <div class="text-sm text-gray-500 dark:text-gray-400">{{ product.description }}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                      {{ product.sku }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                      ₹{{ product.price.toLocaleString() }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span :class="[
                        'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                        getStockClass(product.stock)
                      ]">
                        {{ product.stock }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                      {{ product.category }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                      {{ product.petType }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span :class="[
                        'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                        getStockStatusClass(product.stock)
                      ]">
                        {{ getStockStatus(product.stock) }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div class="flex space-x-2">
                        <button
                          @click="updateStock(product)"
                          class="text-blue-600 dark:text-blue-400 hover:text-blue-900 dark:hover:text-blue-300"
                        >
                          Update Stock
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-if="filteredProducts.length === 0" class="text-center py-12">
              <div class="text-gray-400 dark:text-gray-500 mb-4">
                <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                </svg>
              </div>
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No products found</h3>
              <p class="text-gray-500 dark:text-gray-400">No products match the current filters</p>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Update Inventory Modal -->
    <div v-if="showUpdateModal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-screen overflow-y-auto">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Update Inventory</h3>
          <button @click="closeUpdateModal" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        <div class="px-6 py-4">
          <div class="space-y-4">
            <div class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-md p-4">
              <div class="flex">
                <div class="flex-shrink-0">
                  <svg class="h-5 w-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.726-1.36 3.491 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                  </svg>
                </div>
                <div class="ml-3">
                  <h3 class="text-sm font-medium text-yellow-800 dark:text-yellow-200">
                    Stock Update Notice
                  </h3>
                  <div class="mt-2 text-sm text-yellow-700 dark:text-yellow-300">
                    <p>You can only update stock quantities in this view. Other product details cannot be modified here.</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="space-y-4">
              <div v-for="product in products" :key="product.id" class="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                <div class="flex items-center space-x-4">
                  <img :src="product.image" :alt="product.name" class="h-12 w-12 rounded-lg object-cover" />
                  <div>
                    <h4 class="text-sm font-medium text-gray-900 dark:text-white">{{ product.name }}</h4>
                    <p class="text-sm text-gray-500 dark:text-gray-400">SKU: {{ product.sku }}</p>
                    <p class="text-sm text-gray-500 dark:text-gray-400">Current Stock: {{ product.stock }}</p>
                  </div>
                </div>
                <div class="flex items-center space-x-2">
                  <button
                    @click="decrementStock(product.id)"
                    class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-300 dark:hover:bg-gray-600 flex items-center justify-center"
                  >
                    -
                  </button>
                  <input
                    v-model.number="stockUpdates[product.id]"
                    type="number"
                    min="0"
                    class="w-16 px-2 py-1 text-center border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900"
                  />
                  <button
                    @click="incrementStock(product.id)"
                    class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-300 dark:hover:bg-gray-600 flex items-center justify-center"
                  >
                    +
                  </button>
                </div>
              </div>
            </div>

            <div class="flex space-x-3 pt-4">
              <button
                @click="notifyUsers"
                class="flex-1 bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors flex items-center justify-center"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5-5-5h5v-5a7.5 7.5 0 1 0-15 0v5h5l-5 5-5-5h5v-5a7.5 7.5 0 1 0 15 0v5z"></path>
                </svg>
                Notify Users
              </button>
              <button
                @click="updateInventory"
                class="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
              >
                Update Inventory
              </button>
              <button
                @click="closeUpdateModal"
                class="flex-1 bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-300 py-2 px-4 rounded-md hover:bg-gray-400 dark:hover:bg-gray-500 transition-colors"
              >
                Cancel
              </button>
            </div>
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

interface Product {
  id: string
  name: string
  description: string
  image: string
  sku: string
  price: number
  stock: number
  category: string
  petType: string
  status: string
}

const isOpen = ref(false)
const showUpdateModal = ref(false)

// Filter states
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedPetType = ref('')
const selectedStockStatus = ref('')

// Stock update tracking
const stockUpdates = ref<Record<string, number>>({})

// Filter options
const categories = ref(['Food', 'Toys', 'Accessories', 'Health', 'Grooming', 'Beds'])
const petTypes = ref(['Dog', 'Cat', 'Bird', 'Fish', 'Rabbit', 'Hamster'])

// Sample products data (same as Products page)
const products = ref<Product[]>([
  {
    id: '1',
    name: 'Premium Dog Food',
    description: 'High-quality nutrition for adult dogs',
    image: 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=100&h=100&fit=crop&crop=center',
    sku: 'DOG-FOOD-001',
    price: 1200,
    stock: 45,
    category: 'Food',
    petType: 'Dog',
    status: 'active'
  },
  {
    id: '2',
    name: 'Cat Scratching Post',
    description: 'Durable scratching post for cats',
    image: 'https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=100&h=100&fit=crop&crop=center',
    sku: 'CAT-TOY-001',
    price: 800,
    stock: 12,
    category: 'Toys',
    petType: 'Cat',
    status: 'active'
  },
  {
    id: '3',
    name: 'Aquarium Set',
    description: 'Complete aquarium setup for fish',
    image: 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=100&h=100&fit=crop&crop=center',
    sku: 'FISH-TANK-001',
    price: 2500,
    stock: 3,
    category: 'Accessories',
    petType: 'Fish',
    status: 'active'
  },
  {
    id: '4',
    name: 'Bird Cage',
    description: 'Spacious cage for small birds',
    image: 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=100&h=100&fit=crop&crop=center',
    sku: 'BIRD-CAGE-001',
    price: 1500,
    stock: 0,
    category: 'Accessories',
    petType: 'Bird',
    status: 'inactive'
  },
  {
    id: '5',
    name: 'Dog Leash',
    description: 'Strong and comfortable dog leash',
    image: 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=100&h=100&fit=crop&crop=center',
    sku: 'DOG-LEASH-001',
    price: 300,
    stock: 8,
    category: 'Accessories',
    petType: 'Dog',
    status: 'active'
  },
  {
    id: '6',
    name: 'Cat Health Supplements',
    description: 'Essential vitamins for cat health',
    image: 'https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=100&h=100&fit=crop&crop=center',
    sku: 'CAT-HEALTH-001',
    price: 600,
    stock: 25,
    category: 'Health',
    petType: 'Cat',
    status: 'active'
  }
])

// Computed properties
const totalInventoryValue = computed(() => {
  return products.value.reduce((total, product) => total + (product.price * product.stock), 0)
})

const lowStockCount = computed(() => {
  return products.value.filter(product => product.stock > 0 && product.stock <= 10).length
})

const outOfStockCount = computed(() => {
  return products.value.filter(product => product.stock === 0).length
})

const filteredProducts = computed(() => {
  let filtered = products.value

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(product => 
      product.name.toLowerCase().includes(query) ||
      product.sku.toLowerCase().includes(query) ||
      product.description.toLowerCase().includes(query)
    )
  }

  // Category filter
  if (selectedCategory.value) {
    filtered = filtered.filter(product => product.category === selectedCategory.value)
  }

  // Pet type filter
  if (selectedPetType.value) {
    filtered = filtered.filter(product => product.petType === selectedPetType.value)
  }

  // Stock status filter
  if (selectedStockStatus.value) {
    filtered = filtered.filter(product => {
      if (selectedStockStatus.value === 'in-stock') return product.stock > 10
      if (selectedStockStatus.value === 'low-stock') return product.stock > 0 && product.stock <= 10
      if (selectedStockStatus.value === 'out-of-stock') return product.stock === 0
      return true
    })
  }

  return filtered
})

// Methods
const getStockClass = (stock: number) => {
  if (stock === 0) return 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300'
  if (stock <= 10) return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300'
  return 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300'
}

const getStockStatusClass = (stock: number) => {
  if (stock === 0) return 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300'
  if (stock <= 10) return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300'
  return 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300'
}

const getStockStatus = (stock: number) => {
  if (stock === 0) return 'Out of Stock'
  if (stock <= 10) return 'Low Stock'
  return 'In Stock'
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = ''
  selectedPetType.value = ''
  selectedStockStatus.value = ''
}

const updateStock = (product: Product) => {
  stockUpdates.value[product.id] = product.stock
  showUpdateModal.value = true
}

const incrementStock = (productId: string) => {
  if (!stockUpdates.value[productId]) {
    stockUpdates.value[productId] = 0
  }
  stockUpdates.value[productId]++
}

const decrementStock = (productId: string) => {
  if (!stockUpdates.value[productId]) {
    stockUpdates.value[productId] = 0
  }
  if (stockUpdates.value[productId] > 0) {
    stockUpdates.value[productId]--
  }
}

const notifyUsers = () => {
  // In a real app, this would send notifications to users
  alert('Users have been notified about stock updates!')
}

const updateInventory = () => {
  // Update stock for all products
  Object.keys(stockUpdates.value).forEach(productId => {
    const product = products.value.find(p => p.id === productId)
    if (product) {
      product.stock = stockUpdates.value[productId]
    }
  })
  
  // Clear updates and close modal
  stockUpdates.value = {}
  showUpdateModal.value = false
  
  // Show success message
  alert('Inventory updated successfully!')
}

const closeUpdateModal = () => {
  showUpdateModal.value = false
  stockUpdates.value = {}
}
</script>
