<template>
  <div>
    <h2>Admin Dashboard</h2>
    
    <!-- Stats -->
    <div class="row mb-4">
        <div class="col-md-4">
            <div class="card bg-info text-white">
                <div class="card-body">
                    <h5>Doctors</h5>
                    <h3>{{ stats.doctors }}</h3>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card bg-success text-white">
                <div class="card-body">
                    <h5>Patients</h5>
                    <h3>{{ stats.patients }}</h3>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card bg-warning text-dark">
                <div class="card-body">
                    <h5>Appointments</h5>
                    <h3>{{ stats.appointments }}</h3>
                </div>
            </div>
        </div>
    </div>

    <ul class="nav nav-tabs mb-3">
        <li class="nav-item"><a class="nav-link" :class="{active: tab==='doctors'}" @click="tab='doctors'" href="#">Doctors</a></li>
        <li class="nav-item"><a class="nav-link" :class="{active: tab==='patients'}" @click="tab='patients'" href="#">Patients</a></li>
        <li class="nav-item"><a class="nav-link" :class="{active: tab==='appointments'}" @click="tab='appointments'" href="#">All Appointments</a></li>
    </ul>

    <!-- Doctors Tab -->
    <div v-if="tab==='doctors'">
        <div class="card mb-3">
            <div class="card-header">Add Doctor</div>
            <div class="card-body">
                <form @submit.prevent="addDoctor" class="row g-3">
                    <div class="col-md-4"><input v-model="newDoc.name" placeholder="Name" class="form-control" required></div>
                    <div class="col-md-4"><input v-model="newDoc.email" placeholder="Email" class="form-control" type="email" required></div>
                     <div class="col-md-4"><input v-model="newDoc.password" placeholder="Password" class="form-control" type="password" required></div>
                     <div class="col-md-4">
                         <select v-model="newDoc.specialization_id" class="form-select" required>
                             <option value="" disabled>Select Department</option>
                             <option v-for="dept in departments" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
                         </select>
                         <small><a href="#" @click.prevent="showDeptModal=true">Add Dept</a></small>
                     </div>
                      <div class="col-md-4"><input v-model="newDoc.experience_years" placeholder="Experience (yrs)" type="number" class="form-control"></div>
                      <div class="col-md-4"><button type="submit" class="btn btn-primary w-100">Add Doctor</button></div>
                </form>
            </div>
        </div>
        <table class="table table-striped">
            <thead><tr><th>Name</th><th>Specialization</th><th>Experience</th><th>Action</th></tr></thead>
            <tbody>
                <tr v-for="doc in doctors" :key="doc.id">
                    <td>{{ doc.name }}</td><td>{{ doc.specialization }}</td><td>{{ doc.experience_years }}</td>
                    <td><button @click="deleteDoctor(doc.id)" class="btn btn-danger btn-sm">Delete</button></td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- Patients Tab -->
    <div v-if="tab==='patients'">
         <table class="table table-striped">
            <thead><tr><th>Name</th><th>Contact</th><th>Address</th></tr></thead>
            <tbody>
                <tr v-for="p in patients" :key="p.id">
                    <td>{{ p.name }}</td><td>{{ p.contact_info }}</td><td>{{ p.address }}</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- Appointments Tab -->
    <div v-if="tab==='appointments'">
         <table class="table table-striped">
            <thead><tr><th>Date</th><th>Patient</th><th>Doctor</th><th>Status</th></tr></thead>
            <tbody>
                <tr v-for="appt in appointments" :key="appt.id">
                    <td>{{ new Date(appt.date_time).toLocaleString() }}</td>
                    <td>{{ appt.patient_name }}</td>
                    <td>{{ appt.doctor_name }}</td>
                    <td>
                        <span :class="{'badge bg-success': appt.status==='completed', 'badge bg-warning': appt.status==='booked', 'badge bg-danger': appt.status==='cancelled'}">{{ appt.status }}</span>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    
    <!-- Add Dept Modal (Simple prompt logic for now to save time or inline) -->
    <div v-if="showDeptModal" class="modal d-block" style="background: rgba(0,0,0,0.5)">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header"><h5 class="modal-title">Add Department</h5></div>
                <div class="modal-body">
                    <input v-model="newDeptName" class="form-control mb-2" placeholder="Name">
                    <input v-model="newDeptDesc" class="form-control" placeholder="Description">
                </div>
                <div class="modal-footer">
                    <button @click="showDeptModal=false" class="btn btn-secondary">Close</button>
                    <button @click="addDepartment" class="btn btn-primary">Save</button>
                </div>
            </div>
        </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import axios from 'axios'

const stats = ref({ doctors: 0, patients: 0, appointments: 0 })
const tab = ref('doctors')
const doctors = ref([])
const patients = ref([])
const appointments = ref([])
const departments = ref([])
const showDeptModal = ref(false)
const newDeptName = ref('')
const newDeptDesc = ref('')

const newDoc = reactive({ name: '', email: '', password: '', specialization_id: '', experience_years: 0 })

const API_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000') + '/api/admin'

const loadData = async () => {
    const statsRes = await axios.get(`${API_URL}/stats`)
    stats.value = statsRes.data
    
    const docsRes = await axios.get(`${API_URL}/doctors`)
    doctors.value = docsRes.data
    
    const patsRes = await axios.get(`${API_URL}/patients`)
    patients.value = patsRes.data
    
    const apptsRes = await axios.get(`${API_URL}/appointments`)
    appointments.value = apptsRes.data
    
    const deptsRes = await axios.get(`${API_URL}/departments`)
    departments.value = deptsRes.data
}

const addDoctor = async () => {
    try {
        await axios.post(`${API_URL}/doctors`, newDoc)
        alert('Doctor added')
        loadData()
        // Reset form
        Object.assign(newDoc, { name: '', email: '', password: '', specialization_id: '', experience_years: 0 })
    } catch (e) {
        alert(e.response?.data?.error || 'Error adding doctor')
    }
}

const deleteDoctor = async (id) => {
    if(!confirm('Are you sure?')) return
    try {
        await axios.delete(`${API_URL}/doctors/${id}`)
        loadData()
    } catch (e) {
        alert('Error deleting')
    }
}

const addDepartment = async () => {
    try {
        await axios.post(`${API_URL}/departments`, { name: newDeptName.value, description: newDeptDesc.value })
        showDeptModal.value = false
        loadData()
    } catch (e) {
        alert('Error')
    }
}

onMounted(loadData)
</script>
