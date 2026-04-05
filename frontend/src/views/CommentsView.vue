<!--
  CommentsView.vue — Public Comments / Reviews Page
  Shows ALL site comments (not filtered by tour).
  Full write form + all comment cards in a beautiful dedicated page.
-->
<template>
  <div class="comments-page">
    <!-- ── Page Hero ── -->
    <section class="comments-page-hero">
      <div class="comments-page-hero-overlay">
        <div class="container">
          <div class="comments-page-hero-content">
            <div class="comments-page-badge">💬 {{ $t('comments.title') }}</div>
            <h1>{{ $t('comments.pageTitle') }}</h1>
            <p>{{ $t('comments.pageSubtitle') }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Main Content ── -->
    <section class="section">
      <div class="container" style="max-width: 860px; margin: 0 auto;">
        <CommentsSection :tourId="null" />
      </div>
    </section>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import CommentsSection from '../components/CommentsSection.vue'

const { t } = useI18n()
</script>
