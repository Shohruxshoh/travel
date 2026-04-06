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

          <div class="comment-form-group" style="position:relative;">
            <label class="comment-form-label">
              {{ $t('comments.country') }} <span class="required-star">*</span>
            </label>
            <div class="country-dropdown" ref="countryDropdownRef">
              <!-- Trigger -->
              <div
                class="comment-form-input country-trigger"
                :class="{ 'input-error': errors.country, 'open': showDropdown }"
                @click="toggleDropdown"
                tabindex="0"
                @keydown.escape="showDropdown = false"
              >
                <span v-if="form.country" class="country-trigger-val">
                  {{ getFlag(form.country) }} {{ form.country }}
                </span>
                <span v-else class="country-trigger-placeholder">{{ $t('comments.countryPlaceholder') }}</span>
                <svg class="country-arrow" :class="{ rotated: showDropdown }" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>
              </div>

              <!-- Dropdown panel -->
              <div v-if="showDropdown" class="country-panel">
                <!-- Search -->
                <div class="country-search-wrap">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
                  <input
                    v-model="countrySearch"
                    class="country-search-input"
                    :placeholder="$t('comments.countrySearch') || 'Search country...' "
                    autofocus
                    @click.stop
                  />
                </div>
                <!-- List -->
                <ul class="country-list">
                  <li
                    v-for="c in filteredCountries"
                    :key="c.code"
                    class="country-item"
                    :class="{ selected: form.country === c.name }"
                    @click="selectCountry(c)"
                  >
                    <span class="country-code">{{ c.code }}</span>
                    {{ c.flag }} {{ c.name }}
                  </li>
                  <li v-if="!filteredCountries.length" class="country-no-result">No results</li>
                </ul>
              </div>
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
import { ref, reactive, computed, onMounted, onBeforeUnmount } from 'vue'
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
const showDropdown = ref(false)
const countrySearch = ref('')
const countryDropdownRef = ref(null)

const form = reactive({
  author_name: '',
  country: '',
  description: '',
})
const errors = reactive({ author_name: false, country: false, description: false })

