# 🚂 Deploy to Railway (Recommended)

Railway is the easiest way to deploy your healthcare API with full server capabilities.

## 🚀 Quick Deploy (2 minutes)

### Method 1: GitHub Integration (Recommended)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Deploy to Railway"
   git push origin main
   ```

2. **Connect to Railway**:
   - Go to [railway.app](https://railway.app)
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Click "Deploy Now"

3. **Set Environment Variables** (optional):
   - Go to Variables tab
   - Add `SOLANA_ENDPOINT=https://api.devnet.solana.com`

4. **Get Your URL**:
   - Railway will give you a URL like: `https://your-app.railway.app`
   - Test it: `https://your-app.railway.app/health`

### Method 2: Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

## ✅ Why Railway is Better

- **✅ Full Server**: No serverless limitations
- **✅ PyTorch Support**: Full ML library support
- **✅ Persistent Storage**: If you need file storage
- **✅ Real-time Logs**: Easy debugging
- **✅ Auto-scaling**: Handles traffic spikes
- **✅ Custom Domains**: Free SSL certificates
- **✅ Database Support**: PostgreSQL, Redis, etc.

## 💰 Pricing

- **Hobby Plan**: $5/month (perfect for this project)
- **Pro Plan**: $20/month (for production)
- **Free Trial**: Available for testing

## 🔧 Configuration Files Added

- `railway.json` - Railway deployment config
- Uses existing `requirements.txt`
- Uses existing `agents/` code

## 📊 After Deployment

Your API will be available at:
- **Health**: `GET https://your-app.railway.app/health`
- **Docs**: `GET https://your-app.railway.app/docs`
- **Eligibility**: `POST https://your-app.railway.app/eligibility/verify`
- **Prescription**: `POST https://your-app.railway.app/prescription/validate`

## 🔗 Update Telegram Bot

After Railway deployment, update your bot:

```bash
# Edit telegram_bot/.env
API_BASE_URL=https://your-app.railway.app
```

## 🚀 Deploy Now

Choose your method:
1. **GitHub** (easiest): Push code → Connect at railway.app
2. **CLI**: `railway up`

Railway will automatically detect it's a Python app and deploy it correctly!