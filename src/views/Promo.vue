<template>
  <div class="flex min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100">
    <Sidebar :isOpen="isOpen" @close="isOpen = false" />

    <div class="flex-1 flex flex-col md:ml-64">
      <Navbar @toggle-sidebar="isOpen = !isOpen" />

      <main class="w-full py-8 px-4 sm:px-6 lg:px-8">
        <div class="space-y-8 max-w-6xl ml-4">
          <div class="mb-8 flex justify-between items-center">
            <div>
              <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Promo Codes</h1>
              <p class="mt-2 text-gray-600 dark:text-gray-400">Create and manage promotional codes</p>
            </div>
            <div>
              <button
                v-if="!showAddPromoPage"
                @click="showAddPromoPage = true"
                class="bg-blue-600 text-white py-2 px-4 rounded-md shadow-sm hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900 transition-colors flex items-center"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                </svg>
                Add new Promo Code
              </button>
            </div>
          </div>

          <AddPromo
            v-if="showAddPromoPage"
            @close="showAddPromoPage = false"
            @promo-saved="handlePromoSaved"
          />

          <div v-else>
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                  <thead class="bg-gray-50 dark:bg-gray-700">
                    <tr>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                        Promo Code
                      </th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                        Code Description
                      </th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                        Discount offered
                      </th>                      
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                        Type
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
                    <tr v-for="promo in promos" :key="promo.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm font-medium text-gray-900 dark:text-white">{{ promo.code }}</div>                        
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm text-gray-500 dark:text-gray-400">{{ promo.description }}</div>
                      </td>                      
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                        {{ formatDiscount(promo) }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                        {{ promo.type }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span :class="[
                          'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                          getStatusClass(promo.status)
                        ]">
                          {{ promo.status }}
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div class="flex space-x-2">
                          <button
                            @click="viewPromo(promo)"
                            class="text-blue-600 dark:text-blue-400 hover:text-blue-900 dark:hover:text-blue-300"
                          >
                            View
                          </button>
                          <button
                            @click="editPromo(promo)"
                            class="text-green-600 dark:text-green-400 hover:text-green-900 dark:hover:text-green-300"
                          >
                            Edit
                          </button>
                          <button
                            @click="deletePromo(promo)"
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
            </div>
          </div>
        </div>
      </main>
    </div>

    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-screen overflow-y-auto">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Edit Promo Code</h3>
          <button @click="closeEditModal" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        <div class="px-6 py-4">
          <div v-if="editingPromo" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Promo Code</label>
                <input v-model="editingPromo.code" type="text" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Description</label>
                <textarea v-model="editingPromo.description" rows="3" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900"></textarea>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Discount</label>
                <input v-model.number="editingPromo.discount" type="number" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
              </div>              
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Type</label>
                <select v-model="editingPromo.type" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
                  <option v-for="t in types" :key="t" :value="t">{{ t }}</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Status</label>
                <select v-model="editingPromo.status" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                  <option value="expired">Expired</option>
                </select>
              </div>
            </div>            
            <div class="flex space-x-3 pt-4">
              <button @click="savePromo" class="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors">
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

    <!-- View Promo Modal -->
    <div v-if="showViewModal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-96 overflow-y-auto">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Promo Code Details</h3>
          <button @click="closeViewModal" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        <div class="px-6 py-4">
          <div v-if="selectedPromo" class="space-y-4">
            <div class="flex items-start space-x-4">
              <div class="flex-1">
                <h4 class="text-xl font-semibold text-gray-900 dark:text-white">{{ selectedPromo.code }}</h4>
                <p class="text-gray-600 dark:text-gray-400 mt-1">{{ selectedPromo.description }}</p>
                <div class="flex items-center space-x-4 mt-2">
                  <span class="text-2xl font-bold text-gray-900 dark:text-white">{{ formatDiscount(selectedPromo) }}</span>
                </div>
              </div>
            </div>            
            <div class="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200 dark:border-gray-700">              
              <div>
                <label class="text-sm font-medium text-gray-500 dark:text-gray-400">Type</label>
                <p class="text-lg text-gray-900 dark:text-white">{{ selectedPromo.type }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500 dark:text-gray-400">Status</label>
                <span :class="[
                  'inline-flex px-3 py-1 text-sm font-semibold rounded-full',
                  getStatusClass(selectedPromo.status)
                ]">
                  {{ selectedPromo.status }}
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
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Delete Promo Code</h3>
        </div>
        <div class="px-6 py-4">
          <p class="text-gray-600 dark:text-gray-400 mb-4">
            Are you sure you want to delete "{{ promoToDelete ? promoToDelete.code : '' }}"? This action cannot be undone.
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
import { ref } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import Navbar from '@/components/Navbar.vue'
import AddPromo from '@/views/AddPromo.vue'

interface Promo {
  id: string
  code: string
  description: string
  discount?: number
  type: string
  status: string
}

const isOpen = ref(false)
const showAddPromoPage = ref(false)

// Modal states
const showEditModal = ref(false)
const showViewModal = ref(false)
const showDeleteModal = ref(false)
const editingPromo = ref<Promo | null>(null)
const selectedPromo = ref<Promo | null>(null)
const promoToDelete = ref<Promo | null>(null)

const types = ref(['Percentage', 'Fixed', 'Free Shipping', 'Buy One Get One'])

// Sample promo data
const promos = ref<Promo[]>([
  {
    id: '1',
    code: 'SAVE10',
    description: 'Get 10% off on all products',
    discount: 10,
    type: 'Percentage',
    status: 'active'
  },
  {
    id: '2',
    code: 'FLAT200',
    description: 'Flat ₹200 off on orders above ₹1000',
    discount: 200,
    type: 'Fixed',
    status: 'active'
  },
  {
    id: '3',
    code: 'FREESHIP',
    description: 'Free shipping on all orders this week',
    discount: 0,
    type: 'Free Shipping',
    status: 'inactive'
  },
  {
    id: '4',
    code: 'BOGOFUN',
    description: 'Buy one get one free on selected pet toys',
    discount: 0,
    type: 'Buy One Get One',
    status: 'active'
  },
  {
    id: '5',
    code: 'SAVE50',
    description: '50% off clearance sale items',
    discount: 50,
    type: 'Percentage',
    status: 'expired'
  },
  {
    id: '6',
    code: 'FLAT500',
    description: '₹500 off for first-time customers',
    discount: 500,
    type: 'Fixed',
    status: 'inactive'
  }
])

// Methods
const getStatusClass = (status: string) => {
  const classes = {
    active: 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300',
    inactive: 'bg-gray-100 text-gray-800 dark:bg-gray-900/40 dark:text-gray-300',
    expired: 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300'
  }
  return classes[status as keyof typeof classes] || 'bg-gray-100 text-gray-800 dark:bg-gray-900/40 dark:text-gray-300'
}

const formatDiscount = (promo: Promo) => {
  if (promo.type === 'Percentage') return `${promo.discount}%`
  if (promo.type === 'Fixed') return `₹${promo.discount}`
  return '-'
}

const editPromo = (promo: Promo) => {
  editingPromo.value = {
    id: promo.id,
    code: promo.code,
    description: promo.description,
    discount: promo.discount,
    type: promo.type,
    status: promo.status
  }
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
  editingPromo.value = null
}

// View Promo functionality
const viewPromo = (promo: Promo) => {
  selectedPromo.value = promo
  showViewModal.value = true
}
const closeViewModal = () => {
  showViewModal.value = false
  selectedPromo.value = null
}

// Delete Promo functionality
const deletePromo = (promo: Promo) => {
  promoToDelete.value = promo
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  promoToDelete.value = null
}

const confirmDelete = () => {
  if (promoToDelete.value) {
    const index = promos.value.findIndex(promo => promo.id === promoToDelete.value!.id)
    if (index !== -1) {
      promos.value.splice(index, 1)
    }
  }
  closeDeleteModal()
}

const savePromo = () => {
  if (editingPromo.value) {
    const index = promos.value.findIndex(promo => promo.id === editingPromo.value!.id)
    if (index !== -1) {
      promos.value[index] = { ...editingPromo.value }
    }
  }
  closeEditModal()
}

type NewPromo = Omit<Promo, 'id'>

const handlePromoSaved = (newPromo: NewPromo) => {
  const promoToAdd: Promo = {
    id: `promo-${Date.now()}`,
    code: newPromo.code,
    description: newPromo.description,
    discount: newPromo.discount,
    type: newPromo.type,
    status: newPromo.status
  }
  promos.value.unshift(promoToAdd)
  showAddPromoPage.value = false
}
</script>
