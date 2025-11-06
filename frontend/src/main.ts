import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import { router } from './router'
import { useAuthStore } from './store/auth'

const app = createApp(App)
app.use(createPinia())

const authStore = useAuthStore()

async function initializeApp() {
    try {
        await authStore.attemptRefresh()
    } catch (e) {
        console.log("No valid refresh token found, user must log in.")
    } finally {
        app.use(router)
        app.mount('#app')
    }
}

initializeApp()