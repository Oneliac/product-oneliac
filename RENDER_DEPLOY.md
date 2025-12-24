# 🎨 Deploy to Render - Complete Guide

Render is perfect for your healthcare API with free tier and easy deployment!

## 🚀 Quick Deploy (3 minutes)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

### Step 2: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended)
3. Connect your GitHub account

### Step 3: Deploy Web Service
1. **Click "New +"** → **"Web Service"**
2. **Connect Repository**: Select your healthcare agents repo
3. **Configure Service**:
   - **Name**: `healthcare-agents-api`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r agents/requirements.txt`
   - **Start Command**: `python -m uvicorn agents.api:app --host 0.0.0.0 --port $PORT`

### Step 4: Environment Variables
Add these in the "Environment" section:
```
PYTHONPATH=.
SOLANA_ENDPOINT=https://api.devnet.solana.com
```

### Step 5: Choose Plan
- **Free Tier**: $0/month (perfect for testing)
  - 512MB RAM, sleeps after 15min inactivity
- **Starter**: $7/month (recommended for production)
  - 512MB RAM, always on
- **Standard**: $25/month (for high traffic)

### Step 6: Deploy
1. Click **"Create Web Service"**
2. Wait 3-5 minutes for deployment
3. Get your URL: `https://healthcare-agents-api.onrender.com`

## ✅ Test Your Deployment

```bash
# Test health endpoint
curl https://healthcare-agents-api.onrender.com/health

# Expected response:
# {"status":"healthy","version":"0.1.0","message":"Healthcare agents API operational"}

# Test API docs
# Visit: https://healthcare-agents-api.onrender.com/docs
```

## 🔧 Render Configuration Files

I've already created the `render.yaml` file for you:

```yaml
services:
  - type: web
    name: healthcare-agents-api
    env: python
    buildCommand: pip install -r agents/requirements.txt
    startCommand: python -m uvicorn agents.api:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    envVars:
      - key: PYTHONPATH
        value: .
      - key: SOLANA_ENDPOINT
        value: https://api.devnet.solana.com
```

## 🤖 Update Telegram Bot

After successful deployment, update your bot configuration:

```bash
cd telegram_bot

# Edit .env file
nano .env

# Update API_BASE_URL
API_BASE_URL=https://healthcare-agents-api.onrender.com
```

Then restart your bot:
```bash
python bot.py
```

## 📊 Your API Endpoints

Once deployed, these endpoints will be available:

- **Health Check**: `GET /health`
- **API Documentation**: `GET /docs` (Swagger UI)
- **ReDoc**: `GET /redoc`
- **Eligibility Verification**: `POST /eligibility/verify`
- **Prescription Validation**: `POST /prescription/validate`
- **Federated Learning**: `POST /federated-learning/train`
- **FL Status**: `GET /federated-learning/status`

## 🔍 Monitoring & Debugging

### View Logs
1. Go to your Render dashboard
2. Click on your service
3. Go to "Logs" tab
4. See real-time application logs

### Check Metrics
- **CPU Usage**: Monitor in dashboard
- **Memory Usage**: Track RAM consumption
- **Response Times**: See request latency
- **Error Rates**: Monitor failed requests

### Common Issues & Solutions

#### 1. Build Failures
```
Error: No module named 'torch'
```
**Solution**: The mock PyTorch should handle this. Check if `agents/torch_mock.py` exists.

#### 2. Import Errors
```
ModuleNotFoundError: No module named 'agents'
```
**Solution**: Ensure `PYTHONPATH=.` is set in environment variables.

#### 3. Port Issues
```
Error: Address already in use
```
**Solution**: Render automatically sets `$PORT`. Make sure start command uses `--port $PORT`.

#### 4. Memory Issues (Free Tier)
```
Service killed due to memory limit
```
**Solution**: Upgrade to Starter plan ($7/month) for more memory.

## 🔄 Auto-Deployment

Render automatically redeploys when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Update healthcare agents"
git push origin main

# Render will automatically detect and redeploy!
```

## 🌐 Custom Domain (Optional)

### Free Subdomain
Render provides: `https://healthcare-agents-api.onrender.com`

### Custom Domain ($7/month plan required)
1. Go to "Settings" → "Custom Domains"
2. Add your domain: `api.yourdomain.com`
3. Update DNS records as shown
4. SSL certificate automatically provisioned

## 💰 Pricing Comparison

| Feature | Free | Starter ($7/mo) | Standard ($25/mo) |
|---------|------|-----------------|-------------------|
| **RAM** | 512MB | 512MB | 1GB |
| **Always On** | ❌ (sleeps) | ✅ | ✅ |
| **Custom Domain** | ❌ | ✅ | ✅ |
| **Build Minutes** | 500/month | Unlimited | Unlimited |
| **Bandwidth** | 100GB | Unlimited | Unlimited |

## 🚀 Production Checklist

### Before Going Live:
- [ ] Test all API endpoints
- [ ] Set up custom domain
- [ ] Configure monitoring alerts
- [ ] Set up database (if needed)
- [ ] Enable HTTPS (automatic)
- [ ] Test Telegram bot integration

### Security:
- [ ] Review environment variables
- [ ] Set up proper CORS policies
- [ ] Enable rate limiting
- [ ] Monitor for suspicious activity

## 🔗 Integration with Other Services

### Database (Optional)
```bash
# Add PostgreSQL database
# In Render dashboard: New → PostgreSQL
# Get connection string and add to environment variables
DATABASE_URL=postgresql://user:pass@host:port/db
```

### Redis Cache (Optional)
```bash
# Add Redis for caching
# In Render dashboard: New → Redis
# Get connection string
REDIS_URL=redis://user:pass@host:port
```

## 📞 Support & Resources

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **Community**: [community.render.com](https://community.render.com)
- **Status Page**: [status.render.com](https://status.render.com)
- **Support**: Available on paid plans

## 🎯 Next Steps

1. **Deploy to Render** using the steps above
2. **Test your API** with the health endpoint
3. **Update Telegram bot** with new URL
4. **Test bot commands** to ensure everything works
5. **Share your API docs** at `/docs` endpoint

---

**Ready to deploy?** Follow the steps above and you'll have your healthcare API live on Render in minutes! 🎨🚀