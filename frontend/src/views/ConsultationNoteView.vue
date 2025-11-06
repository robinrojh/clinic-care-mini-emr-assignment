<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue';
import apiClient from '@/api';
import type { Note, NoteForm, DiagnosisCode } from '@/types';

const defaultForm: NoteForm = {
  title: '',
  content: '',
  email: 'rygrobin@gmail.com',
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
    selectedCode.value = null;
    newConsultation.codes = [];
    getConsultations();

  } catch (err: any) {
    submitError.value = 'Failed to save: ' + (err.response?.data?.detail || err.message);
  } finally {
    submitting.value = false;
  }
}

const consultations = ref<Note[]>([]);
const loadingList = ref<boolean>(false);

async function getConsultations() {
  loadingList.value = true;
  consultations.value = [];
  try {
    const response = await apiClient.get('/consultation', {
      params: {
        email: newConsultation.email
      }
    });
    consultations.value = response.data;
  } catch (err: any) {

  } finally {
    loadingList.value = false;
  }
}

onMounted(() => {
  getConsultations();
});

const searchQuery = ref<string>('');
const searchResults = ref<DiagnosisCode[]>([]);
const searchLoading = ref<boolean>(false);
const searchError = ref<string | null>(null);
const selectedCode = ref<DiagnosisCode | null>(null);
const debounceTimer = ref<number | null>(null);


// Possible improvement: add a new list state of `code`, making the client fetch all codes when the page loads.
// This can minimize the API calls to the server since the ICD-10 codes are typically not modified.
watch(searchQuery, (newQuery) => {
  if (debounceTimer.value) {
    clearTimeout(debounceTimer.value);
  }

  searchLoading.value = true;

  debounceTimer.value = window.setTimeout(async () => {
    try {
      searchError.value = null;
      if (!newQuery || newQuery.length == 0) {
        searchResults.value = []
        searchError.value = "You need at least one character."
        return;
      }

      if (newQuery.length > 4) {
        searchResults.value = []
        searchError.value = "Too long! Keep codes less than 5 characters."
        return;
      }
      else {
        const chapter_code = newQuery[0]
        const category_code = newQuery.length >= 2 ? newQuery.substring(1, 3) : ''
        const subcategory_code = newQuery.length >= 3 ? newQuery[3] : ''
        const response = await apiClient.get<DiagnosisCode[]>('/diagnosis', {
          params: {
            chapter_code: chapter_code,
            category_code: category_code,
            subcategory_code: subcategory_code,
          },
        });
        searchResults.value = response.data
      }
    } catch (err: any) {
      searchError.value = 'Search failed: ' + (err.response?.data?.detail || err.message);
    } finally {
      searchLoading.value = false;
    }
  }, 500);
});

function selectCode(code: DiagnosisCode) {
  newConsultation.codes.push(code);

  searchQuery.value = '';
  searchResults.value = [];
  selectedCode.value = null;
}

function removeCode(index: number) {
  newConsultation.codes.splice(index, 1);
}

function formatCode(code: DiagnosisCode): string {
  const base = `${code.chapter_code}${code.category_code}`;
  const sub = code.subcategory_code === 'X' ? '' : `.${code.subcategory_code}`;
  return `${base}${sub} - ${code.title}`;
}
</script>

<template>
  <div class="page-layout">
    <div class="form-container">
      <h2>Save Consultation</h2>
      <form @submit.prevent="saveConsultation">
        <div class="form-group">
          <label>Your Email:</label>
          <input v-model="newConsultation.email" type="email" />
        </div>
        <div class="form-group">
          <label>Note Title:</label>
          <textarea v-model="newConsultation.title"></textarea>
          <label>Notes:</label>
          <textarea v-model="newConsultation.content"></textarea>
        </div>

        <hr>

        <h3>Diagnosis Codes</h3>

        <ul v-if="newConsultation.codes.length > 0" class="selected-code-list">
          <li v-for="(code, index) in newConsultation.codes" :key="index">
            <span>{{ formatCode(code) }}</span>
            <button type="button" @click="removeCode(index)" class="remove-btn">
              &times;
            </button>
          </li>
        </ul>

        <div>
          <div class="form-group">
            <label>Search Code (e.g., "A010"):</label>
            <input v-model.trim="searchQuery" type="text" placeholder="Start typing to search..." />
          </div>
          <div v-if="searchLoading">Searching...</div>
          <div v-if="searchError" class="error-message">{{ searchError }}</div>

          <ul v-if="searchResults.length > 0" class="search-results">
            <li v-for="code in searchResults"
              :key="`${code.chapter_code}-${code.category_code}-${code.subcategory_code}`" @click="selectCode(code)">
              {{ formatCode(code) }}
            </li>
          </ul>
        </div>

        <button type="submit" :disabled="submitting" class="submit-btn">
          {{ submitting ? 'Saving...' : 'Save Consultation' }}
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
        <li v-for="item in consultations" :key="item.note_id">
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

.form-container,
.list-container {
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

hr {
  border: none;
  border-top: 1px solid #eee;
  margin: 20px 0;
}

.submit-btn {
  margin-top: 20px;
}

/* New Search Styles */
.search-results {
  list-style: none;
  padding: 0;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
  max-height: 200px;
  overflow-y: auto;
}

.search-results li {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #eee;
}

.search-results li:last-child {
  border-bottom: none;
}

.search-results li:hover {
  background-color: #f0f0f0;
}

.selected-code {
  display: flex;
  align-items: center;
  gap: 10px;
}

.selected-code pre {
  flex-grow: 1;
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.remove-btn {
  background-color: #e74c3c;
  font-size: 0.8rem;
  padding: 5px 8px;
}

.remove-btn:hover {
  background-color: #c0392b;
}
</style>