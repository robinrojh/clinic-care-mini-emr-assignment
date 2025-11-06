<template>
  <header>
    <nav>
      <RouterLink to="/">Diagnosis Search</RouterLink>
      <RouterLink to="/consultations">Consultations</RouterLink>
    </nav>
  </header>
  <main>
    <RouterView />
  </main>
</template>

<style scoped>
header {
  padding: 20px 0;
  border-bottom: 1px solid #ccc;
  margin-bottom: 20px;
}
nav {
  display: flex;
  gap: 20px;
  font-size: 1.2rem;
}
nav a {
  text-decoration: none;
  color: #2c3e50;
}
nav a.router-link-exact-active {
  color: #42b983;
  font-weight: bold;
}
main {
  padding: 0 20px;
}
</style>