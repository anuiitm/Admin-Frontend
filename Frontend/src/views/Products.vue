<template>
  <div class="flex min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100">
    <Sidebar :isOpen="isOpen" @close="isOpen = false" />

    <div class="flex-1 flex flex-col md:ml-64">
      <Navbar @toggle-sidebar="isOpen = !isOpen" />

      <main class="w-full py-8 px-4 sm:px-6 lg:px-8">
        <div class="space-y-8 max-w-6xl ml-4">
          <div class="mb-8 flex justify-between items-center">
            <div>
              <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Products</h1>
              <p class="mt-2 text-gray-600 dark:text-gray-400">Manage your product catalog</p>
            </div>
            <div>
              <button
                v-if="!showAddProductPage"
                @click="showAddProductPage = true"
                class="bg-blue-600 text-white py-2 px-4 rounded-md shadow-sm hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900 transition-colors flex items-center"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                </svg>
                Add Product
              </button>
            </div>
          </div>

          <AddProduct
            v-if="showAddProductPage"
            :categories="categories"
            @close="showAddProductPage = false"
            @product-saved="handleProductSaved"
          />
          
          <div v-else>
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
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Category</label>
                    <select
                      v-model="selectedCategory"
                      class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900"
                    >
                      <option value="">All Categories</option>
                      <option v-for="category in categories" :key="category" :value="category">{{ category }}</option>
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
                        Tags
                      </th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                        SKU
                      </th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                        Price
                      </th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                        Stock
                      </th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                        Category
                      </th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                        Pet Type
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
                    <tr v-for="product in filteredProducts" :key="product.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                      <td class="px-6 py-4 whitespace-nowrap">
                        <img v-if="product.image" :src="product.image.startsWith('http') ? product.image : `http://localhost:5001${product.image}`" :alt="product.name" class="h-12 w-12 rounded-lg object-cover" />
                        <div v-else class="h-12 w-12 rounded-lg bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
                          <span class="text-xs text-gray-500 dark:text-gray-400">No image</span>
                        </div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm font-medium text-gray-900 dark:text-white">{{ product.name }}</div>
                        <div class="text-sm text-gray-500 dark:text-gray-400">{{ product.description }}</div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="flex flex-wrap gap-1">
                          <span
                            v-for="tag in product.tags"
                            :key="tag"
                            class="inline-flex px-2 py-1 text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-full"
                          >
                            {{ tag }}
                          </span>
                        </div>
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
                          getStatusClass(product.status)
                        ]">
                          {{ product.status }}
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div class="flex space-x-2">
                          <button
                            @click="viewProduct(product)"
                            class="text-blue-600 dark:text-blue-400 hover:text-blue-900 dark:hover:text-blue-300"
                          >
                            View
                          </button>
                          <button
                            @click="editProduct(product)"
                            class="text-green-600 dark:text-green-400 hover:text-green-900 dark:hover:text-green-300"
                          >
                            Edit
                          </button>
                          <button
                            @click="deleteProduct(product)"
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
        </div>
      </main>
    </div>

    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-screen overflow-y-auto">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Edit Product</h3>
          <button @click="closeEditModal" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        <div class="px-6 py-4">
          <div v-if="editingProduct" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Name</label>
                <input v-model="editingProduct.name" type="text" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">SKU</label>
                <input v-model="editingProduct.sku" type="text" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Price</label>
                <input v-model.number="editingProduct.price" type="number" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Stock</label>
                <input v-model.number="editingProduct.stock" type="number" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Category</label>
                <select v-model="editingProduct.category" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
                  <option v-for="category in categories" :key="category" :value="category">{{ category }}</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Pet Type</label>
                <select v-model="editingProduct.petType" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
                  <option v-for="petType in petTypes" :key="petType" :value="petType">{{ petType }}</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Status</label>
                <select v-model="editingProduct.status" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                  <option value="discontinued">Discontinued</option>
                </select>
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Description</label>
              <textarea v-model="editingProduct.description" rows="3" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900"></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Tags (comma separated)</label>
              <input v-model="tagsInput" type="text" placeholder="premium, organic, bestseller" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Product Image</label>
              <input
                type="file"
                accept="image/*"
                @change="handleImageUpload"
                class="w-full text-gray-900 dark:text-white"
              />
              <div v-if="imagePreview" class="mt-2">
                <img
                  :src="imagePreview"
                  alt="Preview"
                  class="w-32 h-32 object-cover rounded-md border border-gray-300 dark:border-gray-600"
                />
              </div>
            </div>
            <div class="flex space-x-3 pt-4">
              <button @click="saveProduct" class="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors">
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

    <!-- View Product Modal -->
    <div v-if="showViewModal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-96 overflow-y-auto">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Product Details</h3>
          <button @click="closeViewModal" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        <div class="px-6 py-4">
          <div v-if="selectedProduct" class="space-y-4">
            <div class="flex items-start space-x-4">
              <img :src="selectedProduct.image" :alt="selectedProduct.name" class="w-20 h-20 rounded-lg object-cover" />
              <div class="flex-1">
                <h4 class="text-xl font-semibold text-gray-900 dark:text-white">{{ selectedProduct.name }}</h4>
                <p class="text-gray-600 dark:text-gray-400 mt-1">{{ selectedProduct.description }}</p>
                <div class="flex items-center space-x-4 mt-2">
                  <span class="text-2xl font-bold text-gray-900 dark:text-white">₹{{ selectedProduct.price.toLocaleString() }}</span>
                  <span :class="[
                    'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                    getStockClass(selectedProduct.stock)
                  ]">
                    {{ selectedProduct.stock }} in stock
                  </span>
                </div>
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200 dark:border-gray-700">
              <div>
                <label class="text-sm font-medium text-gray-500 dark:text-gray-400">SKU</label>
                <p class="text-lg text-gray-900 dark:text-white">{{ selectedProduct.sku }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500 dark:text-gray-400">Category</label>
                <p class="text-lg text-gray-900 dark:text-white">{{ selectedProduct.category }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500 dark:text-gray-400">Pet Type</label>
                <p class="text-lg text-gray-900 dark:text-white">{{ selectedProduct.petType }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500 dark:text-gray-400">Status</label>
                <span :class="[
                  'inline-flex px-3 py-1 text-sm font-semibold rounded-full',
                  getStatusClass(selectedProduct.status)
                ]">
                  {{ selectedProduct.status }}
                </span>
              </div>
            </div>
            
            <div class="pt-4 border-t border-gray-200 dark:border-gray-700">
              <label class="text-sm font-medium text-gray-500 dark:text-gray-400">Tags</label>
              <div class="flex flex-wrap gap-2 mt-2">
                <span
                  v-for="tag in selectedProduct.tags"
                  :key="tag"
                  class="inline-flex px-2 py-1 text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-full"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Delete Product</h3>
        </div>
        <div class="px-6 py-4">
          <p class="text-gray-600 dark:text-gray-400 mb-4">
            Are you sure you want to delete "{{ productToDelete ? productToDelete.name : '' }}"? This action cannot be undone.
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
import { ref, computed, onMounted } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import Navbar from '@/components/Navbar.vue'
import AddProduct from '@/views/AddProduct.vue'
import { useApi } from '@/composables/useApi'

interface Product {
  id: string
  name: string
  description: string
  image: string
  tags: string[]
  sku: string
  price: number
  stock: number
  category: string
  petType: string
  status: string
}

// type NewProduct = Omit<Product, 'id' | 'image'>

const isOpen = ref(false)
const showAddProductPage = ref(false) // // Filter states
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedPetType = ref('')
const selectedStockStatus = ref('')

// Modal states
const showEditModal = ref(false)
const showViewModal = ref(false)
const showDeleteModal = ref(false)
const editingProduct = ref<Product | null>(null)
const selectedProduct = ref<Product | null>(null)
const productToDelete = ref<Product | null>(null)
const tagsInput = ref('')
const imageFile = ref<File | null>(null)
const imagePreview = ref<string | null>(null)

// Filter options
const categories = ref(['Food', 'Toys', 'Accessories', 'Health', 'Grooming', 'Beds'])
const petTypes = ref(['Dog', 'Cat', 'Bird', 'Fish', 'Rabbit', 'Hamster'])

// Products data (start empty; to be populated from API)
const products = ref<Product[]>([])
const api = useApi()

// Computed properties
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

const getStatusClass = (status: string) => {
  const classes = {
    active: 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300',
    inactive: 'bg-gray-100 text-gray-800 dark:bg-gray-900/40 dark:text-gray-300',
    discontinued: 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300'
  }
  return classes[status as keyof typeof classes] || 'bg-gray-100 text-gray-800 dark:bg-gray-900/40 dark:text-gray-300'
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = ''
  selectedPetType.value = ''
  selectedStockStatus.value = ''
}

const editProduct = (product: Product) => {
  // Create a deep copy to prevent modal changes from affecting the list before saving
  editingProduct.value = {
    id: product.id,
    name: product.name,
    description: product.description,
    image: product.image, 
    tags: [...product.tags],
    sku: product.sku,
    price: product.price,
    stock: product.stock,
    category: product.category,
    petType: product.petType,
    status: product.status
  }
  imagePreview.value = product.image
  imageFile.value = null
  tagsInput.value = product.tags.join(', ')
  showEditModal.value = true
}

const handleImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    imageFile.value = target.files[0]
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target?.result as string
    }
    reader.readAsDataURL(imageFile.value)
  }
}

