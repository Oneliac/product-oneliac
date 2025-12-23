@echo off
REM Healthcare Agents - Vercel Deployment Script (Windows)
REM Copyright 2025 Raza Ahmad. Licensed under Apache 2.0.

echo 🏥 Healthcare Agents - Vercel Deployment
echo ========================================

REM Check if Vercel CLI is installed
where vercel >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Vercel CLI not found. Installing...
    npm install -g vercel
)

REM Check if we're in a git repository
if not exist ".git" (
    echo ⚠️  Not a git repository. Initializing...
    git init
    git add .
    git commit -m "Initial commit for Vercel deployment"
)

echo 🚀 Deploying to Vercel...
echo.

REM Deploy to production
vercel --prod

echo.
echo ✅ Deployment complete!
echo.
echo 📋 Next steps:
echo 1. Test your API endpoints
echo 2. Set up custom domain (optional)
echo 3. Configure monitoring
echo.
echo 📖 Full guide: VERCEL_DEPLOYMENT.md

pause