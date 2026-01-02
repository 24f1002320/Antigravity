<template>
  <div>
    <h2>Doctor Dashboard</h2>
    
    <div class="row">
        <div class="col-md-8">
            <h4>My Appointments</h4>
            <table class="table table-striped">
                <thead><tr><th>Date</th><th>Patient</th><th>Status</th><th>Action</th></tr></thead>
                <tbody>
                    <tr v-for="appt in appointments" :key="appt.id">
                        <td>{{ new Date(appt.date_time).toLocaleString() }}</td>
                        <td>{{ appt.patient_name }}</td>
                        <td>
                            <span :class="{'badge bg-success': appt.status==='completed', 'badge bg-warning': appt.status==='booked', 'badge bg-danger': appt.status==='cancelled'}">{{ appt.status }}</span>
                        </td>
                        <td>
                            <button v-if="appt.status==='booked'" class="btn btn-primary btn-sm" @click="openComplete(appt)">Complete</button>
                            <span v-else>-</span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="col-md-4">
             <h4>Availability</h4>
             <div class="card">
                 <div class="card-body">
                     <p>Manage your weekly availability.</p>
                     <textarea class="form-control mb-2" v-model="availabilityJson" rows="5" placeholder='{"Monday": ["09:00", "17:00"]}'></textarea>
                     <button class="btn btn-secondary w-100" @click="updateAvailability">Update</button>
                 </div>
             </div>
        </div>
    </div>

    <!-- Complete Modal -->
    <div v-if="showCompleteModal" class="modal d-block" style="background: rgba(0,0,0,0.5)">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header"><h5 class="modal-title">Complete Appointment</h5></div>
                <div class="modal-body">
                    <p><strong>Patient:</strong> {{ currentAppt.patient_name }}</p>
                    <div class="mb-2">
                        <label>Diagnosis</label>
                        <textarea class="form-control" v-model="treatment.diagnosis"></textarea>
                    </div>
                     <div class="mb-2">
                        <label>Prescription</label>
                        <textarea class="form-control" v-model="treatment.prescription"></textarea>
                    </div>
                     <div class="mb-2">
                        <label>Notes</label>
                        <textarea class="form-control" v-model="treatment.notes"></textarea>
                    </div>
                </div>
                <div class="modal-footer">
                    <button @click="showCompleteModal=false" class="btn btn-secondary">Close</button>
                    <button @click="submitTreatment" class="btn btn-success">Complete Visit</button>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import axios from 'axios'

const appointments = ref([])
const availabilityJson = ref('')
const showCompleteModal = ref(false)
const currentAppt = ref(null)
const treatment = reactive({ diagnosis: '', prescription: '', notes: '' })

const API_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000') + '/api/doctor'

const loadData = async () => {
    const apptsRes = await axios.get(`${API_URL}/appointments`)
    appointments.value = apptsRes.data
    
    const availRes = await axios.get(`${API_URL}/availability`)
    availabilityJson.value = JSON.stringify(availRes.data, null, 2)
}

const updateAvailability = async () => {
    try {
        const data = JSON.parse(availabilityJson.value)
        await axios.put(`${API_URL}/availability`, data)
        alert('Availability updated')
    } catch (e) {
        alert('Invalid JSON')
    }
}

const openComplete = (appt) => {
    currentAppt.value = appt
    showCompleteModal.value = true
    treatment.diagnosis = ''
    treatment.prescription = ''
    treatment.notes = ''
}

const submitTreatment = async () => {
    try {
        await axios.post(`${API_URL}/appointments/${currentAppt.value.id}/complete`, treatment)
        showCompleteModal.value = false
        loadData()
    } catch (e) {
        alert('Error completing appointment')
    }
}

onMounted(loadData)
</script>