const closeEditModal = () => {
  showEditModal.value = false
  editingProduct.value = null
  tagsInput.value = ''
}

// View Product functionality
const viewProduct = (product: Product) => {
  selectedProduct.value = product
  showViewModal.value = true
}

const closeViewModal = () => {
  showViewModal.value = false
  selectedProduct.value = null
}

// Delete Product functionality
const deleteProduct = (product: Product) => {
  productToDelete.value = product
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  productToDelete.value = null
}

const confirmDelete = () => {
  if (productToDelete.value) {
    const index = products.value.findIndex(product => product.id === productToDelete.value!.id)
    if (index !== -1) {
      products.value.splice(index, 1)
    }
  }
  closeDeleteModal()
}

const saveProduct = () => {
  if (editingProduct.value) {
    const index = products.value.findIndex(product => product.id === editingProduct.value!.id)
    if (index !== -1) {
      // Update tags from input
      editingProduct.value.tags = tagsInput.value.split(',').map(tag => tag.trim()).filter(tag => tag)
      editingProduct.value.image = imageFile.value ? URL.createObjectURL(imageFile.value) : editingProduct.value.image
      products.value[index] = { ...editingProduct.value }
    }
  }
  closeEditModal()
}

type NewProduct = Omit<Product, 'id' | 'image'> & { image?: File | null  }

