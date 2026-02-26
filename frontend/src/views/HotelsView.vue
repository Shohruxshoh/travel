<!--
  HotelsView.vue — Lists partner hotels with star ratings
-->
<template>
  <div>
    <div class="page-header">
      <h1>{{ $t('hotels.title') }}</h1>
    </div>
    <section class="section">
      <div class="card-grid container">
        <div v-for="hotel in hotels" :key="hotel.id" class="card">
          <div
            class="card-image"
            :style="hotel.image_url ? { backgroundImage: `url(${hotel.image_url})`, backgroundSize: 'cover', backgroundPosition: 'center' } : {}"
          ></div>
          <div class="card-body">
            <h3 class="card-title">{{ hotel.name }}</h3>
            <p class="stars">{{ '★'.repeat(hotel.star_rating) }}{{ '☆'.repeat(5 - hotel.star_rating) }}</p>
            <p class="card-text">{{ hotel.city }}, {{ hotel.country }}</p>
            <p class="card-text">{{ getField(hotel, 'description') }}</p>
            <span class="card-price">
              {{ $t('hotels.fromPrice') }} ${{ hotel.price_from }}
              <span>{{ $t('hotels.perNight') }}</span>
            </span>
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
const hotels = ref([])

function getField(obj, prefix) {
  return obj[`${prefix}_${locale.value}`] || obj[`${prefix}_en`] || ''
}

onMounted(async () => {
  try {
    const res = await api.get('/hotels/')
    hotels.value = res.data
  } catch (e) {
    console.error('Failed to load hotels:', e)
  }
})
</script>
