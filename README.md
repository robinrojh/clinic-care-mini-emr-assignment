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

## Set Up Locally
- Frontend: `npm install`, then `npm run dev`
- Backend:
    - Install PostgreSQL version 16
    - `pip install -r requirements.txt` to install all required Python packages (virtual environment)
    - Create a database using the parameters in the `code_to_sql.ipynb` file from the `icd_codes` directory. These are currently hard-coded, so please do not store any sensitive information within these databases.
    -`fastapi run` to start backend; this will initialize the database. Turn off the FastAPI server once done.
- Additional backend set up (JWT & ICD-10 code DB):
    - Run the `code_processor_ipynb` in the `icd_codes` directory to process the input file (text file with codes)
    - Then, run the `code_to_sql.ipynb` file to populate the database with some ICD-10 diagnostic codes
    - Create an `.env` file in the backend directory with the following keys: `SECRET_KEY`, `REFRESH_SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_MINUTES`
        - `SECRET_KEY` and `REFRESH_SECRET_KEY` will be used for JWT. Do NOT share this with anyone. A random string can be generated using `openssl rand -hex 32` for our purpose.
        - `ALGORITHM` is `"HS256"`
        - `ACCESS_TOKEN_EXPIRE_MINUTES` should be `"30"` to represent 30-minute expiry of JWT tokens
        - `REFRESH_TOKEN_EXPIRE_MINUTES` should be `"10080"` to represent 1-week expiry of long-term refresh tokens
        - All 5 variables must be present in `.env`.
## Run
- Frontend: `npm run dev`
- Backend: `fastapi run` (Modify the CORS settings in `main.py` if your frontend localhost port is not 5173!)
