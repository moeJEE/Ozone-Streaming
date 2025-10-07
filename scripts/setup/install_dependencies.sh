#!/bin/bash

# Install Dependencies Script
# This script installs all required dependencies for the data streaming pipeline

set -e

echo "🔧 Installing dependencies..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version or higher is required. Current version: $python_version"
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python packages..."
pip3 install -r requirements.txt

# Install additional system dependencies
echo "📦 Installing system dependencies..."

# Detect OS and install appropriate packages
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y postgresql-client curl wget
    elif command -v yum &> /dev/null; then
        sudo yum install -y postgresql curl wget
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if command -v brew &> /dev/null; then
        brew install postgresql curl wget
    fi
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/raw
mkdir -p data/processed
mkdir -p logs
mkdir -p monitoring/data

# Set permissions
chmod +x scripts/setup/*.sh
chmod +x scripts/deploy/*.sh
chmod +x scripts/monitoring/*.sh

echo "✅ Dependencies installed successfully!"
echo ""
echo "Next steps:"
echo "1. Copy config/.env.example to config/.env and update values"
echo "2. Run 'docker-compose up -d' to start services"
echo "3. Run 'make test' to verify installation"
