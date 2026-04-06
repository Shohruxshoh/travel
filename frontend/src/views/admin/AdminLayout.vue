<!--
  AdminLayout.vue — Sidebar layout with logout
-->
<template>
  <div class="admin-layout">
    <aside class="admin-sidebar">
      <div class="admin-sidebar-header">
        <h3>✈️ Admin Panel</h3>
      </div>
      <ul class="admin-nav">
        <li><router-link to="/admin" exact><span class="nav-icon">📊</span> Dashboard</router-link></li>
        <li><router-link to="/admin/bookings"><span class="nav-icon">📋</span> Bookings</router-link></li>
        <li><router-link to="/admin/tours"><span class="nav-icon">🗺️</span> Tours</router-link></li>
        <li><router-link to="/admin/hotels"><span class="nav-icon">🏨</span> Hotels</router-link></li>
        <li><router-link to="/admin/services"><span class="nav-icon">🛎️</span> Services</router-link></li>
        <li><router-link to="/admin/blog"><span class="nav-icon">📝</span> Blog</router-link></li>
        <li><router-link to="/admin/gallery"><span class="nav-icon">🖼️</span> Gallery</router-link></li>
        <li><router-link to="/admin/operators"><span class="nav-icon">📧</span> Operators</router-link></li>
        <li><router-link to="/admin/comments"><span class="nav-icon">💬</span> Comments</router-link></li>
      </ul>
      <div style="padding:16px 20px; margin-top:auto; border-top:1px solid rgba(255,255,255,0.06);">
        <button class="btn btn-outline btn-sm" style="width:100%" @click="handleLogout">🚪 Logout</button>
        <router-link to="/" style="display:block; text-align:center; margin-top:10px; font-size:0.78rem; color:var(--sidebar-text);">
          ← Back to site
        </router-link>
      </div>
    </aside>
    <div class="admin-content">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { logout } from '../../api/adminApi.js'

function handleLogout() {
  logout()
}
</script>
