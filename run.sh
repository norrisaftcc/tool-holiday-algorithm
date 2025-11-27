#!/bin/bash
# Holiday Gifting Dashboard - Quick Start Script
# Investigator: Clive
# Mission: Launch with maximum efficiency

echo "🎁 Holiday Gifting Dashboard - Starting Investigation..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )[\d.]+')
echo "✓ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt --quiet

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔐 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration"
fi

# Create data directory if it doesn't exist
mkdir -p data

# Run the application
echo "🚀 Launching Holiday Gifting Dashboard..."
echo "📍 Access at: http://localhost:8501"
echo "Press Ctrl+C to stop"
streamlit run app/main.py
