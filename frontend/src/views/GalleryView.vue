<!--
  GalleryView.vue — Photo & Video Gallery with filter tabs + lightbox
-->
<template>
  <div>
    <div class="page-header">
      <h1>{{ $t('gallery.title') }}</h1>
    </div>
    <section class="section">
      <!-- Filter tabs -->
      <div style="display: flex; justify-content: center; gap: 8px; margin-bottom: 32px;">
        <button
          class="btn"
          :class="filter === 'all' ? 'btn-primary' : ''"
          :style="filter !== 'all' ? 'background: var(--gray-100); color: var(--gray-600);' : ''"
          @click="filter = 'all'"
        >{{ $t('gallery.filterAll') }}</button>
        <button
          class="btn"
          :class="filter === 'image' ? 'btn-primary' : ''"
          :style="filter !== 'image' ? 'background: var(--gray-100); color: var(--gray-600);' : ''"
          @click="filter = 'image'"
        >{{ $t('gallery.filterPhotos') }}</button>
        <button
          class="btn"
          :class="filter === 'video' ? 'btn-primary' : ''"
          :style="filter !== 'video' ? 'background: var(--gray-100); color: var(--gray-600);' : ''"
          @click="filter = 'video'"
        >{{ $t('gallery.filterVideos') }}</button>
      </div>

      <div class="gallery-grid container">
        <div
          v-for="item in filteredItems"
          :key="item.id"
          class="gallery-item"
          @click="item.media_type === 'image' ? openLightbox(item) : null"
        >
          <img
            v-if="item.media_type === 'image'"
            :src="item.url"
            :alt="getField(item, 'caption')"
            loading="lazy"
          />
          <video
            v-else
            :src="item.url"
            controls
            :poster="item.thumbnail_url"
          ></video>
          <div class="gallery-item-zoom" v-if="item.media_type === 'image'">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>
          </div>
        </div>
      </div>

      <p v-if="!filteredItems.length" style="text-align: center; color: var(--gray-400); padding: 40px;">
        No gallery items available.
      </p>
    </section>

    <!-- Lightbox -->
    <teleport to="body">
      <transition name="lightbox">
        <div v-if="lightboxItem" class="gallery-lightbox" @click.self="closeLightbox">
          <button class="gallery-lightbox-close" @click="closeLightbox">✕</button>
          <button class="gallery-lightbox-prev" @click="prevImage" v-if="imageItems.length > 1">‹</button>
          <img :src="lightboxItem.url" :alt="getField(lightboxItem, 'caption')" class="gallery-lightbox-img" />
          <button class="gallery-lightbox-next" @click="nextImage" v-if="imageItems.length > 1">›</button>
          <div class="gallery-lightbox-counter" v-if="imageItems.length > 1">
            {{ lightboxIndex + 1 }} / {{ imageItems.length }}
          </div>
        </div>
      </transition>
    </teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '../api/axios.js'

const { locale } = useI18n()
const items = ref([])
const filter = ref('all')
const lightboxItem = ref(null)
const lightboxIndex = ref(0)

const filteredItems = computed(() => {
  if (filter.value === 'all') return items.value
  return items.value.filter(item => item.media_type === filter.value)
})

const imageItems = computed(() => items.value.filter(item => item.media_type === 'image'))

function getField(obj, prefix) {
  return obj[`${prefix}_${locale.value}`] || obj[`${prefix}_en`] || ''
}

function openLightbox(item) {
  const idx = imageItems.value.findIndex(i => i.id === item.id)
  lightboxIndex.value = idx >= 0 ? idx : 0
  lightboxItem.value = item
  document.body.style.overflow = 'hidden'
}

function closeLightbox() {
  lightboxItem.value = null
  document.body.style.overflow = ''
}

function prevImage() {
  lightboxIndex.value = (lightboxIndex.value - 1 + imageItems.value.length) % imageItems.value.length
  lightboxItem.value = imageItems.value[lightboxIndex.value]
}

function nextImage() {
  lightboxIndex.value = (lightboxIndex.value + 1) % imageItems.value.length
  lightboxItem.value = imageItems.value[lightboxIndex.value]
}

function handleKeydown(e) {
  if (!lightboxItem.value) return
  if (e.key === 'Escape') closeLightbox()
  if (e.key === 'ArrowLeft') prevImage()
  if (e.key === 'ArrowRight') nextImage()
}

onMounted(async () => {
  document.addEventListener('keydown', handleKeydown)
  try {
    const res = await api.get('/gallery/')
    items.value = res.data
  } catch (e) {
    console.error('Failed to load gallery:', e)
  }
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>
