import type { DiagnosisCode } from "@/types";

function formatCode(code: DiagnosisCode): string {
    const base = `${code.chapter_code}${code.category_code}`;
    const sub = code.subcategory_code === '-' ? '' : `.${code.subcategory_code}`;
    return `${base}${sub} - ${code.title}`;
}

function formatTimestamp(timestamp: string): string {
    if (!timestamp) return 'N/A';
    try {
        return new Date(timestamp).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        });
    } catch (e) {
        return timestamp;
    }
}

export {
    formatCode, formatTimestamp
}