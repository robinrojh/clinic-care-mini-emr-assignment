import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api'

interface TokenPayload {
    access_token: string
}

export const useAuthStore = defineStore('auth', () => {
    const accessToken = ref<string | null>(null)
    const userEmail = ref<string | null>(null)
    const router = useRouter()

    const isLoggedIn = computed(() => !!accessToken.value)

    function setLoginState(payload: TokenPayload, email: string) {
        accessToken.value = payload.access_token
        userEmail.value = email
    }

    async function login(email: string, password: string) {
        const params = new URLSearchParams()
        params.append('username', email)
        params.append('password', password)

        const response = await apiClient.post<TokenPayload>('/token', params, {
            withCredentials: true,
        })

        setLoginState(response.data, email)
    }

    async function attemptRefresh() {
        try {
            const response = await apiClient.post<TokenPayload>('/token/refresh', {}, {
                withCredentials: true,
            })

            accessToken.value = response.data.access_token
            return response.data.access_token

        } catch (e) {
            clearAuth()
            throw new Error('Refresh token invalid or expired.')
        }
    }

    function clearAuth() {
        accessToken.value = null
        userEmail.value = null
    }

    async function logout() {
        try {
            await apiClient.post('/logout', {}, {
                withCredentials: true,
            })
        } catch (e) {
            console.error("Error during logout, clearing frontend anyway", e)
        } finally {
            clearAuth()
            router.push('/login')
        }
    }

    return {
        accessToken,
        userEmail,
        isLoggedIn,
        login,
        logout,
        attemptRefresh,
    }
})