<template>
    <header
        class="flex items-center justify-between bg-white dark:bg-gray-800 p-4 shadow-md"
    >
        <button @click="$emit('toggle-sidebar')" class="md:hidden p-2 rounded bg-gray-800 text-white"> ☰ </button>
        <div class="flex items-center w-full max-w-md">
            <input
                type="text"
                placeholder="Search products, orders..."
                class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-200 focus:outline-none"
            />
        </div>

        <div class="flex items-center gap-4">
            <button class="p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700">🔔</button>
            <button class="p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700">⚙️</button>
            <ThemeToggle />
            <button
                @click="logout"
                class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm"
            > Logout </button>
        </div>
    </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import ThemeToggle from '@/components/ThemeToggle.vue'

const router = useRouter()
function logout() {
    localStorage.removeItem('auth_token')
    router.push({ name: 'login' })
}
</script>
