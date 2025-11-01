<template>
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
      <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Add New Question</h3>
        <button @click="cancel" class="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300">
          &larr; Back to FAQ
        </button>
      </div>
      
      <div class="px-6 py-4">
        <div class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Question</label>
              <textarea v-model="newFAQ.question" rows="3" placeholder="Enter your question..." class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white text-gray-900 resize-none"></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Answer</label>
              <textarea v-model="newFAQ.answer" rows="3" placeholder="Enter your answer..." class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white text-gray-900 resize-none"></textarea>
            </div>
          </div>
          <div>                
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Categories (comma separated)</label>
            <input v-model="categoriesInput" type="text" placeholder="General, Payments, Product" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white">
          </div>
          
          <div class="flex justify-end space-x-3 pt-4">
            <button @click="cancel" class="bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-300 py-2 px-4 rounded-md hover:bg-gray-400 dark:hover:bg-gray-500 transition-colors">
              Cancel
            </button>
            <button @click="saveNewFAQ" class="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors">
              Save
            </button>
          </div>
        </div>
      </div>
    </div>
</template>
  
<script setup lang="ts">
import { ref } from 'vue'

// Define Emits
const emit = defineEmits<{
  (e: 'close'): void
  (e: 'faq-saved', FAQ: any): void // We'll send the new data
}>()

// Form state
const categoriesInput = ref('')
const newFAQ = ref({
  question: '',
  answer: '',
  categories: [] as string[]
})

// Methods
const cancel = () => {
  emit('close')
}

const saveNewFAQ = () => {
  newFAQ.value.categories = categoriesInput.value
    .split(',')
    .map(category => category.trim())
    .filter(category => category) // Remove any empty strings

  emit('faq-saved', newFAQ.value)
}
</script>