# Interview-Simulator
AI-powered job interview simulation. Get highly personalized feedback about conversational flow, tone, appearance, and many more.

To run:

## Frontend
```bash
cd frontend
npm install
npm run dev
# Frontend will be available at http://localhost:5173
```

## Backend Services

### User Service
```bash
cd services/user_service
pip install -r requirements.txt
uvicorn src.user_service:app --host 0.0.0.0 --port 8000
# API docs available at http://localhost:8000/docs
```

### Database Service
```bash
cd services/db_service
pip install -r requirements.txt
uvicorn src.db_service:app --host 0.0.0.0 --port 8001
# API docs available at http://localhost:8001/docs
```

### Structure Service
```bash
cd services/structure_service
pip install -r requirements.txt
uvicorn src.structure_service:app --host 0.0.0.0 --port 8002
# API docs available at http://localhost:8002/docs
```

### Interaction Service
```bash
cd services/interaction_service
pip install -r requirements.txt
uvicorn src.interaction_service:app --host 0.0.0.0 --port 8003
# API docs available at http://localhost:8003/docs
```

## Prerequisites
- Node.js and npm for frontend
- Python 3.8+ and pip for backend services
- Each service should be run in a separate terminal window

Next steps:
- Rewriting some microservices in more robust languages (Rust, Go, etc.)