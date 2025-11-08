<script setup lang="ts">
import { ref, watch } from 'vue';
import apiClient from '@/api';
import type { DiagnosisCode } from '@/types';

const emit = defineEmits<{
    (e: 'code-selected', code: DiagnosisCode): void
}>()

const searchQuery = ref<string>('');
const searchResults = ref<DiagnosisCode[]>([]);
const searchLoading = ref<boolean>(false);
const searchError = ref<string | null>(null);
const debounceTimer = ref<number | null>(null);

watch(searchQuery, (newQuery) => {
    if (debounceTimer.value) {
        clearTimeout(debounceTimer.value);
    }

    // Clear results if query is empty
    if (!newQuery || newQuery.length === 0) {
        searchResults.value = [];
        searchError.value = null;
        searchLoading.value = false;
        return;
    }

    searchLoading.value = true;
    searchError.value = null;

    debounceTimer.value = window.setTimeout(async () => {
        try {
            if (newQuery.length > 4) {
                searchResults.value = []
                searchError.value = "Too long! Keep codes less than 5 characters."
                return;
            }

            const chapter_code = newQuery[0]
            const category_code = newQuery.length >= 2 ? newQuery.substring(1, 3) : ''
            const subcategory_code = newQuery.length == 4 ? newQuery[3] : ''

            const response = await apiClient.get<DiagnosisCode[]>('/diagnosis', {
                params: {
                    chapter_code: chapter_code,
                    category_code: category_code,
                    subcategory_code: subcategory_code,
                },
            });
            searchResults.value = response.data
            if (response.data.length === 0) {
                searchError.value = "No codes found for this query."
            }

        } catch (err: any) {
            searchError.value = 'Search failed: ' + (err.response?.data?.detail || err.message);
        } finally {
            searchLoading.value = false;
        }
    }, 500); // 500ms debounce
});

function selectCode(code: DiagnosisCode) {
    emit('code-selected', code);

    // Reset the search
    searchQuery.value = '';
    searchResults.value = [];
    searchError.value = null;
}

function formatCode(code: DiagnosisCode): string {
    const base = `${code.chapter_code}${code.category_code}`;
    const sub = code.subcategory_code === 'X' ? '' : `.${code.subcategory_code}`;
    return `${base}${sub} - ${code.title}`;
}
</script>

<template>
    <div>
        <div class="form-group">
            <label for="code-search">Search Code (e.g., "I010"):</label>
            <input id="code-search" v-model.trim="searchQuery" type="text" placeholder="Start typing to search..."
                class="form-control" />
        </div>

        <div v-if="searchLoading" class="loading-state" style="padding: 10px;">Searching...</div>
        <div v-if="searchError" class="error-message">{{ searchError }}</div>

        <ul v-if="searchResults.length > 0" class="search-results-list">
            <li v-for="code in searchResults"
                :key="`${code.chapter_code}-${code.category_code}-${code.subcategory_code}`" @click="selectCode(code)">
                {{ formatCode(code) }}
            </li>
        </ul>
    </div>
</template>

<style scoped>
.search-results-list {
    list-style: none;
    padding: 0;
    margin-top: 5px;
    border: 1px solid var(--color-border-light);
    border-radius: var(--border-radius);
    max-height: 200px;
    overflow-y: auto;
    background-color: #fff;
}

.search-results-list li {
    padding: 10px 12px;
    cursor: pointer;
    border-bottom: 1px solid var(--color-border-light);
}

.search-results-list li:last-child {
    border-bottom: none;
}

.search-results-list li:hover {
    background-color: var(--color-bg-light);
    color: var(--color-primary);
}
</style>