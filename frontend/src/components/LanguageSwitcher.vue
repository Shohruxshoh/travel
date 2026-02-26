<!--
  LanguageSwitcher.vue
  Toggles between RU / EN / FR locales.
  Persists the choice to localStorage and updates the
  vue-i18n locale + the document lang attribute.
-->
<template>
  <div class="lang-switcher">
    <button
      v-for="lang in languages"
      :key="lang"
      class="lang-btn"
      :class="{ active: locale === lang }"
      @click="switchLanguage(lang)"
    >
      {{ lang }}
    </button>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()
const languages = ['ru', 'en', 'fr']

function switchLanguage(lang) {
  locale.value = lang
  localStorage.setItem('locale', lang)
  document.documentElement.lang = lang
}

// Restore saved locale on mount
const saved = localStorage.getItem('locale')
if (saved && languages.includes(saved)) {
  locale.value = saved
  document.documentElement.lang = saved
}
</script>