// ── Country list (195 countries) ─────────────────────────────────
const countries = [
  { code: 'AF', name: 'Afghanistan', flag: '🇦🇫' },
  { code: 'AL', name: 'Albania', flag: '🇦🇱' },
  { code: 'DZ', name: 'Algeria', flag: '🇩🇿' },
  { code: 'AD', name: 'Andorra', flag: '🇦🇩' },
  { code: 'AO', name: 'Angola', flag: '🇦🇴' },
  { code: 'AG', name: 'Antigua and Barbuda', flag: '🇦🇬' },
  { code: 'AR', name: 'Argentina', flag: '🇦🇷' },
  { code: 'AM', name: 'Armenia', flag: '🇦🇲' },
  { code: 'AU', name: 'Australia', flag: '🇦🇺' },
  { code: 'AT', name: 'Austria', flag: '🇦🇹' },
  { code: 'AZ', name: 'Azerbaijan', flag: '🇦🇿' },
  { code: 'BS', name: 'Bahamas', flag: '🇧🇸' },
  { code: 'BH', name: 'Bahrain', flag: '🇧🇭' },
  { code: 'BD', name: 'Bangladesh', flag: '🇧🇩' },
  { code: 'BB', name: 'Barbados', flag: '🇧🇧' },
  { code: 'BY', name: 'Belarus', flag: '🇧🇾' },
  { code: 'BE', name: 'Belgium', flag: '🇧🇪' },
  { code: 'BZ', name: 'Belize', flag: '🇧🇿' },
  { code: 'BJ', name: 'Benin', flag: '🇧🇯' },
  { code: 'BT', name: 'Bhutan', flag: '🇧🇹' },
  { code: 'BO', name: 'Bolivia', flag: '🇧🇴' },
  { code: 'BA', name: 'Bosnia and Herzegovina', flag: '🇧🇦' },
  { code: 'BW', name: 'Botswana', flag: '🇧🇼' },
  { code: 'BR', name: 'Brazil', flag: '🇧🇷' },
  { code: 'BN', name: 'Brunei', flag: '🇧🇳' },
  { code: 'BG', name: 'Bulgaria', flag: '🇧🇬' },
  { code: 'BF', name: 'Burkina Faso', flag: '🇧🇫' },
  { code: 'BI', name: 'Burundi', flag: '🇧🇮' },
  { code: 'CV', name: 'Cabo Verde', flag: '🇨🇻' },
  { code: 'KH', name: 'Cambodia', flag: '🇰🇭' },
  { code: 'CM', name: 'Cameroon', flag: '🇨🇲' },
  { code: 'CA', name: 'Canada', flag: '🇨🇦' },
  { code: 'CF', name: 'Central African Republic', flag: '🇨🇫' },
  { code: 'TD', name: 'Chad', flag: '🇹🇩' },
  { code: 'CL', name: 'Chile', flag: '🇨🇱' },
  { code: 'CN', name: 'China', flag: '🇨🇳' },
  { code: 'CO', name: 'Colombia', flag: '🇨🇴' },
  { code: 'KM', name: 'Comoros', flag: '🇰🇲' },
  { code: 'CG', name: 'Congo', flag: '🇨🇬' },
  { code: 'CR', name: 'Costa Rica', flag: '🇨🇷' },
  { code: 'HR', name: 'Croatia', flag: '🇭🇷' },
  { code: 'CU', name: 'Cuba', flag: '🇨🇺' },
  { code: 'CY', name: 'Cyprus', flag: '🇨🇾' },
  { code: 'CZ', name: 'Czech Republic', flag: '🇨🇿' },
  { code: 'DK', name: 'Denmark', flag: '🇩🇰' },
  { code: 'DJ', name: 'Djibouti', flag: '🇩🇯' },
  { code: 'DM', name: 'Dominica', flag: '🇩🇲' },
  { code: 'DO', name: 'Dominican Republic', flag: '🇩🇴' },
  { code: 'CD', name: 'DR Congo', flag: '🇨🇩' },
  { code: 'EC', name: 'Ecuador', flag: '🇪🇨' },
  { code: 'EG', name: 'Egypt', flag: '🇪🇬' },
  { code: 'SV', name: 'El Salvador', flag: '🇸🇻' },
  { code: 'GQ', name: 'Equatorial Guinea', flag: '🇬🇶' },
  { code: 'ER', name: 'Eritrea', flag: '🇪🇷' },
  { code: 'EE', name: 'Estonia', flag: '🇪🇪' },
  { code: 'SZ', name: 'Eswatini', flag: '🇸🇿' },
  { code: 'ET', name: 'Ethiopia', flag: '🇪🇹' },
  { code: 'FJ', name: 'Fiji', flag: '🇫🇯' },
  { code: 'FI', name: 'Finland', flag: '🇫🇮' },
  { code: 'FR', name: 'France', flag: '🇫🇷' },
  { code: 'GA', name: 'Gabon', flag: '🇬🇦' },
  { code: 'GM', name: 'Gambia', flag: '🇬🇲' },
  { code: 'GE', name: 'Georgia', flag: '🇬🇪' },
  { code: 'DE', name: 'Germany', flag: '🇩🇪' },
  { code: 'GH', name: 'Ghana', flag: '🇬🇭' },
  { code: 'GR', name: 'Greece', flag: '🇬🇷' },
  { code: 'GD', name: 'Grenada', flag: '🇬🇩' },
  { code: 'GT', name: 'Guatemala', flag: '🇬🇹' },
  { code: 'GN', name: 'Guinea', flag: '🇬🇳' },
  { code: 'GW', name: 'Guinea-Bissau', flag: '🇬🇼' },
  { code: 'GY', name: 'Guyana', flag: '🇬🇾' },
  { code: 'HT', name: 'Haiti', flag: '🇭🇹' },
  { code: 'HN', name: 'Honduras', flag: '🇭🇳' },
  { code: 'HU', name: 'Hungary', flag: '🇭🇺' },
  { code: 'IS', name: 'Iceland', flag: '🇮🇸' },
  { code: 'IN', name: 'India', flag: '🇮🇳' },
  { code: 'ID', name: 'Indonesia', flag: '🇮🇩' },
  { code: 'IR', name: 'Iran', flag: '🇮🇷' },
  { code: 'IQ', name: 'Iraq', flag: '🇮🇶' },
  { code: 'IE', name: 'Ireland', flag: '🇮🇪' },
  { code: 'IL', name: 'Israel', flag: '🇮🇱' },
  { code: 'IT', name: 'Italy', flag: '🇮🇹' },
  { code: 'CI', name: 'Ivory Coast', flag: '🇨🇮' },
  { code: 'JM', name: 'Jamaica', flag: '🇯🇲' },
  { code: 'JP', name: 'Japan', flag: '🇯🇵' },
  { code: 'JO', name: 'Jordan', flag: '🇯🇴' },
  { code: 'KZ', name: 'Kazakhstan', flag: '🇰🇿' },
  { code: 'KE', name: 'Kenya', flag: '🇰🇪' },
  { code: 'KI', name: 'Kiribati', flag: '🇰🇮' },
  { code: 'KW', name: 'Kuwait', flag: '🇰🇼' },
  { code: 'KG', name: 'Kyrgyzstan', flag: '🇰🇬' },
  { code: 'LA', name: 'Laos', flag: '🇱🇦' },
  { code: 'LV', name: 'Latvia', flag: '🇱🇻' },
  { code: 'LB', name: 'Lebanon', flag: '🇱🇧' },
  { code: 'LS', name: 'Lesotho', flag: '🇱🇸' },
  { code: 'LR', name: 'Liberia', flag: '🇱🇷' },
  { code: 'LY', name: 'Libya', flag: '🇱🇾' },
  { code: 'LI', name: 'Liechtenstein', flag: '🇱🇮' },
  { code: 'LT', name: 'Lithuania', flag: '🇱🇹' },
  { code: 'LU', name: 'Luxembourg', flag: '🇱🇺' },
  { code: 'MG', name: 'Madagascar', flag: '🇲🇬' },
  { code: 'MW', name: 'Malawi', flag: '🇲🇼' },
  { code: 'MY', name: 'Malaysia', flag: '🇲🇾' },
  { code: 'MV', name: 'Maldives', flag: '🇲🇻' },
  { code: 'ML', name: 'Mali', flag: '🇲🇱' },
  { code: 'MT', name: 'Malta', flag: '🇲🇹' },
  { code: 'MH', name: 'Marshall Islands', flag: '🇲🇭' },
  { code: 'MR', name: 'Mauritania', flag: '🇲🇷' },
  { code: 'MU', name: 'Mauritius', flag: '🇲🇺' },
  { code: 'MX', name: 'Mexico', flag: '🇲🇽' },
  { code: 'FM', name: 'Micronesia', flag: '🇫🇲' },
  { code: 'MD', name: 'Moldova', flag: '🇲🇩' },
  { code: 'MC', name: 'Monaco', flag: '🇲🇨' },
  { code: 'MN', name: 'Mongolia', flag: '🇲🇳' },
  { code: 'ME', name: 'Montenegro', flag: '🇲🇪' },
  { code: 'MA', name: 'Morocco', flag: '🇲🇦' },
  { code: 'MZ', name: 'Mozambique', flag: '🇲🇿' },
  { code: 'MM', name: 'Myanmar', flag: '🇲🇲' },
  { code: 'NA', name: 'Namibia', flag: '🇳🇦' },
  { code: 'NR', name: 'Nauru', flag: '🇳🇷' },
  { code: 'NP', name: 'Nepal', flag: '🇳🇵' },
  { code: 'NL', name: 'Netherlands', flag: '🇳🇱' },
  { code: 'NZ', name: 'New Zealand', flag: '🇳🇿' },
  { code: 'NI', name: 'Nicaragua', flag: '🇳🇮' },
  { code: 'NE', name: 'Niger', flag: '🇳🇪' },
  { code: 'NG', name: 'Nigeria', flag: '🇳🇬' },
  { code: 'KP', name: 'North Korea', flag: '🇰🇵' },
  { code: 'MK', name: 'North Macedonia', flag: '🇲🇰' },
  { code: 'NO', name: 'Norway', flag: '🇳🇴' },
  { code: 'OM', name: 'Oman', flag: '🇴🇲' },
  { code: 'PK', name: 'Pakistan', flag: '🇵🇰' },
  { code: 'PW', name: 'Palau', flag: '🇵🇼' },
  { code: 'PA', name: 'Panama', flag: '🇵🇦' },
  { code: 'PG', name: 'Papua New Guinea', flag: '🇵🇬' },
  { code: 'PY', name: 'Paraguay', flag: '🇵🇾' },
  { code: 'PE', name: 'Peru', flag: '🇵🇪' },
  { code: 'PH', name: 'Philippines', flag: '🇵🇭' },
  { code: 'PL', name: 'Poland', flag: '🇵🇱' },
  { code: 'PT', name: 'Portugal', flag: '🇵🇹' },
  { code: 'QA', name: 'Qatar', flag: '🇶🇦' },
  { code: 'RO', name: 'Romania', flag: '🇷🇴' },
  { code: 'RU', name: 'Russia', flag: '🇷🇺' },
  { code: 'RW', name: 'Rwanda', flag: '🇷🇼' },
  { code: 'KN', name: 'Saint Kitts and Nevis', flag: '🇰🇳' },
  { code: 'LC', name: 'Saint Lucia', flag: '🇱🇨' },
  { code: 'VC', name: 'Saint Vincent and the Grenadines', flag: '🇻🇨' },
  { code: 'WS', name: 'Samoa', flag: '🇼🇸' },
  { code: 'SM', name: 'San Marino', flag: '🇸🇲' },
  { code: 'ST', name: 'Sao Tome and Principe', flag: '🇸🇹' },
  { code: 'SA', name: 'Saudi Arabia', flag: '🇸🇦' },
  { code: 'SN', name: 'Senegal', flag: '🇸🇳' },
  { code: 'RS', name: 'Serbia', flag: '🇷🇸' },
  { code: 'SC', name: 'Seychelles', flag: '🇸🇨' },
  { code: 'SL', name: 'Sierra Leone', flag: '🇸🇱' },
  { code: 'SG', name: 'Singapore', flag: '🇸🇬' },
  { code: 'SK', name: 'Slovakia', flag: '🇸🇰' },
  { code: 'SI', name: 'Slovenia', flag: '🇸🇮' },
  { code: 'SB', name: 'Solomon Islands', flag: '🇸🇧' },
  { code: 'SO', name: 'Somalia', flag: '🇸🇴' },
  { code: 'ZA', name: 'South Africa', flag: '🇿🇦' },
  { code: 'SS', name: 'South Sudan', flag: '🇸🇸' },
  { code: 'KR', name: 'South Korea', flag: '🇰🇷' },
  { code: 'ES', name: 'Spain', flag: '🇪🇸' },
  { code: 'LK', name: 'Sri Lanka', flag: '🇱🇰' },
  { code: 'SD', name: 'Sudan', flag: '🇸🇩' },
  { code: 'SR', name: 'Suriname', flag: '🇸🇷' },
  { code: 'SE', name: 'Sweden', flag: '🇸🇪' },
  { code: 'CH', name: 'Switzerland', flag: '🇨🇭' },
  { code: 'SY', name: 'Syria', flag: '🇸🇾' },
  { code: 'TW', name: 'Taiwan', flag: '🇹🇼' },
  { code: 'TJ', name: 'Tajikistan', flag: '🇹🇯' },
  { code: 'TZ', name: 'Tanzania', flag: '🇹🇿' },
  { code: 'TH', name: 'Thailand', flag: '🇹🇭' },
  { code: 'TL', name: 'Timor-Leste', flag: '🇹🇱' },
  { code: 'TG', name: 'Togo', flag: '🇹🇬' },
  { code: 'TO', name: 'Tonga', flag: '🇹🇴' },
  { code: 'TT', name: 'Trinidad and Tobago', flag: '🇹🇹' },
  { code: 'TN', name: 'Tunisia', flag: '🇹🇳' },
  { code: 'TR', name: 'Turkey', flag: '🇹🇷' },
  { code: 'TM', name: 'Turkmenistan', flag: '🇹🇲' },
  { code: 'TV', name: 'Tuvalu', flag: '🇹🇻' },
  { code: 'UG', name: 'Uganda', flag: '🇺🇬' },
  { code: 'UA', name: 'Ukraine', flag: '🇺🇦' },
  { code: 'AE', name: 'UAE', flag: '🇦🇪' },
  { code: 'GB', name: 'United Kingdom', flag: '🇬🇧' },
  { code: 'US', name: 'United States', flag: '🇺🇸' },
  { code: 'UY', name: 'Uruguay', flag: '🇺🇾' },
  { code: 'UZ', name: 'Uzbekistan', flag: '🇺🇿' },
  { code: 'VU', name: 'Vanuatu', flag: '🇻🇺' },
  { code: 'VA', name: 'Vatican City', flag: '🇻🇦' },
  { code: 'VE', name: 'Venezuela', flag: '🇻🇪' },
  { code: 'VN', name: 'Vietnam', flag: '🇻🇳' },
  { code: 'YE', name: 'Yemen', flag: '🇾🇪' },
  { code: 'ZM', name: 'Zambia', flag: '🇿🇲' },
  { code: 'ZW', name: 'Zimbabwe', flag: '🇿🇼' },
  { code: 'XX', name: 'Other', flag: '🌍' },
]

