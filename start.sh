#!/bin/bash

# Advanced Auction System - Quick Start Script

echo "======================================"
echo "  Advanced Online Auction System"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed"
    exit 1
fi

echo "✓ pip3 found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "======================================"
echo "  Starting Auction Server..."
echo "======================================"
echo ""
echo "🌐 Server will be accessible at:"
echo "   Local:    http://localhost:5000"
echo "   External: http://<YOUR_IP>:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the server
python3 web_server.py
