<template>
  <div class="admin-comments-page">
    <!-- Header -->
    <div class="admin-page-header">
      <div>
        <h1 class="admin-page-title">💬 Comments</h1>
        <p class="admin-page-sub">Manage visitor reviews and feedback</p>
      </div>
      <div class="admin-header-actions">
        <select v-model="filterApproved" class="admin-select" @change="loadComments">
          <option value="">All</option>
          <option value="true">Approved</option>
          <option value="false">Pending</option>
        </select>
        <span class="admin-badge">{{ filtered.length }} comments</span>
      </div>
    </div>

    <!-- Search -->
    <div class="admin-search-bar">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
      <input v-model="search" placeholder="Search by name, country, or text..." class="admin-search-input" />
    </div>

    <!-- Table -->
    <div class="admin-table-wrap">
      <div v-if="isLoading" class="admin-loading">Loading…</div>
      <div v-else-if="!filtered.length" class="admin-empty">No comments found.</div>
      <table v-else class="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Author</th>
            <th>Country</th>
            <th>Review</th>
            <th>Image</th>
            <th>Status</th>
            <th>Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in filtered" :key="c.id" :class="{ 'row-pending': !c.approved }">
            <td class="td-id">#{{ c.id }}</td>
            <td class="td-author">
              <div class="author-avatar" :style="{ background: avatarColor(c.author_name) }">
                {{ initials(c.author_name) }}
              </div>
              {{ c.author_name }}
            </td>
            <td>{{ c.country }}</td>
            <td class="td-desc">
              <span class="desc-text">{{ c.description }}</span>
            </td>
            <td>
              <a v-if="c.image_url" :href="c.image_url" target="_blank" class="img-thumb-link">
                <img :src="c.image_url" class="img-thumb" />
              </a>
              <span v-else class="no-img">—</span>
            </td>
            <td>
              <button
                class="status-badge"
                :class="c.approved ? 'approved' : 'pending'"
                @click="toggleApprove(c)"
                :title="c.approved ? 'Click to reject' : 'Click to approve'"
              >
                {{ c.approved ? '✅ Approved' : '⏳ Pending' }}
              </button>
            </td>
            <td class="td-date">{{ formatDate(c.created_at) }}</td>
            <td class="td-actions">
              <button class="btn-icon edit" @click="openEdit(c)" title="Edit">✏️</button>
              <button class="btn-icon del" @click="confirmDelete(c)" title="Delete">🗑️</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Edit Modal -->
    <teleport to="body">
      <div v-if="editModal" class="modal-overlay" @click.self="editModal = null">
        <div class="modal-box">
          <h3 class="modal-title">✏️ Edit Comment #{{ editModal.id }}</h3>
          <div class="modal-field">
            <label>Author Name</label>
            <input v-model="editModal.author_name" class="admin-input" maxlength="100" />
          </div>
          <div class="modal-field">
            <label>Country</label>
            <input v-model="editModal.country" class="admin-input" maxlength="100" />
          </div>
          <div class="modal-field">
            <label>Review Text</label>
            <textarea v-model="editModal.description" class="admin-textarea" rows="5" maxlength="1000"></textarea>
          </div>
          <div class="modal-field" style="flex-direction:row;align-items:center;gap:10px;">
            <label>Approved</label>
            <input type="checkbox" v-model="editModal.approved" style="width:18px;height:18px;cursor:pointer;" />
          </div>
          <div class="modal-actions">
            <button class="btn btn-outline" @click="editModal = null">Cancel</button>
            <button class="btn btn-primary" :disabled="isSaving" @click="saveEdit">
              {{ isSaving ? 'Saving…' : 'Save' }}
            </button>
          </div>
        </div>
      </div>
    </teleport>

    <!-- Delete Confirm Modal -->
    <teleport to="body">
      <div v-if="deleteTarget" class="modal-overlay" @click.self="deleteTarget = null">
        <div class="modal-box modal-sm">
          <h3 class="modal-title">🗑️ Delete Comment?</h3>
          <p style="color:var(--text-secondary);font-size:0.9rem;margin-bottom:20px;">
            This action cannot be undone. Comment by <strong>{{ deleteTarget.author_name }}</strong> will be permanently deleted.
          </p>
          <div class="modal-actions">
            <button class="btn btn-outline" @click="deleteTarget = null">Cancel</button>
            <button class="btn btn-danger" :disabled="isDeleting" @click="doDelete">
              {{ isDeleting ? 'Deleting…' : 'Delete' }}
            </button>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import adminApi from '../../api/adminApi.js'

