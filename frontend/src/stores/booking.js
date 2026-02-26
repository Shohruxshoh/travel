/**
 * Booking Pinia Store
 * Manages booking form state, tour list, and API submission.
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api/axios.js'

export const useBookingStore = defineStore('booking', () => {
    // ── State ─────────────────────────────────────────────────────
    const tours = ref([])
    const isLoadingTours = ref(false)
    const isSubmitting = ref(false)
    const submitSuccess = ref(false)
    const submitError = ref(null)

    // ── Actions ───────────────────────────────────────────────────

    /**
     * Fetch available tours from the API.
     */
    async function fetchTours() {
        isLoadingTours.value = true
        try {
            const response = await api.get('/tours/')
            tours.value = response.data
        } catch (error) {
            console.error('Failed to fetch tours:', error)
        } finally {
            isLoadingTours.value = false
        }
    }

    /**
     * Submit a booking to the API.
     * The language field is critical — it drives the smart email routing.
     *
     * @param {Object} bookingData - { tour_id, customer_name, customer_email, customer_phone, message, language }
     */
    async function submitBooking(bookingData) {
        isSubmitting.value = true
        submitSuccess.value = false
        submitError.value = null

        try {
            await api.post('/bookings/', bookingData)
            submitSuccess.value = true
        } catch (error) {
            submitError.value =
                error.response?.data?.detail || 'An unexpected error occurred.'
        } finally {
            isSubmitting.value = false
        }
    }

    /**
     * Reset the submission state (e.g., when re-opening the form).
     */
    function resetState() {
        submitSuccess.value = false
        submitError.value = null
    }

    return {
        tours,
        isLoadingTours,
        isSubmitting,
        submitSuccess,
        submitError,
        fetchTours,
        submitBooking,
        resetState,
    }
})
