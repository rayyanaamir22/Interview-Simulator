#!/bin/bash

# Function to install Python service dependencies
install_python_dependencies() {
    local service=$1
    echo "Installing dependencies for $service..."
    cd $service
    pip install -r requirements.txt
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
    install_python_dependencies $service
done

echo "All dependencies have been installed successfully!" 