const comments = ref([])
const isLoading = ref(true)
const isSaving = ref(false)
const isDeleting = ref(false)
const search = ref('')
const filterApproved = ref('')
const editModal = ref(null)
const deleteTarget = ref(null)

// ── Filtered list ─────────────────────────────────────────────────
const filtered = computed(() => {
  const q = search.value.toLowerCase().trim()
  return comments.value.filter(c => {
    if (!q) return true
    return (
      c.author_name.toLowerCase().includes(q) ||
      c.country.toLowerCase().includes(q) ||
      c.description.toLowerCase().includes(q)
    )
  })
})

// ── Load ─────────────────────────────────────────────────────────
async function loadComments() {
  isLoading.value = true
  try {
    const params = {}
    if (filterApproved.value !== '') params.approved = filterApproved.value
    const res = await adminApi.get('/admin/comments', { params })
    comments.value = res.data
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
}

// ── Approve/Reject toggle ─────────────────────────────────────────
async function toggleApprove(c) {
  try {
    const res = await adminApi.put(`/admin/comments/${c.id}`, { approved: !c.approved })
    const idx = comments.value.findIndex(x => x.id === c.id)
    if (idx !== -1) comments.value[idx] = res.data
  } catch (e) {
    console.error(e)
  }
}

// ── Edit ─────────────────────────────────────────────────────────
function openEdit(c) {
  editModal.value = { ...c }
}

async function saveEdit() {
  if (!editModal.value) return
  isSaving.value = true
  try {
    const res = await adminApi.put(`/admin/comments/${editModal.value.id}`, {
      author_name: editModal.value.author_name,
      country: editModal.value.country,
      description: editModal.value.description,
      approved: editModal.value.approved,
    })
    const idx = comments.value.findIndex(x => x.id === res.data.id)
    if (idx !== -1) comments.value[idx] = res.data
    editModal.value = null
  } catch (e) {
    console.error(e)
  } finally {
    isSaving.value = false
  }
}

// ── Delete ────────────────────────────────────────────────────────
function confirmDelete(c) {
  deleteTarget.value = c
}

async function doDelete() {
  if (!deleteTarget.value) return
  isDeleting.value = true
  try {
    await adminApi.delete(`/admin/comments/${deleteTarget.value.id}`)
    comments.value = comments.value.filter(x => x.id !== deleteTarget.value.id)
    deleteTarget.value = null
  } catch (e) {
    console.error(e)
  } finally {
    isDeleting.value = false
  }
}

// ── Helpers ───────────────────────────────────────────────────────
const COLORS = ['#2563eb','#7c3aed','#db2777','#059669','#d97706','#dc2626','#0891b2','#65a30d']
function avatarColor(name) {
  let h = 0
  for (const ch of (name || 'x')) h = (h * 31 + ch.charCodeAt(0)) & 0xffffffff
  return COLORS[Math.abs(h) % COLORS.length]
}
function initials(name) {
  return (name || '?').split(' ').map(w => w[0]?.toUpperCase() || '').slice(0, 2).join('')
}
function formatDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('en-GB', { day:'2-digit', month:'short', year:'numeric' })
}

onMounted(loadComments)
</script>

<style scoped>
.admin-comments-page { padding: 32px; }

.admin-page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 12px;
}
.admin-page-title { font-size: 1.6rem; font-weight: 800; color: var(--text-primary); }
.admin-page-sub { color: var(--text-secondary); font-size: 0.88rem; margin-top: 4px; }
.admin-header-actions { display: flex; align-items: center; gap: 10px; }
.admin-select {
  padding: 7px 12px; border-radius: 8px; border: 1px solid var(--border-medium);
  background: var(--bg-elevated); color: var(--text-primary); font-size: 0.85rem;
  cursor: pointer;
}
.admin-badge {
  background: var(--sidebar-active); color: var(--text-brand);
  padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;
}

