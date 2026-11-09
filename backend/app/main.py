from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
import bcrypt
import jwt

from app.database import SessionLocal, engine, Base
from app import models

# Ensure tables are created safely
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Advanced Project & Team Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    full_name: str
    username: str
    email: str
    password: str
    role: str = "employee"

class ProjectCreate(BaseModel):
    title: str
    description: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Advanced Project & Team Management API!"}

@app.post("/api/auth/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    new_user = models.User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@app.post("/api/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        (models.User.email == form_data.username) | 
        (models.User.full_name == form_data.username)
    ).first()
    
    if not user or not bcrypt.checkpw(form_data.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    token = jwt.encode({"sub": user.email}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/projects")
@app.get("/api/projects/")
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all() if hasattr(models, 'Project') else []

@app.post("/api/projects")
@app.post("/api/projects/")
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    new_project = models.Project(
        title=project.title,
        description=project.description,
        owner_email="user@example.com"
    ) if hasattr(models, 'Project') else None
    
    if not new_project:
        raise HTTPException(status_code=500, detail="Project model not found")
        
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project