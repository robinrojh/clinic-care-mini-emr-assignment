from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def check_health():
    return {"status": "Up and running!"}

@app.get("/diagnosis")
def search_diagnosis_code(code: str):
    pass

@app.post("/consultation")
def save_consultation():
    pass

@app.get("/consultation")
def get_consultation_list():
    pass