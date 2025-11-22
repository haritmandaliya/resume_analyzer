#!/bin/bash

# Resume Analyzer Single Server Startup Script

echo "🚀 Starting Resume Analyzer Single Server..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Install React dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing React dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install React dependencies"
        exit 1
    fi
    echo "✅ React dependencies installed!"
else
    echo "✅ React dependencies already installed"
fi

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install fastapi uvicorn python-multipart rapidfuzz PyPDF2

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p resumes
mkdir -p history/JDhistory

# Build React app
echo "⚛️  Building React app..."
npm run build
if [ $? -ne 0 ]; then
    echo "❌ Failed to build React app"
    exit 1
fi
echo "✅ React app built successfully!"

# Start FastAPI server
echo "🔧 Starting FastAPI server on http://localhost:8000..."
echo ""
echo "🎉 Resume Analyzer is now running!"
echo ""
echo "📱 Access the app: http://localhost:8000"
echo "🔧 API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"

python3 main.py 