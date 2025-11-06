<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api'

const formData = reactive({
    email: '',
    first_name: '',
    last_name: '',
    password: '',
})

const error = ref<string | null>(null)
const loading = ref(false)
const router = useRouter()

async function handleSubmit() {
    loading.value = true
    error.value = null

    try {
        await apiClient.post('/signup', formData)
        router.push('/login')
    } catch (err: any) {
        error.value = err.response?.data?.detail || 'Failed to create account.'
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="auth-container">
        <div class="auth-form">
            <h2>Create Account</h2>
            <form @submit.prevent="handleSubmit">
                <div class="form-group">
                    <label>First Name:</label>
                    <input v-model="formData.first_name" type="text" class="form-control" />
                </div>
                <div class="form-group">
                    <label>Last Name:</label>
                    <input v-model="formData.last_name" type="text" class="form-control" />
                </div>
                <div class="form-group">
                    <label>Email:</label>
                    <input v-model="formData.email" type="email" class="form-control" />
                </div>
                <div class="form-group">
                    <label>Password:</label>
                    <input v-model="formData.password" type="password" class="form-control" />
                </div>
                <button type="submit" :disabled="loading" class="btn btn-primary submit-btn">
                    {{ loading ? 'Creating...' : 'Sign Up' }}
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