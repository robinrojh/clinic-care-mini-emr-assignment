<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/store/auth'
import { router } from '@/router'

const email = ref('')
const password = ref('')
const error = ref<string | null>(null)
const loading = ref(false)

const authStore = useAuthStore()

async function handleLogin() {
    if (!email.value || !password.value) {
        error.value = 'Please enter both email and password'
        return
    }

    loading.value = true
    error.value = null

    try {
        await authStore.login(email.value, password.value)
        router.push('/consultations')
    } catch (err: any) {
        console.error(err)
        if (err.response?.status === 401) {
            error.value = 'Incorrect username or password.'
        } else {
            error.value = 'An unknown error occurred. Please try again.'
        }
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="auth-container">
        <div class="auth-form">
            <h2>Log In</h2>
            <form @submit.prevent="handleLogin">
                <div class="form-group">
                    <label>Email:</label>
                    <input v-model="email" type="email" class="form-control" />
                </div>
                <div class="form-group">
                    <label>Password:</label>
                    <input v-model="password" type="password" class="form-control" />
                </div>
                <button type="submit" :disabled="loading" class="btn btn-primary submit-btn">
                    {{ loading ? 'Logging in...' : 'Log In' }}
                </button>
                <div v-if="error" class="error-message">{{ error }}</div>
            </form>
        </div>
    </div>
</template>

<style scoped>
.auth-container {
    display: flex;
    justify-content: center;
    padding-top: 40px;
}

.auth-form {
    max-width: 400px;
    width: 100%;
    padding: 20px;
    border: 1px solid var(--color-border-light);
    border-radius: var(--border-radius);
    background-color: var(--color-bg-light);
}

.submit-btn {
    width: 100%;
}
</style>