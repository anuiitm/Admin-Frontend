import { ref, watchEffect } from 'vue'

type Theme = 'light' | 'dark' | 'system'

const theme = ref<Theme>('system')

function getSystemPrefersDark(): boolean {
	return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
}

function applyTheme(t: Theme) {
	const root = document.documentElement
	const isDark = t === 'dark' || (t === 'system' && getSystemPrefersDark())
	root.classList.toggle('dark', isDark)
}

export function useTheme() {
	if (typeof window !== 'undefined') {
		const saved = localStorage.getItem('theme') as Theme | null
		theme.value = saved || 'system'
		applyTheme(theme.value)

		// react to system changes when in system mode
		const mq = window.matchMedia('(prefers-color-scheme: dark)')
		mq.addEventListener?.('change', () => {
			if (theme.value === 'system') applyTheme('system')
		})
	}

	watchEffect(() => {
		try {
			localStorage.setItem('theme', theme.value)
			applyTheme(theme.value)
		} catch {}
	})

	return { theme }
}

