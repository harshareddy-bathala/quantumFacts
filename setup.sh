#!/bin/bash
# Setup script for Mac/Linux

echo "========================================"
echo "  Viral Shorts Generator - Setup"
echo "========================================"
echo

# Check Python
echo "Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python not found!"
    echo "Please install Python 3.9+ from python.org"
    exit 1
fi
python3 --version
echo

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi
echo

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt
echo

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo ".env file created. Please edit it with your API keys."
else
    echo ".env file already exists."
fi
echo

# Create directories
echo "Creating directories..."
mkdir -p assets/music
mkdir -p output
mkdir -p temp
mkdir -p logs
echo "Directories created."
echo

# Run setup check
echo "Running setup verification..."
python setup_check.py
echo

echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo
echo "Next steps:"
echo "  1. Edit .env file with your API keys"
echo "  2. Add background music to assets/music/"
echo "  3. Run: python src/viral_shorts/main.py"
echo
