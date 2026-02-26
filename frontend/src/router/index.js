/**
 * Vue Router Configuration
 * Public pages + Admin panel with auth guard.
 */

import { createRouter, createWebHistory } from 'vue-router'
import { isAuthenticated } from '../api/adminApi.js'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('../views/HomeView.vue'),
    },
    {
        path: '/tours',
        name: 'Tours',
        component: () => import('../views/ToursView.vue'),
    },
    {
        path: '/tours/:id',
        name: 'TourDetail',
        component: () => import('../views/TourDetailView.vue'),
    },
    {
        path: '/info',
        name: 'Info',
        component: () => import('../views/InfoView.vue'),
    },
    {
        path: '/hotels',
        name: 'Hotels',
        component: () => import('../views/HotelsView.vue'),
    },
    {
        path: '/blog',
        name: 'Blog',
        component: () => import('../views/BlogView.vue'),
    },
    {
        path: '/gallery',
        name: 'Gallery',
        component: () => import('../views/GalleryView.vue'),
    },
    {
        path: '/monuments',
        name: 'Monuments',
        component: () => import('../views/MonumentsView.vue'),
    },
    // ─── Admin Login (public) ───
    {
        path: '/admin/login',
        name: 'AdminLogin',
        component: () => import('../views/admin/AdminLogin.vue'),
        meta: { hideNavbar: true, hideFooter: true },
    },
    // ─── Admin Panel (requires auth) ───
    {
        path: '/admin',
        component: () => import('../views/admin/AdminLayout.vue'),
        meta: { requiresAuth: true },
        children: [
            {
                path: '',
                name: 'AdminDashboard',
                component: () => import('../views/admin/AdminDashboard.vue'),
            },
            {
                path: 'bookings',
                name: 'AdminBookings',
                component: () => import('../views/admin/AdminBookings.vue'),
            },
            {
                path: 'tours',
                name: 'AdminTours',
                component: () => import('../views/admin/AdminTours.vue'),
            },
            {
                path: 'operators',
                name: 'AdminOperators',
                component: () => import('../views/admin/AdminOperators.vue'),
            },
            {
                path: 'hotels',
                name: 'AdminHotels',
                component: () => import('../views/admin/AdminHotels.vue'),
            },
            {
                path: 'services',
                name: 'AdminServices',
                component: () => import('../views/admin/AdminServices.vue'),
            },
            {
                path: 'blog',
                name: 'AdminBlog',
                component: () => import('../views/admin/AdminBlog.vue'),
            },
            {
                path: 'gallery',
                name: 'AdminGallery',
                component: () => import('../views/admin/AdminGallery.vue'),
            },
        ],
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior() {
        return { top: 0 }
    },
})

// ─── Auth Guard ───
router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!isAuthenticated()) {
            next({ name: 'AdminLogin' })
        } else {
            next()
        }
    } else {
        next()
    }
})

export default router
