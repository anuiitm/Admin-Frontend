export function useApi() {
    const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001/api/admin'

    const headers = (): HeadersInit => {
        const token = localStorage.getItem('auth_token')
        const h: Record<string, string> = { 'Content-Type': 'application/json' }
        if (token) h['Authorization'] = `Bearer ${token}`
        return h
    }

    async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
        const res = await fetch(`${baseUrl}${path}`, {
            ...options,
            headers: { ...(options.headers || {}), ...headers() },
        })
        const contentType = res.headers.get('content-type') || ''
        let data: any = null
        if (contentType.includes('application/json')) {
            try { data = await res.json() } catch (_) { data = null }
        } else {
            try { data = await res.text() } catch (_) { data = null }
        }
        if (!res.ok) {
            const message = (data && (data.error || data.message)) || `API ${res.status}`
            throw new Error(message)
        }
        return data as T
    }

    return {
        get: <T>(path: string) => request<T>(path),
        post: <T>(path: string, body?: any) => request<T>(path, { method: 'POST', body: JSON.stringify(body || {}) }),
        put: <T>(path: string, body?: any) => request<T>(path, { method: 'PUT', body: JSON.stringify(body || {}) }),
        del: <T>(path: string) => request<T>(path, { method: 'DELETE' }),
    }
}


