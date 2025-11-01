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
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Search Results</h1>
            <p class="mt-2 text-gray-600 dark:text-gray-400">
              {{ searchQuery ? `Results for "${searchQuery}"` : 'Search across all entities' }}
            </p>
          </div>

          <!-- Search Filters -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Search Query</label>
                <input
                  v-model="searchQuery"
                  @keyup.enter="performSearch"
                  type="text"
                  placeholder="Search products, customers, orders..."
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Entity Type</label>
                <select
                  v-model="selectedEntity"
                  @change="performSearch"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900"
                >
                  <option value="all">All Entities</option>
                  <option value="products">Products</option>
                  <option value="customers">Customers</option>
                  <option value="orders">Orders</option>
                </select>
              </div>

              <div class="flex items-end">
                <button
                  @click="performSearch"
                  class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors flex items-center justify-center"
                >
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                  </svg>
                  Search
                </button>
              </div>
            </div>
          </div>

          <!-- Results Summary -->
          <div v-if="hasSearched" class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-4">
                <span class="text-sm text-gray-600 dark:text-gray-400">
                  Found {{ totalResults }} results
                </span>
                <div class="flex space-x-2">
                  <span v-if="productResults.length > 0" class="px-2 py-1 bg-blue-100 dark:bg-blue-900/40 text-blue-800 dark:text-blue-300 text-xs rounded-full">
                    {{ productResults.length }} Products
                  </span>
                  <span v-if="customerResults.length > 0" class="px-2 py-1 bg-green-100 dark:bg-green-900/40 text-green-800 dark:text-green-300 text-xs rounded-full">
                    {{ customerResults.length }} Customers
                  </span>
                  <span v-if="orderResults.length > 0" class="px-2 py-1 bg-purple-100 dark:bg-purple-900/40 text-purple-800 dark:text-purple-300 text-xs rounded-full">
                    {{ orderResults.length }} Orders
                  </span>
                </div>
              </div>
              <button
                @click="clearSearch"
                class="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200"
              >
                Clear Search
              </button>
            </div>
          </div>

          <!-- Search Results -->
          <div v-if="hasSearched" class="space-y-6">
            <!-- Products Results -->
            <div v-if="productResults.length > 0 && (selectedEntity === 'all' || selectedEntity === 'products')" class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
              <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                  <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                  </svg>
                  Products ({{ productResults.length }})
                </h3>
              </div>
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                  <thead class="bg-gray-50 dark:bg-gray-700">
                    <tr>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Image</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Name</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">SKU</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Price</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Stock</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Status</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Actions</th>
                    </tr>
                  </thead>
                  <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                    <tr v-for="product in productResults" :key="product.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                      <td class="px-6 py-4 whitespace-nowrap">
                        <img :src="product.image" :alt="product.name" class="h-12 w-12 rounded-lg object-cover" />
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm font-medium text-gray-900 dark:text-white">{{ product.name }}</div>
                        <div class="text-sm text-gray-500 dark:text-gray-400">{{ product.description }}</div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">{{ product.sku }}</td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">₹{{ product.price.toLocaleString() }}</td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span :class="[
                          'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                          getStockClass(product.stock)
                        ]">
                          {{ product.stock }}
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span :class="[
                          'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                          getStatusClass(product.status)
                        ]">
                          {{ product.status }}
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div class="flex space-x-2">
                          <button @click="viewProduct(product)" class="text-blue-600 dark:text-blue-400 hover:text-blue-900 dark:hover:text-blue-300">View</button>
                          <button @click="editProduct(product)" class="text-green-600 dark:text-green-400 hover:text-green-900 dark:hover:text-green-300">Edit</button>
                          <button @click="deleteProduct(product)" class="text-red-600 dark:text-red-400 hover:text-red-900 dark:hover:text-red-300">Delete</button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Customers Results -->
            <div v-if="customerResults.length > 0 && (selectedEntity === 'all' || selectedEntity === 'customers')" class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
              <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                  <svg class="w-5 h-5 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                  </svg>
                  Customers ({{ customerResults.length }})
                </h3>
              </div>
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                  <thead class="bg-gray-50 dark:bg-gray-700">
                    <tr>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Name</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Email</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Location</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Total Spends</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Orders</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Status</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Actions</th>
                    </tr>
                  </thead>
                  <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                    <tr v-for="customer in customerResults" :key="customer.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
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
                            <div class="text-sm text-gray-500 dark:text-gray-400">{{ customer.userId }}</div>
                          </div>
                        </div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">{{ customer.email }}</td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">{{ customer.location }}</td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">₹{{ customer.totalSpends.toLocaleString() }}</td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">{{ customer.totalOrders }}</td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span :class="[
                          'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                          getCustomerStatusClass(customer.status)
                        ]">
                          {{ customer.status }}
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div class="flex space-x-2">
                          <button @click="viewCustomer(customer)" class="text-blue-600 dark:text-blue-400 hover:text-blue-900 dark:hover:text-blue-300">View</button>
                          <button @click="toggleBlockCustomer(customer)" :class="[
                            'px-2 py-1 text-xs font-medium rounded-md transition-colors',
                            customer.status === 'active' 
                              ? 'bg-red-100 text-red-800 hover:bg-red-200 dark:bg-red-900/40 dark:text-red-300 dark:hover:bg-red-900/60'
                              : 'bg-green-100 text-green-800 hover:bg-green-200 dark:bg-green-900/40 dark:text-green-300 dark:hover:bg-green-900/60'
                          ]">
                            {{ customer.status === 'active' ? 'Block' : 'Unblock' }}
                          </button>
                          <button @click="deleteCustomer(customer)" class="text-red-600 dark:text-red-400 hover:text-red-900 dark:hover:text-red-300">Delete</button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Orders Results -->
            <div v-if="orderResults.length > 0 && (selectedEntity === 'all' || selectedEntity === 'orders')" class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
              <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                  <svg class="w-5 h-5 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                  </svg>
                  Orders ({{ orderResults.length }})
                </h3>
              </div>
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                  <thead class="bg-gray-50 dark:bg-gray-700">
                    <tr>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Order ID</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Date</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Customer</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Total</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Status</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Actions</th>
                    </tr>
                  </thead>
                  <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                    <tr v-for="order in orderResults" :key="order.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">#{{ order.id }}</td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{{ order.date }}</td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">{{ order.customer }}</td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">₹{{ order.total.toLocaleString() }}</td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span :class="[
                          'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                          getOrderStatusClass(order.status)
                        ]">
                          {{ order.status }}
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div class="flex space-x-2">
                          <button @click="viewOrder(order)" class="text-blue-600 dark:text-blue-400 hover:text-blue-900 dark:hover:text-blue-300">View</button>
                          <button @click="editOrder(order)" class="text-green-600 dark:text-green-400 hover:text-green-900 dark:hover:text-green-300">Edit</button>
                          <button @click="deleteOrder(order)" class="text-red-600 dark:text-red-400 hover:text-red-900 dark:hover:text-red-300">Delete</button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- No Results -->
            <div v-if="hasSearched && totalResults === 0" class="text-center py-12">
              <div class="text-gray-400 dark:text-gray-500 mb-4">
                <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
              </div>
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No results found</h3>
              <p class="text-gray-500 dark:text-gray-400">Try adjusting your search terms or filters</p>
            </div>
          </div>

          <!-- Initial State -->
          <div v-else class="text-center py-12">
            <div class="text-gray-400 dark:text-gray-500 mb-4">
              <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </div>
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">Start your search</h3>
            <p class="text-gray-500 dark:text-gray-400">Search across products, customers, and orders</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import Navbar from '@/components/Navbar.vue'