const flagMap = Object.fromEntries(countries.map(c => [c.name, c.flag]))

function getFlag(country) {
  return flagMap[country] || '🌍'
}

// ── Searchable dropdown ───────────────────────────────────────────
const filteredCountries = computed(() => {
  const q = countrySearch.value.toLowerCase().trim()
  if (!q) return countries
  return countries.filter(c =>
    c.name.toLowerCase().includes(q) || c.code.toLowerCase().includes(q)
  )
})

function toggleDropdown() {
  showDropdown.value = !showDropdown.value
  if (showDropdown.value) countrySearch.value = ''
}

function selectCountry(c) {
  form.country = c.name
  errors.country = false
  showDropdown.value = false
  countrySearch.value = ''
}

function handleClickOutside(e) {
  if (countryDropdownRef.value && !countryDropdownRef.value.contains(e.target)) {
    showDropdown.value = false
  }
}

onBeforeUnmount(() => document.removeEventListener('click', handleClickOutside))

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
  if (!file) return
  // Allow if type is empty (some browsers return '' for webp/avif) or starts with 'image/'
  const t = file.type.toLowerCase()
  if (t && !t.startsWith('image/')) return
  processFile(file)
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
    const detail = e.response?.data?.detail || 'Upload failed'
    submitError.value = detail
    imagePreview.value = null
    imageUrl.value = null
    console.error('Upload failed:', detail)
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

