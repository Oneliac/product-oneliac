#!/usr/bin/env python3
# Copyright 2025 Raza Ahmad. Licensed under Apache 2.0.

"""
Production-ready Telegram bot runner with auto-restart and monitoring
"""

import os
import sys
import time
import logging
import subprocess
import signal
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class BotRunner:
    def __init__(self):
        self.process = None
        self.running = True
        self.restart_count = 0
        self.max_restarts = 10
        self.restart_delay = 5
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False
        if self.process:
            self.process.terminate()
    
    def check_environment(self):
        """Check if required environment variables are set"""
        required_vars = ['TELEGRAM_BOT_TOKEN', 'API_BASE_URL']
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
            logger.error("Please set them in .env file or environment")
            return False
        
        return True
    
    def start_bot(self):
        """Start the bot process"""
        try:
            logger.info("Starting Telegram bot...")
            self.process = subprocess.Popen(
                [sys.executable, 'bot.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            return True
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            return False
    
    def monitor_bot(self):
        """Monitor bot process and handle output"""
        if not self.process:
            return False
        
        try:
            # Read output line by line
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    print(line.strip())
                
                # Check if process is still running
                if self.process.poll() is not None:
                    break
            
            # Wait for process to complete
            return_code = self.process.wait()
            logger.info(f"Bot process exited with code: {return_code}")
            
            return return_code == 0
            
        except Exception as e:
            logger.error(f"Error monitoring bot: {e}")
            return False
    
    def run(self):
        """Main run loop with auto-restart"""
        if not self.check_environment():
            sys.exit(1)
        
        logger.info("Starting bot runner...")
        
        while self.running and self.restart_count < self.max_restarts:
            if self.start_bot():
                success = self.monitor_bot()
                
                if not success and self.running:
                    self.restart_count += 1
                    logger.warning(f"Bot crashed. Restart attempt {self.restart_count}/{self.max_restarts}")
                    
                    if self.restart_count < self.max_restarts:
                        logger.info(f"Restarting in {self.restart_delay} seconds...")
                        time.sleep(self.restart_delay)
                        
                        # Increase delay for subsequent restarts
                        self.restart_delay = min(self.restart_delay * 1.5, 60)
                    else:
                        logger.error("Max restart attempts reached. Stopping.")
                        break
                else:
                    # Successful exit or manual stop
                    break
            else:
                logger.error("Failed to start bot process")
                break
        
        logger.info("Bot runner stopped")

if __name__ == "__main__":
    # Load environment variables from .env file if it exists
    env_file = Path('.env')
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv()
    
    runner = BotRunner()
    runner.run()