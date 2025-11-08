<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import apiClient from '@/api';
import type { Note, NoteForm, DiagnosisCode } from '@/types';
import { formatCode, formatTimestamp } from '@/utils/formatter';
import { router } from '@/router';


const consultations = ref<Note[]>([]);
const loadingList = ref<boolean>(false);

async function getConsultations() {
    loadingList.value = true;
    consultations.value = [];
    try {
        const response = await apiClient.get('/consultation');
        consultations.value = response.data;
    } catch (err: any) {

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
        <div class="list-container">
            <h2>Consultation List</h2>
            <div class="btn-row">
                <button @click="getConsultations" :disabled="loadingList" class="btn" style="margin-bottom: 10px;">
                    {{ loadingList ? 'Refreshing...' : 'Refresh' }}
                </button>
                <button @click="router.push('consultations/post')" class="btn btn-primary submit-btn">
                    Create New Consultation Note
                </button>
            </div>

            <div v-if="loadingList" class="loading-state">Loading...</div>

            <div v-else-if="!loadingList && consultations.length === 0" class="empty-state">
                No consultations found.
            </div>

            <table v-else class="data-table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Title</th>
                        <th>Content</th>
                        <th>Codes</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in consultations" :key="item.note_id">
                        <td class="timestamp-cell">
                            {{ formatTimestamp(item.created_at) }}
                        </td>
                        <td>{{ item.title }}</td>
                        <td class="content-cell">{{ item.content }}</td>
                        <td class="codes-cell">
                            <ul v-if="item.codes.length > 0" class="inner-code-list">
                                <li v-for="code in item.codes" :title="code.title!">
                                    {{ formatCode(code) }}
                                </li>
                            </ul>
                            <span v-else class="no-data">—</span>
                        </td>
                    </tr>
                </tbody>
            </table>

        </div>
    </div>
</template>

<style scoped>
.page-layout {
    display: grid;
    grid-template-columns: 1fr;
    gap: 30px;
}

.btn-row {
    display: flex;
    justify-content: space-between;
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