// Interfaces
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
  tags: string[]
}

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

interface Order {
  id: string
  date: string
  customer: string
  total: number
  status: string
}

// Reactive data
const isOpen = ref(false)
const searchQuery = ref('')
const selectedEntity = ref('all')
const hasSearched = ref(false)

// Sample data (in a real app, this would come from an API)
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
    status: 'active',
    tags: ['premium', 'nutrition', 'adult']
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
    status: 'active',
    tags: ['scratching', 'durable', 'indoor']
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
    status: 'active',
    tags: ['aquarium', 'complete', 'fish']
  },
  {
    id: '4',
    name: 'Dog Leash',
    description: 'Strong and comfortable dog leash',
    image: 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=100&h=100&fit=crop&crop=center',
    sku: 'DOG-LEASH-001',
    price: 300,
    stock: 8,
    category: 'Accessories',
    petType: 'Dog',
    status: 'active',
    tags: ['leash', 'strong', 'comfortable']
  },
  {
    id: '5',
    name: 'Cat Health Supplements',
    description: 'Essential vitamins for cat health',
    image: 'https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=100&h=100&fit=crop&crop=center',
    sku: 'CAT-HEALTH-001',
    price: 600,
    stock: 25,
    category: 'Health',
    petType: 'Cat',
    status: 'active',
    tags: ['health', 'vitamins', 'supplements']
  },
  {
    id: '6',
    name: 'Bird Cage',
    description: 'Spacious cage for small birds',
    image: 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=100&h=100&fit=crop&crop=center',
    sku: 'BIRD-CAGE-001',
    price: 1500,
    stock: 7,
    category: 'Accessories',
    petType: 'Bird',
    status: 'active',
    tags: ['cage', 'spacious', 'birds']
  },
  {
    id: '7',
    name: 'Bird Seed Mix',
    description: 'Premium seed mix for all types of birds',
    image: 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=100&h=100&fit=crop&crop=center',
    sku: 'BIRD-FOOD-001',
    price: 450,
    stock: 20,
    category: 'Food',
    petType: 'Bird',
    status: 'active',
    tags: ['seeds', 'premium', 'nutrition']
  },
  {
    id: '8',
    name: 'Bird Perch Set',
    description: 'Natural wood perches for bird cages',
    image: 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=100&h=100&fit=crop&crop=center',
    sku: 'BIRD-PERCH-001',
    price: 200,
    stock: 15,
    category: 'Accessories',
    petType: 'Bird',
    status: 'active',
    tags: ['perch', 'wood', 'natural']
  }
])

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
    status: 'blocked'
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
  }
])

