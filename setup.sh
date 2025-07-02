#!/bin/bash

# GitHub Webhook Monitor Setup Script
echo "🚀 GitHub Webhook Monitor Setup"
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found"

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/
MONGO_DB_NAME=webhook_db
MONGO_COLLECTION_NAME=github_events

# Flask Configuration
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')
FLASK_DEBUG=True

# GitHub Webhook Configuration
GITHUB_WEBHOOK_SECRET=test-secret

# Application Configuration
HOST=0.0.0.0
PORT=5000
EOF
    echo "✅ .env file created with default values"
    echo "⚠️  Please update GITHUB_WEBHOOK_SECRET and MONGO_URI as needed"
else
    echo "ℹ️  .env file already exists"
fi

# Check MongoDB connection
echo "🔍 Checking MongoDB connection..."
python3 -c "
import pymongo
from config import Config
try:
    client = pymongo.MongoClient(Config.MONGO_URI)
    client.server_info()
    print('✅ MongoDB connection successful')
except Exception as e:
    print(f'❌ MongoDB connection failed: {e}')
    print('⚠️  Please ensure MongoDB is running or update MONGO_URI in .env')
"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Start the application: python3 app.py"
echo "2. Open browser to: http://localhost:5000"
echo "3. Test webhooks: python3 test_webhook.py"
echo "4. Configure GitHub webhook to point to your public URL"
echo ""
echo "For production deployment, see README.md" 