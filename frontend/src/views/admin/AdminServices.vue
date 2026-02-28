<!--
  AdminServices.vue — Full CRUD for services
-->
<template>
  <div>
    <div class="admin-content-header">
      <h1>🛎️ Services</h1>
      <button class="btn btn-primary" @click="openModal()">+ Add Service</button>
    </div>

    <div class="admin-table-wrapper">
      <table class="admin-table">
        <thead><tr><th>ID</th><th>Name (EN)</th><th>Price</th><th>Icon</th><th>Status</th><th>Actions</th></tr></thead>
        <tbody>
          <tr v-for="s in items" :key="s.id">
            <td>#{{ s.id }}</td>
            <td>{{ s.name_en }}</td>
            <td>{{ s.price ? '$' + s.price : '-' }}</td>
            <td>{{ s.icon || '-' }}</td>
            <td><span class="status-badge" :class="s.is_active ? 'status-active' : 'status-inactive'">{{ s.is_active ? 'Active' : 'Inactive' }}</span></td>
            <td>
              <button class="btn btn-outline btn-sm" @click="openModal(s)">Edit</button>
              <button class="btn btn-danger btn-sm" @click="remove(s.id)" style="margin-left:6px;">Delete</button>
            </td>
          </tr>
          <tr v-if="!items.length"><td colspan="6" style="text-align:center; color:var(--text-tertiary); padding:24px;">No services yet.</td></tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div v-show="showModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ editing ? 'Edit Service' : 'Add Service' }}</h2>
          <button class="modal-close" @click="showModal=false">✕</button>
        </div>
        <form @submit.prevent="save">
          <div class="form-group"><label class="form-label">Name (RU)</label><input v-model="form.name_ru" class="form-input" required /></div>
          <div class="form-group"><label class="form-label">Name (EN)</label><input v-model="form.name_en" class="form-input" required /></div>
          <div class="form-group"><label class="form-label">Name (FR)</label><input v-model="form.name_fr" class="form-input" required /></div>
          <div class="form-group"><label class="form-label">Description (RU)</label><textarea v-model="form.description_ru" class="form-input form-textarea"></textarea></div>
          <div class="form-group"><label class="form-label">Description (EN)</label><textarea v-model="form.description_en" class="form-input form-textarea"></textarea></div>
          <div class="form-group"><label class="form-label">Description (FR)</label><textarea v-model="form.description_fr" class="form-input form-textarea"></textarea></div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
            <div class="form-group"><label class="form-label">Price ($)</label><input v-model.number="form.price" type="number" class="form-input" /></div>
            <div class="form-group"><label class="form-label">Icon (emoji)</label><input v-model="form.icon" class="form-input" /></div>
          </div>
          <div class="form-group">
            <label class="form-label">Active</label>
            <select v-model="form.is_active" class="form-input"><option :value="true">Active</option><option :value="false">Inactive</option></select>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn btn-outline" @click="showModal=false">Cancel</button>
            <button type="submit" class="btn btn-primary">{{ editing ? 'Update' : 'Create' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import adminApi from '../../api/adminApi.js'

const items = ref([])
const showModal = ref(false)
const editing = ref(null)
const form = ref(getEmpty())

function getEmpty() {
  return { name_ru:'',name_en:'',name_fr:'',description_ru:'',description_en:'',description_fr:'',price:null,icon:'',is_active:true }
}

async function load() { items.value = (await adminApi.get('/admin/services')).data }

function openModal(item) {
  if (item) { editing.value = item.id; form.value = { ...item } }
  else { editing.value = null; form.value = getEmpty() }
  showModal.value = true
}

async function save() {
  if (editing.value) await adminApi.put(`/admin/services/${editing.value}`, form.value)
  else await adminApi.post('/admin/services', form.value)
  showModal.value = false; await load()
}

async function remove(id) {
  if (confirm('Delete this service?')) { await adminApi.delete(`/admin/services/${id}`); await load() }
}

onMounted(load)
</script>
