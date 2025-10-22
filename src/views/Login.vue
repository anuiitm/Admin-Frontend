<template>
    <div class="min-h-screen flex relative">
        <!-- Global top-right theme toggle -->
        <div class="absolute top-4 right-4 z-20">
            <ThemeToggle />
        </div>
		<!-- Left: Illustration / branding -->
		<div class="hidden lg:flex w-1/2 bg-gradient-to-br from-primary-600 to-primary-800 text-white items-center justify-center p-12 relative overflow-hidden">
			<div class="absolute inset-0 opacity-10">
				<div class="absolute -top-20 -left-20 w-96 h-96 bg-white rounded-full blur-3xl"></div>
				<div class="absolute -bottom-20 -right-20 w-[30rem] h-[30rem] bg-white rounded-full blur-3xl"></div>
			</div>
			<div class="relative z-10 max-w-md">
				<div class="flex items-center gap-3 mb-6">
					<div class="bg-white/20 p-3 rounded-xl shadow-soft">
						<!-- Simple paw icon -->
						<svg class="w-8 h-8" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
							<path d="M12 21c4 0 7-2.5 7-5.5 0-2-2.5-3.5-5-2-1-.5-2-.5-3 0-2.5-1.5-5 0-5 2 0 3 3 5.5 7 5.5Z" fill="currentColor"/>
							<circle cx="5.5" cy="8.5" r="2.5" fill="currentColor"/>
							<circle cx="18.5" cy="8.5" r="2.5" fill="currentColor"/>
							<circle cx="9.5" cy="5.5" r="2.5" fill="currentColor"/>
							<circle cx="14.5" cy="5.5" r="2.5" fill="currentColor"/>
						</svg>
					</div>
					<h1 class="text-3xl font-semibold tracking-tight">PETTRY ADMIN</h1>
				</div>
				<p class="text-white/80 leading-relaxed">Manage products, orders, and customers with a sleek, modern interface. Sign in to continue to your dashboard.</p>
			</div>
		</div>

		<!-- Right: Login form -->
		<div class="flex-1 flex items-center justify-center p-8">
			<div class="w-full max-w-md">
				<div class="mb-8 text-center">
					<h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">Welcome back</h2>
					<p class="mt-1 text-gray-500 dark:text-gray-400">Sign in to your pettry admin account</p>
				</div>

				<form @submit.prevent="onSubmit" class="bg-white dark:bg-gray-800 rounded-2xl shadow-soft p-6 border border-gray-100 dark:border-gray-700">
					<div class="space-y-4">
						<div>
							<label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Email</label>
							<input v-model="email" id="email" type="email" required autocomplete="email" class="form-input block w-full rounded-xl border-gray-300 dark:border-gray-600 dark:bg-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500" placeholder="you@company.com" />
						</div>
						<div>
							<label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Password</label>
							<input v-model="password" id="password" type="password" required autocomplete="current-password" class="form-input block w-full rounded-xl border-gray-300 dark:border-gray-600 dark:bg-gray-900 dark:text-gray-100 focus:border-primary-500 focus:ring-primary-500" placeholder="••••••••" />
						</div>
						<div class="flex items-center justify-between">
							<label class="inline-flex items-center gap-2 text-sm text-gray-600 dark:text-gray-300">
								<input type="checkbox" v-model="remember" class="form-checkbox rounded text-primary-600 focus:ring-primary-500 dark:bg-gray-900 dark:border-gray-600" />
								<span>Remember me</span>
							</label>
						</div>
						<button :disabled="loading" type="submit" class="w-full inline-flex justify-center items-center gap-2 rounded-xl bg-primary-600 text-white py-2.5 font-medium hover:bg-primary-700 transition focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-60">
							<span v-if="!loading">Sign in</span>
							<svg v-else class="animate-spin h-5 w-5" viewBox="0 0 24 24">
								<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
								<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
							</svg>
						</button>
					</div>
				</form>

				<!-- Spacer below form (toggle moved to top-right) -->
				<div class="mt-6"></div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import ThemeToggle from '@/components/ThemeToggle.vue'

const router = useRouter()
const email = ref('')
const password = ref('')
const remember = ref(true)
const loading = ref(false)

async function onSubmit() {
	loading.value = true
	// Simulate auth and persist token
	setTimeout(() => {
		localStorage.setItem('auth_token', 'demo-token')
		if (remember.value) localStorage.setItem('remember_me', '1')
		loading.value = false
		router.push({ name: 'dashboard' })
	}, 800)
}
</script>

<style scoped>
</style>