const orders = ref<Order[]>([
  {
    id: '1234',
    date: '2025-09-15',
    customer: 'John Doe',
    total: 2500,
    status: 'processing'
  },
  {
    id: '1235',
    date: '2025-09-14',
    customer: 'Jane Smith',
    total: 1800,
    status: 'shipped'
  },
  {
    id: '1236',
    date: '2025-09-13',
    customer: 'Mike Johnson',
    total: 3200,
    status: 'completed'
  },
  {
    id: '1237',
    date: '2025-09-12',
    customer: 'Sarah Wilson',
    total: 1500,
    status: 'cancelled'
  },
  {
    id: '1238',
    date: '2025-09-11',
    customer: 'David Brown',
    total: 2800,
    status: 'processing'
  }
])

// Search results
const productResults = ref<Product[]>([])
const customerResults = ref<Customer[]>([])
const orderResults = ref<Order[]>([])

// Computed properties
const totalResults = computed(() => {
  return productResults.value.length + customerResults.value.length + orderResults.value.length
})

// Methods
const performSearch = () => {
  if (!searchQuery.value.trim()) {
    hasSearched.value = false
    productResults.value = []
    customerResults.value = []
    orderResults.value = []
    return
  }

  hasSearched.value = true
  const query = searchQuery.value.toLowerCase()

  // Search products
  if (selectedEntity.value === 'all' || selectedEntity.value === 'products') {
    productResults.value = products.value.filter(product =>
      product.name.toLowerCase().includes(query) ||
      product.description.toLowerCase().includes(query) ||
      product.sku.toLowerCase().includes(query) ||
      product.category.toLowerCase().includes(query) ||
      product.petType.toLowerCase().includes(query) ||
      product.tags.some(tag => tag.toLowerCase().includes(query))
    )
  } else {
    productResults.value = []
  }

  // Search customers
  if (selectedEntity.value === 'all' || selectedEntity.value === 'customers') {
    customerResults.value = customers.value.filter(customer =>
      customer.name.toLowerCase().includes(query) ||
      customer.email.toLowerCase().includes(query) ||
      customer.userId.toLowerCase().includes(query) ||
      customer.location.toLowerCase().includes(query)
    )
  } else {
    customerResults.value = []
  }

  // Search orders
  if (selectedEntity.value === 'all' || selectedEntity.value === 'orders') {
    orderResults.value = orders.value.filter(order =>
      order.id.toLowerCase().includes(query) ||
      order.customer.toLowerCase().includes(query) ||
      order.status.toLowerCase().includes(query)
    )
  } else {
    orderResults.value = []
  }

  // Update URL
  updateURL()
}

