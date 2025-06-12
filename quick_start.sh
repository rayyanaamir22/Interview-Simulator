#!/bin/bash

# Function to start a service in a new terminal window
start_service() {
    osascript -e "tell application \"Terminal\" to do script \"cd $(pwd) && $1\""
}

# Activate virtual environment
source proto-env/bin/activate

# Start frontend
echo "Starting frontend..."
start_service "cd frontend && npm run dev"

# Start backend services
echo "Starting backend services..."

# Structure Service (Port 8001)
start_service "cd services/structure_service && source ../../proto-env/bin/activate && PYTHONPATH=$PYTHONPATH:$(pwd) uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload"

# User Service (Port 8002)
start_service "cd services/user_service && source ../../proto-env/bin/activate && PYTHONPATH=$PYTHONPATH:$(pwd) uvicorn src.main:app --host 0.0.0.0 --port 8002 --reload"

# DB Service (Port 8003)
start_service "cd services/db_service && source ../../proto-env/bin/activate && PYTHONPATH=$PYTHONPATH:$(pwd) uvicorn src.main:app --host 0.0.0.0 --port 8003 --reload"

# Interaction Service (Port 8004)
start_service "cd services/interaction_service && source ../../proto-env/bin/activate && PYTHONPATH=$PYTHONPATH:$(pwd) uvicorn src.main:app --host 0.0.0.0 --port 8004 --reload"

# IPs and Ports
echo "All services are starting up..."
echo "Frontend will be available at http://localhost:5173"
echo "API docs will be available at:"
echo "- Structure Service: http://localhost:8001/docs"
echo "- User Service: http://localhost:8002/docs"
echo "- DB Service: http://localhost:8003/docs"
echo "- Interaction Service: http://localhost:8004/docs" 