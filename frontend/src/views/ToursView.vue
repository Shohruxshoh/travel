<!--
  ToursView.vue — Lists tour packages from the API
-->
<template>
  <div>
    <div class="page-header">
      <h1>{{ $t('tours.title') }}</h1>
    </div>
    <section class="section">
      <div class="card-grid container">
        <router-link v-for="tour in tours" :key="tour.id" :to="`/tours/${tour.id}`" class="card" style="text-decoration:none; color:inherit;">
          <div class="card-image" :style="tour.cover_image ? { backgroundImage: `url(${tour.cover_image})`, backgroundSize: 'cover', backgroundPosition: 'center' } : (tour.images_json?.length ? { backgroundImage: `url(${tour.images_json[0]})`, backgroundSize: 'cover', backgroundPosition: 'center' } : {})"></div>
          <div class="card-body">
            <h3 class="card-title">{{ getField(tour, 'title') }}</h3>
            <p class="card-text">{{ truncate(getField(tour, 'description'), 120) }}</p>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="card-price">
                €{{ tour.price }} <span>/ {{ $t('tours.perPerson') }}</span>
              </span>
              <span style="color: var(--gray-400); font-size: 0.85rem;">{{ tour.duration_days }} {{ $t('tours.duration') }}</span>
            </div>
          </div>
        </router-link>
      </div>
      <p v-if="!tours.length" style="text-align: center; color: var(--gray-400); padding: 40px;">
        No tours available.
      </p>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '../api/axios.js'

const { locale } = useI18n()
const tours = ref([])

function getField(obj, prefix) {
  return obj[`${prefix}_${locale.value}`] || obj[`${prefix}_en`] || ''
}

function truncate(str, len) {
  return str.length > len ? str.slice(0, len) + '...' : str
}

onMounted(async () => {
  try {
    const res = await api.get('/tours/')
    tours.value = res.data
  } catch (e) {
    console.error('Failed to load tours:', e)
  }
})
</script>
