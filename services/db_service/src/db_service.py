"""
Database utils
"""

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Generator
import os

app = FastAPI()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./users.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy model
class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    preferences = Column(JSON, default={})
    created_interactions = Column(JSON, default=list)
    created_structures = Column(JSON, default=list)

# Pydantic model for request/response
class UserBase(BaseModel):
    username: str
    email: str
    preferences: dict = {}
    created_interactions: List[str] = []
    created_structures: List[str] = []

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: str

    class Config:
        orm_mode = True

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}/preferences")
async def update_user_preferences(user_id: str, preferences: dict, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.preferences.update(preferences)
    db.commit()
    return {"message": "Preferences updated successfully"}

@app.post("/users/{user_id}/interactions/{interaction_id}")
async def add_user_interaction(user_id: str, interaction_id: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    interactions = user.created_interactions or []
    if interaction_id not in interactions:
        interactions.append(interaction_id)
        user.created_interactions = interactions
        db.commit()
    return {"message": "Interaction added successfully"}

@app.post("/users/{user_id}/structures/{structure_id}")
async def add_user_structure(user_id: str, structure_id: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    structures = user.created_structures or []
    if structure_id not in structures:
        structures.append(structure_id)
        user.created_structures = structures
        db.commit()
    return {"message": "Structure added successfully"} 