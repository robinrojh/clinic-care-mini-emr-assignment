# ClinicCare Mini EMR Assignment

## Background
- Clinics record diagnosis code and treatment notes for every consultation.

## Goal
- Create a minimal, secure, and intuitive tool to manage the notes.

## Backend Tech Stack
- Python 3.13.5 with Virtual Environment
- FastAPI
    - Diagnosis code search endpoint
    - Create & read consultation notes
    - JWT authentication
- PostgreSQL for lightweight DB
    - Local PostgreSQL instance
- Pydantic for input validation and basic error handling

## Frontend Tech Stack
- Vue 3
- JWT authentication for login, sign up, and access control