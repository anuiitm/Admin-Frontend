<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
    <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Add New Product</h3>
      <button @click="cancel" class="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300">
        &larr; Back to Products
      </button>
    </div>
    
    <div class="px-6 py-4">
      <div v-if="errorMsg" class="mb-4 rounded-lg border border-red-300 bg-red-50 text-red-700 px-3 py-2 text-sm">
        {{ errorMsg }}
      </div>
      <div class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Name</label>
            <input v-model="newProduct.name" type="text" placeholder="e.g., Premium Dog Food" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">SKU</label>
            <input v-model="newProduct.sku" type="text" placeholder="e.g., DOG-FOOD-001" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Price (₹)</label>
            <input v-model.number="newProduct.price" type="number" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Stock</label>
            <input v-model.number="newProduct.stock" type="number" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Category</label>
            <select v-model="newProduct.category" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
              <option disabled value="">Please select one</option>
              <option v-for="category in props.categories" :key="category" :value="category">{{ category }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Pet Type</label>
            <select v-model="newProduct.petType" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
              <option disabled value="">Please select one</option>
              <option v-for="petType in petTypes" :key="petType" :value="petType">{{ petType }}</option>
              <option value="Other">Other</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Status</label>
            <select v-model="newProduct.status" class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900">
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Description</label>
          <textarea v-model="newProduct.description" rows="3" placeholder="High-quality nutrition..." class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white bg-white text-gray-900"></textarea>
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
          <!-- show preview -->
          <div v-if="imagePreview" class="mt-2">
            <img :src="imagePreview" alt="Preview" class="w-32 h-32 object-cover rounded-md border border-gray-300 dark:border-gray-600" />
          </div>
        </div>
        
        <div class="flex justify-end space-x-3 pt-4">
          <button @click="cancel" class="bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-300 py-2 px-4 rounded-md hover:bg-gray-400 dark:hover:bg-gray-500 transition-colors">
            Cancel
          </button>
          <button @click="saveNewProduct" class="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors">
            Save Product
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'

// Define Props
const props = defineProps<{
  categories: string[]
}>()

// Define Emits
const emit = defineEmits<{
  (e: 'close'): void
  (e: 'product-saved', product: any): void // We'll send the new product data
}>()

// Pet types data
const petTypes = ref(['Dog', 'Cat', 'Bird', 'Fish', 'Rabbit', 'Hamster'])

// Image upload
const imageFile = ref<File | null>(null)
const imagePreview = ref<string | null>(null)
const errorMsg = ref('')

// Form state
const tagsInput = ref('')
const api = useApi()
const newProduct = ref({
  name: '',
  description: '',
  tags: ref<string[]>([]),
  sku: '',
  price: 0.0,
  stock: 0,
  category: props.categories[0] || '', // Default to first category
  petType: '', // Will be set by user
  status: 'active'
})

// Methods
const cancel = () => {
  emit('close')
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

const saveNewProduct = async () => {
  // Process tags
  newProduct.value.tags = tagsInput.value
    .split(',')
    .map(tag => tag.trim())
    .filter(tag => tag) // Remove any empty strings

  errorMsg.value = ''
  try {
    // Ensure defaults
    if (!newProduct.value.category && props.categories && props.categories.length > 0) {
      newProduct.value.category = props.categories[0]
    }
    if (!newProduct.value.petType) {
      newProduct.value.petType = 'general'
    }

    // Upload image first if available
    let imageUrl = '/paws.png';
    if (imageFile.value) {
      const formData = new FormData();
      formData.append('image', imageFile.value);
      const response = await fetch('http://localhost:5001/api/admin/upload-product-image', {
        method: 'POST',
        body: formData
      });
      const result = await response.json();
      if (result.url) {
        imageUrl = result.url;
      }
    }

    const payload: any = {
      name: newProduct.value.name,
      sku: newProduct.value.sku,
      description: newProduct.value.description,
      price: newProduct.value.price,
      stock: newProduct.value.stock,
      main_image_url: imageUrl,
      tags: newProduct.value.tags,
      category_name: newProduct.value.category,
      pet_type: newProduct.value.petType,
      is_active: newProduct.value.status === 'active'
    }
    if (!payload.name || !payload.sku || !payload.price || !payload.category_name || !payload.pet_type) {
      alert('Please fill name, SKU, price, category and pet type.')
      return
    }
    await api.post(`/products`, payload)
    emit('product-saved', newProduct.value)
  } catch (e: any) {
    errorMsg.value = e?.message || 'Failed to create product'
  }
}

onMounted(async () => {
  // If categories not passed, could fetch here via /categories
})
</script>