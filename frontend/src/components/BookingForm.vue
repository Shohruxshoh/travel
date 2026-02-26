<!--
  BookingForm.vue
  ─────────────────────────────────────────────────────────────────
  The main booking form component.
  
  KEY FEATURE: Smart Email Routing Integration
  ─────────────────────────────────────────────
  1. Uses vue-i18n's `useI18n()` to get the current locale.
  2. Includes the locale in the booking payload as `language`.
  3. Also sends the locale via the `Accept-Language` header (Axios interceptor).
  4. The backend uses this `language` to route notification emails
     to the correct language-specific operator.
-->
<template>
  <section class="booking-section" id="booking-form">
    <div class="container">
      <h2 class="section-title">{{ t('booking.title') }}</h2>
      <p class="section-subtitle">{{ t('booking.subtitle') }}</p>

      <div class="booking-form-wrapper">
        <!-- Success message -->
        <div v-if="store.submitSuccess" class="alert alert-success">
          ✅ {{ t('booking.success') }}
        </div>

        <!-- Error message -->
        <div v-if="store.submitError" class="alert alert-error">
          ❌ {{ store.submitError }}
        </div>

        <form v-if="!store.submitSuccess" @submit.prevent="handleSubmit" novalidate>
          <!-- Tour selection -->
          <div class="form-group">
            <label class="form-label" for="booking-tour">{{ t('booking.tour') }}</label>
            <select
              id="booking-tour"
              v-model="form.tour_id"
              class="form-select"
              :class="{ error: errors.tour_id }"
            >
              <option value="" disabled>{{ t('booking.tourPlaceholder') }}</option>
              <option
                v-for="tour in store.tours"
                :key="tour.id"
                :value="tour.id"
              >
                {{ getLocalizedField(tour, 'title') }} — ${{ tour.price }}
              </option>
            </select>
            <p v-if="errors.tour_id" class="form-error">{{ t('booking.required') }}</p>
          </div>

          <!-- Customer name -->
          <div class="form-group">
            <label class="form-label" for="booking-name">{{ t('booking.name') }}</label>
            <input
              id="booking-name"
              v-model="form.customer_name"
              type="text"
              class="form-input"
              :class="{ error: errors.customer_name }"
              :placeholder="t('booking.namePlaceholder')"
            />
            <p v-if="errors.customer_name" class="form-error">{{ t('booking.required') }}</p>
          </div>

          <!-- Customer email -->
          <div class="form-group">
            <label class="form-label" for="booking-email">{{ t('booking.email') }}</label>
            <input
              id="booking-email"
              v-model="form.customer_email"
              type="email"
              class="form-input"
              :class="{ error: errors.customer_email }"
              :placeholder="t('booking.emailPlaceholder')"
            />
            <p v-if="errors.customer_email" class="form-error">
              {{ emailErrorMessage }}
            </p>
          </div>

          <!-- Customer phone -->
          <div class="form-group">
            <label class="form-label" for="booking-phone">{{ t('booking.phone') }}</label>
            <input
              id="booking-phone"
              v-model="form.customer_phone"
              type="tel"
              class="form-input"
              :placeholder="t('booking.phonePlaceholder')"
            />
          </div>

          <!-- Message -->
          <div class="form-group">
            <label class="form-label" for="booking-message">{{ t('booking.message') }}</label>
            <textarea
              id="booking-message"
              v-model="form.message"
              class="form-textarea"
              :placeholder="t('booking.messagePlaceholder')"
              rows="4"
            ></textarea>
          </div>

          <!-- Submit button -->
          <button
            type="submit"
            class="btn btn-primary"
            style="width: 100%"
            :disabled="store.isSubmitting"
          >
            <span v-if="store.isSubmitting" class="spinner"></span>
            {{ store.isSubmitting ? t('booking.submitting') : t('booking.submit') }}
          </button>
        </form>

        <!-- Reset button after success -->
        <button
          v-if="store.submitSuccess"
          class="btn btn-primary"
          style="width: 100%; margin-top: 16px"
          @click="resetForm"
        >
          {{ t('booking.submit') }}
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
/**
 * BookingForm.vue — Script Setup (Composition API)
 *
 * This component is the heart of the smart email routing feature.
 * When the user submits a booking:
 *   1. `locale.value` (from vue-i18n) provides the current language.
 *   2. This language code is included in the POST payload as `language`.
 *   3. The FastAPI backend reads `language` and dispatches a Celery task
 *      that routes the notification email to the correct operator.
 */
import { ref, reactive, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useBookingStore } from '../stores/booking.js'

const { t, locale } = useI18n()
const store = useBookingStore()

// ── Form state ──────────────────────────────────────────────────
const form = reactive({
  tour_id: '',
  customer_name: '',
  customer_email: '',
  customer_phone: '',
  message: '',
})

const errors = reactive({
  tour_id: false,
  customer_name: false,
  customer_email: false,
})

// ── Email validation ────────────────────────────────────────────
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

const emailErrorMessage = computed(() => {
  if (!form.customer_email) return t('booking.required')
  if (!emailRegex.test(form.customer_email)) return t('booking.invalidEmail')
  return ''
})

// ── Helper: get localized field from tour object ────────────────
function getLocalizedField(obj, fieldPrefix) {
  const key = `${fieldPrefix}_${locale.value}`
  return obj[key] || obj[`${fieldPrefix}_en`] || ''
}

// ── Form validation ─────────────────────────────────────────────
function validate() {
  let isValid = true

  errors.tour_id = !form.tour_id
  if (errors.tour_id) isValid = false

  errors.customer_name = !form.customer_name.trim()
  if (errors.customer_name) isValid = false

  errors.customer_email =
    !form.customer_email.trim() || !emailRegex.test(form.customer_email)
  if (errors.customer_email) isValid = false

  return isValid
}

// ── Submit handler ──────────────────────────────────────────────
async function handleSubmit() {
  if (!validate()) return

  // CRITICAL: Include the current locale as the 'language' field.
  // This value drives the smart email routing on the backend.
  await store.submitBooking({
    tour_id: Number(form.tour_id),
    customer_name: form.customer_name.trim(),
    customer_email: form.customer_email.trim(),
    customer_phone: form.customer_phone.trim() || null,
    message: form.message.trim() || null,
    language: locale.value,  // ← The key field for email routing
  })
}

// ── Reset form ──────────────────────────────────────────────────
function resetForm() {
  form.tour_id = ''
  form.customer_name = ''
  form.customer_email = ''
  form.customer_phone = ''
  form.message = ''
  errors.tour_id = false
  errors.customer_name = false
  errors.customer_email = false
  store.resetState()
}

// ── Load available tours on mount ───────────────────────────────
onMounted(() => {
  store.fetchTours()
})
</script>
