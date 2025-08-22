# Deploy zk-SNARK Backend to Azure
# Run this script after setting up Azure CLI

Write-Host "🔐 Deploying zk-SNARK Age Verification to Azure..." -ForegroundColor Cyan

# Variables
$resourceGroup = "zksnark-rg"
$appName = "zksnark-age-verification"
$location = "East US"
$templateFile = "azure/app-service-template.json"

# Check if logged into Azure
Write-Host "📝 Checking Azure login..." -ForegroundColor Yellow
$loginCheck = az account show 2>$null
if (-not $loginCheck) {
    Write-Host "❌ Not logged into Azure. Please run: az login" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Azure login verified" -ForegroundColor Green

# Create resource group
Write-Host "🏗️ Creating resource group..." -ForegroundColor Yellow
az group create --name $resourceGroup --location $location

# Deploy ARM template
Write-Host "🚀 Deploying Azure resources..." -ForegroundColor Yellow
$deployment = az deployment group create `
    --resource-group $resourceGroup `
    --template-file $templateFile `
    --parameters appName=$appName

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Azure resources created successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Resource deployment failed" -ForegroundColor Red
    exit 1
}

# Deploy code
Write-Host "📦 Deploying application code..." -ForegroundColor Yellow
Push-Location backend

# Create ZIP package
Write-Host "📦 Creating deployment package..." -ForegroundColor Yellow
Compress-Archive -Path * -DestinationPath ../deploy.zip -Force

Pop-Location

# Deploy to Azure App Service
az webapp deployment source config-zip `
    --resource-group $resourceGroup `
    --name $appName `
    --src deploy.zip

if ($LASTEXITCODE -eq 0) {
    Write-Host "🎉 Deployment completed successfully!" -ForegroundColor Green
    
    # Get the URL
    $appUrl = az webapp show --resource-group $resourceGroup --name $appName --query "defaultHostName" --output tsv
    
    Write-Host ""
    Write-Host "🌐 Your zk-SNARK API is now live at:" -ForegroundColor Cyan
    Write-Host "   📡 API Base URL: https://$appUrl" -ForegroundColor White
    Write-Host "   📚 API Docs: https://$appUrl/docs" -ForegroundColor White
    Write-Host "   🔍 ZKP Info: https://$appUrl/zkp-info" -ForegroundColor White
    Write-Host ""
    Write-Host "🔧 Next steps:" -ForegroundColor Yellow
    Write-Host "   1. Update your Flutter app's backend URL to: https://$appUrl" -ForegroundColor White
    Write-Host "   2. Test the API endpoints" -ForegroundColor White
    Write-Host "   3. Configure custom domain (optional)" -ForegroundColor White
    
} else {
    Write-Host "❌ Code deployment failed" -ForegroundColor Red
    exit 1
}

# Cleanup
Remove-Item deploy.zip -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "🎯 Deployment Summary:" -ForegroundColor Cyan
Write-Host "   Resource Group: $resourceGroup" -ForegroundColor White
Write-Host "   App Service: $appName" -ForegroundColor White
Write-Host "   Location: $location" -ForegroundColor White
