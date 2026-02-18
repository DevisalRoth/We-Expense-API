#!/bin/bash

# Exit on error
set -e

echo "🚀 Setting up Expense API locally..."

# 1. Check/Create Virtual Environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# 2. Activate Virtual Environment
source venv/bin/activate

# 3. Install Dependencies
echo "⬇️ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Run the Server
echo "🔥 Starting Server on http://0.0.0.0:8000"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
