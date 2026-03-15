<!--
  DestinationsView.vue — Detailed city destination pages
  Premium UI with hero cards, expandable content, and beautiful typography
-->
<template>
  <div class="destinations-page">
    <!-- ═══ HERO HEADER ═══ -->
    <section class="dest-hero">
      <div class="dest-hero-overlay"></div>
      <div class="dest-hero-content">
        <span class="dest-badge">{{ $t('destinations.badge') }}</span>
        <h1>{{ $t('destinations.title') }}</h1>
        <p>{{ $t('destinations.subtitle') }}</p>
      </div>
    </section>

    <!-- ═══ CITY CARDS GRID ═══ -->
    <section class="dest-section">
      <div class="dest-grid">
        <div
          v-for="city in cities"
          :key="city.key"
          class="city-card"
          :class="{ expanded: activeCity === city.key }"
        >
          <!-- Card Header (always visible) -->
          <div class="city-card-header" @click="toggleCity(city.key)">
            <div class="city-card-img" :style="{ backgroundImage: `url(${city.image})` }">
              <div class="city-card-img-overlay"></div>
              <div class="city-card-img-content">
                <span class="city-tagline">{{ city.tagline }}</span>
                <h2 class="city-name">{{ city.name }}</h2>
              </div>
            </div>
          </div>

          <!-- Card Body -->
          <div class="city-card-body">
            <p class="city-desc">{{ city.desc }}</p>
            <button class="city-toggle-btn" @click="toggleCity(city.key)">
              <span>{{ activeCity === city.key ? '▲' : $t('destinations.learnMore') + ' ▼' }}</span>
            </button>
          </div>

          <!-- Expandable Full Content -->
          <transition name="expand">
            <div v-if="activeCity === city.key" class="city-full-content">
              <div class="city-full-inner">
                <div class="city-full-text">
                  <p v-for="(paragraph, i) in city.full.split('\n\n')" :key="i" class="city-paragraph">
                    {{ paragraph }}
                  </p>
                </div>
                <div class="city-full-footer">
                  <router-link to="/monuments" class="btn btn-primary">
                    {{ $t('nav.monuments') }} →
                  </router-link>
                  <router-link to="/tours" class="btn btn-outline">
                    {{ $t('tours.viewDetails') }} →
                  </router-link>
                </div>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </section>

    <!-- ═══ CTA SECTION ═══ -->
    <section class="dest-cta">
      <h2>{{ $t('home.ctaTitle') }}</h2>
      <p>{{ $t('home.ctaDesc') }}</p>
      <router-link to="/tours" class="btn btn-white">{{ $t('hero.cta') }} →</router-link>
    </section>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const activeCity = ref(null)

function toggleCity(key) {
  activeCity.value = activeCity.value === key ? null : key
}

const cities = computed(() => [
  {
    key: 'samarkand',
    name: t('destinations.samarkandName'),
    tagline: t('destinations.samarkandTag'),
    desc: t('destinations.samarkandDesc'),
    full: t('destinations.samarkandFull'),
    image: '/monuments/registon.png',
  },
  {
    key: 'bukhara',
    name: t('destinations.bukharaName'),
    tagline: t('destinations.bukharaTag'),
    desc: t('destinations.bukharaDesc'),
    full: t('destinations.bukharaFull'),
    image: '/monuments/ark_fortress.png',
  },
  {
    key: 'khiva',
    name: t('destinations.khivaName'),
    tagline: t('destinations.khivaTag'),
    desc: t('destinations.khivaDesc'),
    full: t('destinations.khivaFull'),
    image: '/monuments/ichan_kala.png',
  },
  {
    key: 'tashkent',
    name: t('destinations.tashkentName'),
    tagline: t('destinations.tashkentTag'),
    desc: t('destinations.tashkentDesc'),
    full: t('destinations.tashkentFull'),
    image: '/monuments/minor_mosque.png',
  },
])
</script>

<style scoped>
/* ═══ HERO ═══ */
.dest-hero {
  position: relative;
  height: 50vh;
  min-height: 350px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: url('/monuments/hero_registan_pano.jpg') center/cover no-repeat;
  text-align: center;
  overflow: hidden;
}
.dest-hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(10, 25, 47, 0.85) 0%, rgba(30, 60, 90, 0.7) 100%);
}
.dest-hero-content {
  position: relative;
  z-index: 2;
  max-width: 700px;
  padding: 0 24px;
}
.dest-badge {
  display: inline-block;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  padding: 6px 20px;
  border-radius: 30px;
  font-size: 0.85rem;
  color: #f0c040;
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 16px;
  font-weight: 600;
}
.dest-hero-content h1 {
  font-size: clamp(2rem, 5vw, 3.2rem);
  color: #fff;
  margin: 0 0 16px;
  font-weight: 700;
  line-height: 1.2;
}
.dest-hero-content p {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.85);
  line-height: 1.6;
}

