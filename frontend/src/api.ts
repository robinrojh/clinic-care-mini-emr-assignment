import axios from 'axios'
import { useAuthStore } from '@/store/auth'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
})

apiClient.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    const token = authStore.accessToken
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (
      error.response?.status === 401 &&
      originalRequest.url !== '/token/refresh' &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true
      const authStore = useAuthStore()

      try {
        const newAccessToken = await authStore.attemptRefresh()
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
        return apiClient(originalRequest)
      } catch (refreshError) {
        authStore.logout()
        return Promise.reject(refreshError)
      }
    }

    if (error.response?.status === 401 && originalRequest.url === '/token/refresh') {
      const authStore = useAuthStore()
      authStore.logout()
    }

    return Promise.reject(error)
  }
)

export default apiClient