const updateURL = () => {
  const queryParams: any = {}
  if (searchQuery.value.trim()) {
    queryParams.q = searchQuery.value
  }
  if (selectedEntity.value !== 'all') {
    queryParams.entity = selectedEntity.value
  }
  
  router.replace({ 
    name: 'SearchResults', 
    query: queryParams 
  })
}

const clearSearch = () => {
  searchQuery.value = ''
  selectedEntity.value = 'all'
  hasSearched.value = false
  productResults.value = []
  customerResults.value = []
  orderResults.value = []
  updateURL()
}

// Status classes
const getStockClass = (stock: number) => {
  if (stock === 0) return 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300'
  if (stock <= 10) return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300'
  return 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300'
}

const getStatusClass = (status: string) => {
  const classes = {
    active: 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300',
    inactive: 'bg-gray-100 text-gray-800 dark:bg-gray-900/40 dark:text-gray-300',
    discontinued: 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300'
  }
  return classes[status as keyof typeof classes] || 'bg-gray-100 text-gray-800 dark:bg-gray-900/40 dark:text-gray-300'
}

const getCustomerStatusClass = (status: string) => {
  const classes = {
    active: 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300',
    blocked: 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300'
  }
  return classes[status as keyof typeof classes] || 'bg-gray-100 text-gray-800 dark:bg-gray-900/40 dark:text-gray-300'
}

const getOrderStatusClass = (status: string) => {
  const classes = {
    processing: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300',
    shipped: 'bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300',
    completed: 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300',
    cancelled: 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300'
  }
  return classes[status as keyof typeof classes] || 'bg-gray-100 text-gray-800 dark:bg-gray-900/40 dark:text-gray-300'
}

// Action methods
const viewProduct = (product: Product) => {
  // Navigate to products page with specific product
  router.push({ name: 'products', query: { view: product.id } })
}

const editProduct = (product: Product) => {
  // Navigate to products page with edit mode
  router.push({ name: 'products', query: { edit: product.id } })
}

const deleteProduct = (product: Product) => {
  // Show confirmation and delete
  if (confirm(`Are you sure you want to delete "${product.name}"?`)) {
    const index = products.value.findIndex(p => p.id === product.id)
    if (index !== -1) {
      products.value.splice(index, 1)
      performSearch() // Refresh search results
    }
  }
}

const viewCustomer = (customer: Customer) => {
  // Navigate to customers page with specific customer
  router.push({ name: 'customers', query: { view: customer.id } })
}

const toggleBlockCustomer = (customer: Customer) => {
  customer.status = customer.status === 'active' ? 'blocked' : 'active'
  performSearch() // Refresh search results
}

const deleteCustomer = (customer: Customer) => {
  // Show confirmation and delete
  if (confirm(`Are you sure you want to delete customer "${customer.name}"?`)) {
    const index = customers.value.findIndex(c => c.id === customer.id)
    if (index !== -1) {
      customers.value.splice(index, 1)
      performSearch() // Refresh search results
    }
  }
}

const viewOrder = (order: Order) => {
  // Navigate to orders page with specific order
  router.push({ name: 'orders', query: { view: order.id } })
}

const editOrder = (order: Order) => {
  // Navigate to orders page with edit mode
  router.push({ name: 'orders', query: { edit: order.id } })
}

const deleteOrder = (order: Order) => {
  // Show confirmation and delete
  if (confirm(`Are you sure you want to delete order #${order.id}?`)) {
    const index = orders.value.findIndex(o => o.id === order.id)
    if (index !== -1) {
      orders.value.splice(index, 1)
      performSearch() // Refresh search results
    }
  }
}

// Initialize search from URL query
const route = useRoute()
const router = useRouter()

// Watchers
watch(() => route.query, (newQuery) => {
  if (newQuery.q) {
    searchQuery.value = newQuery.q as string
  } else {
    searchQuery.value = ''
  }
  
  if (newQuery.entity) {
    selectedEntity.value = newQuery.entity as string
  } else {
    selectedEntity.value = 'all'
  }
  
  if (searchQuery.value) {
    performSearch()
  } else {
    hasSearched.value = false
    productResults.value = []
    customerResults.value = []
    orderResults.value = []
  }
}, { immediate: true })

onMounted(() => {
  if (route.query.q) {
    searchQuery.value = route.query.q as string
  }
  if (route.query.entity) {
    selectedEntity.value = route.query.entity as string
  }
  if (searchQuery.value) {
    performSearch()
  }
})
</script>