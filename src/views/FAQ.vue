<template>
  <div class="flex min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100">
    <Sidebar :isOpen="isOpen" @close="isOpen = false" />

    <div class="flex-1 flex flex-col md:ml-64">
      <Navbar @toggle-sidebar="isOpen = !isOpen" />

      <main class="w-full py-8 px-4 sm:px-6 lg:px-8">
        <div class="space-y-8 max-w-6xl ml-4">
          <div class="mb-8 flex justify-between items-center">
            <div>
              <h1 class="text-3xl font-bold text-gray-900 dark:text-white">FAQ</h1>
              <p class="mt-2 text-gray-600 dark:text-gray-400">Frequently asked questions and help center</p>
            </div>
            <div>
              <button
                v-if="!showAddFAQPage"
                @click="showAddFAQPage = true"
                class="bg-blue-600 text-white py-2 px-4 rounded-md shadow-sm hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900 transition-colors flex items-center"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                </svg>
                Add New Question
              </button>
            </div>
          </div>

          <AddFAQ
            v-if="showAddFAQPage"
            @close="showAddFAQPage = false"
            @faq-saved="handleFAQSaved"
          />

          <div v-else>
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
              <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Search FAQ</label>
                    <input
                      v-model="searchQuery"
                      type="text"
                      placeholder="Search..."
                      class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Category</label>
                    <select
                      v-model="selectedCategory"
                      class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900"
                    >
                      <option value="">Question Category</option>
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
                        No.
                      </th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                        Question
                      </th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                        Answer
                      </th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                        Category
                      </th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                        Feedback
                      </th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                        Actions
                      </th>
                    </tr>
                  </thead>
                  <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                    <tr v-for="(faq, index) in filteredFAQ" :key="faq.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                      <td class="px-6 py-4 whitespace-nowrap">
                        {{ index + 1 }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm font-medium text-gray-900 dark:text-white">{{ faq.question }}</div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm text-gray-500 dark:text-gray-400">{{ faq.answer }}</div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="flex flex-wrap gap-1">
                          <span
                            v-for="category in faq.categories"
                            :key="category"
                            class="inline-flex px-2 py-1 text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-full"
                          >
                            {{ category }}
                          </span>
                        </div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                        {{ faq.feedback }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div class="flex space-x-2">
                          <button
                            @click="viewFAQ(faq)"
                            class="text-blue-600 dark:text-blue-400 hover:text-blue-900 dark:hover:text-blue-300"
                          >
                            View
                          </button>
                          <button
                            @click="editFAQ(faq)"
                            class="text-green-600 dark:text-green-400 hover:text-green-900 dark:hover:text-green-300"
                          >
                            Edit
                          </button>
                          <button
                            @click="deleteFAQ(faq)"
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

              <div v-if="filteredFAQ.length === 0" class="text-center py-12">
                <div class="text-gray-400 dark:text-gray-500 mb-4">
                  <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                  </svg>
                </div>
                <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No FAQ found</h3>
                <p class="text-gray-500 dark:text-gray-400">No Questions match the current filters</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-screen overflow-y-auto">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Edit FAQ</h3>
          <button @click="closeEditModal" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        <div class="px-6 py-4">
          <div v-if="editingFAQ" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Question</label>
                <textarea v-model="editingFAQ.question" rows="3" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white resize-none bg-white text-gray-900"></textarea>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Answer</label>
                <textarea v-model="editingFAQ.answer" rows="3" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white resize-none bg-white text-gray-900"></textarea>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Categories (comma separated)</label>
                <input v-model="categoriesInput" type="text" placeholder="General, Payments, Product" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
              </div>
            </div>
            <div class="flex space-x-3 pt-4">
              <button @click="saveFAQ" class="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors">
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

    <!-- View FAQ Modal -->
    <div v-if="showViewModal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-96 overflow-y-auto">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">FAQ</h3>
          <button @click="closeViewModal" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        <div class="px-6 py-4">
          <div v-if="selectedFAQ" class="space-y-4">
            <div class="flex items-start space-x-4">
              <div class="flex-1">
                <h4 class="text-gray-900 dark:text-gray-100 mt-1 font-semibold">Question: {{ selectedFAQ.question }}</h4>
                <div class="flex items-center space-x-4 mt-2">
                  <h4 class="text-gray-900 dark:text-gray-100 mt-1 font-semibold">Answer: {{ selectedFAQ.answer }}</h4>
                </div>
              </div>
            </div>
            
            <div class="pt-4 border-t border-gray-200 dark:border-gray-700">
              <label class="text-sm font-medium text-gray-900 dark:text-gray-100 font-semibold">Category</label>
              <div class="flex flex-wrap gap-2 mt-2">
                <span
                  v-for="category in selectedFAQ.categories"
                  :key="category"
                  class="inline-flex px-2 py-1 text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-full"
                >
                  {{ category }}
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
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Delete FAQ</h3>
        </div>
        <div class="px-6 py-4">
          <p class="text-gray-600 dark:text-gray-400 mb-4">
            Are you sure you want to delete "{{ FAQToDelete?.question }}"? This action cannot be undone.
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
import { ref, computed  } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import Navbar from '@/components/Navbar.vue'
import AddFAQ from '@/views/AddFAQ.vue'

interface FAQ {
  id: string
  question: string
  answer: string
  categories: string[]
  feedback: string
}

const isOpen = ref(false)
const showAddFAQPage = ref(false) // Filter states
const searchQuery = ref('')
const selectedCategory = ref('')

// Modal states
const showEditModal = ref(false)
const showViewModal = ref(false)
const showDeleteModal = ref(false)
const editingFAQ = ref<FAQ | null>(null)
const selectedFAQ = ref<FAQ | null>(null)
const FAQToDelete = ref<FAQ | null>(null)
const categoriesInput = ref('')

// Filter options
const categories = ref(['General', 'Product', 'Delivery', 'Discount', 'Payments'])

// Sample FAQ data
const faqs = ref<FAQ[]>([
  {
    id: '1',
    question: "How can I reset my password?",
    answer: "Click on 'Forgot Password' on the login screen and follow the instructions to reset your password.",
    categories: ['General'],
    feedback: 'helpful'
  },
  {
    id: '2',
    question: "How do I request a refund?",
    answer: "To request a refund, go to your Orders page, select the item, and click ‘Request Refund’.",
    categories: ['Payments'],
    feedback: 'helpful'
  }
])

// Computed properties
const filteredFAQ = computed(() => {
  let filtered = faqs.value

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(faq => 
      faq.question.toLowerCase().includes(query) ||
      faq.answer.toLowerCase().includes(query)
    )
  }

  // Category filter
  if (selectedCategory.value) {
    filtered = filtered.filter(faq => faq.categories.includes(selectedCategory.value))
  }

  return filtered
})

// Methods
const clearFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = ''
}

