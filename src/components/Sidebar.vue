<template>
    <div>
        <!-- Overlay for small screens -->
        <div
            v-if="props.isOpen"
            @click="$emit('close')"
            class="fixed inset-0 bg-black bg-opacity-50 z-20 md:hidden"
        >
        </div>
        <aside
            class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white w-64 min-h-screen p-4 flex flex-col fixed inset-y-0 left-0 transform transition-transform duration-300 z-30 -translate-x-full md:translate-x-0 border-r border-gray-200 dark:border-gray-700"
            :class="{ 'translate-x-0': props.isOpen }"
        >
            <div class="flex items-center gap-2 mb-8">
                <div class="w-10 h-10 bg-gray-200 dark:bg-gray-700 rounded-full grid place-items-center">
                    <span class="text-lg font-semibold text-gray-800 dark:text-white">P</span>
                </div>
                <h1 class="font-semibold text-lg">PETTRY ADMIN</h1>
            </div>

            <nav class="flex-1 space-y-2">
                <a
                    v-for="item in menu"
                    :key="item.label"
                    @click.prevent="goTo(item.path)"
                    href="#"
                    class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition cursor-pointer text-gray-700 dark:text-gray-300"
                >
                    <i :class="item.icon"></i>
                    <span>{{ item.label }}</span>
                </a>
            </nav>
        </aside>
    </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const props = defineProps<{ isOpen: boolean }>()
const router = useRouter()

const menu = [
    { label: 'Dashboard', icon: 'fa-solid fa-home', path: '/' },
    { label: 'Orders', icon: 'fa-solid fa-box-open', path: 'orders' },
    { label: 'Products', icon: 'fa-solid fa-bone', path: 'products'},
    { label: 'Inventory', icon: 'fa-solid fa-warehouse', path: 'inventory' },
    { label: 'Promo codes', icon: 'fa-solid fa-ticket', path: 'promo' },
    { label: 'Customers', icon: 'fa-solid fa-users', path: 'customers' },
    { label: 'Product Analysis', icon: 'fa-solid fa-chart-line', path: 'analysis' },
    { label: 'FAQ', icon: 'fa-solid fa-circle-question', path: 'faq' }
]

function goTo(path: string) {
    router.push(path)
}

</script>

<style scoped>
@import 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css';
</style>
