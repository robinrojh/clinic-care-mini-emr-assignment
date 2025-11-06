from typing import List
from db.db import Code, Note, User, get_db
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.models import CodeModel, NoteModel, NoteCreateModel
from sqlalchemy.orm import Session, joinedload

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
    
    query = db.query(Code).filter(Code.chapter_code == chapter_code)
    
    if len(category_code) > 0:
        query = query.filter(Code.category_code == category_code)
        
    if len(subcategory_code) > 0:
        query = query.filter(Code.subcategory_code == subcategory_code)
        
    results = query.all()
    
    if not results:
        raise HTTPException(status_code=404, detail="Codes not found")
        
    return results

@app.post("/consultation", response_model=NoteModel)
def save_consultation(note: NoteCreateModel, db: Session = Depends(get_db)):
    # user = db.query(User).filter(User.email == note.email).first()
    # if not user:
    #     raise HTTPException(status_code=404, detail=f"User with email {note.email} not found.")

    db_codes: List[Code] = []
    for code_model in note.codes:
        db_code = db.query(Code).filter(
            Code.chapter_code == code_model.chapter_code,
            Code.category_code == code_model.category_code,
            Code.subcategory_code == code_model.subcategory_code
        ).first()
        
        if db_code:
            db_codes.append(db_code)

    new_note = Note(email=note.email, title=note.title, content=note.content, codes=db_codes)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note

@app.get("/consultation")
def get_consultation_list(email: str, db: Session = Depends(get_db)):
    results = db.query(Note).filter(
            Note.email == email
        ).options(
            joinedload(Note.codes)
        ).all()
    if not results:
        raise HTTPException(status_code=404, detail="User not found! Are you logged in?")
    
    return results