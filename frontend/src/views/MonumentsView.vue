<!--
  MonumentsView.vue — Historical Monuments of Uzbekistan
  Features: Hero section, city filter, monument cards with images,
  lightbox modal, smooth animations, i18n support.
-->
<template>
  <div>
    <!-- ═══ HERO ═══ -->
    <section class="monuments-hero">
      <div class="monuments-hero-overlay"></div>
      <div class="monuments-hero-content">
        <div class="monuments-hero-badge">🏛️ {{ $t('monuments.badge') }}</div>
        <h1>{{ $t('monuments.title') }}</h1>
        <p>{{ $t('monuments.subtitle') }}</p>
      </div>
      <!-- Decorative floating shapes -->
      <div class="monuments-hero-shape monuments-hero-shape--1"></div>
      <div class="monuments-hero-shape monuments-hero-shape--2"></div>
    </section>

    <!-- ═══ FILTER + GRID ═══ -->
    <section class="section">
      <!-- City Filter Tabs -->
      <div class="monuments-filters">
        <button
          v-for="city in cities"
          :key="city.value"
          class="monuments-filter-btn"
          :class="{ active: activeFilter === city.value }"
          @click="activeFilter = city.value"
        >
          <span class="monuments-filter-icon">{{ city.icon }}</span>
          {{ city.label }}
        </button>
      </div>

      <!-- Monuments Grid -->
      <div class="monuments-grid container">
        <transition-group name="monument-card" tag="div" class="monuments-grid-inner">
          <div
            v-for="(monument, index) in filteredMonuments"
            :key="monument.id"
            class="monument-card"
            :style="{ animationDelay: `${index * 80}ms` }"
            @click="openLightbox(monument)"
          >
            <div class="monument-card-image-wrapper">
              <img
                :src="monument.image"
                :alt="monument.name"
                class="monument-card-image"
                loading="lazy"
              />
              <div class="monument-card-overlay">
                <div class="monument-card-overlay-content">
                  <span class="monument-card-era">{{ monument.era }}</span>
                  <span class="monument-card-view-btn">{{ $t('monuments.viewMore') }} →</span>
                </div>
              </div>
              <div class="monument-card-city-badge">
                <span>📍</span> {{ monument.city }}
              </div>
            </div>
            <div class="monument-card-body">
              <h3 class="monument-card-title">{{ monument.name }}</h3>
              <p class="monument-card-desc">{{ monument.shortDesc }}</p>
            </div>
          </div>
        </transition-group>
      </div>

      <!-- Empty State -->
      <div v-if="!filteredMonuments.length" class="empty-state" style="text-align:center; padding:60px 20px;">
        <div class="empty-icon">🏛️</div>
        <p>{{ $t('monuments.noResults') }}</p>
      </div>
    </section>

    <!-- ═══ INFO SECTION ═══ -->
    <section class="monuments-info-section">
      <div class="monuments-info-inner container">
        <div class="monuments-info-text">
          <div class="section-line"></div>
          <h2>{{ $t('monuments.infoTitle') }}</h2>
          <p>{{ $t('monuments.infoDesc') }}</p>
          <div class="monuments-info-stats">
            <div class="monuments-info-stat">
              <span class="monuments-info-stat-num">7000+</span>
              <span class="monuments-info-stat-label">{{ $t('monuments.statMonuments') }}</span>
            </div>
            <div class="monuments-info-stat">
              <span class="monuments-info-stat-num">4</span>
              <span class="monuments-info-stat-label">{{ $t('monuments.statUnesco') }}</span>
            </div>
            <div class="monuments-info-stat">
              <span class="monuments-info-stat-num">2500+</span>
              <span class="monuments-info-stat-label">{{ $t('monuments.statYears') }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══ LIGHTBOX MODAL ═══ -->
    <teleport to="body">
      <transition name="lightbox">
        <div
          v-if="lightboxMonument"
          class="monument-lightbox"
          @click.self="closeLightbox"
        >
          <div class="monument-lightbox-inner">
            <button class="monument-lightbox-close" @click="closeLightbox">✕</button>
            <div class="monument-lightbox-image-wrapper">
              <img
                :src="lightboxMonument.image"
                :alt="lightboxMonument.name"
                class="monument-lightbox-image"
              />
            </div>
            <div class="monument-lightbox-info">
              <div class="monument-lightbox-city">
                <span>📍</span> {{ lightboxMonument.city }}
              </div>
              <h2>{{ lightboxMonument.name }}</h2>
              <div class="monument-lightbox-era">{{ lightboxMonument.era }}</div>
              <p>{{ lightboxMonument.fullDesc }}</p>
            </div>
          </div>
        </div>
      </transition>
    </teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const activeFilter = ref('all')
const lightboxMonument = ref(null)

const cities = computed(() => [
  { value: 'all', label: t('monuments.filterAll'), icon: '🌍' },
  { value: 'Samarkand', label: t('monuments.filterSamarkand'), icon: '🕌' },
  { value: 'Bukhara', label: t('monuments.filterBukhara'), icon: '🏰' },
  { value: 'Khiva', label: t('monuments.filterKhiva'), icon: '🏜️' },
  { value: 'Tashkent', label: t('monuments.filterTashkent'), icon: '🌆' },
  { value: 'Shakhrisabz', label: t('monuments.filterShakhrisabz'), icon: '⛰️' },
])

const monuments = computed(() => [
  {
    id: 'registon',
    name: t('monuments.registon'),
    city: 'Samarkand',
    era: t('monuments.era15_17'),
    image: '/monuments/registon.png',
    shortDesc: t('monuments.registonShort'),
    fullDesc: t('monuments.registonFull'),
  },
  {
    id: 'bibi_khanym',
    name: t('monuments.bibiKhanym'),
    city: 'Samarkand',
    era: t('monuments.era14'),
    image: '/monuments/bibi_khanym.png',
    shortDesc: t('monuments.bibiKhanymShort'),
    fullDesc: t('monuments.bibiKhanymFull'),
  },
  {
    id: 'ark_fortress',
    name: t('monuments.arkFortress'),
    city: 'Bukhara',
    era: t('monuments.era5'),
    image: '/monuments/ark_fortress.png',
    shortDesc: t('monuments.arkFortressShort'),
    fullDesc: t('monuments.arkFortressFull'),
  },
  {
    id: 'chor_minor',
    name: t('monuments.chorMinor'),
    city: 'Bukhara',
    era: t('monuments.era19'),
    image: '/monuments/chor_minor.png',
    shortDesc: t('monuments.chorMinorShort'),
    fullDesc: t('monuments.chorMinorFull'),
  },
  {
    id: 'ichan_kala',
    name: t('monuments.ichanKala'),
    city: 'Khiva',
    era: t('monuments.era10'),
    image: '/monuments/ichan_kala.png',
    shortDesc: t('monuments.ichanKalaShort'),
    fullDesc: t('monuments.ichanKalaFull'),
  },
  {
    id: 'ak_saray',
    name: t('monuments.akSaray'),
    city: 'Shakhrisabz',
    era: t('monuments.era14'),
    image: '/monuments/ak_saray.png',
    shortDesc: t('monuments.akSarayShort'),
    fullDesc: t('monuments.akSarayFull'),
  },
  {
    id: 'yassavi',
    name: t('monuments.yassavi'),
    city: 'Samarkand',
    era: t('monuments.era14'),
    image: '/monuments/yassavi.png',
    shortDesc: t('monuments.yassaviShort'),
    fullDesc: t('monuments.yassaviFull'),
  },
  {
    id: 'minor_mosque',
    name: t('monuments.minorMosque'),
    city: 'Tashkent',
    era: t('monuments.era21'),
    image: '/monuments/minor_mosque.png',
    shortDesc: t('monuments.minorMosqueShort'),
    fullDesc: t('monuments.minorMosqueFull'),
  },
  {
    id: 'shohizinda',
    name: t('monuments.shohizinda'),
    city: 'Samarkand',
    era: t('monuments.era14'),
    image: '/monuments/shohizinda.jpg',
    shortDesc: t('monuments.shohizindaShort'),
    fullDesc: t('monuments.shohizindaFull'),
  },
])

const filteredMonuments = computed(() => {
  if (activeFilter.value === 'all') return monuments.value
  return monuments.value.filter(m => m.city === activeFilter.value)
})

function openLightbox(monument) {
  lightboxMonument.value = monument
  document.body.style.overflow = 'hidden'
}

function closeLightbox() {
  lightboxMonument.value = null
  document.body.style.overflow = ''
}

function handleKeydown(e) {
  if (e.key === 'Escape') closeLightbox()
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
  document.body.style.overflow = ''
})
</script>