.admin-search-bar {
  display: flex; align-items: center; gap: 10px;
  background: var(--bg-elevated); border: 1px solid var(--border-light);
  border-radius: 10px; padding: 10px 14px; margin-bottom: 20px;
  color: var(--text-tertiary);
}
.admin-search-input {
  flex: 1; background: transparent; border: none; outline: none;
  font-size: 0.9rem; color: var(--text-primary); font-family: inherit;
}

.admin-table-wrap {
  background: var(--bg-elevated); border-radius: 14px;
  border: 1px solid var(--border-light); overflow-x: auto;
}
.admin-table { width: 100%; border-collapse: collapse; }
.admin-table th {
  padding: 12px 14px; text-align: left; font-size: 0.75rem; font-weight: 700;
  color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0.8px;
  border-bottom: 1px solid var(--border-light);
}
.admin-table td {
  padding: 12px 14px; border-bottom: 1px solid var(--border-light);
  font-size: 0.87rem; color: var(--text-primary); vertical-align: middle;
}
.admin-table tr:last-child td { border-bottom: none; }
.admin-table tr:hover td { background: var(--bg-tertiary); }
.row-pending td { opacity: 0.75; }

.td-id { color: var(--text-tertiary); font-size: 0.8rem; }
.td-author { display: flex; align-items: center; gap: 8px; font-weight: 600; white-space: nowrap; }
.author-avatar {
  width: 30px; height: 30px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.7rem; font-weight: 700; color: #fff; flex-shrink: 0;
}
.td-desc { max-width: 260px; }
.desc-text {
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
  overflow: hidden; line-height: 1.4;
}
.img-thumb { width: 44px; height: 36px; object-fit: cover; border-radius: 6px; display: block; }
.img-thumb-link { display: block; }
.no-img { color: var(--text-tertiary); }
.td-date { white-space: nowrap; color: var(--text-secondary); font-size: 0.82rem; }

.status-badge {
  padding: 4px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 700;
  cursor: pointer; border: none; transition: all 0.15s ease;
}
.status-badge.approved { background: rgba(16,185,129,0.15); color: #10b981; }
.status-badge.approved:hover { background: rgba(16,185,129,0.3); }
.status-badge.pending { background: rgba(245,158,11,0.15); color: #f59e0b; }
.status-badge.pending:hover { background: rgba(245,158,11,0.3); }

.td-actions { display: flex; gap: 6px; }
.btn-icon {
  width: 32px; height: 32px; border: 1px solid var(--border-light); border-radius: 8px;
  background: transparent; cursor: pointer; font-size: 0.9rem;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.15s ease;
}
.btn-icon.edit:hover { background: rgba(99,102,241,0.15); border-color: #6366f1; }
.btn-icon.del:hover { background: rgba(239,68,68,0.15); border-color: #ef4444; }

/* Modal */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.6); z-index: 5000;
  display: flex; align-items: center; justify-content: center; padding: 20px;
  backdrop-filter: blur(4px);
}
.modal-box {
  background: var(--bg-elevated); border-radius: 16px; padding: 28px;
  width: 100%; max-width: 520px; border: 1px solid var(--border-light);
  box-shadow: 0 20px 60px rgba(0,0,0,0.4);
}
.modal-sm { max-width: 380px; }
.modal-title { font-size: 1.1rem; font-weight: 700; margin-bottom: 20px; color: var(--text-primary); }
.modal-field { display: flex; flex-direction: column; gap: 6px; margin-bottom: 16px; }
.modal-field label { font-size: 0.8rem; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px; }
.admin-input, .admin-textarea {
  padding: 10px 12px; border: 1px solid var(--border-medium); border-radius: 8px;
  background: var(--bg-secondary); color: var(--text-primary); font-family: inherit;
  font-size: 0.9rem; outline: none; transition: border-color 0.15s;
}
.admin-input:focus, .admin-textarea:focus { border-color: var(--brand-primary); }
.admin-textarea { resize: vertical; min-height: 100px; }
.modal-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; }
.btn-danger {
  background: #ef4444; color: #fff; border: none; padding: 10px 22px;
  border-radius: 8px; font-weight: 600; cursor: pointer; transition: background 0.15s;
}
.btn-danger:hover { background: #dc2626; }
.btn-danger:disabled { opacity: 0.5; cursor: not-allowed; }

.admin-loading, .admin-empty {
  padding: 60px; text-align: center; color: var(--text-tertiary); font-size: 0.95rem;
}
</style>
