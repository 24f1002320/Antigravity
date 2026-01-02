<template>
  <div>
    <h2>Patient Dashboard</h2>
    
    <ul class="nav nav-tabs mb-3">
        <li class="nav-item"><a class="nav-link" :class="{active: tab==='doctors'}" @click="tab='doctors'" href="#">Book Appointment</a></li>
        <li class="nav-item"><a class="nav-link" :class="{active: tab==='appointments'}" @click="tab='appointments'" href="#">My Appointments</a></li>
        <li class="nav-item"><a class="nav-link" :class="{active: tab==='history'}" @click="tab='history'" href="#">History</a></li>
    </ul>

    <!-- Doctors Search & Book -->
    <div v-if="tab==='doctors'">
        <div class="row mb-3">
            <div class="col-md-4">
                <select class="form-select" v-model="selectedDept" @change="searchDoctors">
                    <option value="">All Departments</option>
                    <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
                </select>
            </div>
        </div>
        <div class="row">
            <div class="col-md-4 mb-3" v-for="doc in doctors" :key="doc.id">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">{{ doc.name }}</h5>
                        <h6 class="card-subtitle mb-2 text-muted">{{ doc.specialization }}</h6>
                        <p class="card-text">Experience: {{ doc.experience_years }} years</p>
                        <p class="small">Availability: {{ doc.availability_schedule }}</p>
                        <button class="btn btn-primary w-100" @click="openBook(doc)">Book Appointment</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- My Appointments -->
    <div v-if="tab==='appointments'">
        <table class="table table-striped">
            <thead><tr><th>Date</th><th>Doctor</th><th>Status</th><th>Action</th></tr></thead>
            <tbody>
                <tr v-for="appt in appointments" :key="appt.id">
                    <td>{{ new Date(appt.date_time).toLocaleString() }}</td>
                    <td>{{ appt.doctor_name }}</td>
                    <td>{{ appt.status }}</td>
                    <td>
                        <button v-if="appt.status==='booked'" class="btn btn-danger btn-sm" @click="cancelAppt(appt.id)">Cancel</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- History -->
    <div v-if="tab==='history'">
        <div class="mb-3 text-end">
            <button class="btn btn-secondary" @click="exportHistory">Export History (CSV)</button>
        </div>
        <div v-for="appt in history" :key="appt.id" class="card mb-3">
            <div class="card-header">{{ new Date(appt.date_time).toLocaleDateString() }} - {{ appt.doctor_name }}</div>
            <div class="card-body">
                <p><strong>Diagnosis:</strong> {{ appt.diagnosis }}</p>
                 <p><strong>Prescription:</strong> {{ appt.prescription }}</p>
                  <p><strong>Notes:</strong> {{ appt.notes }}</p>
            </div>
        </div>
    </div>

    <!-- Book Modal -->
    <div v-if="showBookModal" class="modal d-block" style="background: rgba(0,0,0,0.5)">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header"><h5 class="modal-title">Book with {{ bookingDoc.name }}</h5></div>
                <div class="modal-body">
                    <label>Date & Time</label>
                    <input type="datetime-local" class="form-control" v-model="bookingDate">
                </div>
                <div class="modal-footer">
                    <button @click="showBookModal=false" class="btn btn-secondary">Close</button>
                    <button @click="confirmBooking" class="btn btn-success">Book</button>
                </div>
            </div>
        </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const tab = ref('doctors')
const doctors = ref([])
const departments = ref([])
const appointments = ref([])
const history = ref([])
const selectedDept = ref('')
const showBookModal = ref(false)
const bookingDoc = ref(null)
const bookingDate = ref('')

const API_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000') + '/api/patient'

const searchDoctors = async () => {
    const params = selectedDept.value ? { specialization_id: selectedDept.value } : {}
    const res = await axios.get(`${API_URL}/doctors`, { params })
    doctors.value = res.data
}

const loadData = async () => {
    // Departments
    const deptRes = await axios.get(`${API_URL}/departments`)
    departments.value = deptRes.data
    searchDoctors()
    
    // History includes all appts, we can filter for just history view or use the same endpoint
    // "History" usually means completed. "My Appointments" means upcoming.
    // The endpoint `get_history` returns all in strict implementation (ordered desc).
    const histRes = await axios.get(`${API_URL}/history`)
    const all = histRes.data
    appointments.value = all.filter(a => a.status === 'booked')
    history.value = all.filter(a => a.status === 'completed')
}

const openBook = (doc) => {
    bookingDoc.value = doc
    showBookModal.value = true
}

const confirmBooking = async () => {
    try {
        await axios.post(`${API_URL}/appointments`, {
            doctor_id: bookingDoc.value.id,
            date_time: bookingDate.value // datetime-local sends ISO-like format
        })
        showBookModal.value = false
        alert('Booked successfully')
        loadData()
    } catch (e) {
        alert(e.response?.data?.error || 'Error booking')
    }
}

const cancelAppt = async (id) => {
    if(!confirm('Cancel appointment?')) return
    try {
        await axios.put(`${API_URL}/appointments/${id}`, { status: 'cancelled' })
        loadData()
    } catch (e) {
        alert('Error cancelling')
    }
}

const exportHistory = async () => {
    try {
        await axios.post(`${API_URL}/export`)
        alert('Export job started. You will be notified.')
    } catch (e) {
        alert('Error starting export')
    }
}

onMounted(loadData)
</script>
