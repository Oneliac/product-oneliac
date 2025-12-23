# 🚀 Deploy to Vercel in 2 Minutes

Your healthcare agents API is ready for Vercel deployment!

## Quick Start

### Option 1: One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/healthcare-agents-api)

### Option 2: CLI Deploy

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### Option 3: Git Integration

1. Push to GitHub
2. Connect at [vercel.com](https://vercel.com)
3. Auto-deploy on every push

## What's Included

✅ **Serverless FastAPI** - Optimized for Vercel Functions  
✅ **PyTorch Mock** - Lightweight ML inference  
✅ **Auto HTTPS** - SSL certificates included  
✅ **Global CDN** - Fast worldwide access  
✅ **Zero Config** - Works out of the box  

## API Endpoints

After deployment, test your live API:

```bash
# Replace with your Vercel URL
curl https://your-app.vercel.app/health
curl https://your-app.vercel.app/docs
```

## Files Added for Vercel

- `vercel.json` - Deployment configuration
- `api/index.py` - Serverless entry point  
- `api/torch_mock.py` - Lightweight PyTorch replacement
- `requirements.txt` - Vercel-compatible dependencies
- `.vercelignore` - Exclude unnecessary files

## Cost

- **Free Tier**: 100GB bandwidth/month
- **Pro Tier**: $20/month for unlimited usage
- **No server management** required

## Support

📖 **Full Guide**: [VERCEL_DEPLOYMENT.md](./VERCEL_DEPLOYMENT.md)  
🔧 **Troubleshooting**: Check Vercel function logs  
💬 **Community**: [Vercel Discord](https://vercel.com/discord)  

---

**Ready to deploy?** Run `vercel --prod` or use the deploy button above!