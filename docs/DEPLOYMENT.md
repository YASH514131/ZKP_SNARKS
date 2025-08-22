# Azure Deployment Guide

## Backend Deployment (Azure App Service)

### Option 1: Using Azure CLI

1. **Login to Azure**
   ```bash
   az login
   ```

2. **Create Resource Group**
   ```bash
   az group create --name zkp-age-verification-rg --location "East US"
   ```

3. **Deploy ARM Template**
   ```bash
   az deployment group create \
     --resource-group zkp-age-verification-rg \
     --template-file azure/arm-template.json \
     --parameters appName=zkp-age-verification
   ```

4. **Deploy Code**
   ```bash
   # Zip the backend code
   cd backend
   zip -r ../backend.zip . -x "__pycache__/*" "*.pyc"
   
   # Deploy to App Service
   az webapp deployment source config-zip \
     --resource-group zkp-age-verification-rg \
     --name zkp-age-verification-<unique-id> \
     --src ../backend.zip
   ```

### Option 2: GitHub Actions (Recommended)

Create `.github/workflows/deploy-backend.yml`:

```yaml
name: Deploy Backend to Azure

on:
  push:
    branches: [ main ]
    paths: [ 'backend/**' ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd backend
        pytest test_main.py -v
    
    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: 'zkp-age-verification'
        slot-name: 'production'
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
        package: './backend'
```

## Frontend Deployment (Azure Static Web Apps)

### Option 1: Using Azure CLI

1. **Build Flutter Web App**
   ```bash
   cd frontend/zkp_age_app
   flutter build web
   ```

2. **Create Static Web App**
   ```bash
   az staticwebapp create \
     --name zkp-age-verification-frontend \
     --resource-group zkp-age-verification-rg \
     --source https://github.com/yourusername/zkp-age-verification \
     --location "East US 2" \
     --branch main \
     --app-location "/frontend/zkp_age_app" \
     --output-location "build/web"
   ```

### Option 2: GitHub Actions (Automatic)

Azure Static Web Apps automatically creates a GitHub Action when you connect your repository.

The generated workflow will look like:

```yaml
name: Azure Static Web Apps CI/CD

on:
  push:
    branches:
      - main
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches:
      - main

jobs:
  build_and_deploy_job:
    if: github.event_name == 'push' || (github.event_name == 'pull_request' && github.event.action != 'closed')
    runs-on: ubuntu-latest
    name: Build and Deploy Job
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: true
      
      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.32.8'
      
      - name: Build Flutter Web
        run: |
          cd frontend/zkp_age_app
          flutter pub get
          flutter build web
      
      - name: Build And Deploy
        id: builddeploy
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: "upload"
          app_location: "/frontend/zkp_age_app"
          output_location: "build/web"
```

## Configuration Steps

### 1. Update Backend URL in Frontend

After deploying the backend, update the `backendUrl` in Flutter:

```dart
// In frontend/zkp_age_app/lib/main.dart
static const String backendUrl = 'https://zkp-age-verification-<unique-id>.azurewebsites.net';
```

### 2. Configure CORS in Backend

Update the CORS settings in `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-static-web-app-url.azurestaticapps.net",
        "http://localhost:3000",  # For local testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Set Environment Variables

For the Azure App Service, set these environment variables:

```bash
az webapp config appsettings set \
  --resource-group zkp-age-verification-rg \
  --name zkp-age-verification-<unique-id> \
  --settings PYTHON_VERSION=3.11
```

## Testing Deployment

1. **Test Backend API**
   ```bash
   curl https://zkp-age-verification-<unique-id>.azurewebsites.net/health
   ```

2. **Test Frontend**
   - Open your Static Web App URL
   - Try the age verification functionality
   - Check browser console for any errors

## Monitoring and Logs

### View Backend Logs
```bash
az webapp log tail \
  --resource-group zkp-age-verification-rg \
  --name zkp-age-verification-<unique-id>
```

### Application Insights
Enable Application Insights for monitoring:

```bash
az monitor app-insights component create \
  --app zkp-age-verification-insights \
  --location "East US" \
  --resource-group zkp-age-verification-rg
```

## Security Best Practices

1. **Enable HTTPS Only**
   ```bash
   az webapp update \
     --resource-group zkp-age-verification-rg \
     --name zkp-age-verification-<unique-id> \
     --https-only true
   ```

2. **Configure Custom Domain** (Optional)
   ```bash
   az webapp config hostname add \
     --webapp-name zkp-age-verification-<unique-id> \
     --resource-group zkp-age-verification-rg \
     --hostname yourdomain.com
   ```

3. **Set up SSL Certificate**
   ```bash
   az webapp config ssl bind \
     --certificate-thumbprint <thumbprint> \
     --ssl-type SNI \
     --name zkp-age-verification-<unique-id> \
     --resource-group zkp-age-verification-rg
   ```

## Scaling

### Backend Scaling
```bash
az appservice plan update \
  --name zkp-age-verification-plan \
  --resource-group zkp-age-verification-rg \
  --sku B1  # Scale up to Basic tier
```

### Frontend Scaling
Azure Static Web Apps automatically scales based on demand.

## Cost Optimization

- Use **F1 (Free)** tier for development
- Use **B1 (Basic)** tier for production
- Monitor usage with Azure Cost Management
- Set up spending alerts
