<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import apiClient from '@/api';
import type { Consultation, ConsultationForm } from '@/types.ts';

const defaultForm: ConsultationForm = {
  patient_id: 1,
  doctor_notes: '',
  user_email: 'rygrobin@gmail.com', // Default email for testing
  chapter_code: '',
  category_code: '',
  subcategory_code: '',
};

const newConsultation = reactive<ConsultationForm>({ ...defaultForm });

const submitting = ref<boolean>(false);
const submitError = ref<string | null>(null);

async function saveConsultation() {
  submitting.value = true;
  submitError.value = null;
  try {
    await apiClient.post('/consultation', newConsultation);
    
    Object.assign(newConsultation, defaultForm);
    getConsultations(); 

  } catch (err: any) {
    submitError.value = 'Failed to save: ' + (err.response?.data?.detail || err.message);
  } finally {
    submitting.value = false;
  }
}

const consultations = ref<Consultation[]>([]);
const loadingList = ref<boolean>(false);

async function getConsultations() {
  loadingList.value = true;
  consultations.value = [];
  try {
    const response = await apiClient.get<Consultation[]>('/consultation');
    consultations.value = response.data;
  } catch (err: any) {
    console.error(err);
  } finally {
    loadingList.value = false;
  }
}

onMounted(() => {
  getConsultations();
});
</script>

<template>
  <div class="page-layout">
    <div class="form-container">
      <h2>Save Consultation</h2>
      <form @submit.prevent="saveConsultation">
        <div class="form-group">
          <label>Patient ID:</label>
          <input v-model.number="newConsultation.patient_id" type="number" />
        </div>
        <div class="form-group">
          <label>Your Email:</label>
          <input v-model="newConsultation.user_email" type="email" />
        </div>
        <div class="form-group">
          <label>Doctor Notes:</label>
          <textarea v-model="newConsultation.doctor_notes"></textarea>
        </div>
        <hr>
        <div class="form-group">
          <label>Chapter Code:</label>
          <input v-model="newConsultation.chapter_code" type="text" />
        </div>
        <div class="form-group">
          <label>Category Code:</label>
          <input v-model="newConsultation.category_code" type="text" />
        </div>
        <div class="form-group">
          <label>Subcategory Code:</label>
          <input v-model="newConsultation.subcategory_code" type="text" />
        </div>
        <button type="submit" :disabled="submitting">
          {{ submitting ? 'Saving...' : 'Save' }}
        </button>
        <div v-if="submitError" class="error-message">{{ submitError }}</div>
      </form>
    </div>

    <div class="list-container">
      <h2>Consultation List</h2>
      <button @click="getConsultations" :disabled="loadingList">Refresh</button>
      <div v-if="loadingList">Loading...</div>
      <div v-if="!loadingList && consultations.length === 0">No consultations found.</div>
      <ul v-if="consultations.length > 0">
        <li v-for="item in consultations" :key="item.consultation_id">
          <pre>{{ item }}</pre>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.page-layout {
  display: flex;
  gap: 30px;
}
.form-container, .list-container {
  flex: 1;
}
.list-container ul {
  list-style: none;
  padding: 0;
}
.list-container li {
  background-color: #f9f9f9;
  border: 1px solid #eee;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
}
</style>