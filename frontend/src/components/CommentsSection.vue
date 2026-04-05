<!--
  CommentsSection.vue
  -------------------
  Public comment / review section.
  Props:
    tourId (Number|null) — if provided, shows/saves comments for that tour.
  Features:
    - Write form: name, country (dropdown), description, optional image upload
    - Comments list: avatar initials, country flag, timeago, description, image
    - Skeleton loader + empty state
    - Responsive, glassmorphism design
-->
<template>
  <section class="comments-section">
    <!-- ── Section Header ── -->
    <div class="comments-header">
      <div class="comments-header-text">
        <h2 class="comments-title">
          <span class="comments-title-icon">💬</span>
          {{ $t('comments.title') }}
        </h2>
        <p class="comments-subtitle">{{ $t('comments.subtitle') }}</p>
      </div>
      <div v-if="comments.length" class="comments-count-badge">
        {{ comments.length }} {{ $t('comments.reviewCount', { n: comments.length }) }}
      </div>
    </div>

    <!-- ── Write Form ── -->
    <div class="comment-form-wrapper">
      <h3 class="comment-form-title">✏️ {{ $t('comments.writeTitle') }}</h3>

      <div v-if="submitSuccess" class="comment-alert comment-alert-success">
        ✅ {{ $t('comments.success') }}
      </div>
      <div v-if="submitError" class="comment-alert comment-alert-error">
        ❌ {{ submitError }}
      </div>

      <form v-if="!submitSuccess" @submit.prevent="handleSubmit" novalidate class="comment-form">
        <!-- Row 1: Name + Country -->
        <div class="comment-form-row">
          <div class="comment-form-group">
            <label class="comment-form-label">
              {{ $t('comments.name') }} <span class="required-star">*</span>
            </label>
            <input
              v-model="form.author_name"
              type="text"
              class="comment-form-input"
              :class="{ 'input-error': errors.author_name }"
              :placeholder="$t('comments.namePlaceholder')"
              maxlength="100"
            />
            <span v-if="errors.author_name" class="comment-form-error">
              {{ $t('comments.required') }}
            </span>
          </div>

          <div class="comment-form-group">
            <label class="comment-form-label">
              {{ $t('comments.country') }} <span class="required-star">*</span>
            </label>
            <div class="comment-country-select-wrapper">
              <select
                v-model="form.country"
                class="comment-form-input comment-form-select"
                :class="{ 'input-error': errors.country }"
              >
                <option value="" disabled>{{ $t('comments.countryPlaceholder') }}</option>
                <option v-for="c in countries" :key="c.name" :value="c.name">
                  {{ c.flag }} {{ c.name }}
                </option>
              </select>
              <span v-if="form.country" class="comment-country-flag">
                {{ getFlag(form.country) }}
              </span>
            </div>
            <span v-if="errors.country" class="comment-form-error">
              {{ $t('comments.required') }}
            </span>
          </div>
        </div>

        <!-- Row 2: Description -->
        <div class="comment-form-group">
          <label class="comment-form-label">
            {{ $t('comments.description') }} <span class="required-star">*</span>
          </label>
          <textarea
            v-model="form.description"
            class="comment-form-textarea"
            :class="{ 'input-error': errors.description }"
            :placeholder="$t('comments.descriptionPlaceholder')"
            rows="4"
            maxlength="1000"
          ></textarea>
          <div class="comment-char-row">
            <span v-if="errors.description" class="comment-form-error">
              {{ $t('comments.required') }}
            </span>
            <span class="comment-char-count">{{ form.description.length }}/1000</span>
          </div>
        </div>

        <!-- Row 3: Image Upload (optional) -->
        <div class="comment-form-group">
          <label class="comment-form-label">📷 {{ $t('comments.image') }}</label>
          <div
            class="comment-upload-area"
            :class="{ 'has-image': imagePreview }"
            @click="$refs.fileInput.click()"
            @dragover.prevent
            @drop.prevent="handleDrop"
          >
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              class="comment-file-input"
              @change="handleFileChange"
            />
            <template v-if="!imagePreview">
              <div class="comment-upload-icon">🖼️</div>
              <p class="comment-upload-hint">{{ $t('comments.imageHint') }}</p>
            </template>
            <template v-else>
              <img :src="imagePreview" class="comment-image-preview" :alt="$t('comments.imagePreview')" />
              <button
                type="button"
                class="comment-remove-image"
                @click.stop="removeImage"
              >✕ {{ $t('comments.removeImage') }}</button>
            </template>
            <div v-if="isUploading" class="comment-upload-progress">
              <span class="spinner" style="border-color:var(--primary);border-top-color:transparent;"></span>
              {{ $t('comments.uploading') }}
            </div>
          </div>
        </div>

        <!-- Submit -->
        <button type="submit" class="btn btn-primary comment-submit-btn" :disabled="isSubmitting || isUploading">
          <span v-if="isSubmitting" class="spinner"></span>
          {{ isSubmitting ? $t('comments.submitting') : $t('comments.submit') }}
        </button>
      </form>

      <button v-if="submitSuccess" class="btn btn-primary" @click="resetForm" style="margin-top:12px;">
        ✏️ {{ $t('comments.writeTitle') }}
      </button>
    </div>

    <!-- ── Comments List ── -->
    <div class="comments-list">
      <!-- Skeleton Loading -->
      <template v-if="isLoading">
        <div v-for="i in 3" :key="i" class="comment-card comment-card-skeleton">
          <div class="skeleton-avatar"></div>
          <div class="skeleton-content">
            <div class="skeleton-line short"></div>
            <div class="skeleton-line medium"></div>
            <div class="skeleton-line long"></div>
          </div>
        </div>
      </template>

      <!-- Empty State -->
      <div v-else-if="!isLoading && !comments.length" class="comments-empty">
        <div class="comments-empty-icon">🌍</div>
        <h4>{{ $t('comments.noComments') }}</h4>
        <p>{{ $t('comments.noCommentsDesc') }}</p>
      </div>

      <!-- Actual Comments -->
      <TransitionGroup v-else name="comment-list" tag="div" class="comments-cards">
        <article
          v-for="comment in comments"
          :key="comment.id"
          class="comment-card"
        >
          <div class="comment-card-left">
            <div class="comment-avatar" :style="{ background: avatarColor(comment.author_name) }">
              {{ initials(comment.author_name) }}
            </div>
          </div>
          <div class="comment-card-body">
            <div class="comment-card-header">
              <div class="comment-author-info">
                <span class="comment-author-name">{{ comment.author_name }}</span>
                <span class="comment-country">
                  {{ getFlag(comment.country) }} {{ comment.country }}
                </span>
              </div>
              <time class="comment-time" :title="formatDateTime(comment.created_at)">
                {{ timeAgo(comment.created_at) }}
              </time>
            </div>
            <p class="comment-description">{{ comment.description }}</p>
            <div v-if="comment.image_url" class="comment-image-wrap" @click="openLightbox(comment.image_url)">
              <img :src="comment.image_url" class="comment-img" :alt="`${comment.author_name} photo`" />
              <div class="comment-img-overlay">🔍</div>
            </div>
          </div>
        </article>
      </TransitionGroup>
    </div>

    <!-- Image lightbox -->
    <div v-if="lightboxUrl" class="comment-lightbox" @click="lightboxUrl = null">
      <button class="comment-lightbox-close" @click="lightboxUrl = null">✕</button>
      <img :src="lightboxUrl" class="comment-lightbox-img" @click.stop />
    </div>
  </section>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '../api/axios.js'

