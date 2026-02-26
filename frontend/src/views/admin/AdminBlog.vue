<!--
  AdminBlog.vue — Full CRUD for blog articles with cover image upload
-->
<template>
  <div>
    <div class="admin-content-header">
      <h1>📝 Blog Articles</h1>
      <button class="btn btn-primary" @click="openModal()">+ Add Article</button>
    </div>

    <div class="admin-table-wrapper">
      <table class="admin-table">
        <thead><tr><th>ID</th><th>Image</th><th>Title (EN)</th><th>Slug</th><th>Author</th><th>Published</th><th>Actions</th></tr></thead>
        <tbody>
          <tr v-for="a in items" :key="a.id">
            <td>#{{ a.id }}</td>
            <td><img v-if="a.cover_image" :src="a.cover_image" class="admin-thumb" /><span v-else class="admin-thumb-empty">📷</span></td>
            <td>{{ a.title_en }}</td>
            <td>{{ a.slug }}</td>
            <td>{{ a.author || '-' }}</td>
            <td><span class="status-badge" :class="a.is_published ? 'status-active' : 'status-pending'">{{ a.is_published ? 'Published' : 'Draft' }}</span></td>
            <td>
              <button class="btn btn-outline btn-sm" @click="openModal(a)">Edit</button>
              <button class="btn btn-danger btn-sm" @click="remove(a.id)" style="margin-left:6px;">Delete</button>
            </td>
          </tr>
          <tr v-if="!items.length"><td colspan="7" style="text-align:center; color:var(--text-tertiary); padding:24px;">No articles yet.</td></tr>
        </tbody>
      </table>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="showModal=false">
      <div class="modal-content" style="max-width:620px;">
        <div class="modal-header">
          <h2>{{ editing ? 'Edit Article' : 'Add Article' }}</h2>
          <button class="modal-close" @click="showModal=false">✕</button>
        </div>
        <form @submit.prevent="save">
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
          </div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
            <div class="form-group"><label class="form-label">Title (FR)</label><input v-model="form.title_fr" class="form-input" required /></div>
            <div class="form-group"><label class="form-label">Slug</label><input v-model="form.slug" class="form-input" required /></div>
          </div>
          <div class="form-group"><label class="form-label">Content (RU)</label><textarea v-model="form.content_ru" class="form-input form-textarea" required></textarea></div>
          <div class="form-group"><label class="form-label">Content (EN)</label><textarea v-model="form.content_en" class="form-input form-textarea" required></textarea></div>
          <div class="form-group"><label class="form-label">Content (FR)</label><textarea v-model="form.content_fr" class="form-input form-textarea" required></textarea></div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
            <div class="form-group"><label class="form-label">Author</label><input v-model="form.author" class="form-input" /></div>
            <div class="form-group">
              <label class="form-label">Published</label>
              <select v-model="form.is_published" class="form-input"><option :value="true">Published</option><option :value="false">Draft</option></select>
            </div>
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
  return { title_ru:'',title_en:'',title_fr:'',content_ru:'',content_en:'',content_fr:'',slug:'',author:'',cover_image:'',is_published:false }
}

async function load() { items.value = (await adminApi.get('/admin/blog')).data }

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
  } finally { uploading.value = false }
}

function clearImage() { form.value.cover_image = ''; imagePreview.value = null }

async function save() {
  if (editing.value) await adminApi.put(`/admin/blog/${editing.value}`, form.value)
  else await adminApi.post('/admin/blog', form.value)
  showModal.value = false; await load()
}

async function remove(id) {
  if (confirm('Delete this article?')) { await adminApi.delete(`/admin/blog/${id}`); await load() }
}

onMounted(load)
</script>
