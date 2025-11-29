#!/bin/bash

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "🚀 Setting up Onda Cloud Version..."

# Check if python3 is available
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
    PIP_CMD=pip3
else
    echo "❌ Python 3 is not installed. Please install it."
    exit 1
fi

# Kill any existing process on port 8000
PID=$(lsof -ti :8000)
if [ ! -z "$PID" ]; then
  echo "⚠️  Killing old server process (PID $PID)..."
  kill -9 $PID
fi

# Install requirements
echo "📦 Installing dependencies..."
$PYTHON_CMD -m pip install -r backend/requirements.txt

# Run the server
echo "✨ Starting server..."
echo "🌍 Open http://localhost:8000 in your browser"
$PYTHON_CMD backend/main.py
