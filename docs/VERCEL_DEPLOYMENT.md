# Vercel Deployment Guide

Deploy your healthcare agents API to Vercel in minutes with serverless functions.

## Prerequisites

- [Vercel CLI](https://vercel.com/cli) installed: `npm i -g vercel`
- Vercel account (free tier available)
- Git repository (GitHub, GitLab, or Bitbucket)

## Quick Deploy

### Option 1: Deploy from Git (Recommended)

1. **Push to Git repository**:
   ```bash
   git add .
   git commit -m "Add Vercel deployment config"
   git push origin main
   ```

2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your Git repository
   - Vercel will auto-detect the configuration

3. **Deploy**:
   - Click "Deploy"
   - Wait 2-3 minutes for build completion
   - Get your live URL: `https://your-project.vercel.app`

### Option 2: Deploy with CLI

1. **Login to Vercel**:
   ```bash
   vercel login
   ```

2. **Deploy**:
   ```bash
   vercel --prod
   ```

3. **Follow prompts**:
   - Set up and deploy? `Y`
   - Which scope? Select your account
   - Link to existing project? `N` (for first deploy)
   - Project name? `healthcare-agents-api`
   - Directory? `./` (current directory)

## Configuration Files

The following files have been created for Vercel deployment:

### `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ],
  "env": {
    "PYTHONPATH": "."
  },
  "functions": {
    "api/index.py": {
      "maxDuration": 30
    }
  }
}
```

### `api/index.py`
- Serverless entry point
- Handles PyTorch compatibility issues
- Imports the main FastAPI app

### `requirements.txt` (root level)
- Vercel-compatible dependencies
- Excludes PyTorch (uses mock implementation)
- Optimized for serverless deployment

## API Endpoints

Once deployed, your API will be available at:

- **Health Check**: `GET /health`
- **API Docs**: `GET /docs` (Swagger UI)
- **ReDoc**: `GET /redoc`
- **Eligibility**: `POST /eligibility/verify`
- **Prescription**: `POST /prescription/validate`
- **Federated Learning**: `POST /federated-learning/train`

## Testing Deployment

Test your deployed API:

```bash
# Replace with your Vercel URL
curl https://your-project.vercel.app/health

# Expected response:
# {"status":"healthy","version":"0.1.0","message":"Healthcare agents API operational"}
```

## Environment Variables

For production, set environment variables in Vercel dashboard:

1. Go to your project in Vercel dashboard
2. Navigate to Settings → Environment Variables
3. Add any required variables:
   - `SOLANA_ENDPOINT` (optional, defaults to devnet)
   - `ENCRYPTION_KEY` (for production encryption)

## Limitations & Considerations

### Serverless Constraints
- **Cold starts**: First request may be slower (~2-3 seconds)
- **Execution time**: 30-second maximum per request
- **Memory**: Limited to 1GB on free tier
- **File system**: Read-only, no persistent storage

### PyTorch Compatibility
- Uses lightweight mock implementation
- Real PyTorch models would require different deployment strategy
- For production ML workloads, consider Railway or dedicated servers

### Performance Optimization
- **Caching**: Implement Redis for frequently accessed data
- **Database**: Use external database (PostgreSQL, MongoDB)
- **CDN**: Vercel automatically provides global CDN

## Monitoring & Debugging

### View Logs
```bash
vercel logs your-project-url
```

### Function Analytics
- Visit Vercel dashboard
- Go to Functions tab
- Monitor invocations, duration, and errors

### Common Issues

1. **Import Errors**:
   - Check `requirements.txt` includes all dependencies
   - Verify Python path configuration

2. **Timeout Errors**:
   - Optimize slow operations
   - Consider async processing for heavy tasks

3. **Memory Issues**:
   - Reduce memory usage in functions
   - Upgrade to Pro plan for more memory

## Scaling & Production

### Free Tier Limits
- 100GB bandwidth/month
- 100 serverless function invocations/day
- 10 deployments/day

### Upgrade Benefits
- Unlimited bandwidth
- Unlimited function invocations
- Custom domains
- Team collaboration
- Advanced analytics

## Custom Domain

1. **Add domain in Vercel dashboard**:
   - Go to Settings → Domains
   - Add your domain: `api.yourdomain.com`

2. **Configure DNS**:
   - Add CNAME record pointing to `cname.vercel-dns.com`

3. **SSL Certificate**:
   - Automatically provisioned by Vercel
   - HTTPS enabled by default

## Comparison with Other Platforms

| Feature | Vercel | Railway | Fly.io |
|---------|--------|---------|--------|
| **Setup Time** | 2 minutes | 5 minutes | 10 minutes |
| **Cost (Free)** | 100GB/month | $5/month | $3/month |
| **Cold Starts** | Yes | No | No |
| **PyTorch Support** | Limited | Full | Full |
| **Persistent Storage** | No | Yes | Yes |
| **Global CDN** | Yes | No | Yes |

## Next Steps

1. **Test all endpoints** with your Vercel URL
2. **Set up monitoring** with Vercel Analytics
3. **Configure custom domain** for production
4. **Implement caching** for better performance
5. **Add authentication** for secure access

## Support

- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **FastAPI + Vercel**: [vercel.com/guides/deploying-fastapi-with-vercel](https://vercel.com/guides/deploying-fastapi-with-vercel)
- **Project Issues**: Check GitHub repository issues

---

**Deployment Status**: ✅ Ready for Vercel
**Estimated Deploy Time**: 2-3 minutes
**Live URL**: Available after deployment