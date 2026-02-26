<!--
  ServicesView.vue — Lists agency services
-->
<template>
  <div>
    <div class="page-header">
      <h1>{{ $t('services.title') }}</h1>
    </div>
    <section class="section">
      <p class="section-subtitle">{{ $t('services.subtitle') }}</p>
      <div class="card-grid container">
        <div v-for="svc in services" :key="svc.id" class="card">
          <div class="card-body">
            <div style="font-size: 2rem; margin-bottom: 12px;">{{ svc.icon || '✈️' }}</div>
            <h3 class="card-title">{{ getField(svc, 'name') }}</h3>
            <p class="card-text">{{ getField(svc, 'description') }}</p>
            <span v-if="svc.price" class="card-price">${{ svc.price }}</span>
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
const services = ref([])

function getField(obj, prefix) {
  return obj[`${prefix}_${locale.value}`] || obj[`${prefix}_en`] || ''
}

onMounted(async () => {
  try {
    const res = await api.get('/services/')
    services.value = res.data
  } catch (e) {
    console.error('Failed to load services:', e)
  }
})
</script>
