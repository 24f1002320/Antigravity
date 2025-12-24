import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:5000/api/auth'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        user: JSON.parse(localStorage.getItem('user')) || null,
    }),
    actions: {
        async login(email, password) {
            try {
                const response = await axios.post(`${API_URL}/login`, { email, password })
                this.token = response.data.token
                this.user = response.data.user
                localStorage.setItem('token', this.token)
                localStorage.setItem('user', JSON.stringify(this.user))
                return true
            } catch (error) {
                throw error
            }
        },
        async register(patientData) {
            await axios.post(`${API_URL}/register`, patientData)
        },
        logout() {
            this.token = null
            this.user = null
            localStorage.removeItem('token')
            localStorage.removeItem('user')
        }
    }
})