const props = defineProps({
  tourId: { type: Number, default: null }
})

const { t } = useI18n()

// ── State ────────────────────────────────────────────────────────
const comments = ref([])
const isLoading = ref(true)
const isSubmitting = ref(false)
const isUploading = ref(false)
const submitSuccess = ref(false)
const submitError = ref('')
const imagePreview = ref(null)
const imageUrl = ref(null)
const fileInput = ref(null)
const lightboxUrl = ref(null)

const form = reactive({
  author_name: '',
  country: '',
  description: '',
})
const errors = reactive({ author_name: false, country: false, description: false })

// ── Country list ─────────────────────────────────────────────────
const countries = [
  { name: 'Uzbekistan', flag: '🇺🇿' },
  { name: 'Russia', flag: '🇷🇺' },
  { name: 'France', flag: '🇫🇷' },
  { name: 'Germany', flag: '🇩🇪' },
  { name: 'United Kingdom', flag: '🇬🇧' },
  { name: 'United States', flag: '🇺🇸' },
  { name: 'China', flag: '🇨🇳' },
  { name: 'Japan', flag: '🇯🇵' },
  { name: 'South Korea', flag: '🇰🇷' },
  { name: 'Turkey', flag: '🇹🇷' },
  { name: 'Kazakhstan', flag: '🇰🇿' },
  { name: 'Italy', flag: '🇮🇹' },
  { name: 'Spain', flag: '🇪🇸' },
  { name: 'Poland', flag: '🇵🇱' },
  { name: 'Netherlands', flag: '🇳🇱' },
  { name: 'Canada', flag: '🇨🇦' },
  { name: 'Australia', flag: '🇦🇺' },
  { name: 'India', flag: '🇮🇳' },
  { name: 'UAE', flag: '🇦🇪' },
  { name: 'Saudi Arabia', flag: '🇸🇦' },
  { name: 'Iran', flag: '🇮🇷' },
  { name: 'Israel', flag: '🇮🇱' },
  { name: 'Thailand', flag: '🇹🇭' },
  { name: 'Malaysia', flag: '🇲🇾' },
  { name: 'Switzerland', flag: '🇨🇭' },
  { name: 'Sweden', flag: '🇸🇪' },
  { name: 'Belgium', flag: '🇧🇪' },
  { name: 'Austria', flag: '🇦🇹' },
  { name: 'Czech Republic', flag: '🇨🇿' },
  { name: 'Brazil', flag: '🇧🇷' },
  { name: 'Argentina', flag: '🇦🇷' },
  { name: 'Mexico', flag: '🇲🇽' },
  { name: 'Tajikistan', flag: '🇹🇯' },
  { name: 'Kyrgyzstan', flag: '🇰🇬' },
  { name: 'Turkmenistan', flag: '🇹🇲' },
  { name: 'Azerbaijan', flag: '🇦🇿' },
  { name: 'Georgia', flag: '🇬🇪' },
  { name: 'Ukraine', flag: '🇺🇦' },
  { name: 'Other', flag: '🌍' },
]

