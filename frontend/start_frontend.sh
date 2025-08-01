#!/bin/bash

# Frontend Startup Script
# This script starts the React development server

echo "Starting User Plan Demo Frontend..."
echo "Frontend will be available at: http://localhost:3000"
echo ""
echo "Make sure the mock server is running on port 3001"
echo "You can start it with: cd ../mock_server && python main.py"
echo ""
echo "Press Ctrl+C to stop the frontend server"
echo ""

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
    echo ""
fi

# Start the development server
npm start
