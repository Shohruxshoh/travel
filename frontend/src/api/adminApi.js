/**
 * Admin API helper
 * Handles authentication and adds JWT token to admin requests.
 */

import axios from 'axios'

const API_BASE = '/api'

// ── Token management ────────────────────────────
export function getToken() {
    return localStorage.getItem('admin_token')
}

export function setToken(token) {
    localStorage.setItem('admin_token', token)
}

export function removeToken() {
    localStorage.removeItem('admin_token')
}

export function isAuthenticated() {
    return !!getToken()
}

// ── Authenticated Axios instance for admin ──────
const adminApi = axios.create({
    baseURL: API_BASE,
    headers: { 'Content-Type': 'application/json' },
})

// Attach JWT token to every request
adminApi.interceptors.request.use((config) => {
    const token = getToken()
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

// Handle 401 errors (redirect to login)
adminApi.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            removeToken()
            window.location.href = '/admin/login'
        }
        return Promise.reject(error)
    }
)

// ── Auth API ────────────────────────────────────
export async function login(username, password) {
    const res = await axios.post(`${API_BASE}/auth/login`, { username, password })
    const { access_token, username: name } = res.data
    setToken(access_token)
    return name
}

export function logout() {
    removeToken()
    window.location.href = '/admin/login'
}

export default adminApi
