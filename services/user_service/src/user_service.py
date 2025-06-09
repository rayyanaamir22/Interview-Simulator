from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid

app = FastAPI()

class User(BaseModel):
    id: str
    username: str
    email: str
    preferences: dict = {}
    created_interactions: List[str] = []
    created_structures: List[str] = []

# In-memory storage for users (will be replaced by database service)
users = {}

@app.post("/users/", response_model=User)
async def create_user(username: str, email: str):
    if any(user.email == email for user in users.values()):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = str(uuid.uuid4())
    user = User(
        id=user_id,
        username=username,
        email=email
    )
    users[user_id] = user
    return user

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@app.put("/users/{user_id}/preferences")
async def update_user_preferences(user_id: str, preferences: dict):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id].preferences.update(preferences)
    return {"message": "Preferences updated successfully"}

@app.post("/users/{user_id}/interactions/{interaction_id}")
async def add_user_interaction(user_id: str, interaction_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id].created_interactions.append(interaction_id)
    return {"message": "Interaction added successfully"}

@app.post("/users/{user_id}/structures/{structure_id}")
async def add_user_structure(user_id: str, structure_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id].created_structures.append(structure_id)
    return {"message": "Structure added successfully"} 