onMounted(() => {
  loadComments()
  document.addEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* ── Searchable Country Dropdown ── */
.country-dropdown {
  position: relative;
  width: 100%;
}

.country-trigger {
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  user-select: none;
  gap: 8px;
}

.country-trigger-placeholder {
  color: var(--text-tertiary, #94a3b8);
  font-size: 0.875rem;
  flex: 1;
}

.country-trigger-val {
  flex: 1;
  font-size: 0.875rem;
}

.country-arrow {
  flex-shrink: 0;
  color: var(--text-tertiary, #94a3b8);
  transition: transform 0.2s ease;
}

.country-arrow.rotated {
  transform: rotate(180deg);
}

.country-panel {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  z-index: 999;
  background: var(--bg-elevated, #1e293b);
  border: 1px solid var(--border-medium, rgba(255,255,255,0.1));
  border-radius: 10px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.35);
  overflow: hidden;
  animation: dropIn 0.15s ease;
}

@keyframes dropIn {
  from { opacity: 0; transform: translateY(-6px); }
  to   { opacity: 1; transform: translateY(0); }
}

.country-search-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-bottom: 1px solid var(--border-light, rgba(255,255,255,0.06));
  color: var(--text-tertiary, #94a3b8);
}

.country-search-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  font-size: 0.875rem;
  color: var(--text-primary, #f1f5f9);
  font-family: inherit;
}

.country-search-input::placeholder {
  color: var(--text-tertiary, #94a3b8);
}

.country-list {
  list-style: none;
  max-height: 240px;
  overflow-y: auto;
  margin: 0;
  padding: 4px;
  scrollbar-width: thin;
  scrollbar-color: rgba(255,255,255,0.15) transparent;
}

.country-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  color: var(--text-primary, #f1f5f9);
  transition: background 0.13s ease;
}

.country-item:hover {
  background: rgba(99,102,241,0.15);
}

.country-item.selected {
  background: rgba(99,102,241,0.2);
  color: #818cf8;
  font-weight: 600;
}

.country-code {
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--text-tertiary, #94a3b8);
  letter-spacing: 0.5px;
  min-width: 22px;
}

.country-no-result {
  padding: 12px;
  text-align: center;
  color: var(--text-tertiary, #94a3b8);
  font-size: 0.85rem;
}
</style>
