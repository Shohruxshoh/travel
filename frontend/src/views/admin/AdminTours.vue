<!--
  AdminTours.vue — Full CRUD for tours with image upload
-->
<template>
  <div>
    <div class="admin-content-header">
      <h1>🗺️ Tours</h1>
      <button class="btn btn-primary" @click="openModal()">+ Add Tour</button>
    </div>

    <div class="admin-table-wrapper">
      <table class="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Image</th>
            <th>Title (EN)</th>
            <th>Destination</th>
            <th>Price</th>
            <th>Days</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in items" :key="t.id">
            <td>#{{ t.id }}</td>
            <td><img v-if="t.cover_image" :src="t.cover_image" class="admin-thumb" /><span v-else class="admin-thumb-empty">📷</span></td>
            <td>{{ t.title_en }}</td>
            <td>{{ t.destination }}</td>
            <td>€{{ t.price }}</td>
            <td>{{ t.duration_days }}</td>
            <td><span class="status-badge" :class="t.is_active ? 'status-active' : 'status-inactive'">{{ t.is_active ? 'Active' : 'Inactive' }}</span></td>
            <td>
              <button class="btn btn-outline btn-sm" @click="openModal(t)">Edit</button>
              <button class="btn btn-danger btn-sm" @click="remove(t.id)" style="margin-left:6px;">Delete</button>
            </td>
          </tr>
          <tr v-if="!items.length"><td colspan="8" style="text-align:center; color:var(--text-tertiary); padding:24px;">No tours yet. Click "Add Tour" to create one.</td></tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal=false">
      <div class="modal-content" style="max-width:620px;">
        <div class="modal-header">
          <h2>{{ editing ? 'Edit Tour' : 'Add Tour' }}</h2>
          <button class="modal-close" @click="showModal=false">✕</button>
        </div>
        <form @submit.prevent="save">
          <!-- Image Upload -->
          <div class="form-group">
            <label class="form-label">Cover Image</label>
            <div class="image-upload-area">
              <img v-if="imagePreview || form.cover_image" :src="imagePreview || form.cover_image" class="image-preview" />
              <div v-else class="image-placeholder">📷 No image</div>
              <div style="display:flex; gap:8px; margin-top:8px;">
                <label class="btn btn-outline btn-sm" style="cursor:pointer;">
                  📁 Choose File
                  <input type="file" accept="image/*" @change="handleFileSelect" style="display:none;" />
                </label>
                <button v-if="imagePreview || form.cover_image" type="button" class="btn btn-danger btn-sm" @click="clearImage">✕ Remove</button>
              </div>
              <span v-if="uploading" class="upload-status">⏳ Uploading...</span>
            </div>
          </div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
            <div class="form-group"><label class="form-label">Title (RU)</label><input v-model="form.title_ru" class="form-input" required /></div>
            <div class="form-group"><label class="form-label">Title (EN)</label><input v-model="form.title_en" class="form-input" required /></div>
            <div class="form-group"><label class="form-label">Title (FR)</label><input v-model="form.title_fr" class="form-input" required /></div>
            <div class="form-group"><label class="form-label">Price (€)</label><input v-model.number="form.price" type="number" class="form-input" required min="1" /></div>
            <div class="form-group"><label class="form-label">Duration (days)</label><input v-model.number="form.duration_days" type="number" class="form-input" required min="1" /></div>
          </div>
          <div class="form-group"><label class="form-label">Description (RU)</label><textarea v-model="form.description_ru" class="form-input form-textarea"></textarea></div>
          <div class="form-group"><label class="form-label">Description (EN)</label><textarea v-model="form.description_en" class="form-input form-textarea"></textarea></div>
          <div class="form-group"><label class="form-label">Description (FR)</label><textarea v-model="form.description_fr" class="form-input form-textarea"></textarea></div>
          <div class="form-group">
            <label class="form-label">Active</label>
            <select v-model="form.is_active" class="form-input">
              <option :value="true">Active</option>
              <option :value="false">Inactive</option>
            </select>
          </div>
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
  return { title_ru:'',title_en:'',title_fr:'',description_ru:'',description_en:'',description_fr:'',price:100,duration_days:7,destination:'',cover_image:'',is_active:true }
}

async function load() {
  const res = await adminApi.get('/admin/tours')
  items.value = res.data
}

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
    form.value.cover_image = res.data.url
  } catch (err) {
    alert('Upload failed: ' + (err.response?.data?.detail || err.message))
    imagePreview.value = null
  } finally {
    uploading.value = false
  }
}

function clearImage() {
  form.value.cover_image = ''
  imagePreview.value = null
}

async function save() {
  if (editing.value) {
    await adminApi.put(`/admin/tours/${editing.value}`, form.value)
  } else {
    await adminApi.post('/admin/tours', form.value)
  }
  showModal.value = false
  await load()
}

async function remove(id) {
  if (confirm('Delete this tour?')) {
    await adminApi.delete(`/admin/tours/${id}`)
    await load()
  }
}

onMounted(load)
</script>
