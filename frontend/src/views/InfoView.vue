<!--
  InfoView.vue — Info page with tabbed sections
  Content sourced from info/ docx files, organized into logical categories:
  1. About Us (Qui sommes-nous)
  2. Uzbekistan (Geography, History, General Info)
  3. Travel Tips (Transport, Best Period, Vaccination, Useful to Know)
-->
<template>
  <div>
    <!-- ═══ HERO ═══ -->
    <section class="info-hero">
      <div class="info-hero-overlay"></div>
      <div class="info-hero-content">
        <div class="info-hero-badge">ℹ️ {{ $t('info.badge') }}</div>
        <h1>{{ $t('info.title') }}</h1>
        <p>{{ $t('info.subtitle') }}</p>
      </div>
    </section>

    <!-- ═══ TABS + CONTENT ═══ -->
    <section class="section">
      <div class="container">
        <!-- Tab Navigation -->
        <div class="info-tabs">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            class="info-tab-btn"
            :class="{ active: activeTab === tab.id }"
            @click="activeTab = tab.id"
          >
            <span class="info-tab-icon">{{ tab.icon }}</span>
            {{ tab.label }}
          </button>
        </div>

        <!-- Tab Content -->
        <transition name="tab-fade" mode="out-in">

          <!-- ── About Us ── -->
          <div v-if="activeTab === 'about'" key="about" class="info-content">
            <div class="info-section">
              <h2>{{ $t('info.aboutTitle') }}</h2>
              <div class="info-text-block">
                <p>{{ $t('info.about1') }}</p>
                <p>{{ $t('info.about2') }}</p>
                <p>{{ $t('info.about3') }}</p>
                <p>{{ $t('info.about4') }}</p>
                <p>{{ $t('info.about5') }}</p>
                <p>{{ $t('info.about6') }}</p>
                <blockquote class="info-quote">{{ $t('info.aboutSlogan') }}</blockquote>
              </div>
            </div>
          </div>

          <!-- ── General Info ── -->
          <div v-else-if="activeTab === 'general'" key="general" class="info-content">
            <div class="info-section">
              <h2>{{ $t('info.generalTitle') }}</h2>
              <div class="info-text-block" v-html="$t('info.generalContent')"></div>
            </div>
          </div>

          <!-- ── Geography ── -->
          <div v-else-if="activeTab === 'geography'" key="geography" class="info-content">
            <div class="info-section">
              <h2>{{ $t('info.geographyTitle') }}</h2>
              <div class="info-text-block" v-html="$t('info.geographyContent')"></div>
            </div>
          </div>

          <!-- ── History ── -->
          <div v-else-if="activeTab === 'history'" key="history" class="info-content">
            <div class="info-section">
              <h2>{{ $t('info.historyTitle') }}</h2>
              <div class="info-text-block" v-html="$t('info.historyContent')"></div>
            </div>
          </div>

          <!-- ── Best Travel Period ── -->
          <div v-else-if="activeTab === 'season'" key="season" class="info-content">
            <div class="info-section">
              <h2>{{ $t('info.seasonTitle') }}</h2>
              <div class="info-text-block" v-html="$t('info.seasonContent')"></div>
            </div>
          </div>

          <!-- ── Transport ── -->
          <div v-else-if="activeTab === 'transport'" key="transport" class="info-content">
            <div class="info-section">
              <h2>{{ $t('info.transportTitle') }}</h2>
              <div class="info-text-block" v-html="$t('info.transportContent')"></div>
            </div>
          </div>

          <!-- ── Vaccination ── -->
          <div v-else-if="activeTab === 'health'" key="health" class="info-content">
            <div class="info-section">
              <h2>{{ $t('info.healthTitle') }}</h2>
              <div class="info-text-block" v-html="$t('info.healthContent')"></div>
            </div>
          </div>

          <!-- ── Useful to Know ── -->
          <div v-else-if="activeTab === 'useful'" key="useful" class="info-content">
            <div class="info-section">
              <h2>{{ $t('info.usefulTitle') }}</h2>
              <div class="info-text-block" v-html="$t('info.usefulContent')"></div>
            </div>
          </div>

        </transition>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'

const { t } = useI18n()
const route = useRoute()
const activeTab = ref('about')

const tabs = computed(() => [
  { id: 'about', label: t('info.tabAbout'), icon: '👥' },
  { id: 'general', label: t('info.tabGeneral'), icon: '📋' },
  { id: 'geography', label: t('info.tabGeography'), icon: '🗺️' },
  { id: 'history', label: t('info.tabHistory'), icon: '📜' },
  { id: 'season', label: t('info.tabSeason'), icon: '☀️' },
  { id: 'transport', label: t('info.tabTransport'), icon: '🚂' },
  { id: 'health', label: t('info.tabHealth'), icon: '💉' },
  { id: 'useful', label: t('info.tabUseful'), icon: '💡' },
])

// Sync tab from URL query ?tab=xxx
function syncTab() {
  const tabParam = route.query.tab
  if (tabParam && tabs.value.some(t => t.id === tabParam)) {
    activeTab.value = tabParam
  }
}

onMounted(syncTab)
watch(() => route.query.tab, syncTab)
</script>
