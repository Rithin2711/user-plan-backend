#!/bin/bash

# Mock Server Startup Script
# This script starts the mock server with proper configuration

echo "Starting Mock User Plan Server..."
echo "Server will be available at: http://localhost:8081"
echo "API Documentation at: http://localhost:8081/docs"
echo "OpenAPI JSON at: http://localhost:8081/openapi.json"
echo ""
echo "Test users:"
echo "  - alice (normal plan)"
echo "  - bob (premium plan)" 
echo "  - carol (ultra plan)"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python main.py
