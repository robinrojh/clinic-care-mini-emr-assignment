<script setup lang="ts">
import { useAuthStore } from '@/store/auth'
import { router } from './router'

const authStore = useAuthStore()

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <header>
    <nav class="container">
      <RouterLink to="/">Diagnosis Search</RouterLink>
      <RouterLink to="/consultations">Consultations</RouterLink>
      <RouterLink to="/consultations/post">Create Notes</RouterLink>
      <div class="auth-links">
        <template v-if="authStore.isLoggedIn">
          <button @click="handleLogout" class="btn btn-logout">Logout</button>
        </template>
        <template v-else>
          <RouterLink to="/login" class="nav-link">Login</RouterLink>
          <RouterLink to="/signup" class="nav-link">Sign Up</RouterLink>
        </template>
      </div>
    </nav>
  </header>

  <main>
    <div class="container">
      <RouterView />
    </div>
  </main>
</template>

<style scoped>
header {
  padding: 20px 0;
  border-bottom: 1px solid var(--color-border-light);
  margin-bottom: var(--spacing);
  background-color: var(--color-bg-light);
}

nav {
  display: flex;
  align-items: center;
  gap: var(--spacing);
  font-size: 1.2rem;
}

nav a {
  text-decoration: none;
  color: var(--color-text-light);
  font-weight: 600;
  transition: color 0.2s ease;
}

nav a:hover {
  color: var(--color-text);
}

nav a.router-link-exact-active {
  color: var(--color-primary);
}

.auth-links {
  margin-left: auto;
  display: flex;
  gap: 15px;
  align-items: center;
}

.nav-link {
  font-size: 1rem;
}

.btn-logout {
  padding: 5px 10px;
  font-size: 0.9rem;
  font-weight: 600;
  background-color: transparent;
  border: 1px solid var(--color-border);
  color: var(--color-text-light);
  cursor: pointer;
}

.btn-logout:hover {
  background-color: var(--color-bg-light);
  color: var(--color-danger);
  border-color: var(--color-danger);
}
</style>