<template>
  <header>
    <nav class="container">
      <RouterLink to="/">Diagnosis Search</RouterLink>
      <RouterLink to="/consultations">Consultations</RouterLink>
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
</style>