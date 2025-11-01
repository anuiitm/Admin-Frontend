<template>
	<div class="inline-flex items-center gap-2 select-none">
		<!-- Icon light -->
		<svg class="w-4 h-4 text-yellow-500" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
			<path d="M6.76 4.84l-1.8-1.79-1.41 1.41 1.79 1.8 1.42-1.42zm10.48 14.32l1.79 1.8 1.41-1.41-1.8-1.79-1.4 1.4zM12 4V1h-0v3h0zm0 19v-3h0v3h0zm8-11h3v0h-3v0zM1 12h3v0H1v0zm15.24-7.16l1.8-1.79-1.41-1.41-1.79 1.8 1.4 1.4zM4.22 19.78l1.79-1.8-1.41-1.41-1.8 1.79 1.42 1.42zM12 6a6 6 0 100 12 6 6 0 000-12z"/>
		</svg>
		<!-- Switch -->
		<button @click="cycle" class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none"
			:class="isDark ? 'bg-primary-600' : 'bg-gray-300 dark:bg-gray-700'"
			aria-label="Toggle theme">
			<span class="inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition" :class="isDark ? 'translate-x-5' : 'translate-x-1'"></span>
		</button>
		<!-- Icon dark -->
		<svg class="w-4 h-4 text-gray-500 dark:text-gray-300" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
			<path d="M21.64 13a9 9 0 11-10.63-10.6 1 1 0 01.93.25 1 1 0 01.27.92A7 7 0 0020 13a1 1 0 01.64.93 1 1 0 01-.27.92 1 1 0 01-.73.29z"/>
		</svg>
	</div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useTheme } from '@/composables/useTheme'

const { theme } = useTheme()
const isDark = computed(() => theme.value === 'dark' || (theme.value === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches))

function cycle() {
	if (theme.value === 'light') theme.value = 'dark'
	else if (theme.value === 'dark') theme.value = 'system'
	else theme.value = 'light'
}
</script>

<style scoped>
</style>

