<!--
  TourDetailView.vue — Full tour detail page (uzbektravel.fr style)
  Shows ALL tour info: hero, price, description, itinerary, gallery.
  "Book Now" button toggles booking form.
-->
<template>
  <div v-if="tour">
    <!-- ═══ HERO ═══ -->
    <section class="tour-detail-hero" :style="heroStyle">
      <div class="tour-detail-hero-overlay">
        <div class="container">
          <div class="tour-detail-hero-content">
            <div class="tour-detail-badge">📍 {{ tour.destination }}</div>
            <h1>{{ getField(tour, 'title') }}</h1>
            <div class="tour-detail-meta">
              <span>📅 {{ tour.duration_days }} {{ $t('tours.duration') || 'days' }}</span>
              <span>💰 €{{ tour.price }} / {{ $t('tours.perPerson') || 'person' }}</span>
            </div>
            <button class="btn btn-accent btn-lg" @click="scrollToBooking" style="margin-top:20px;">
              📋 {{ $t('booking.title') || 'Book This Tour' }}
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══ MAIN CONTENT ═══ -->
    <section class="section">
      <div class="container" style="max-width:900px; margin:0 auto;">

        <!-- Price & Quick Info Bar -->
        <div class="tour-info-cards">
          <div class="tour-info-card">
            <div class="tour-info-icon">💰</div>
            <div class="tour-info-label">{{ $t('tours.priceLabel') || 'Price' }}</div>
            <div class="tour-info-value">€{{ tour.price }}</div>
          </div>
          <div class="tour-info-card">
            <div class="tour-info-icon">📅</div>
            <div class="tour-info-label">{{ $t('tours.duration') || 'Duration' }}</div>
            <div class="tour-info-value">{{ tour.duration_days }} {{ $t('tours.days') || 'days' }}</div>
          </div>
          <div class="tour-info-card">
            <div class="tour-info-icon">📍</div>
            <div class="tour-info-label">{{ $t('tours.destinationLabel') || 'Destination' }}</div>
            <div class="tour-info-value">{{ tour.destination }}</div>
          </div>
          <div class="tour-info-card">
            <div class="tour-info-icon">{{ tour.is_active ? '✅' : '⏸️' }}</div>
            <div class="tour-info-label">{{ $t('tours.statusLabel') || 'Status' }}</div>
            <div class="tour-info-value">{{ tour.is_active ? ($t('tours.available') || 'Available') : ($t('tours.unavailable') || 'Unavailable') }}</div>
          </div>
        </div>

        <!-- Description -->
        <div class="tour-detail-body">
          <h2 class="tour-detail-section-title">{{ $t('tours.aboutTour') || 'About This Tour' }}</h2>
          <div class="tour-detail-description" v-html="formatDescription(getField(tour, 'description'))"></div>
        </div>

        <!-- Itinerary -->
        <div v-if="tour.itinerary_json && tour.itinerary_json.length" class="tour-detail-body">
          <h2 class="tour-detail-section-title">🗓️ {{ $t('tours.itinerary') || 'Tour Itinerary' }}</h2>
          <div class="tour-itinerary">
            <div v-for="(day, idx) in tour.itinerary_json" :key="idx" class="itinerary-day">
              <div class="itinerary-day-marker">
                <div class="itinerary-day-num">{{ idx + 1 }}</div>
                <div class="itinerary-day-line" v-if="idx < tour.itinerary_json.length - 1"></div>
              </div>
              <div class="itinerary-day-content">
                <h3 class="itinerary-day-title">
                  <span class="itinerary-day-label">{{ $t('tours.day') || 'Day' }} {{ idx + 1 }}</span>
                  {{ day.title || day.location || '' }}
                </h3>
                <p class="itinerary-day-desc">{{ day.description || day.activities || '' }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Gallery / Images -->
        <div v-if="allImages.length > 1" class="tour-detail-body">
          <h2 class="tour-detail-section-title">📷 {{ $t('tours.gallery') || 'Gallery' }}</h2>
          <div class="tour-gallery-grid">
            <div v-for="(img, i) in allImages" :key="i" class="tour-gallery-item" @click="openLightbox(i)">
              <img :src="img" :alt="`${getField(tour, 'title')} photo ${i + 1}`" />
            </div>
          </div>
        </div>

        <!-- Lightbox -->
        <div v-if="lightboxOpen" class="tour-lightbox" @click.self="lightboxOpen = false">
          <button class="tour-lightbox-close" @click="lightboxOpen = false">✕</button>
          <button class="tour-lightbox-arrow left" @click.stop="lightboxIdx = (lightboxIdx - 1 + allImages.length) % allImages.length">◀</button>
          <img :src="allImages[lightboxIdx]" class="tour-lightbox-img" />
          <button class="tour-lightbox-arrow right" @click.stop="lightboxIdx = (lightboxIdx + 1) % allImages.length">▶</button>
          <div class="tour-lightbox-counter">{{ lightboxIdx + 1 }} / {{ allImages.length }}</div>
        </div>

        <!-- Book Now CTA -->
        <div style="text-align:center; padding:40px 0;" v-if="!showBooking">
          <button class="btn btn-primary btn-lg" @click="showBooking = true; $nextTick(() => scrollToBooking())">
            📋 {{ $t('booking.title') || 'Book This Tour' }}
          </button>
        </div>

        <!-- Booking Form (toggleable) -->
        <div v-if="showBooking" class="tour-booking-section" ref="bookingSection">
          <h2 class="tour-detail-section-title">📋 {{ $t('booking.title') || 'Book This Tour' }}</h2>
          <p style="color:var(--text-secondary); margin-bottom:24px; font-size:0.95rem;">
            <strong>{{ getField(tour, 'title') }}</strong> — €{{ tour.price }} / {{ $t('tours.perPerson') || 'person' }} · {{ tour.duration_days }} {{ $t('tours.days') || 'days' }}
          </p>

          <div v-if="submitSuccess" class="alert alert-success">
            ✅ {{ $t('booking.success') || 'Booking submitted successfully!' }}
          </div>
          <div v-if="submitError" class="alert alert-error">
            ❌ {{ submitError }}
          </div>

          <form v-if="!submitSuccess" @submit.prevent="handleSubmit" novalidate>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
              <div class="form-group">
                <label class="form-label">{{ $t('booking.name') || 'Full Name' }} *</label>
                <input v-model="form.customer_name" type="text" class="form-input" :class="{ error: errors.customer_name }" :placeholder="$t('booking.namePlaceholder') || 'Your full name'" />
                <p v-if="errors.customer_name" class="form-error">{{ $t('booking.required') || 'Required' }}</p>
              </div>
              <div class="form-group">
                <label class="form-label">{{ $t('booking.email') || 'Email' }} *</label>
                <input v-model="form.customer_email" type="email" class="form-input" :class="{ error: errors.customer_email }" :placeholder="$t('booking.emailPlaceholder') || 'your@email.com'" />
                <p v-if="errors.customer_email" class="form-error">{{ $t('booking.required') || 'Required' }}</p>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">{{ $t('booking.phone') || 'Phone' }}</label>
              <input v-model="form.customer_phone" type="tel" class="form-input" :placeholder="$t('booking.phonePlaceholder')" />
            </div>
            <div class="form-group">
              <label class="form-label">{{ $t('booking.message') || 'Message' }}</label>
              <textarea v-model="form.message" class="form-textarea" :placeholder="$t('booking.messagePlaceholder') || 'Any special requests...'" rows="4"></textarea>
            </div>
            <button type="submit" class="btn btn-primary" style="width:100%;" :disabled="isSubmitting">
              <span v-if="isSubmitting" class="spinner"></span>
              {{ isSubmitting ? ($t('booking.submitting') || 'Sending...') : ($t('booking.submit') || 'Send Booking Request') }}
            </button>
          </form>

          <button v-if="submitSuccess" class="btn btn-primary" style="width:100%; margin-top:16px;" @click="resetForm">
            {{ $t('booking.newBooking') || 'Book Again' }}
          </button>
        </div>

      </div>
    </section>
  </div>

  <!-- Loading state -->
  <div v-else class="section" style="text-align:center; padding:80px 20px;">
    <div class="spinner" style="width:32px; height:32px; border-width:3px;"></div>
    <p style="margin-top:16px; color:var(--text-secondary);">Loading tour...</p>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import api from '../api/axios.js'

const route = useRoute()
const { locale, t } = useI18n()
const tour = ref(null)
const showBooking = ref(false)
const bookingSection = ref(null)
const isSubmitting = ref(false)
const submitSuccess = ref(false)
const submitError = ref('')
const lightboxOpen = ref(false)
const lightboxIdx = ref(0)

const form = reactive({
  customer_name: '',
  customer_email: '',
  customer_phone: '',
  message: '',
})

const errors = reactive({
  customer_name: false,
  customer_email: false,
})

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function getField(obj, prefix) {
  return obj[`${prefix}_${locale.value}`] || obj[`${prefix}_en`] || ''
}

function formatDescription(text) {
  if (!text) return ''
  return text.replace(/\n/g, '<br>')
}

const allImages = computed(() => {
  if (!tour.value) return []
  const imgs = []
  if (tour.value.cover_image) imgs.push(tour.value.cover_image)
  if (tour.value.images_json) {
    tour.value.images_json.forEach(img => {
      if (!imgs.includes(img)) imgs.push(img)
    })
  }
  return imgs
})

const heroStyle = computed(() => {
  const img = allImages.value.length ? allImages.value[0] : null
  if (img) {
    return { backgroundImage: `linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.6)), url(${img})`, backgroundSize: 'cover', backgroundPosition: 'center' }
  }
  return { background: 'linear-gradient(135deg, #0f172a 0%, #1e3a5f 40%, #1a56db 100%)' }
})

function openLightbox(idx) {
  lightboxIdx.value = idx
  lightboxOpen.value = true
}

function scrollToBooking() {
  nextTick(() => {
    if (bookingSection.value) {
      bookingSection.value.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  })
}

function validate() {
  let valid = true
  errors.customer_name = !form.customer_name.trim()
  if (errors.customer_name) valid = false
  errors.customer_email = !form.customer_email.trim() || !emailRegex.test(form.customer_email)
  if (errors.customer_email) valid = false
  return valid
}

async function handleSubmit() {
  if (!validate()) return
  isSubmitting.value = true
  submitError.value = ''
  try {
    await api.post('/bookings/', {
      tour_id: tour.value.id,
      customer_name: form.customer_name.trim(),
      customer_email: form.customer_email.trim(),
      customer_phone: form.customer_phone.trim() || null,
      message: form.message.trim() || null,
      language: locale.value,
    })
    submitSuccess.value = true
  } catch (e) {
    submitError.value = e.response?.data?.detail || 'Failed to submit booking'
  } finally {
    isSubmitting.value = false
  }
}

function resetForm() {
  form.customer_name = ''
  form.customer_email = ''
  form.customer_phone = ''
  form.message = ''
  errors.customer_name = false
  errors.customer_email = false
  submitSuccess.value = false
  submitError.value = ''
}

onMounted(async () => {
  try {
    const res = await api.get(`/tours/${route.params.id}`)
    tour.value = res.data
  } catch (e) {
    console.error('Failed to load tour:', e)
  }
})
</script>
