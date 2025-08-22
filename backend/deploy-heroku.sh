#!/bin/bash

# 🚀 Quick Heroku Deployment Script for zk-SNARK Backend

echo "🔐 Deploying zk-SNARK Age Verification to Heroku..."

# Check if we're in the right directory
if [ ! -f "zksnark_main.py" ]; then
    echo "❌ Please run this script from the backend directory"
    exit 1
fi

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first:"
    echo "   https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "🔐 Please login to Heroku first:"
    heroku login
fi

# Get app name from user
echo "📝 Enter your Heroku app name (e.g., zksnark-age-verification):"
read -r APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "❌ App name cannot be empty"
    exit 1
fi

echo "🚀 Creating Heroku app: $APP_NAME"

# Create Heroku app
heroku create "$APP_NAME"

# Set environment variables
echo "⚙️ Setting environment variables..."
heroku config:set ENVIRONMENT=production --app "$APP_NAME"
heroku config:set CORS_ORIGINS="*" --app "$APP_NAME"

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: zk-SNARK age verification backend"
fi

# Add Heroku remote
heroku git:remote -a "$APP_NAME"

echo "🚀 Deploying to Heroku..."
git add .
git commit -m "Deploy zk-SNARK backend to Heroku" || echo "No changes to commit"
git push heroku main || git push heroku master

echo "✅ Deployment complete!"
echo ""
echo "🌐 Your zk-SNARK API is now live at:"
echo "   https://$APP_NAME.herokuapp.com/"
echo ""
echo "📚 API Documentation:"
echo "   https://$APP_NAME.herokuapp.com/docs"
echo ""
echo "🔍 ZKP Information:"
echo "   https://$APP_NAME.herokuapp.com/zkp-info"
echo ""
echo "📊 Monitor logs:"
echo "   heroku logs --tail --app $APP_NAME"
echo ""
echo "🔄 Don't forget to update your Flutter frontend URL to:"
echo "   https://$APP_NAME.herokuapp.com"
