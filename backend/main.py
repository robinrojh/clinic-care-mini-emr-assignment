from typing import Union
from db.session import engine
from sqlalchemy import text
from sqlalchemy.orm import Session
from models.models import Code
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def check_health():
    return {"status": "Up and running!"}

@app.get("/diagnosis")
def search_diagnosis_code(chapter_code: str, category_code: str, subcategory_code: str):
    with engine.connect() as connection:
        query = text("SELECT * FROM codes WHERE chapter_code=:id_1 AND category_code=:id_2 AND subcategory_code=:id_3")
        result = connection.execute(query, {"id_1": chapter_code, "id_2": category_code, "id_3": subcategory_code}).first()
        return result

@app.post("/consultation")
def save_consultation(user_id: int, title: str, content: str):
    with engine.connect() as connection:
        query = text("INSERT INTO notes (user_id, title, content) VALUES (:user_id, :title, :content)")
        result = connection.execute(query, {"user_id": user_id, "title": title, "content": content}).all()
        return result

@app.get("/consultation")
def get_consultation_list(user_id: int):
    with engine.connect() as connection:
        query = text("SELECT * FROM notes WHERE user_id=:user_id")
        result = connection.execute(query, { "user_id": user_id }).all()
        return result