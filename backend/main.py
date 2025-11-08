from typing import List, Annotated

from fastapi import FastAPI, Depends, HTTPException, status, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from db.db import Code, Note, User, get_db
from models.models import CodeModel, NoteModel, NoteCreateModel, UserModelInDB, UserModel, UserCreateModel, TokenModel, TokenData
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from jwt.exceptions import InvalidTokenError

import os
from dotenv import load_dotenv

load_dotenv()

try:
    SECRET_KEY = os.environ["SECRET_KEY"]
    REFRESH_SECRET_KEY = os.environ["REFRESH_SECRET_KEY"]
    ALGORITHM = os.environ.get("ALGORITHM", "HS256")
    
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
    REFRESH_TOKEN_EXPIRE_MINUTES = int(os.environ["REFRESH_TOKEN_EXPIRE_MINUTES"])

except KeyError as e:
    raise RuntimeError(f"Environment variable {e} not set!")
except ValueError:
    raise RuntimeError("Token expiry minutes must be integers!")

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
password_hash = PasswordHash.recommended()

def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return password_hash.hash(password)

def get_user(email: str, db: Session = Depends(get_db)) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    return user

def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
    user = get_user(email=email, db=db)
    if not user:
        return False
    if not verify_password(password, user.hashed_pw):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(db=db, email=token_data.username)
    if user is None:
        raise credentials_exception
    return user

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

@app.post("/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreateModel, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    db_user = get_user(db=db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already in use!"
        )
    
    hashed_password = get_password_hash(user.password)
    
    new_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_pw=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@app.post("/token")
async def login_for_access_token(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> TokenModel:
    user = authenticate_user(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="strict",
        secure=False, # Set to True in production (requires HTTPS)
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60
    )
    return TokenModel(
            access_token=access_token, 
            token_type="bearer"
        )

@app.post("/token/refresh", response_model=TokenModel)
async def refresh_access_token(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Takes a refresh token and returns a new access token
    and a new refresh token (for refresh token rotation).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token is None:
        raise credentials_exception
    
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user(db=db, email=username) 
    if user is None:
        raise credentials_exception

    new_token_data = {"sub": user.email}
    new_access_token = create_access_token(data=new_token_data)
    new_refresh_token = create_refresh_token(data=new_token_data)
    
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        samesite="strict",
        secure=False, # Set to True in production (requires HTTPS)
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60
    )

    return TokenModel(access_token=new_access_token, token_type="bearer")

@app.post("/logout")
async def logout(response: Response):
    response.set_cookie(
        key="refresh_token",
        value="",
        httponly=True,
        samesite="strict",
        secure=False, # Set to True in production (requires HTTPS)
        max_age=0
    )
    return {"message": "Logged out successfully"}

@app.get("/diagnosis", response_model=List[CodeModel])
def search_diagnosis_code(chapter_code: str, category_code: str, subcategory_code: str, db: Session = Depends(get_db)):
    
    query = db.query(Code).filter(Code.chapter_code.icontains(chapter_code))
    
    if len(category_code) > 0:
        query = query.filter(Code.category_code.icontains(category_code))
        
    if len(subcategory_code) > 0:
        query = query.filter(Code.subcategory_code.icontains(subcategory_code))
        
    results = query.all()
    
    if not results:
        raise HTTPException(status_code=404, detail="Codes not found")
        
    return results

@app.post("/consultation", response_model=NoteModel)
def save_consultation(current_user: Annotated[User, Depends(get_current_user)], note: NoteCreateModel, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with email {current_user.email} not found.")

    db_codes: List[Code] = []
    for code_model in note.codes:
        db_code = db.query(Code).filter(
            Code.chapter_code == code_model.chapter_code,
            Code.category_code == code_model.category_code,
            Code.subcategory_code == code_model.subcategory_code
        ).first()
        
        if db_code:
            db_codes.append(db_code)

    new_note = Note(email=current_user.email, title=note.title, content=note.content, codes=db_codes)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note

@app.get("/consultation")
def get_consultation_list(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    results = db.query(Note).filter(
            Note.email == current_user.email
        ).options(
            joinedload(Note.codes)
        ).all()
    if not results:
        raise HTTPException(status_code=404, detail="User not found! Are you logged in?")
    
    return results