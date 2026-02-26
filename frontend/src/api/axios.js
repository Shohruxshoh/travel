/**
 * Axios Instance Configuration
 * All API calls go through this instance, which automatically
 * attaches the Accept-Language header from the current locale.
 */

import axios from 'axios'

const api = axios.create({
    baseURL: '/api',
    timeout: 15000,
    headers: {
        'Content-Type': 'application/json',
    },
})

// ── Request interceptor: attach Accept-Language ─────────────────
api.interceptors.request.use((config) => {
    // vue-i18n stores locale in the i18n instance;
    // we read it from localStorage as a lightweight approach
    const locale = localStorage.getItem('locale') || 'en'
    config.headers['Accept-Language'] = locale
    return config
})

// ── Response interceptor: handle errors globally ────────────────
api.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error('API Error:', error.response?.data || error.message)
        return Promise.reject(error)
    }
)

export default api
