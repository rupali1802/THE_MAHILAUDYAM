#!/bin/bash
# Mahila Udyam - Quick Setup Script
# Run: bash setup.sh

set -e

echo ""
echo "=================================================="
echo "   🌸 Mahila Udyam - Setup Script"
echo "   महिला उद्यम | மகிளா உத்யம்"
echo "=================================================="
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10+"
    exit 1
fi
echo "✓ Python: $(python3 --version)"

# Check Node
if ! command -v node &>/dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi
echo "✓ Node: $(node --version)"

echo ""
echo "=== Setting up Backend ==="
cd backend

# Virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null || true

# Install packages
pip install -r requirements.txt -q
echo "✓ Python packages installed"

# SQLite config for quick setup
echo "ℹ️  Using SQLite for development (edit settings.py for MySQL)"

# Run migrations
python manage.py migrate --run-syncdb 2>/dev/null || python manage.py migrate
echo "✓ Database migrations complete"

# Train ML model
echo "🤖 Training ML model..."
python ml_models/model_training.py
echo "✓ ML model trained"

cd ..

echo ""
echo "=== Setting up Frontend ==="
cd frontend
npm install --silent
echo "✓ Frontend packages installed"
cd ..

echo ""
echo "=================================================="
echo "✅ Setup Complete!"
echo ""
echo "To start the app:"
echo ""
echo "  Terminal 1 (Backend):"
echo "    cd backend"
echo "    source venv/bin/activate"
echo "    python manage.py runserver 0.0.0.0:8000"
echo ""
echo "  Terminal 2 (Frontend):"
echo "    cd frontend"
echo "    npm start"
echo ""
echo "  Open: http://localhost:3001"
echo "  Admin: http://localhost:8000/admin"
echo "=================================================="
