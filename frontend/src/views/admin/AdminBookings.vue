<!--
  AdminBookings.vue — View, update status, and delete bookings
-->
<template>
  <div>
    <div class="admin-content-header">
      <h1>📋 Bookings</h1>
    </div>

    <div class="admin-table-wrapper">
      <table class="admin-table">
        <thead><tr><th>ID</th><th>Customer</th><th>Email</th><th>Phone</th><th>Language</th><th>Status</th><th>Date</th><th>Actions</th></tr></thead>
        <tbody>
          <tr v-for="b in items" :key="b.id">
            <td>#{{ b.id }}</td>
            <td>{{ b.customer_name }}</td>
            <td>{{ b.customer_email }}</td>
            <td>{{ b.customer_phone || '-' }}</td>
            <td>{{ b.language?.toUpperCase() }}</td>
            <td>
              <select
                :value="b.status || 'pending'"
                @change="updateStatus(b.id, $event.target.value)"
                class="form-input"
                style="padding:4px 8px; font-size:0.78rem; width:auto;"
              >
                <option value="pending">Pending</option>
                <option value="active">Active</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </td>
            <td>{{ formatDate(b.created_at) }}</td>
            <td>
              <button class="btn btn-danger btn-sm" @click="remove(b.id)">Delete</button>
            </td>
          </tr>
          <tr v-if="!items.length"><td colspan="8" style="text-align:center; color:var(--text-tertiary); padding:24px;">No bookings yet.</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import adminApi from '../../api/adminApi.js'

const items = ref([])

function formatDate(dt) { return dt ? new Date(dt).toLocaleDateString() : '-' }

async function load() { items.value = (await adminApi.get('/admin/bookings')).data }

async function updateStatus(id, status) {
  await adminApi.put(`/admin/bookings/${id}`, { status })
  await load()
}

async function remove(id) {
  if (confirm('Delete this booking?')) { await adminApi.delete(`/admin/bookings/${id}`); await load() }
}

onMounted(load)
</script>
