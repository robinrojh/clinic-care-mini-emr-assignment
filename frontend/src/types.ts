export interface DiagnosisCode {
  chapter_code: string;
  category_code: string;
  subcategory_code: string;
  title: string | null;
}

export interface NoteForm {
  title: string;
  content: string;
  codes: DiagnosisCode[];
}

export interface Note extends NoteForm {
  note_id: number;
  created_at: string;
}