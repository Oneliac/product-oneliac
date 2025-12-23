#!/bin/bash

# Healthcare Agents - Vercel Deployment Script
# Copyright 2025 Raza Ahmad. Licensed under Apache 2.0.

echo "🏥 Healthcare Agents - Vercel Deployment"
echo "========================================"

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "⚠️  Not a git repository. Initializing..."
    git init
    git add .
    git commit -m "Initial commit for Vercel deployment"
fi

echo "🚀 Deploying to Vercel..."
echo ""

# Deploy to production
vercel --prod

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Test your API endpoints"
echo "2. Set up custom domain (optional)"
echo "3. Configure monitoring"
echo ""
echo "📖 Full guide: VERCEL_DEPLOYMENT.md"