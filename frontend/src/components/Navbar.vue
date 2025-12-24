<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4" v-if="auth.token">
    <div class="container">
      <a class="navbar-brand" href="#">HMS</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item" v-if="auth.user?.role === 'admin'">
            <router-link class="nav-link" to="/admin">Admin Dashboard</router-link>
          </li>
          <li class="nav-item" v-if="auth.user?.role === 'doctor'">
            <router-link class="nav-link" to="/doctor">Doctor Dashboard</router-link>
          </li>
          <li class="nav-item" v-if="auth.user?.role === 'patient'">
            <router-link class="nav-link" to="/patient">Patient Dashboard</router-link>
          </li>
        </ul>
        <div class="d-flex">
            <span class="navbar-text me-3" v-if="auth.user">Welcome, {{ auth.user.name || auth.user.email }}</span>
            <button class="btn btn-outline-light btn-sm" @click="logout">Logout</button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '../store/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const logout = () => {
    auth.logout()
    router.push('/login')
}
</script>
