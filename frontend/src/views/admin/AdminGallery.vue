<!--
  AdminGallery.vue — Full CRUD for gallery items with image/video upload
-->
<template>
  <div>
    <div class="admin-content-header">
      <h1>🖼️ Gallery</h1>
      <button class="btn btn-primary" @click="openModal()">+ Add Media</button>
    </div>

    <div class="gallery-admin-grid">
      <div v-for="g in items" :key="g.id" class="gallery-admin-card">
        <div class="gallery-admin-media">
          <img v-if="g.media_type === 'image'" :src="g.url" :alt="g.caption_en" />
          <video v-else :src="g.url" muted></video>
          <span class="gallery-type-badge">{{ g.media_type === 'image' ? '🖼️' : '🎬' }}</span>
        </div>
        <div class="gallery-admin-info">
          <p class="gallery-meta" v-if="g.tour_id">Tour #{{ g.tour_id }}</p>
          <div class="gallery-admin-actions">
            <button class="btn btn-outline btn-sm" @click="openModal(g)">Edit</button>
            <button class="btn btn-danger btn-sm" @click="remove(g.id)">Delete</button>
          </div>
        </div>
      </div>
      <div v-if="!items.length" class="empty-state" style="grid-column:1/-1;">
        <div class="empty-icon">🖼️</div>
        <p>No gallery items yet. Click "+ Add Media" to upload.</p>
      </div>
    </div>

    <!-- Modal -->
    <div v-show="showModal" class="modal-overlay">
      <div class="modal-content" style="max-width:520px;">
        <div class="modal-header">
          <h2>{{ editing ? 'Edit Media' : 'Add Media' }}</h2>
          <button class="modal-close" @click="showModal=false">✕</button>
        </div>
        <form @submit.prevent="save">
          <!-- File Upload -->
          <div class="form-group">
            <label class="form-label">Media File</label>
            <div class="image-upload-area">
              <img v-if="(imagePreview || form.url) && form.media_type === 'image'" :src="imagePreview || form.url" class="image-preview" />
              <video v-else-if="(imagePreview || form.url) && form.media_type === 'video'" :src="imagePreview || form.url" class="image-preview" muted controls></video>
              <div v-else class="image-placeholder">📷 No media selected</div>
              <div style="display:flex; gap:8px; margin-top:8px;">
                <label class="btn btn-outline btn-sm" style="cursor:pointer;">
                  📁 Choose File
                  <input type="file" accept="image/*,video/mp4,video/webm" @change="handleFileSelect" style="display:none;" />
                </label>
                <button v-if="imagePreview || form.url" type="button" class="btn btn-danger btn-sm" @click="clearMedia">✕ Remove</button>
              </div>
              <span v-if="uploading" class="upload-status">⏳ Uploading...</span>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Media Type</label>
            <select v-model="form.media_type" class="form-input" required>
              <option value="image">🖼️ Image</option>
              <option value="video">🎬 Video</option>
            </select>
          </div>
          <div class="form-group"><label class="form-label">Tour ID (optional)</label><input v-model.number="form.tour_id" type="number" class="form-input" placeholder="Link to tour" /></div>
          <div class="form-group"><label class="form-label">Sort Order</label><input v-model.number="form.sort_order" type="number" class="form-input" /></div>
          <div class="modal-actions">
            <button type="button" class="btn btn-outline" @click="showModal=false">Cancel</button>
            <button type="submit" class="btn btn-primary" :disabled="uploading || !form.url">{{ editing ? 'Update' : 'Create' }}</button>
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
  return { media_type:'image', url:'', thumbnail_url:'', caption_ru:'', caption_en:'', caption_fr:'', tour_id:null, sort_order:0 }
}

async function load() { items.value = (await adminApi.get('/admin/gallery')).data }

function openModal(item) {
  imagePreview.value = null
  if (item) { editing.value = item.id; form.value = { ...item } }
  else { editing.value = null; form.value = getEmpty() }
  showModal.value = true
}

async function handleFileSelect(e) {
  const file = e.target.files[0]
  if (!file) return
  // Auto-detect media type
  if (file.type.startsWith('video/')) form.value.media_type = 'video'
  else form.value.media_type = 'image'

  imagePreview.value = URL.createObjectURL(file)
  uploading.value = true
  try {
    const fd = new FormData()
    fd.append('file', file)
    const res = await adminApi.post('/upload/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    form.value.url = res.data.url
  } catch (err) {
    alert('Upload failed: ' + (err.response?.data?.detail || err.message))
    imagePreview.value = null
  } finally { uploading.value = false }
}

function clearMedia() { form.value.url = ''; imagePreview.value = null }

async function save() {
  if (editing.value) await adminApi.put(`/admin/gallery/${editing.value}`, form.value)
  else await adminApi.post('/admin/gallery', form.value)
  showModal.value = false; await load()
}

async function remove(id) {
  if (confirm('Delete this gallery item?')) { await adminApi.delete(`/admin/gallery/${id}`); await load() }
}

onMounted(load)
</script>
