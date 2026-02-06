#!/bin/bash

# Quick Start Script for Household Spending App

echo "🏠 Household Spending Estimates - Quick Start"
echo "=============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment exists"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Run the application
echo ""
echo "🚀 Starting Flask application..."
echo ""
echo "   Dashboard: http://localhost:5000"
echo "   Press Ctrl+C to stop"
echo ""
python app.py