const flagMap = Object.fromEntries(countries.map(c => [c.name, c.flag]))

function getFlag(country) {
  return flagMap[country] || '🌍'
}

// ── Avatar helpers ───────────────────────────────────────────────
const AVATAR_COLORS = [
  '#2563eb', '#7c3aed', '#db2777', '#059669', '#d97706',
  '#dc2626', '#0891b2', '#65a30d', '#c026d3', '#0369a1',
]
function avatarColor(name) {
  let hash = 0
  for (const ch of name) hash = (hash * 31 + ch.charCodeAt(0)) & 0xffffffff
  return AVATAR_COLORS[Math.abs(hash) % AVATAR_COLORS.length]
}
function initials(name) {
  return name.split(' ').map(w => w[0]?.toUpperCase() || '').slice(0, 2).join('')
}

// ── Time formatting ──────────────────────────────────────────────
function timeAgo(dateStr) {
  if (!dateStr) return ''
  const diff = Math.floor((Date.now() - new Date(dateStr).getTime()) / 1000)
  if (diff < 60) return t('comments.justNow')
  if (diff < 3600) return t('comments.minutesAgo', { n: Math.floor(diff / 60) })
  if (diff < 86400) return t('comments.hoursAgo', { n: Math.floor(diff / 3600) })
  return t('comments.daysAgo', { n: Math.floor(diff / 86400) })
}
function formatDateTime(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString()
}

// ── Image handling ───────────────────────────────────────────────
function handleFileChange(e) {
  const file = e.target.files?.[0]
  if (file) processFile(file)
}
function handleDrop(e) {
  const file = e.dataTransfer.files?.[0]
  if (file && file.type.startsWith('image/')) processFile(file)
}
function processFile(file) {
  const reader = new FileReader()
  reader.onload = (e) => { imagePreview.value = e.target.result }
  reader.readAsDataURL(file)
  uploadFile(file)
}
async function uploadFile(file) {
  isUploading.value = true
  try {
    const fd = new FormData()
    fd.append('file', file)
    const res = await api.post('/comments/upload-image/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    imageUrl.value = res.data.url || null
  } catch (e) {
    console.error('Upload failed:', e)
    imageUrl.value = null
  } finally {
    isUploading.value = false
  }
}
function removeImage() {
  imagePreview.value = null
  imageUrl.value = null
  if (fileInput.value) fileInput.value.value = ''
}

// ── Lightbox ─────────────────────────────────────────────────────
function openLightbox(url) {
  lightboxUrl.value = url
}

// ── Form ─────────────────────────────────────────────────────────
function validate() {
  errors.author_name = !form.author_name.trim()
  errors.country = !form.country
  errors.description = !form.description.trim()
  return !errors.author_name && !errors.country && !errors.description
}

async function handleSubmit() {
  if (!validate()) return
  isSubmitting.value = true
  submitError.value = ''
  try {
    const payload = {
      author_name: form.author_name.trim(),
      country: form.country,
      description: form.description.trim(),
      tour_id: props.tourId || null,
      image_url: imageUrl.value || null,
    }
    const res = await api.post('/comments/', payload)
    comments.value.unshift(res.data)
    submitSuccess.value = true
  } catch (e) {
    submitError.value = e.response?.data?.detail || t('comments.error')
  } finally {
    isSubmitting.value = false
  }
}

function resetForm() {
  form.author_name = ''
  form.country = ''
  form.description = ''
  errors.author_name = false
  errors.country = false
  errors.description = false
  submitSuccess.value = false
  submitError.value = ''
  removeImage()
}

// ── Load comments ────────────────────────────────────────────────
async function loadComments() {
  isLoading.value = true
  try {
    const params = props.tourId ? { tour_id: props.tourId } : {}
    const res = await api.get('/comments/', { params })
    comments.value = res.data
  } catch (e) {
    console.error('Failed to load comments:', e)
  } finally {
    isLoading.value = false
  }
}

onMounted(loadComments)
</script>
