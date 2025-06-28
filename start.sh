#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "pip is not installed. Please install pip and try again."
    exit 1
fi

# Check if Redis is running
if ! command -v redis-cli &> /dev/null || ! redis-cli ping &> /dev/null; then
    echo "Redis is not running. Please start Redis and try again."
    echo "You can install and start Redis with:"
    echo "  sudo apt-get update"
    echo "  sudo apt-get install redis-server"
    echo "  sudo systemctl start redis-server"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start FastAPI server in the background
echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > fastapi.log 2>&1 &
FASTAPI_PID=$!

# Start Celery worker
echo "Starting Celery worker..."
celery -A app.core.celery_app worker --loglevel=info

# Cleanup function to kill background processes when the script exits
function cleanup {
    echo "Stopping FastAPI server..."
    kill $FASTAPI_PID
}

# Register the cleanup function to be called on script exit
trap cleanup EXIT

# Keep the script running until Ctrl+C is pressed
wait
