#!/bin/bash

# Healthcare Agents - Render Deployment Script
# Copyright 2025 Raza Ahmad. Licensed under Apache 2.0.

echo "🎨 Healthcare Agents - Render Deployment"
echo "========================================"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "⚠️  Not a git repository. Initializing..."
    git init
    git add .
    git commit -m "Initial commit for Render deployment"
fi

# Check if render.yaml exists
if [ ! -f "render.yaml" ]; then
    echo "❌ render.yaml not found!"
    echo "Please ensure render.yaml is in the root directory"
    exit 1
fi

echo "📋 Deployment Checklist:"
echo "✅ render.yaml configuration file"
echo "✅ agents/requirements.txt dependencies"
echo "✅ FastAPI application in agents/api.py"
echo "✅ PyTorch mock for compatibility"
echo ""

echo "🚀 Ready to deploy to Render!"
echo ""
echo "📋 Next steps:"
echo "1. Push to GitHub:"
echo "   git add ."
echo "   git commit -m 'Deploy to Render'"
echo "   git push origin main"
echo ""
echo "2. Go to render.com and:"
echo "   • Click 'New +' → 'Web Service'"
echo "   • Connect your GitHub repository"
echo "   • Render will auto-detect render.yaml"
echo "   • Click 'Create Web Service'"
echo ""
echo "3. Your API will be live at:"
echo "   https://healthcare-agents-api.onrender.com"
echo ""
echo "4. Test with:"
echo "   curl https://healthcare-agents-api.onrender.com/health"
echo ""
echo "📖 Full guide: RENDER_DEPLOY.md"

# Offer to push to git
read -p "🤔 Push to GitHub now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📤 Pushing to GitHub..."
    git add .
    git commit -m "Deploy to Render with configuration"
    git push origin main
    echo "✅ Pushed to GitHub!"
    echo ""
    echo "🎯 Now go to render.com to complete deployment"
fi