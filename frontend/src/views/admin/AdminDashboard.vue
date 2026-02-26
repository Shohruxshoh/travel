<!--
  AdminDashboard.vue — Dashboard with stats from API
-->
<template>
  <div>
    <div class="admin-content-header">
      <h1>📊 Dashboard</h1>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📋</div>
        <div class="stat-value">{{ stats.bookings }}</div>
        <div class="stat-label">Total Bookings</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🗺️</div>
        <div class="stat-value">{{ stats.tours }}</div>
        <div class="stat-label">Active Tours</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🏨</div>
        <div class="stat-value">{{ stats.hotels }}</div>
        <div class="stat-label">Hotels</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🛎️</div>
        <div class="stat-value">{{ stats.services }}</div>
        <div class="stat-label">Services</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📝</div>
        <div class="stat-value">{{ stats.blog }}</div>
        <div class="stat-label">Blog Articles</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📧</div>
        <div class="stat-value">{{ stats.operators }}</div>
        <div class="stat-label">Email Operators</div>
      </div>
    </div>

    <!-- Recent Bookings -->
    <h2 style="margin:24px 0 16px; font-size:1.2rem; color:var(--text-primary);">Recent Bookings</h2>
    <div class="admin-table-wrapper">
      <table class="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Customer</th>
            <th>Email</th>
            <th>Language</th>
            <th>Status</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="b in recentBookings" :key="b.id">
            <td>#{{ b.id }}</td>
            <td>{{ b.customer_name }}</td>
            <td>{{ b.customer_email }}</td>
            <td>{{ b.language?.toUpperCase() }}</td>
            <td><span class="status-badge" :class="'status-' + (b.status || 'pending')">{{ b.status || 'pending' }}</span></td>
            <td>{{ formatDate(b.created_at) }}</td>
          </tr>
          <tr v-if="!recentBookings.length">
            <td colspan="6" style="text-align:center; color:var(--text-tertiary); padding:24px;">No bookings yet</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import adminApi from '../../api/adminApi.js'

const stats = ref({ bookings: 0, tours: 0, hotels: 0, services: 0, operators: 0, blog: 0 })
const recentBookings = ref([])

function formatDate(dt) {
  if (!dt) return '-'
  return new Date(dt).toLocaleDateString()
}

onMounted(async () => {
  try {
    const [statsRes, bookingsRes] = await Promise.all([
      adminApi.get('/admin/stats'),
      adminApi.get('/admin/bookings'),
    ])
    stats.value = statsRes.data
    recentBookings.value = bookingsRes.data.slice(0, 10)
  } catch (e) {
    console.error('Failed to load dashboard', e)
  }
})
</script>
