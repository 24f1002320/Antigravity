import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import DoctorDashboard from '../views/DoctorDashboard.vue'
import PatientDashboard from '../views/PatientDashboard.vue'
import { useAuthStore } from '../store/auth'

const routes = [
    { path: '/', component: Login },
    { path: '/login', component: Login, name: 'Login' },
    { path: '/register', component: Register, name: 'Register' },
    {
        path: '/admin',
        component: AdminDashboard,
        meta: { requiresAuth: true, role: 'admin' }
    },
    {
        path: '/doctor',
        component: DoctorDashboard,
        meta: { requiresAuth: true, role: 'doctor' }
    },
    {
        path: '/patient',
        component: PatientDashboard,
        meta: { requiresAuth: true, role: 'patient' }
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach((to, from, next) => {
    const auth = useAuthStore()
    if (to.meta.requiresAuth) {
        if (!auth.token) {
            return next('/login')
        }
        if (to.meta.role && auth.user.role !== to.meta.role) {
            return next('/login') // or 403 page
        }
    }
    next()
})

export default router
