<!--
  BlogView.vue — Blog articles listing
-->
<template>
  <div>
    <div class="page-header">
      <h1>{{ $t('blog.title') }}</h1>
    </div>
    <section class="section">
      <div class="card-grid container">
        <div v-for="article in articles" :key="article.id" class="card">
          <div
            class="card-image"
            :style="article.cover_image ? { backgroundImage: `url(${article.cover_image})`, backgroundSize: 'cover', backgroundPosition: 'center' } : {}"
          ></div>
          <div class="card-body">
            <h3 class="card-title">{{ getField(article, 'title') }}</h3>
            <p class="card-text">{{ truncate(getField(article, 'content'), 150) }}</p>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span style="color: var(--gray-400); font-size: 0.8rem;">
                {{ article.author || '' }}
              </span>
              <a href="#" class="btn btn-primary" style="padding: 8px 16px; font-size: 0.85rem;">
                {{ $t('blog.readMore') }}
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '../api/axios.js'

const { locale } = useI18n()
const articles = ref([])

function getField(obj, prefix) {
  return obj[`${prefix}_${locale.value}`] || obj[`${prefix}_en`] || ''
}

function truncate(str, len) {
  return str.length > len ? str.slice(0, len) + '...' : str
}

onMounted(async () => {
  try {
    const res = await api.get('/blog/')
    articles.value = res.data
  } catch (e) {
    console.error('Failed to load articles:', e)
  }
})
</script>