/* ═══ CITY SECTION ═══ */
.dest-section {
  max-width: 1100px;
  margin: 0 auto;
  padding: 60px 24px 40px;
}

.dest-grid {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

/* ═══ CITY CARD ═══ */
.city-card {
  background: #fff;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08), 0 1px 4px rgba(0, 0, 0, 0.04);
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}
.city-card:hover {
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.12), 0 2px 8px rgba(0, 0, 0, 0.06);
}
.city-card.expanded {
  box-shadow: 0 16px 56px rgba(0, 0, 0, 0.15);
}

.city-card-header {
  cursor: pointer;
  position: relative;
}

.city-card-img {
  height: 320px;
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  align-items: flex-end;
  transition: height 0.3s ease;
}
.city-card-img-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(0deg, rgba(0, 0, 0, 0.65) 0%, rgba(0, 0, 0, 0.1) 50%, transparent 100%);
}
.city-card-img-content {
  position: relative;
  z-index: 2;
  padding: 32px;
  width: 100%;
}
.city-tagline {
  display: inline-block;
  background: linear-gradient(135deg, #f0c040, #e8a820);
  color: #1a1a2e;
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 8px;
}
.city-name {
  font-size: 2rem;
  color: #fff;
  margin: 0;
  font-weight: 700;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.city-card-body {
  padding: 28px 32px 20px;
}
.city-desc {
  font-size: 1.02rem;
  line-height: 1.75;
  color: #3a3f5c;
  margin: 0 0 16px;
}
.city-toggle-btn {
  background: none;
  border: none;
  color: var(--primary, #2563eb);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  padding: 8px 0;
  transition: color 0.2s;
}
.city-toggle-btn:hover {
  color: var(--primary-dark, #1d4ed8);
}

/* ═══ EXPANDED CONTENT ═══ */
.city-full-content {
  overflow: hidden;
}
.city-full-inner {
  padding: 0 32px 32px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}
.city-full-text {
  padding-top: 24px;
}
.city-paragraph {
  font-size: 1.02rem;
  line-height: 1.85;
  color: #3a3f5c;
  margin: 0 0 18px;
  text-align: justify;
}
.city-paragraph:last-child {
  margin-bottom: 24px;
}
.city-full-footer {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  padding-top: 8px;
}

/* ═══ TRANSITION ═══ */
.expand-enter-active,
.expand-leave-active {
  transition: all 0.4s ease;
  max-height: 2000px;
  opacity: 1;
}
.expand-enter-from,
.expand-leave-to {
  max-height: 0;
  opacity: 0;
}

/* ═══ CTA ═══ */
.dest-cta {
  text-align: center;
  padding: 80px 24px;
  background: linear-gradient(135deg, #0a192f 0%, #1a3a5c 100%);
  color: #fff;
}
.dest-cta h2 {
  font-size: 2rem;
  margin: 0 0 12px;
  font-weight: 700;
}
.dest-cta p {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
  margin: 0 0 28px;
}
.btn-white {
  display: inline-block;
  background: #fff;
  color: #0a192f;
  padding: 14px 32px;
  border-radius: 10px;
  font-weight: 600;
  text-decoration: none;
  transition: transform 0.2s, box-shadow 0.2s;
}
.btn-white:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.2);
}

/* ═══ RESPONSIVE ═══ */
@media (max-width: 768px) {
  .dest-hero { height: 40vh; min-height: 280px; }
  .dest-section { padding: 40px 16px 24px; }
  .dest-grid { gap: 24px; }
  .city-card-img { height: 220px; }
  .city-card-img-content { padding: 20px; }
  .city-name { font-size: 1.5rem; }
  .city-card-body { padding: 20px; }
  .city-full-inner { padding: 0 20px 24px; }
  .dest-cta { padding: 60px 20px; }
}

/* ═══ DARK MODE ═══ */
:root[data-theme="dark"] .city-card {
  background: #1e2a3a;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
}
:root[data-theme="dark"] .city-desc,
:root[data-theme="dark"] .city-paragraph {
  color: #c8d0e0;
}
:root[data-theme="dark"] .city-full-inner {
  border-top-color: rgba(255, 255, 255, 0.08);
}
</style>
