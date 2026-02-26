<!--
  AdminOperators.vue — Full CRUD for language operator configs
-->
<template>
  <div>
    <div class="admin-content-header">
      <h1>📧 Email Operators</h1>
      <button class="btn btn-primary" @click="openModal()">+ Add Operator</button>
    </div>

    <div class="admin-table-wrapper">
      <table class="admin-table">
        <thead><tr><th>ID</th><th>Language</th><th>Operator Name</th><th>Email</th><th>Actions</th></tr></thead>
        <tbody>
          <tr v-for="c in items" :key="c.id">
            <td>#{{ c.id }}</td>
            <td>{{ c.language_code?.toUpperCase() }}</td>
            <td>{{ c.operator_name }}</td>
            <td>{{ c.operator_email }}</td>
            <td>
              <button class="btn btn-outline btn-sm" @click="openModal(c)">Edit</button>
              <button class="btn btn-danger btn-sm" @click="remove(c.id)" style="margin-left:6px;">Delete</button>
            </td>
          </tr>
          <tr v-if="!items.length"><td colspan="5" style="text-align:center; color:var(--text-tertiary); padding:24px;">No operators configured yet.</td></tr>
        </tbody>
      </table>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="showModal=false">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ editing ? 'Edit Operator' : 'Add Operator' }}</h2>
          <button class="modal-close" @click="showModal=false">✕</button>
        </div>
        <form @submit.prevent="save">
          <div class="form-group">
            <label class="form-label">Language Code</label>
            <select v-model="form.language_code" class="form-input" required>
              <option value="ru">RU — Russian</option>
              <option value="en">EN — English</option>
              <option value="fr">FR — French</option>
            </select>
          </div>
          <div class="form-group"><label class="form-label">Operator Name</label><input v-model="form.operator_name" class="form-input" required /></div>
          <div class="form-group"><label class="form-label">Operator Email</label><input v-model="form.operator_email" type="email" class="form-input" required /></div>
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
  return { language_code:'en', operator_name:'', operator_email:'' }
}

async function load() { items.value = (await adminApi.get('/admin/operator-configs')).data }

function openModal(item) {
  if (item) { editing.value = item.id; form.value = { ...item } }
  else { editing.value = null; form.value = getEmpty() }
  showModal.value = true
}

async function save() {
  if (editing.value) await adminApi.put(`/admin/operator-configs/${editing.value}`, form.value)
  else await adminApi.post('/admin/operator-configs', form.value)
  showModal.value = false; await load()
}

async function remove(id) {
  if (confirm('Delete this operator config?')) { await adminApi.delete(`/admin/operator-configs/${id}`); await load() }
}

onMounted(load)
</script>
