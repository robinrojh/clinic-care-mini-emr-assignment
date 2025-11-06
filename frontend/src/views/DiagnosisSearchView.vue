<script setup lang="ts">
import { ref } from 'vue';
import apiClient from '@/api';
import type { DiagnosisCode } from '@/types.ts';

const chapter_code = ref<string>('I');
const category_code = ref<string>('01');
const subcategory_code = ref<string>('');

const loading = ref<boolean>(false);
const error = ref<string | null>(null);
const results = ref<DiagnosisCode[]>([]);

async function searchDiagnosis() {
  loading.value = true;
  error.value = null;
  results.value = [];
  try {
    const response = await apiClient.get<DiagnosisCode[]>('/diagnosis', {
      params: {
        chapter_code: chapter_code.value,
        category_code: category_code.value,
        subcategory_code: subcategory_code.value,
      },
    });
    console.log(response)
    results.value = response.data;
  } catch (err: any) {
    error.value = 'Failed to fetch diagnosis: ' + (err.response?.data?.detail || err.message);
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div>
    <h2>Search Diagnosis Codes</h2>
    <form @submit.prevent="searchDiagnosis" class="form-container">
      <div class="form-group">
        <label>Chapter Code:</label>
        <input v-model="chapter_code" type="text" />
      </div>
      <div class="form-group">
        <label>Category Code:</label>
        <input v-model="category_code" type="text" />
      </div>
      <div class="form-group">
        <label>Subcategory Code:</label>
        <input v-model="subcategory_code" type="text" />
      </div>
      <button type="submit" :disabled="loading">
        {{ loading ? 'Searching...' : 'Search' }}
      </button>
    </form>

    <div v-if="error" class="error-message">{{ error }}</div>

    <div v-if="results.length > 0" class="results-container">
      <h3>Results</h3>
      <pre>{{ results }}</pre>
    </div>
  </div>
</template>