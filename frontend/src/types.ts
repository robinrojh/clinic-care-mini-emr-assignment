export interface DiagnosisCode {
  chapter_code: string;
  category_code: string;
  subcategory_code: string;
  [key: string]: any;
}

export interface ConsultationForm {
  patient_id: number;
  doctor_notes: string;
  user_email: string;
  chapter_code: string;
  category_code: string;
  subcategory_code: string;
}

export interface Consultation extends ConsultationForm {
  consultation_id: number; 
}