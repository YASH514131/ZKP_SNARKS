# 🚀 **Heroku Deployment Guide for zk-SNARK Age Verification**

Deploy your zk-SNARK Python backend to Heroku cloud platform.

## 📋 **Prerequisites**

1. **GitHub Student Developer Pack** (you have this ✅)
2. **Heroku Account** (free with student pack)
3. **Git** installed on your machine
4. **Heroku CLI** installed

## 🛠️ **Step 1: Install Heroku CLI**

### Windows (PowerShell):
```powershell
# Download and install from: https://devcenter.heroku.com/articles/heroku-cli
# Or use winget:
winget install Heroku.CLI
```

### Verify installation:
```bash
heroku --version
```

## 🔐 **Step 2: Login to Heroku**

```bash
heroku login
```
- Opens browser for authentication
- Login with your Heroku account (linked to GitHub Student Pack)

## 📁 **Step 3: Prepare Your Repository**

### Initialize Git (if not already done):
```bash
cd d:\Yash\ZKP
git init
git add .
git commit -m "Initial commit: zk-SNARK age verification system"
```

### Create .gitignore for Python:
```bash
# Already included in your project
__pycache__/
*.py[cod]
*$py.class
.env
venv/
.venv/
```

## 🌐 **Step 4: Create Heroku App**

```bash
cd backend
heroku create your-zksnark-app-name
```

**Replace `your-zksnark-app-name` with a unique name like:**
- `zksnark-age-verification`
- `zk-proof-age-demo`
- `your-name-zksnark`

## ⚙️ **Step 5: Configure Environment Variables**

```bash
# Set any environment variables your app needs
heroku config:set ENVIRONMENT=production
heroku config:set CORS_ORIGINS="*"
```

## 🚀 **Step 6: Deploy to Heroku**

```bash
# Deploy from backend folder
git add .
git commit -m "Ready for Heroku deployment"
git push heroku main
```

**Or if you're on master branch:**
```bash
git push heroku master
```

## 🔍 **Step 7: Verify Deployment**

### Check app status:
```bash
heroku ps:scale web=1
heroku logs --tail
```

### Open your app:
```bash
heroku open
```

Your zk-SNARK API will be available at:
- **Main URL**: `https://your-app-name.herokuapp.com/`
- **API Docs**: `https://your-app-name.herokuapp.com/docs`
- **ZKP Info**: `https://your-app-name.herokuapp.com/zkp-info`

## 🔧 **Step 8: Update Flutter Frontend**

Update your Flutter app to use the Heroku URL:

```dart
// In frontend/zkp_age_app/lib/main.dart
static const String backendUrl = 'https://your-app-name.herokuapp.com';
```

## 📊 **Monitoring & Logs**

### View real-time logs:
```bash
heroku logs --tail
```

### Check app metrics:
```bash
heroku ps
heroku releases
```

### Restart app if needed:
```bash
heroku restart
```

## 🔄 **Continuous Deployment**

### For automatic deployment on git push:
```bash
# Connect GitHub repository
heroku git:remote -a your-app-name

# Enable auto-deployment from GitHub
# Go to: https://dashboard.heroku.com/apps/your-app-name/deploy
# Connect to GitHub and enable automatic deploys
```

## 🛡️ **Security Considerations**

1. **Environment Variables**: Store sensitive data in Heroku config vars
   ```bash
   heroku config:set SECRET_KEY="your-secret-key"
   ```

2. **HTTPS**: Heroku provides SSL certificates automatically

3. **CORS**: Already configured for web access

## 💰 **Cost & Limits (Student Pack)**

- **Free Dynos**: 550-1000 hours/month
- **Custom Domain**: Free with student pack
- **Add-ons**: Many free tiers available

## 🔗 **Useful Commands**

```bash
# View app info
heroku info

# Scale dynos
heroku ps:scale web=1

# Access bash shell
heroku run bash

# Check config variables
heroku config

# View releases
heroku releases

# Rollback to previous version
heroku rollback v<version-number>
```

## 🚨 **Troubleshooting**

### Common Issues:

1. **Build fails**: Check `requirements.txt` and `runtime.txt`
2. **App crashes**: Check logs with `heroku logs --tail`
3. **Port issues**: Heroku sets `$PORT` automatically (handled in Procfile)
4. **Module not found**: Ensure all dependencies in `requirements.txt`

### Debug commands:
```bash
heroku logs --tail
heroku run python --version
heroku run pip list
```

## ✅ **Success Checklist**

- [ ] Heroku CLI installed
- [ ] Logged in to Heroku
- [ ] App created (`heroku create`)
- [ ] Code deployed (`git push heroku main`)
- [ ] App accessible online
- [ ] API endpoints working
- [ ] Flutter frontend updated with new URL
- [ ] zk-SNARK verification working end-to-end

## 🎉 **You're Live!**

Your zk-SNARK age verification system is now running in the cloud! 

**Share your API:**
- `https://your-app-name.herokuapp.com/docs` - Interactive API documentation
- `https://your-app-name.herokuapp.com/zkp-info` - ZKP implementation details

**Next Steps:**
1. Update Flutter frontend URL
2. Test end-to-end verification
3. Share with friends/professors
4. Add to your portfolio!

---

**🔐 You now have a production-grade Zero-Knowledge Proof system running in the cloud!** 🚀
