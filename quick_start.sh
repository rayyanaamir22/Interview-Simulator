#!/bin/bash

# Function to start a service in a new terminal window
start_service() {
    osascript -e "tell application \"Terminal\" to do script \"cd $(pwd) && $1\""
}

# Function to install Python service dependencies
install_python_service() {
    local service=$1
    echo "Installing dependencies for $service..."
    cd $service
    pip install -e .
    cd ../..
}

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Activate virtual environment and install backend dependencies
echo "Installing backend dependencies..."
source proto-env/bin/activate

# Install dependencies for each service
for service in services/*_service; do
    install_python_service $service
done

# Start frontend
echo "Starting frontend..."
start_service "cd frontend && npm run dev"

# Start backend services
echo "Starting backend services..."

# Structure Service (Port 8001)
start_service "cd services/structure_service && source ../../proto-env/bin/activate && PYTHONPATH=$PYTHONPATH:$(pwd) uvicorn src.main:app --host 0.0.0.0 --port 8001"

# User Service (Port 8002)
start_service "cd services/user_service && source ../../proto-env/bin/activate && PYTHONPATH=$PYTHONPATH:$(pwd) uvicorn src.main:app --host 0.0.0.0 --port 8002"

# DB Service (Port 8003)
start_service "cd services/db_service && source ../../proto-env/bin/activate && PYTHONPATH=$PYTHONPATH:$(pwd) uvicorn src.main:app --host 0.0.0.0 --port 8003"

# Interaction Service (Port 8004)
start_service "cd services/interaction_service && source ../../proto-env/bin/activate && PYTHONPATH=$PYTHONPATH:$(pwd) uvicorn src.main:app --host 0.0.0.0 --port 8004"

echo "All services are starting up..."
echo "Frontend will be available at http://localhost:5173"
echo "API docs will be available at:"
echo "- Structure Service: http://localhost:8001/docs"
echo "- User Service: http://localhost:8002/docs"
echo "- DB Service: http://localhost:8003/docs"
echo "- Interaction Service: http://localhost:8004/docs" 