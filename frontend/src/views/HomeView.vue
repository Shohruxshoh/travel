<!--
  HomeView.vue — Professional travel agency homepage
  Premium UI/UX: Full-screen hero with real Uzbekistan photos,
  scroll indicator, engaging sections, mobile-first responsive.
-->
<template>
  <div class="home-page">
    <!-- ═══ 1. HERO CAROUSEL ═══ -->
    <section class="hero-carousel">
      <div
        v-for="(slide, i) in heroSlides"
        :key="i"
        class="hero-slide"
        :class="{ active: currentSlide === i }"
      >
        <img
          :src="slide.image"
          :alt="slide.title"
          class="hero-slide-img"
          loading="eager"
        />
        <div class="hero-slide-overlay"></div>
        <div class="hero-content">
          <div class="hero-label">{{ slide.label }}</div>
          <h1>{{ slide.title }}</h1>
          <p>{{ slide.subtitle }}</p>
          <div class="hero-btns">
            <router-link to="/tours" class="btn btn-accent">{{ $t('hero.cta') }}</router-link>
            <router-link to="/monuments" class="btn btn-hero-outline">{{ $t('nav.monuments') }}</router-link>
          </div>
        </div>
      </div>
      <!-- Arrows -->
      <div class="hero-arrows">
        <button class="hero-arrow" @click="prevSlide">◀</button>
        <button class="hero-arrow" @click="nextSlide">▶</button>
      </div>
      <!-- Dots -->
      <div class="hero-dots">
        <button
          v-for="(_, i) in heroSlides"
          :key="i"
          class="hero-dot"
          :class="{ active: currentSlide === i }"
          @click="currentSlide = i"
        ></button>
      </div>
      <!-- Scroll Indicator -->
      <div class="hero-scroll-indicator" @click="scrollToContent">
        <span class="hero-scroll-text">{{ $t('home.scrollDown') || 'Scroll' }}</span>
        <span class="hero-scroll-arrow">↓</span>
      </div>
    </section>

    <!-- ═══ 2. FEATURED TOURS ═══ -->
    <section class="section" ref="contentSection">
      <div class="section-header">
        <div class="section-line"></div>
        <h2>{{ $t('home.featuredTours') }}</h2>
        <p>{{ $t('home.featuredToursDesc') }}</p>
      </div>
      <div class="card-grid container">
        <router-link v-for="tour in tours" :key="tour.id" :to="`/tours/${tour.id}`" class="card" style="position:relative; text-decoration:none; color:inherit;">
          <div class="card-image-wrapper">
            <div
              class="card-image"
              :style="tour.cover_image
                ? { backgroundImage: `url(${tour.cover_image})`, backgroundSize:'cover', backgroundPosition:'center' }
                : (tour.images_json?.length
                  ? { backgroundImage: `url(${tour.images_json[0]})`, backgroundSize:'cover', backgroundPosition:'center' }
                  : {})"
            ></div>
          </div>
          <div class="card-body">
            <h3 class="card-title">{{ getField(tour, 'title') }}</h3>
            <div class="card-meta">
              <span>📅 {{ tour.duration_days }} {{ $t('tours.duration') }}</span>
              <span>📍 {{ tour.destination }}</span>
            </div>
            <p class="card-text">{{ truncate(getField(tour, 'description'), 100) }}</p>
            <div class="card-footer">
              <span class="card-price">
                <template v-if="tour.is_negotiable">
                  <span style="background:linear-gradient(135deg,#f59e0b,#ef4444);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:700;">{{ $t('tours.negotiable') }}</span>
                </template>
                <template v-else>€{{ tour.price }} <small>/ {{ $t('tours.perPerson') }}</small></template>
              </span>
              <span class="btn btn-primary btn-sm">{{ $t('tours.viewDetails') }}</span>
            </div>
          </div>
        </router-link>
      </div>
      <div v-if="!tours.length" class="empty-state">
        <div class="empty-icon">🗺️</div>
        <p>{{ $t('home.noTours') }}</p>
      </div>
      <div style="text-align:center; margin-top:40px;" v-if="tours.length">
        <router-link to="/tours" class="btn btn-outline">{{ $t('home.viewAllTours') }} →</router-link>
      </div>
    </section>

    <!-- ═══ 3. POPULAR DESTINATIONS ═══ -->
    <section class="section section-alt">
      <div class="section-header">
        <div class="section-line"></div>
        <h2>{{ $t('home.destinations') }}</h2>
        <p>{{ $t('home.destinationsDesc') }}</p>
      </div>
      <div class="dest-grid container">
        <div
          v-for="dest in destinations"
          :key="dest.name"
          class="dest-card"
          :style="{ backgroundImage: `url(${dest.image})` }"
          @click="openDestModal(dest)"
        >
          <div class="dest-overlay"></div>
          <div class="dest-info">
            <span class="dest-tagline">{{ dest.tagline }}</span>
            <h3>{{ dest.name }}</h3>
            <span class="dest-explore-btn">{{ $t('home.explore') || 'Explore' }} →</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Destination Info Modal -->
    <teleport to="body">
      <transition name="lightbox">
        <div v-if="activeDest" class="dest-modal" @click.self="closeDestModal">
          <div class="dest-modal-inner">
            <button class="dest-modal-close" @click="closeDestModal">✕</button>
            <div class="dest-modal-img">
              <img :src="activeDest.image" :alt="activeDest.name" />
            </div>
            <div class="dest-modal-body">
              <span class="dest-modal-tagline">{{ activeDest.tagline }}</span>
              <h2>{{ activeDest.name }}</h2>
              <p class="dest-modal-desc">{{ activeDest.description }}</p>
              <div v-if="activeDest.fullText" class="dest-modal-full">
                <p v-for="(paragraph, i) in activeDest.fullText.split('\n\n')" :key="i" class="dest-modal-paragraph">
                  {{ paragraph }}
                </p>
              </div>
              <div class="dest-modal-highlights">
                <div v-for="h in activeDest.highlights" :key="h" class="dest-modal-highlight">
                  <span class="dest-highlight-icon">✦</span>
                  {{ h }}
                </div>
              </div>
              <router-link to="/monuments" class="btn btn-primary" @click="closeDestModal">
                {{ $t('nav.monuments') }} →
              </router-link>
            </div>
          </div>
        </div>
      </transition>
    </teleport>

    <!-- ═══ 4. OUR SERVICES ═══ -->
    <section class="section">
      <div class="section-header">
        <div class="section-line"></div>
        <h2>{{ $t('home.whyChoose') }}</h2>
        <p>{{ $t('home.whyChooseDesc') }}</p>
      </div>
      <div class="services-grid container">
        <div v-for="svc in serviceItems" :key="svc.icon" class="service-card">
          <div class="service-icon"><span>{{ svc.icon }}</span></div>
          <h3>{{ svc.title }}</h3>
          <p>{{ svc.desc }}</p>
        </div>
      </div>
    </section>

    <!-- ═══ 5. STATS COUNTER BAR ═══ -->
    <section class="stats-bar">
      <div class="stats-bar-inner">
        <div class="stat-item" v-for="s in statsItems" :key="s.label">
          <div class="stat-num">{{ s.value }}</div>
          <div class="stat-label">{{ s.label }}</div>
        </div>
      </div>
    </section>

    <!-- ═══ 6. TESTIMONIALS ═══ -->
    <section class="section">
      <div class="section-header">
        <div class="section-line"></div>
        <h2>{{ $t('home.testimonials') }}</h2>
        <p>{{ $t('home.testimonialsDesc') }}</p>
      </div>
      <div class="testimonials-grid container">
        <div v-for="t in testimonials" :key="t.name" class="testimonial-card">
          <div class="testimonial-stars">{{ '★'.repeat(t.stars) }}</div>
          <p class="testimonial-text">"{{ t.text }}"</p>
          <div class="testimonial-author">
            <div class="testimonial-avatar">{{ t.name.charAt(0) }}</div>
            <div class="testimonial-info">
              <h4>{{ t.name }}</h4>
              <p>{{ t.location }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══ 7. CTA SECTION ═══ -->
    <section class="cta-section">
      <h2>{{ $t('home.ctaTitle') }}</h2>
      <p>{{ $t('home.ctaDesc') }}</p>
      <a href="#booking-form" class="btn btn-white">{{ $t('hero.cta') }} →</a>
    </section>

    <!-- ═══ 8. BOOKING FORM ═══ -->
    <BookingForm />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '../api/axios.js'
import BookingForm from '../components/BookingForm.vue'

const { locale, t } = useI18n()
const tours = ref([])
const currentSlide = ref(0)
const contentSection = ref(null)
let slideTimer = null

// ─── Hero Slides — Real Uzbekistan Photos ───
const heroSlides = computed(() => [
  {
    image: '/monuments/hero_khiva.jpg',
    label: 'Adventure Travel Time',
    title: t('hero.title'),
    subtitle: t('hero.subtitle'),
  },
  {
    image: '/monuments/hero_registan.jpg',
    label: t('home.silkRoad'),
    title: t('home.slide2Title'),
    subtitle: t('home.slide2Desc'),
  },
  {
    image: '/monuments/hero_registan_pano.jpg',
    label: t('home.explore'),
    title: t('home.slide3Title'),
    subtitle: t('home.slide3Desc'),
  },
])

// ─── Destinations with City Info ───
const activeDest = ref(null)

function openDestModal(dest) {
  activeDest.value = dest
  document.body.style.overflow = 'hidden'
}

function closeDestModal() {
  activeDest.value = null
  document.body.style.overflow = ''
}

const destinations = computed(() => [
  {
    name: t('home.destSamarkand'),
    tagline: t('home.destSamarkandTag'),
    description: t('destinations.samarkandDesc'),
    fullText: t('destinations.samarkandFull'),
    image: '/monuments/registon.png',
    highlights: [
      t('home.destSamarkandH1'),
      t('home.destSamarkandH2'),
      t('home.destSamarkandH3'),
    ],
  },
  {
    name: t('home.destBukhara'),
    tagline: t('home.destBukharaTag'),
    description: t('destinations.bukharaDesc'),
    fullText: t('destinations.bukharaFull'),
    image: '/monuments/ark_fortress.png',
    highlights: [
      t('home.destBukharaH1'),
      t('home.destBukharaH2'),
      t('home.destBukharaH3'),
    ],
  },
  {
    name: t('home.destKhiva'),
    tagline: t('home.destKhivaTag'),
    description: t('destinations.khivaDesc'),
    fullText: t('destinations.khivaFull'),
    image: '/monuments/ichan_kala.png',
    highlights: [
      t('home.destKhivaH1'),
      t('home.destKhivaH2'),
      t('home.destKhivaH3'),
    ],
  },
  {
    name: t('home.destTashkent'),
    tagline: t('home.destTashkentTag'),
    description: t('destinations.tashkentDesc'),
    fullText: t('destinations.tashkentFull'),
    image: '/monuments/minor_mosque.png',
    highlights: [
      t('home.destTashkentH1'),
      t('home.destTashkentH2'),
      t('home.destTashkentH3'),
    ],
  },
])

// ─── Services Data ───
const serviceItems = computed(() => [
  { icon: '🗺️', title: t('home.svcTour'), desc: t('home.svcTourDesc') },
  { icon: '🏨', title: t('home.svcHotel'), desc: t('home.svcHotelDesc') },
  { icon: '📋', title: t('home.svcVisa'), desc: t('home.svcVisaDesc') },
  { icon: '🚗', title: t('home.svcTransfer'), desc: t('home.svcTransferDesc') },
  { icon: '🛡️', title: t('home.svcInsurance'), desc: t('home.svcInsuranceDesc') },
  { icon: '🎧', title: t('home.svcSupport'), desc: t('home.svcSupportDesc') },
])

// ─── Stats Data ───
const statsItems = computed(() => [
  { value: '500+', label: t('home.statTours') },
  { value: '10K+', label: t('home.statClients') },
  { value: '50+', label: t('home.statDests') },
  { value: '15+', label: t('home.statYears') },
])

// ─── Testimonials Data ───
const testimonials = computed(() => [
  { name: 'Sarah Johnson', location: 'London, UK', stars: 5, text: t('home.review1') },
  { name: 'Pierre Dubois', location: 'Paris, France', stars: 5, text: t('home.review2') },
  { name: 'Иван Петров', location: 'Москва, Россия', stars: 5, text: t('home.review3') },
])

function getField(obj, prefix) {
  return obj[`${prefix}_${locale.value}`] || obj[`${prefix}_en`] || ''
}
function truncate(str, len) {
  return str.length > len ? str.slice(0, len) + '...' : str
}
function nextSlide() {
  currentSlide.value = (currentSlide.value + 1) % heroSlides.value.length
}
function prevSlide() {
  currentSlide.value = (currentSlide.value - 1 + heroSlides.value.length) % heroSlides.value.length
}
function scrollToContent() {
  contentSection.value?.scrollIntoView({ behavior: 'smooth' })
}

onMounted(async () => {
  slideTimer = setInterval(nextSlide, 5000)
  try {
    const res = await api.get('/tours/')
    tours.value = res.data.slice(0, 6)
  } catch (e) {
    console.log('No tours loaded yet')
  }
})

onUnmounted(() => { if (slideTimer) clearInterval(slideTimer) })
</script>
