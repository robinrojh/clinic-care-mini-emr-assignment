<script setup lang="ts">
import { ref, reactive } from 'vue';
import apiClient from '@/api';
import type { Note, NoteForm, DiagnosisCode } from '@/types';
import DiagnosisCodeSearch from '@/components/DiagnosisCodeSearch.vue';
import { formatCode } from '@/utils/formatter';

const defaultForm: NoteForm = {
  title: '',
  content: '',
  codes: []
};
const newConsultation = reactive<NoteForm>({ ...defaultForm });

const submitting = ref<boolean>(false);
const submitError = ref<string | null>(null);

async function saveConsultation() {
  if (newConsultation.codes.length === 0) {
    submitError.value = 'Please search for and add at least one diagnosis code.';
    return;
  }

  submitting.value = true;
  submitError.value = null;

  try {
    await apiClient.post('/consultation', newConsultation);
    Object.assign(newConsultation, defaultForm);
    newConsultation.codes = [];
  } catch (err: any) {
    console.log(err)
    submitError.value = 'Failed to save: ' + (err.response?.data?.detail || err.message);
  } finally {
    submitting.value = false;
  }
}

function handleCodeSelect(code: DiagnosisCode) {
  const exists = newConsultation.codes.some(
    c => c.chapter_code === code.chapter_code &&
      c.category_code === code.category_code &&
      c.subcategory_code === code.subcategory_code
  );
  if (!exists) {
    newConsultation.codes.push(code);
  }
}

function removeCode(index: number) {
  newConsultation.codes.splice(index, 1);
}
</script>

<template>
  <div class="page-layout">
    <div class="form-container">
      <h2>Save Consultation</h2>
      <form @submit.prevent="saveConsultation">
        <div class="form-group">
          <label>Note Title:</label>
          <input v-model="newConsultation.title" type="text" class="form-control" />
        </div>
        <div class="form-group">
          <label>Notes:</label>
          <textarea v-model="newConsultation.content" class="form-control"></textarea>
        </div>

        <hr>

        <h3>Diagnosis Codes</h3>

        <DiagnosisCodeSearch @code-selected="handleCodeSelect" />

        <ul v-if="newConsultation.codes.length > 0" class="selected-code-list">
          <li v-for="(code, index) in newConsultation.codes" :key="index">
            <span>{{ formatCode(code) }}</span>
            <button type="button" @click="removeCode(index)" class="btn btn-danger remove-btn">
              &times;
            </button>
          </li>
        </ul>
        <div v-else class="empty-state" style="padding: 10px; margin-top: 10px;">
          No codes added yet.
        </div>

        <button type="submit" :disabled="submitting" class="btn btn-primary submit-btn">
          {{ submitting ? 'Saving...' : 'Save Consultation' }}
        </button>
        <div v-if="submitError" class="error-message">{{ submitError }}</div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.page-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.form-container,
.list-container {
  min-width: 0;
}

.consultation-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.submit-btn {
  margin-top: var(--spacing);
}

.selected-code-list {
  list-style: none;
  padding: 0;
  margin-top: 15px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.selected-code-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: var(--color-bg-light);
  border: 1px solid var(--color-border-light);
  border-radius: var(--border-radius);
  font-size: 0.9rem;
}

.remove-btn {
  font-size: 1rem;
  padding: 2px 8px;
  line-height: 1.2;
}
</style>