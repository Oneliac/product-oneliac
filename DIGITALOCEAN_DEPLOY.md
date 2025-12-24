# 🌊 Deploy to DigitalOcean App Platform

DigitalOcean provides reliable hosting with great performance.

## 🚀 Quick Deploy

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Deploy to DigitalOcean"
   git push origin main
   ```

2. **Create App**:
   - Go to [DigitalOcean Apps](https://cloud.digitalocean.com/apps)
   - Click "Create App"
   - Connect your GitHub repository
   - Select your repository and branch

3. **Configure**:
   - **Name**: `healthcare-agents-api`
   - **Plan**: Basic ($5/month)
   - **Build Command**: `pip install -r agents/requirements.txt`
   - **Run Command**: `python -m uvicorn agents.api:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables**:
   ```
   PYTHONPATH=.
   SOLANA_ENDPOINT=https://api.devnet.solana.com
   ```

5. **Deploy**: Click "Create Resources"

## 💰 Pricing
- **Basic**: $5/month
- **Professional**: $12/month
- **Free Trial**: $200 credit

## 🔗 Your URL
- Format: `https://healthcare-agents-api-xxxxx.ondigitalocean.app`
- Test: `https://your-app.ondigitalocean.app/health`