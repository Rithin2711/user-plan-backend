#!/bin/bash
# Runs the mock_server FastAPI backend on port 3001, using environment variables from .env

# Load environment variables from .env if present
if [ -f "../.env" ]; then
  export $(grep -v '^#' ../.env | xargs)
elif [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Start the FastAPI app on port 3001 with auto-reload enabled for development
exec python3 -m uvicorn main:app --host 0.0.0.0 --port 3001 --reload
