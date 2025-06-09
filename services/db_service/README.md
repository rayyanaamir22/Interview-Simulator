# Database Service

The Database Service provides persistent storage for user data in the Interview Simulator system. It uses SQLAlchemy for database operations and supports both SQLite (default) and PostgreSQL databases.

## Features

- Persistent user data storage
- User preferences management
- Tracking user-created interactions
- Tracking user-created structures
- Database migrations support

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

2. Set up environment variables (optional):
```bash
# For PostgreSQL
export DATABASE_URL="postgresql://user:password@localhost:5432/interview_simulator"

# For SQLite (default)
export DATABASE_URL="sqlite:///./users.db"
```

3. Run the service:
```bash
uvicorn src.db_service:app --host 0.0.0.0 --port 8001
```

The service will be available at `http://localhost:8001`

## API Documentation

Once the service is running, you can access:
- Interactive API documentation: `http://localhost:8001/docs`
- Alternative API documentation: `http://localhost:8001/redoc`

## Environment Variables

- `DATABASE_URL`: Database connection string (default: "sqlite:///./users.db")

## Database Schema

The service uses the following schema:

```sql
CREATE TABLE users (
    id VARCHAR PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    email VARCHAR NOT NULL UNIQUE,
    preferences JSON DEFAULT '{}',
    created_interactions ARRAY DEFAULT '[]',
    created_structures ARRAY DEFAULT '[]'
);
```

## Dependencies

- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- psycopg2-binary (for PostgreSQL support)
- python-dotenv 