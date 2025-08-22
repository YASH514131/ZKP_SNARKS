# 🚀 Quick Heroku Deployment Script for zk-SNARK Backend (PowerShell)

Write-Host "🔐 Deploying zk-SNARK Age Verification to Heroku..." -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "zksnark_main.py")) {
    Write-Host "❌ Please run this script from the backend directory" -ForegroundColor Red
    exit 1
}

# Check if Heroku CLI is installed
try {
    heroku --version | Out-Null
} catch {
    Write-Host "❌ Heroku CLI not found. Please install it first:" -ForegroundColor Red
    Write-Host "   https://devcenter.heroku.com/articles/heroku-cli" -ForegroundColor Yellow
    exit 1
}

# Check if logged in to Heroku
try {
    heroku auth:whoami | Out-Null
} catch {
    Write-Host "🔐 Please login to Heroku first:" -ForegroundColor Yellow
    heroku login
}

# Get app name from user
$APP_NAME = Read-Host "📝 Enter your Heroku app name (e.g., zksnark-age-verification)"

if ([string]::IsNullOrEmpty($APP_NAME)) {
    Write-Host "❌ App name cannot be empty" -ForegroundColor Red
    exit 1
}

Write-Host "🚀 Creating Heroku app: $APP_NAME" -ForegroundColor Green

# Create Heroku app
heroku create $APP_NAME

# Set environment variables
Write-Host "⚙️ Setting environment variables..." -ForegroundColor Yellow
heroku config:set ENVIRONMENT=production --app $APP_NAME
heroku config:set CORS_ORIGINS="*" --app $APP_NAME

# Initialize git if needed
if (-not (Test-Path ".git")) {
    Write-Host "📁 Initializing Git repository..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit: zk-SNARK age verification backend"
}

# Add Heroku remote
heroku git:remote -a $APP_NAME

Write-Host "🚀 Deploying to Heroku..." -ForegroundColor Green
git add .
git commit -m "Deploy zk-SNARK backend to Heroku"
git push heroku main

if ($LASTEXITCODE -ne 0) {
    git push heroku master
}

Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Your zk-SNARK API is now live at:" -ForegroundColor Cyan
Write-Host "   https://$APP_NAME.herokuapp.com/" -ForegroundColor White
Write-Host ""
Write-Host "📚 API Documentation:" -ForegroundColor Cyan
Write-Host "   https://$APP_NAME.herokuapp.com/docs" -ForegroundColor White
Write-Host ""
Write-Host "🔍 ZKP Information:" -ForegroundColor Cyan
Write-Host "   https://$APP_NAME.herokuapp.com/zkp-info" -ForegroundColor White
Write-Host ""
Write-Host "📊 Monitor logs:" -ForegroundColor Cyan
Write-Host "   heroku logs --tail --app $APP_NAME" -ForegroundColor White
Write-Host ""
Write-Host "🔄 Don't forget to update your Flutter frontend URL to:" -ForegroundColor Yellow
Write-Host "   https://$APP_NAME.herokuapp.com" -ForegroundColor White
