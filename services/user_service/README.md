# User Service

The User Service is responsible for managing user information and their interactions with the Interview Simulator system. It provides endpoints for user management and maintains relationships with interactions and structures created by users.

## Features

- User creation and management
- User preferences handling
- Tracking user-created interactions
- Tracking user-created structures

## API Endpoints

- `POST /users/` - Create a new user
- `GET /users/{user_id}` - Get user information
- `PUT /users/{user_id}/preferences` - Update user preferences
- `POST /users/{user_id}/interactions/{interaction_id}` - Add an interaction to user's profile
- `POST /users/{user_id}/structures/{structure_id}` - Add a structure to user's profile

## Setup and Running

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the service:
```bash
uvicorn src.user_service:app --host 0.0.0.0 --port 8000
```

The service will be available at `http://localhost:8000`

## API Documentation

Once the service is running, you can access:
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`

## Environment Variables

No environment variables are required for basic operation. The service uses in-memory storage by default.

## Dependencies

- FastAPI
- Uvicorn
- Pydantic
- Requests 