const editFAQ = (faq: FAQ) => {
  // Create a deep copy to prevent modal changes from affecting the list before saving
  editingFAQ.value = {
    id: faq.id,
    question: faq.question,
    answer: faq.answer,
    categories: [...faq.categories],
    feedback: faq.feedback
  }
  categoriesInput.value = faq.categories.join(', ')
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
  editingFAQ.value = null
  categoriesInput.value =''
}

// View FAQ functionality
const viewFAQ = (faq: FAQ) => {
  selectedFAQ.value = faq
  showViewModal.value = true
}

const closeViewModal = () => {
  showViewModal.value = false
  selectedFAQ.value = null
}

// Delete FAQ functionality
const deleteFAQ = (faq: FAQ) => {
  FAQToDelete.value = faq
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  FAQToDelete.value = null
}

const confirmDelete = () => {
  if (FAQToDelete.value) {
    const index = faqs.value.findIndex(faq => faq.id === FAQToDelete.value!.id)
    if (index !== -1) {
      faqs.value.splice(index, 1)
    }
  }
  closeDeleteModal()
}

const saveFAQ = () => {
  if (editingFAQ.value) {
    const index = faqs.value.findIndex(faq => faq.id === editingFAQ.value!.id)
    if (index !== -1) {
      // Update categories from input
      editingFAQ.value.categories = categoriesInput.value.split(',').map(category => category.trim()).filter(category => category)
      faqs.value[index] = { ...editingFAQ.value }
    }
  }
  closeEditModal()
}

type NewFAQ = Omit<FAQ, 'id'> & { feedback?: string }

const handleFAQSaved = (newFAQ: NewFAQ) => {
  const faqToAdd: FAQ = {
    id: `faq-${Date.now()}`, 
    question: newFAQ.question,
    answer: newFAQ.answer,
    categories: newFAQ.categories.map(c => c.trim()).filter(c => c),
    feedback: newFAQ.feedback || ''
  }

  faqs.value.unshift(faqToAdd) 
  showAddFAQPage.value = false 
}

</script>
