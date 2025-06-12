from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_SERVICE_URL = os.getenv("DB_SERVICE_URL", "http://localhost:8003")

app = FastAPI(
    title="User Service",
    description="User management service for Interview Simulator",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    username: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/auth/register")
async def register(request: RegisterRequest):
    logger.info(f"Registration attempt for email: {request.email}")
    async with httpx.AsyncClient() as client:
        try:
            # Create user in DB service
            logger.info("Sending registration request to DB service")
            response = await client.post(
                f"{DB_SERVICE_URL}/users/",
                json={
                    "email": request.email,
                    "password": request.password,
                    "username": request.username
                }
            )
            response.raise_for_status()
            user_data = response.json()
            logger.info(f"Registration successful for user: {request.email}")
            return {"message": "Registration successful", "user_id": user_data["id"]}
        except httpx.HTTPStatusError as e:
            logger.error(f"Registration failed for {request.email}: {str(e)}")
            if e.response.status_code == 400:
                raise HTTPException(status_code=400, detail="Email or username already exists")
            raise HTTPException(status_code=500, detail="Database service error")

@app.post("/auth/login")
async def login(request: LoginRequest):
    logger.info(f"Login attempt for email: {request.email}")
    async with httpx.AsyncClient() as client:
        try:
            # Verify credentials with DB service
            logger.info("Sending verification request to DB service")
            response = await client.post(
                f"{DB_SERVICE_URL}/users/verify",
                json={"email": request.email, "password": request.password}
            )
            response.raise_for_status()
            user_data = response.json()
            logger.info(f"Login successful for user: {request.email}")
            
            # In a real application, you would generate a proper JWT token
            return {
                "message": "Login successful",
                "token": "dummy_jwt_token",
                "user_id": user_data["user_id"]
            }
        except httpx.HTTPStatusError as e:
            logger.error(f"Login failed for {request.email}: {str(e)}")
            if e.response.status_code == 401:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            raise HTTPException(status_code=500, detail="Database service error")

@app.post("/users/")
async def create_user(user: UserCreate):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{DB_SERVICE_URL}/users/",
                json=user.dict()
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                raise HTTPException(status_code=400, detail="Email already registered")
            raise HTTPException(status_code=500, detail="Database service error")

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{DB_SERVICE_URL}/users/{user_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="User not found")
            raise HTTPException(status_code=500, detail="Database service error") 