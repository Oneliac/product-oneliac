# 🎨 Render Deployment - Quick Start

## 🚀 Deploy in 3 Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

### 2. Deploy on Render
1. Go to [render.com](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `healthcare-agents-api`
   - **Build Command**: `pip install -r agents/requirements.txt`
   - **Start Command**: `python -m uvicorn agents.api:app --host 0.0.0.0 --port $PORT`
5. Click **"Create Web Service"**

### 3. Test Your API
```bash
# Your URL will be something like:
curl https://healthcare-agents-api.onrender.com/health

# Expected response:
{"status":"healthy","version":"0.1.0","message":"Healthcare agents API operational"}
```

## 🤖 Update Telegram Bot

After deployment, update your bot:

```bash
cd telegram_bot

# Edit .env file
API_BASE_URL=https://healthcare-agents-api.onrender.com

# Run bot
python bot.py
```

## 💰 Pricing

- **Free**: Perfect for testing (sleeps after 15min)
- **Starter ($7/mo)**: Always-on, recommended for production
- **Standard ($25/mo)**: More resources for high traffic

## ✅ Why Render?

- ✅ **Free tier available**
- ✅ **Full Python support** (no serverless limitations)
- ✅ **PyTorch works** (uses our mock implementation)
- ✅ **Auto-deploy** from GitHub
- ✅ **Built-in SSL** and monitoring
- ✅ **Easy scaling** when you need it

## 📊 Your Live Endpoints

After deployment:
- **Health**: `GET /health`
- **API Docs**: `GET /docs` (Swagger UI)
- **Eligibility**: `POST /eligibility/verify`
- **Prescription**: `POST /prescription/validate`
- **Federated Learning**: `POST /federated-learning/train`

## 🔧 Configuration Files

I've created these for you:
- ✅ `render.yaml` - Render configuration
- ✅ `RENDER_DEPLOY.md` - Complete guide
- ✅ `deploy-render.sh` - Deployment script

**Ready to deploy?** Just follow the 3 steps above! 🚀