#!/bin/bash

# Mock Server Startup Script
# This script starts the mock server with proper environment setup

echo "Starting Mock User Plan Server..."

# Check if we're in the right directory
if [ ! -f "mock_server/main.py" ]; then
    echo "Error: Please run this script from the user-plan-backend directory"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f "mock_server/.env" ]; then
    echo "Creating .env file from template..."
    cp mock_server/.env.example mock_server/.env
fi

# Install dependencies if needed
if [ ! -d "mock_server/__pycache__" ]; then
    echo "Installing Python dependencies..."
    cd mock_server
    pip install -r requirements.txt
    cd ..
fi

# Start the server
echo "Starting server on port 3001..."
cd mock_server
exec ./run_mock_server.sh
