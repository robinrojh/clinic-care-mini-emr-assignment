from typing import List
from db.db import Code, Note, User, get_db
from sqlalchemy import text
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from models.models import CodeModel
from sqlalchemy.orm import Session

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def check_health():
    return {"status": "Up and running!"}

@app.get("/diagnosis", response_model=List[CodeModel])
def search_diagnosis_code(chapter_code: str, category_code: str, subcategory_code: str, db: Session = Depends(get_db)):
    
    results = db.query(Code).filter(
            Code.chapter_code == chapter_code,
            Code.category_code == category_code if len(category_code) > 0 else True,
            Code.subcategory_code == subcategory_code if len(subcategory_code) > 0 else True
        ).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="Codes not found")
        
    return results

@app.post("/consultation")
def save_consultation(user_email: str, title: str, content: str, codes: List[CodeModel], db: Session = Depends(get_db)):
    new_note = Note(user_email=user_email, title=title, content=content, codes=codes)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note

@app.get("/consultation")
def get_consultation_list(user_id: int, db: Session = Depends(get_db)):
    results = db.query(Note).filter(Note.user_id == user_id).all()

    if not results:
        raise HTTPException(status_code=404, detail="User not found! Are you logged in?")
    
    return results