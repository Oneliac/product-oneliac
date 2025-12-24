# Copyright 2025 Raza Ahmad. Licensed under Apache 2.0.

"""
Simple deployment script for Healthcare Telegram Bot
"""

import os
import subprocess
import sys

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check if bot token is set
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or token == "YOUR_BOT_TOKEN_HERE":
        print("❌ TELEGRAM_BOT_TOKEN not set!")
        print("1. Message @BotFather on Telegram")
        print("2. Create a new bot with /newbot")
        print("3. Copy the token and set it in .env file")
        return False
    
    # Check if API URL is set
    api_url = os.getenv("API_BASE_URL")
    if not api_url or "your-project" in api_url:
        print("❌ API_BASE_URL not set!")
        print("1. Deploy your FastAPI to Vercel first")
        print("2. Copy the URL and set it in .env file")
        return False
    
    print("✅ Requirements check passed!")
    return True

def install_dependencies():
    """Install required packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies!")
        return False

def test_bot():
    """Test bot configuration"""
    print("🧪 Testing bot configuration...")
    try:
        from bot import HealthcareBot
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        api_url = os.getenv("API_BASE_URL")
        
        # Just create the bot instance to test imports
        bot = HealthcareBot(token, api_url)
        print("✅ Bot configuration test passed!")
        return True
    except Exception as e:
        print(f"❌ Bot test failed: {e}")
        return False

def main():
    """Main deployment function"""
    print("🤖 Healthcare Telegram Bot Deployment")
    print("=" * 40)
    
    # Load environment variables
    if os.path.exists(".env"):
        from dotenv import load_dotenv
        load_dotenv()
    
    # Run checks
    if not check_requirements():
        return False
    
    if not install_dependencies():
        return False
    
    if not test_bot():
        return False
    
    print("\n🚀 Bot is ready to deploy!")
    print("\nTo start the bot:")
    print("  python bot.py")
    print("\nTo deploy to cloud:")
    print("  1. Heroku: Create Procfile with 'worker: python bot.py'")
    print("  2. Railway: Connect GitHub repo and set env vars")
    print("  3. VPS: Run 'nohup python bot.py &' for background")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)