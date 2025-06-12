# 🤖 Interview-Simulator
AI-powered job interview simulation. Get highly personalized feedback about conversational flow, tone, appearance, and many more.

## 🚀 Quick Start
The easiest way to start all services is using the provided script:

```bash
# Define a venv for Python requirements
python3 -m venv proto-env

# Make the scripts executable (only needed once, unless modified)
chmod +x install_dependencies.sh
chmod +x quick_start.sh

# Start all services
./install_dependencies.sh  # only needed once, unless modified
./quick_start.sh  # can run this any time, assuming correct dependencies are installed
```

This will:
- Install all frontend dependencies
- Install all backend dependencies in the proto-env virtual environment
- Start all services in separate terminal windows
- Frontend will be available at http://localhost:5173
- API docs will be available at their respective ports (see below)

## 🛑 Stopping Services
To stop all running services, you can use the following command:

```bash
pkill -f "uvicorn|npm run dev"
```

This will terminate all running uvicorn (backend) and npm (frontend) processes. If you need to stop services individually, you can use Ctrl+C in their respective terminal windows.

## 🔧 Manual Setup (Alternative)
If you prefer to start services individually or need to run them separately:

### 🎨 Frontend
```bash
cd frontend
npm install
npm run dev
# Frontend will be available at http://localhost:5173
```

### ⚙️ Backend Services

### 👤 User Service
```bash
cd services/user_service
pip install -r requirements.txt
uvicorn src.user_service:app --host 0.0.0.0 --port 8000
# API docs available at http://localhost:8000/docs
```

### 💾 Database Service
```bash
cd services/db_service
pip install -r requirements.txt
uvicorn src.db_service:app --host 0.0.0.0 --port 8001
# API docs available at http://localhost:8001/docs
```

### 🏗️ Structure Service
```bash
cd services/structure_service
pip install -r requirements.txt
uvicorn src.structure_service:app --host 0.0.0.0 --port 8002
# API docs available at http://localhost:8002/docs
```

### 💬 Interaction Service
```bash
cd services/interaction_service
pip install -r requirements.txt
uvicorn src.interaction_service:app --host 0.0.0.0 --port 8003
# API docs available at http://localhost:8003/docs
```

## 📋 Prerequisites
- Node.js and npm for frontend
- Python 3.8+ and pip for backend services
- Each service should be run in a separate terminal window (handled automatically by the startup script)

Next steps:
- Rewriting some microservices in more robust languages (Rust, Go, etc.)