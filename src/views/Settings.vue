<template>
  <div class="flex min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100">
    <Sidebar :isOpen="isOpen" @close="isOpen = false" />

    <div class="flex-1 flex flex-col md:ml-64">
      <Navbar @toggle-sidebar="isOpen = !isOpen" />

      <!-- Content -->
      <main class="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <!-- Header -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Settings</h1>
          <p class="mt-2 text-gray-600 dark:text-gray-400">Configure your application settings</p>
        </div>

      <div class="space-y-8">
        <!-- Payment Modes Section -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
          <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Payment Modes</h2>
            <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">Select the payment methods you want to enable</p>
          </div>
          <div class="p-6">
            <div class="space-y-3">
              <label 
                v-for="mode in paymentModes" 
                :key="mode.id"
                class="flex items-center space-x-3 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700 p-3 rounded-lg transition-colors"
              >
                <input
                  type="checkbox"
                  :id="mode.id"
                  v-model="selectedPaymentModes"
                  :value="mode.id"
                  class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 checked:bg-blue-600 checked:border-blue-600"
                />
                <div class="flex items-center space-x-3">
                  <div class="text-2xl">{{ mode.icon }}</div>
                  <div>
                    <div class="font-medium text-gray-900 dark:text-white">{{ mode.name }}</div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">{{ mode.description }}</div>
                  </div>
                </div>
              </label>
            </div>
          </div>
        </div>

        <!-- Delivery Charges Section -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
          <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Delivery Charges</h2>
            <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">Set delivery charges for different delivery types</p>
          </div>
          <div class="p-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Express Delivery -->
              <div>
                <label for="expressDelivery" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Express Delivery Charges (₹)
                </label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <span class="text-gray-500 dark:text-gray-400 text-sm">₹</span>
                  </div>
                  <input
                    type="number"
                    id="expressDelivery"
                    v-model="deliveryCharges.express"
                    class="block w-full pl-8 pr-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    placeholder="0"
                    min="0"
                    step="0.01"
                  />
                </div>
                <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">Same day or next day delivery</p>
              </div>

              <!-- Normal Delivery -->
              <div>
                <label for="normalDelivery" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Normal Delivery Charges (₹)
                </label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <span class="text-gray-500 dark:text-gray-400 text-sm">₹</span>
                  </div>
                  <input
                    type="number"
                    id="normalDelivery"
                    v-model="deliveryCharges.normal"
                    class="block w-full pl-8 pr-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    placeholder="0"
                    min="0"
                    step="0.01"
                  />
                </div>
                <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">Standard 3-5 business days delivery</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Exempted Areas Section -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
          <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Exempted Areas</h2>
            <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">Add pincodes for areas with free delivery</p>
          </div>
          <div class="p-6">
            <!-- Add Pincode Input -->
            <div class="flex space-x-3 mb-4">
              <div class="flex-1">
                <input
                  type="text"
                  v-model="newPincode"
                  @keyup.enter="addPincode"
                  class="block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                  placeholder="Enter pincode (e.g., 110001)"
                  maxlength="6"
                />
              </div>
              <button
                @click="addPincode"
                :disabled="!newPincode.trim() || newPincode.length !== 6"
                class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Add
              </button>
            </div>

            <!-- Pincode List -->
            <div v-if="exemptedPincodes.length > 0" class="space-y-2">
              <h3 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Exempted Pincodes ({{ exemptedPincodes.length }})</h3>
              <div class="flex flex-wrap gap-2">
                <div
                  v-for="(pincode, index) in exemptedPincodes"
                  :key="index"
                  class="inline-flex items-center space-x-2 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 px-3 py-1 rounded-full text-sm"
                >
                  <span>{{ pincode }}</span>
                  <button
                    @click="removePincode(index)"
                    class="text-blue-500 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-200 transition-colors"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-else class="text-center py-8">
              <div class="text-gray-400 dark:text-gray-500 mb-2">
                <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
              </div>
              <p class="text-gray-500 dark:text-gray-400">No exempted areas added yet</p>
              <p class="text-sm text-gray-400 dark:text-gray-500">Add pincodes above to create exempted areas</p>
            </div>
          </div>
        </div>

        <!-- Save Button -->
        <div class="flex justify-end">
          <button
            @click="saveSettings"
            class="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors"
          >
            Save Settings
          </button>
        </div>
      </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import Navbar from '@/components/Navbar.vue'

const router = useRouter()
const isOpen = ref(false)

// Payment modes data
const paymentModes = ref([
  {
    id: 'upi',
    name: 'UPI',
    description: 'Unified Payments Interface',
    icon: '📱'
  },
  {
    id: 'cod',
    name: 'Cash on Delivery',
    description: 'Pay when you receive',
    icon: '💵'
  },
  {
    id: 'credit_card',
    name: 'Credit Card',
    description: 'Visa, Mastercard, etc.',
    icon: '💳'
  },
  {
    id: 'emi',
    name: 'EMI',
    description: 'Equated Monthly Installments',
    icon: '📅'
  }
])

// Reactive data
const selectedPaymentModes = ref<string[]>(['upi', 'cod'])
const deliveryCharges = reactive({
  express: 50,
  normal: 20
})
const exemptedPincodes = ref<string[]>(['110001', '400001'])
const newPincode = ref('')

// Methods
const addPincode = () => {
  const pincode = newPincode.value.trim()
  if (pincode && pincode.length === 6 && !exemptedPincodes.value.includes(pincode)) {
    exemptedPincodes.value.push(pincode)
    newPincode.value = ''
  }
}

const removePincode = (index: number) => {
  exemptedPincodes.value.splice(index, 1)
}

const saveSettings = () => {
  // Here you would typically save to your backend
  console.log('Saving settings:', {
    paymentModes: selectedPaymentModes.value,
    deliveryCharges: deliveryCharges,
    exemptedPincodes: exemptedPincodes.value
  })
  
  // Show success message and navigate to dashboard
  alert('Settings saved successfully!')
  router.push({ name: 'dashboard' })
}
</script>

<style scoped>
/* Custom checkbox styling for better light/dark mode support */
input[type="checkbox"] {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-color: white;
  border: 2px solid #d1d5db;
  border-radius: 0.25rem;
  position: relative;
  cursor: pointer;
}

input[type="checkbox"]:checked {
  background-color: #2563eb;
  border-color: #2563eb;
}

input[type="checkbox"]:checked::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 12px;
  font-weight: bold;
}

.dark input[type="checkbox"] {
  background-color: #374151;
  border-color: #4b5563;
}

.dark input[type="checkbox"]:checked {
  background-color: #2563eb;
  border-color: #2563eb;
}
</style>
