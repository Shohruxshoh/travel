<!--
  AdminLogin.vue
  Standalone login page for the admin panel.
  Authenticates via /api/auth/login and stores JWT.
-->
<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-header">
        <div class="login-icon">🔐</div>
        <h1>Admin Panel</h1>
        <p>Adventures Travel Time</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div v-if="error" class="alert alert-error">⚠️ {{ error }}</div>

        <div class="form-group">
          <label class="form-label">Username</label>
          <input
            v-model="username"
            type="text"
            class="form-input"
            placeholder="Enter username"
            required
            autofocus
          />
        </div>

        <div class="form-group">
          <label class="form-label">Password</label>
          <input
            v-model="password"
            type="password"
            class="form-input"
            placeholder="Enter password"
            required
          />
        </div>

        <button type="submit" class="btn btn-primary" style="width:100%" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>

      <div class="login-footer">
        <router-link to="/">← Back to website</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../../api/adminApi.js'

const router = useRouter()
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await login(username.value, password.value)
    router.push('/admin')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Invalid username or password'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--brand-gradient-hero);
  padding: 20px;
}
.login-card {
  width: 100%;
  max-width: 420px;
  background: var(--bg-elevated);
  border-radius: var(--radius-xl);
  padding: 44px 36px;
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--border-light);
}
.login-header {
  text-align: center;
  margin-bottom: 32px;
}
.login-icon {
  font-size: 2.5rem;
  margin-bottom: 12px;
}
.login-header h1 {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 4px;
}
.login-header p {
  font-size: 0.88rem;
  color: var(--text-tertiary);
}
.login-form {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.login-footer {
  text-align: center;
  margin-top: 24px;
}
.login-footer a {
  font-size: 0.85rem;
  color: var(--text-tertiary);
}
.login-footer a:hover {
  color: var(--text-brand);
}
</style>
