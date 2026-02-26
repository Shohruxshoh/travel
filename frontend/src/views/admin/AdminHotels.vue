<!--
  AdminHotels.vue — Full CRUD for hotels with image upload
-->
<template>
  <div>
    <div class="admin-content-header">
      <h1>🏨 Hotels</h1>
      <button class="btn btn-primary" @click="openModal()">+ Add Hotel</button>
    </div>

    <div class="admin-table-wrapper">
      <table class="admin-table">
        <thead><tr><th>ID</th><th>Image</th><th>Name</th><th>City</th><th>Stars</th><th>Price From</th><th>Status</th><th>Actions</th></tr></thead>
        <tbody>
          <tr v-for="h in items" :key="h.id">
            <td>#{{ h.id }}</td>
            <td><img v-if="h.image_url" :src="h.image_url" class="admin-thumb" /><span v-else class="admin-thumb-empty">📷</span></td>
            <td>{{ h.name }}</td>
            <td>{{ h.city }}, {{ h.country }}</td>
            <td>{{ '★'.repeat(h.star_rating) }}</td>
            <td>${{ h.price_from }}</td>
            <td><span class="status-badge" :class="h.is_active ? 'status-active' : 'status-inactive'">{{ h.is_active ? 'Active' : 'Inactive' }}</span></td>
            <td>
              <button class="btn btn-outline btn-sm" @click="openModal(h)">Edit</button>
              <button class="btn btn-danger btn-sm" @click="remove(h.id)" style="margin-left:6px;">Delete</button>
            </td>
          </tr>
          <tr v-if="!items.length"><td colspan="8" style="text-align:center; color:var(--text-tertiary); padding:24px;">No hotels yet.</td></tr>
        </tbody>
      </table>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="showModal=false">
      <div class="modal-content" style="max-width:620px;">
        <div class="modal-header">
          <h2>{{ editing ? 'Edit Hotel' : 'Add Hotel' }}</h2>
          <button class="modal-close" @click="showModal=false">✕</button>
        </div>
        <form @submit.prevent="save">
          <div class="form-group">
            <label class="form-label">Hotel Image</label>
            <div class="image-upload-area">
              <img v-if="imagePreview || form.image_url" :src="imagePreview || form.image_url" class="image-preview" />
              <div v-else class="image-placeholder">📷 No image</div>
              <div style="display:flex; gap:8px; margin-top:8px;">
                <label class="btn btn-outline btn-sm" style="cursor:pointer;">
                  📁 Choose File
                  <input type="file" accept="image/*" @change="handleFileSelect" style="display:none;" />
                </label>
                <button v-if="imagePreview || form.image_url" type="button" class="btn btn-danger btn-sm" @click="clearImage">✕ Remove</button>
              </div>
              <span v-if="uploading" class="upload-status">⏳ Uploading...</span>
            </div>
          </div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
            <div class="form-group"><label class="form-label">Name</label><input v-model="form.name" class="form-input" required /></div>
            <div class="form-group"><label class="form-label">City</label><input v-model="form.city" class="form-input" required /></div>
            <div class="form-group"><label class="form-label">Country</label><input v-model="form.country" class="form-input" required /></div>
            <div class="form-group"><label class="form-label">Stars</label><select v-model.number="form.star_rating" class="form-input" required><option v-for="s in 5" :key="s" :value="s">{{ '★'.repeat(s) }}</option></select></div>
            <div class="form-group"><label class="form-label">Price From ($)</label><input v-model.number="form.price_from" type="number" class="form-input" required min="1" /></div>
            <div class="form-group"><label class="form-label">Active</label><select v-model="form.is_active" class="form-input"><option :value="true">Active</option><option :value="false">Inactive</option></select></div>
          </div>
          <div class="form-group"><label class="form-label">Description (RU)</label><textarea v-model="form.description_ru" class="form-input form-textarea"></textarea></div>
          <div class="form-group"><label class="form-label">Description (EN)</label><textarea v-model="form.description_en" class="form-input form-textarea"></textarea></div>
          <div class="form-group"><label class="form-label">Description (FR)</label><textarea v-model="form.description_fr" class="form-input form-textarea"></textarea></div>
          <div class="modal-actions">
            <button type="button" class="btn btn-outline" @click="showModal=false">Cancel</button>
            <button type="submit" class="btn btn-primary" :disabled="uploading">{{ editing ? 'Update' : 'Create' }}</button>
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
const imagePreview = ref(null)
const uploading = ref(false)

function getEmpty() {
  return { name:'',city:'',country:'',star_rating:3,image_url:'',description_ru:'',description_en:'',description_fr:'',price_from:50,is_active:true }
}

async function load() { items.value = (await adminApi.get('/admin/hotels')).data }

function openModal(item) {
  imagePreview.value = null
  if (item) { editing.value = item.id; form.value = { ...item } }
  else { editing.value = null; form.value = getEmpty() }
  showModal.value = true
}

async function handleFileSelect(e) {
  const file = e.target.files[0]
  if (!file) return
  imagePreview.value = URL.createObjectURL(file)
  uploading.value = true
  try {
    const fd = new FormData()
    fd.append('file', file)
    const res = await adminApi.post('/upload/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    form.value.image_url = res.data.url
  } catch (err) {
    alert('Upload failed: ' + (err.response?.data?.detail || err.message))
    imagePreview.value = null
  } finally { uploading.value = false }
}

function clearImage() { form.value.image_url = ''; imagePreview.value = null }

async function save() {
  if (editing.value) await adminApi.put(`/admin/hotels/${editing.value}`, form.value)
  else await adminApi.post('/admin/hotels', form.value)
  showModal.value = false; await load()
}

async function remove(id) {
  if (confirm('Delete this hotel?')) { await adminApi.delete(`/admin/hotels/${id}`); await load() }
}

onMounted(load)
</script>
