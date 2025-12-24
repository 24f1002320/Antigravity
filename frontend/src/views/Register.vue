<template>
  <div class="row justify-content-center mt-5">
    <div class="col-md-8">
      <div class="card">
        <div class="card-header">Patient Registration</div>
        <div class="card-body">
          <form @submit.prevent="handleRegister">
            <div class="mb-3">
              <label class="form-label">Name</label>
              <input type="text" class="form-control" v-model="form.name" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Email</label>
              <input type="email" class="form-control" v-model="form.email" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Password</label>
              <input type="password" class="form-control" v-model="form.password" required>
            </div>
             <div class="mb-3">
              <label class="form-label">Date of Birth</label>
              <input type="date" class="form-control" v-model="form.dob">
            </div>
             <div class="mb-3">
              <label class="form-label">Contact Info</label>
              <input type="text" class="form-control" v-model="form.contact_info">
            </div>
             <div class="mb-3">
              <label class="form-label">Address</label>
              <textarea class="form-control" v-model="form.address"></textarea>
            </div>
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <button type="submit" class="btn btn-success w-100">Register</button>
          </form>
          <div class="mt-3 text-center">
            <router-link to="/login">Already have an account? Login</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useAuthStore } from '../store/auth'
import { useRouter } from 'vue-router'

const form = reactive({
    name: '',
    email: '',
    password: '',
    dob: '',
    contact_info: '',
    address: ''
})
const error = ref('')
const auth = useAuthStore()
const router = useRouter()

const handleRegister = async () => {
    try {
        await auth.register(form)
        alert('Registration successful! Please login.')
        router.push('/login')
    } catch (e) {
        error.value = e.response?.data?.error || 'Registration failed'
    }
}
</script>
