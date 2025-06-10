#!/bin/bash

# Function to start a service in a new terminal window
start_service() {
    osascript -e "tell application \"Terminal\" to do script \"cd $(pwd) && $1\""
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
    echo "Installing dependencies for $service..."
    cd $service
    pip install -r requirements.txt
    cd ../..
done

# Start frontend
echo "Starting frontend..."
start_service "cd frontend && npm run dev"

# Start backend services
echo "Starting backend services..."
start_service "cd services/structure_service && source ../../proto-env/bin/activate && PYTHONPATH=$PYTHONPATH:$(pwd) uvicorn src.main:app --host 0.0.0.0 --port 8002"
start_service "cd services/interaction_service && source ../../proto-env/bin/activate && PYTHONPATH=$PYTHONPATH:$(pwd) uvicorn src.interaction_service:app --host 0.0.0.0 --port 8003"

echo "All services are starting up..."
echo "Frontend will be available at http://localhost:5173"
echo "API docs will be available at:"
echo "- Structure Service: http://localhost:8002/docs"
echo "- Interaction Service: http://localhost:8003/docs" 