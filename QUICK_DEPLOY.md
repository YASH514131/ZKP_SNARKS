# 🚀 **Quick Deployment Guide**

## **Method 1: Azure (Recommended for GitHub Student Pack)**

### **Step 1: Install Azure CLI**
1. Download from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
2. Or run: `winget install Microsoft.AzureCLI`

### **Step 2: Login and Deploy**
```powershell
# Login to Azure
az login

# Navigate to your project
cd "d:\Yash\ZKP"

# Run our deployment script
.\azure\deploy.ps1
```

That's it! The script will:
- ✅ Create Azure resources
- ✅ Deploy your zk-SNARK backend
- ✅ Give you the public URL

---

## **Method 2: Heroku (Easiest)**

### **Step 1: Install Heroku CLI**
Download from: https://devcenter.heroku.com/articles/heroku-cli

### **Step 2: Deploy**
```bash
# Login
heroku login

# Navigate to backend
cd backend

# Create and deploy
git init
git add .
git commit -m "Deploy zk-SNARK API"
heroku create your-app-name
git push heroku main
```

---

## **Method 3: Railway (Super Easy)**

### **Step 1: Sign up**
Go to: https://railway.app (free with GitHub Student Pack)

### **Step 2: Deploy**
1. Connect your GitHub repo
2. Select the `backend` folder
3. Railway auto-deploys!

---

## **Update Frontend After Deployment**

Edit `frontend/zkp_age_app/lib/main.dart`:
```dart
// Change this line:
static const String backendUrl = 'http://localhost:8001';

// To your deployed URL:
static const String backendUrl = 'https://your-app.azurewebsites.net';
```

## **Test Your Deployed API**

Visit: `https://your-app-url/docs` to see your live zk-SNARK API documentation!

🎉 **Your zk-SNARK system will be live on the internet!** 🔐
