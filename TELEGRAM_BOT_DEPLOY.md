# 🤖 Telegram Bot Deployment Guide

## 🚨 **Issue Fixed**: Port Binding Error

The error you encountered happens because Render was trying to deploy the Telegram bot as a **web service** (which needs to bind to a port), but Telegram bots use **polling** and don't need to expose ports.

**Solution**: Deploy as a **background worker** instead.

## 🚀 **Deploy Options**

### Option 1: Deploy Bot with API (Recommended)

The main `render.yaml` now includes both services:
- **Web Service**: Oneliac API (binds to port)
- **Background Worker**: Telegram Bot (no port needed)

```bash
# 1. Push updated render.yaml
git add render.yaml
git commit -m "Fix Telegram bot deployment as background worker"
git push origin main

# 2. In Render dashboard:
# - Go to your existing service
# - It will detect the updated render.yaml
# - Deploy both API and bot together
```

### Option 2: Deploy Bot Separately

Use the dedicated `telegram_bot/render.yaml`:

```bash
# 1. Create new service on Render
# 2. Connect GitHub repo
# 3. Set root directory to: telegram_bot
# 4. Render will auto-detect telegram_bot/render.yaml
```

## 🔧 **Environment Variables Setup**

### In Render Dashboard:

1. **Go to your service** → Environment tab
2. **Add environment variables**:

```bash
TELEGRAM_BOT_TOKEN=8150139391:AAENQbWeIi9NkC99M8ooaZ_fnte8DvafTHM
API_BASE_URL=https://oneliac-api.onrender.com
```

⚠️ **Security Note**: Never commit bot tokens to Git. Always set them in Render dashboard.

## 📋 **Deployment Steps**

### Step 1: Update Configuration
```bash
git add .
git commit -m "Deploy Telegram bot as background worker"
git push origin main
```

### Step 2: Deploy on Render

#### For Combined Deployment:
1. Go to [render.com](https://render.com) dashboard
2. Your existing service will detect the updated `render.yaml`
3. Click "Deploy Latest Commit"
4. Render will create both:
   - **oneliac-api** (web service)
   - **oneliac-telegram-bot** (background worker)

#### For Separate Bot Deployment:
1. Click "New +" → "Background Worker"
2. Connect GitHub repository
3. Set **Root Directory**: `telegram_bot`
4. Render auto-detects `telegram_bot/render.yaml`
5. Add environment variables
6. Deploy

### Step 3: Set Environment Variables

In Render dashboard for the bot service:
```
TELEGRAM_BOT_TOKEN = your_bot_token_here
API_BASE_URL = https://oneliac-api.onrender.com
```

### Step 4: Monitor Deployment

Check logs in Render dashboard:
```
✅ Bot starting polling...
✅ Application started
✅ HTTP Request: POST https://api.telegram.org/bot.../getUpdates "HTTP/1.1 200 OK"
```

## 🧪 **Test Your Bot**

1. **Find your bot** on Telegram
2. **Send `/start`** - should get welcome message
3. **Try `/health`** - should show API status
4. **Test `/eligibility PATIENT_001 PROC001`** - should work with your API

## 🔍 **Troubleshooting**

### Bot Not Responding
```bash
# Check logs in Render dashboard
# Look for:
✅ "Application started" - Bot is running
❌ "Invalid token" - Check TELEGRAM_BOT_TOKEN
❌ "Connection error" - Check API_BASE_URL
```

### Common Fixes

#### 1. Invalid Bot Token
```bash
# In Render dashboard, update:
TELEGRAM_BOT_TOKEN=your_correct_token_here
```

#### 2. API Connection Issues
```bash
# Update API URL in Render dashboard:
API_BASE_URL=https://your-actual-api-url.onrender.com
```

#### 3. Bot Crashes on Start
```bash
# Check requirements.txt includes:
python-telegram-bot>=20.0
aiohttp>=3.9.0
python-dotenv>=1.0.0
```

## 📊 **Monitor Your Bot**

### Render Dashboard
- **Logs**: Real-time bot activity
- **Metrics**: CPU/Memory usage
- **Events**: Deployment history

### Bot Health Check
```bash
# The bot logs show:
2025-12-31 14:55:40,149 - telegram.ext.Application - INFO - Application started
2025-12-31 14:55:50,635 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot.../getUpdates "HTTP/1.1 200 OK"
```

### Auto-Restart Feature
The bot automatically restarts on crashes:
- **Max restarts**: 10 attempts
- **Restart delay**: 5 seconds (increases on repeated failures)
- **Graceful shutdown**: Handles SIGTERM/SIGINT

## 🎯 **Production Checklist**

- [ ] ✅ Bot deployed as background worker (not web service)
- [ ] ✅ Environment variables set in Render dashboard
- [ ] ✅ Bot token kept secure (not in code)
- [ ] ✅ API URL points to live API
- [ ] ✅ Bot responds to `/start` command
- [ ] ✅ Health check works with `/health`
- [ ] ✅ Eligibility check works with real API
- [ ] ✅ Logs show successful polling

## 🚀 **Your Bot is Now Live!**

**Bot Features**:
- ✅ **Auto-restart** on crashes
- ✅ **Comprehensive error handling**
- ✅ **Production logging**
- ✅ **Graceful shutdown**
- ✅ **API integration**
- ✅ **User-friendly interface**

**Commands Available**:
- `/start` - Welcome message
- `/help` - Show all commands
- `/health` - Check API status
- `/eligibility <patient_id> <procedure>` - Check eligibility
- `/prescription <patient_id> <drug>` - Validate prescription

**Your Telegram bot is ready to serve users 24/7!** 🎉

---

## 📞 **Need Help?**

- **Render Docs**: [Background Workers](https://render.com/docs/background-workers)
- **Bot Logs**: Check Render dashboard → Your service → Logs
- **GitHub Issues**: Report problems in your repository
- **Telegram Bot API**: [Official Documentation](https://core.telegram.org/bots/api)