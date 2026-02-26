<!--
  ThemeToggle.vue
  Toggles between dark and light mode.
  Persists preference in localStorage.
  Applies [data-theme] attribute to <html>.
-->
<template>
  <button
    class="theme-toggle"
    @click="toggleTheme"
    :title="isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
    :aria-label="isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
  >
    <transition name="fade" mode="out-in">
      <span v-if="isDark" key="sun">☀️</span>
      <span v-else key="moon">🌙</span>
    </transition>
  </button>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isDark = ref(false)

function applyTheme(dark) {
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light')
  isDark.value = dark
  localStorage.setItem('theme', dark ? 'dark' : 'light')
}

function toggleTheme() {
  applyTheme(!isDark.value)
}

onMounted(() => {
  const saved = localStorage.getItem('theme')
  if (saved === 'dark') {
    applyTheme(true)
  } else if (saved === 'light') {
    applyTheme(false)
  } else {
    // Detect system preference
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    applyTheme(prefersDark)
  }
})
</script>