const handleProductSaved = async (_newProduct: NewProduct) => {
  showAddProductPage.value = false
  // Refresh from API to reflect DB
  try {
    const data = await api.get<any[]>(`/products`)
    products.value = data.map(p => ({
      id: String(p.product_id),
      name: p.name,
      description: p.description || '',
      image: p.main_image_url ? (p.main_image_url.startsWith('http') ? p.main_image_url : `http://localhost:5001${p.main_image_url}`) : '',
      tags: (p.tags ? String(p.tags).split(',').map((t: string) => t.trim()).filter(Boolean) : []),
      sku: p.sku,
      price: p.price,
      stock: p.stock,
      category: p.category_name || '',
      petType: p.pet_type || '',
      status: p.status || 'active',
    }))
  } catch (e) { /* noop */ }
}

onMounted(async () => {
  try {
    const data = await api.get<any[]>(`/products`)
    products.value = data.map(p => ({
      id: String(p.product_id),
      name: p.name,
      description: p.description || '',
      image: p.main_image_url ? (p.main_image_url.startsWith('http') ? p.main_image_url : `http://localhost:5001${p.main_image_url}`) : '',
      tags: (p.tags ? String(p.tags).split(',').map((t: string) => t.trim()).filter(Boolean) : []),
      sku: p.sku,
      price: p.price,
      stock: p.stock,
      category: p.category_name || '',
      petType: p.pet_type || '',
      status: p.status || 'active',
    }))
  } catch (e) { /* noop */ }
})
</script>