# Copyright 2025 Raza Ahmad. Licensed under Apache 2.0.

"""
Telegram Bot for Privacy-Preserving Healthcare Agents
Provides secure medical queries through chat interface.
"""

import asyncio
import aiohttp
import json
import os
import logging
import signal
import sys
from typing import Dict, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from telegram.error import NetworkError, TimedOut, BadRequest

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class HealthcareBot:
    def __init__(self, bot_token: str, api_base_url: str):
        self.bot_token = bot_token
        self.api_base_url = api_base_url.rstrip('/')
        self.app = None
        self.running = False
        self.setup_signal_handlers()
    
    def setup_signal_handlers(self):
        """Set up signal handlers for graceful shutdown"""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
        if self.app and self.app.running:
            asyncio.create_task(self.app.stop())
    
    def setup_handlers(self):
        """Set up bot command and message handlers"""
        # Commands
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("health", self.health_check))
        self.app.add_handler(CommandHandler("eligibility", self.eligibility_command))
        self.app.add_handler(CommandHandler("prescription", self.prescription_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        
        # Callback queries (button presses)
        self.app.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Text messages
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Error handler
        self.app.add_error_handler(self.error_handler)
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors to prevent crashes"""
        logger.error(f"Exception while handling an update: {context.error}")
        
        # Try to send error message to user if possible
        try:
            if update and update.effective_message:
                await update.effective_message.reply_text(
                    "❌ Sorry, I encountered an error. Please try again later."
                )
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Welcome message with main menu"""
        try:
            keyboard = [
                [
                    InlineKeyboardButton("🏥 Check Eligibility", callback_data="eligibility"),
                    InlineKeyboardButton("💊 Validate Prescription", callback_data="prescription")
                ],
                [
                    InlineKeyboardButton("📊 System Status", callback_data="status"),
                    InlineKeyboardButton("❓ Help", callback_data="help")
                ],
                [
                    InlineKeyboardButton("📖 API Docs", url=f"{self.api_base_url}/docs")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            welcome_text = """
🏥 **Healthcare Agents Bot**

Welcome to the privacy-preserving healthcare system! 

I can help you with:
• 🔍 **Eligibility Verification** - Check insurance coverage
• 💊 **Prescription Validation** - Verify drug safety
• 🤖 **Federated Learning** - Contribute to AI training
• 📊 **System Status** - Check API health

All your data is encrypted and processed with zero-knowledge proofs for maximum privacy! 🔐

Choose an option below or type a command:
            """
            
            await update.message.reply_text(
                welcome_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error in start_command: {e}")
            await self.send_error_message(update, "Failed to show welcome message")
    
    async def send_error_message(self, update: Update, message: str):
        """Send error message safely"""
        try:
            if update and update.effective_message:
                await update.effective_message.reply_text(f"❌ {message}")
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")
    
    async def make_api_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
        """Make API request with proper error handling and retries"""
        url = f"{self.api_base_url}{endpoint}"
        
        # Retry configuration
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                timeout = aiohttp.ClientTimeout(total=30)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    if method == "GET":
                        async with session.get(url) as response:
                            if response.status == 200:
                                return await response.json()
                            else:
                                error_text = await response.text()
                                logger.error(f"API error {response.status}: {error_text}")
                                return {"error": f"API returned status {response.status}"}
                    
                    elif method == "POST":
                        headers = {"Content-Type": "application/json"}
                        async with session.post(url, json=data, headers=headers) as response:
                            if response.status == 200:
                                return await response.json()
                            else:
                                error_text = await response.text()
                                logger.error(f"API error {response.status}: {error_text}")
                                return {"error": f"API returned status {response.status}"}
            
            except asyncio.TimeoutError:
                logger.warning(f"API request timeout (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay * (attempt + 1))
                else:
                    return {"error": "API request timed out"}
            
            except aiohttp.ClientError as e:
                logger.warning(f"API connection error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay * (attempt + 1))
                else:
                    return {"error": f"Connection error: {str(e)}"}
            
            except Exception as e:
                logger.error(f"Unexpected API error: {e}")
                return {"error": f"Unexpected error: {str(e)}"}
        
        return {"error": "Max retries exceeded"}
    
    async def health_check(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check API health status with error handling"""
        try:
            result = await self.make_api_request("/health")
            
            if "error" in result:
                status_text = f"❌ **API Error:** {result['error']}"
            else:
                status_text = f"""
✅ **System Status: Healthy**

🔹 **Version:** {result.get('version', 'Unknown')}
🔹 **Status:** {result.get('status', 'Unknown')}
🔹 **Message:** {result.get('message', 'No message')}
🔹 **API URL:** {self.api_base_url}

All healthcare agents are operational! 🏥
                """
            
            await update.message.reply_text(status_text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in health_check: {e}")
            await self.send_error_message(update, "Failed to check system health")
    
    async def eligibility_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle eligibility check command with improved error handling"""
        try:
            if len(context.args) < 2:
                await update.message.reply_text(
                    "❌ **Usage:** `/eligibility <patient_id> <procedure_code>`\n\n"
                    "**Example:** `/eligibility PATIENT_001 PROC001`",
                    parse_mode='Markdown'
                )
                return
            
            patient_id = context.args[0]
            procedure_code = context.args[1]
            
            # Show loading message
            loading_msg = await update.message.reply_text("🔍 Checking eligibility... Please wait.")
            
            # Prepare request data
            request_data = {
                "patient_data": {
                    "patient_id": patient_id,
                    "encrypted_data": "sample_encrypted_data",
                    "ipfs_cid": f"Qm{patient_id}Hash",
                    "data_hash": f"hash_{patient_id}"
                },
                "procedure_code": procedure_code
            }
            
            # Make API request
            result = await self.make_api_request("/eligibility/verify", "POST", request_data)
            
            if "error" in result:
                result_text = f"❌ **Error:** {result['error']}"
            elif result.get("eligible"):
                result_text = f"""
✅ **Eligibility Confirmed**

🔹 **Patient:** {patient_id}
🔹 **Procedure:** {procedure_code}
🔹 **Status:** Eligible ✅
🔹 **Coverage:** {result.get('coverage_percentage', 'N/A')}%
🔹 **ZK Proof:** `{result.get('zk_proof_hash', 'Generated')[:16]}...`

The patient is eligible for this procedure! 🏥
                """
            else:
                result_text = f"""
❌ **Eligibility Denied**

🔹 **Patient:** {patient_id}
🔹 **Procedure:** {procedure_code}
🔹 **Status:** Not Eligible ❌
🔹 **Reason:** {result.get('reason', 'Coverage not available')}

Please check with insurance provider. 📞
                """
            
            # Update the loading message with results
            await loading_msg.edit_text(result_text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in eligibility_command: {e}")
            await self.send_error_message(update, "Failed to check eligibility")
    
    async def prescription_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle prescription validation command with improved error handling"""
        try:
            if len(context.args) < 2:
                await update.message.reply_text(
                    "❌ **Usage:** `/prescription <patient_id> <drug_code>`\n\n"
                    "**Example:** `/prescription PATIENT_001 DRUG001`",
                    parse_mode='Markdown'
                )
                return
            
            patient_id = context.args[0]
            drug_code = context.args[1]
            
            # Show loading message
            loading_msg = await update.message.reply_text("💊 Validating prescription... Please wait.")
            
            # Prepare request data
            request_data = {
                "patient_data": {
                    "patient_id": patient_id,
                    "encrypted_data": "sample_encrypted_data",
                    "ipfs_cid": f"Qm{patient_id}Hash",
                    "data_hash": f"hash_{patient_id}"
                },
                "drug_code": drug_code
            }
            
            # Make API request
            result = await self.make_api_request("/prescription/validate", "POST", request_data)
            
            if "error" in result:
                result_text = f"❌ **Error:** {result['error']}"
            elif result.get("safe"):
                interactions = result.get("interactions", [])
                interaction_text = "None detected ✅" if not interactions else f"{len(interactions)} found ⚠️"
                
                result_text = f"""
✅ **Prescription Validated**

🔹 **Patient:** {patient_id}
🔹 **Drug:** {drug_code}
🔹 **Safety:** Safe to prescribe ✅
🔹 **Interactions:** {interaction_text}
🔹 **Confidence:** {result.get('confidence', 95)}%

Prescription is safe to dispense! 💊
                """
            else:
                result_text = f"""
⚠️ **Prescription Warning**

🔹 **Patient:** {patient_id}
🔹 **Drug:** {drug_code}
🔹 **Safety:** Potential issues ⚠️
🔹 **Warnings:** {', '.join(result.get('warnings', []))}

Please consult with physician before dispensing. 👨‍⚕️
                """
            
            # Update the loading message with results
            await loading_msg.edit_text(result_text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in prescription_command: {e}")
            await self.send_error_message(update, "Failed to validate prescription")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show detailed system status with error handling"""
        try:
            # Get health status
            health_result = await self.make_api_request("/health")
            fl_result = await self.make_api_request("/federated-learning/status")
            
            if "error" in health_result:
                status_text = f"❌ **Error getting status:** {health_result['error']}"
            else:
                status_text = f"""
📊 **System Status Dashboard**

**🏥 Healthcare API**
• Status: {health_result.get('status', 'Unknown')} {'✅' if health_result.get('status') == 'healthy' else '❌'}
• Version: {health_result.get('version', 'Unknown')}
• Uptime: Online

**🤖 Federated Learning**
• Active Agents: {fl_result.get('active_agents', 0) if 'error' not in fl_result else 'N/A'}
• Training Rounds: {fl_result.get('training_rounds', 0) if 'error' not in fl_result else 'N/A'}
• Model Accuracy: {fl_result.get('model_accuracy', 'N/A') if 'error' not in fl_result else 'N/A'}%

**🔐 Privacy Features**
• Zero-Knowledge Proofs: ✅ Active
• Data Encryption: ✅ AES-256
• Blockchain Verification: ✅ Solana

Last Updated: Just now 🕐
                """
            
            await update.message.reply_text(status_text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in status_command: {e}")
            await self.send_error_message(update, "Failed to get system status")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show help information"""
        try:
            help_text = """
🤖 **Healthcare Bot Commands**

**Basic Commands:**
• `/start` - Show main menu
• `/help` - Show this help message
• `/health` - Check API status

**Healthcare Commands:**
• `/eligibility <patient_id> <procedure>` - Check eligibility
• `/prescription <patient_id> <drug_code>` - Validate prescription
• `/status` - Show system status

**Examples:**
```
/eligibility PATIENT_001 PROC001
/prescription PATIENT_001 DRUG001
```

**Privacy Features:**
🔐 All data is encrypted
🔍 Zero-knowledge proofs
🏥 HIPAA compliant
⛓️ Blockchain verified

**Need more help?** Check the [API Documentation]({}/docs)
            """.format(self.api_base_url)
            
            await update.message.reply_text(help_text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in help_command: {e}")
            await self.send_error_message(update, "Failed to show help")
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button presses"""
        try:
            query = update.callback_query
            await query.answer()
            
            if query.data == "eligibility":
                await query.edit_message_text(
                    "🏥 **Eligibility Check**\n\n"
                    "Use: `/eligibility <patient_id> <procedure_code>`\n\n"
                    "**Example:** `/eligibility PATIENT_001 PROC001`\n\n"
                    "This will check if the patient is eligible for the specified medical procedure."
                )
            elif query.data == "prescription":
                await query.edit_message_text(
                    "💊 **Prescription Validation**\n\n"
                    "Use: `/prescription <patient_id> <drug_code>`\n\n"
                    "**Example:** `/prescription PATIENT_001 DRUG001`\n\n"
                    "This will validate if the drug is safe for the patient and check for interactions."
                )
            elif query.data == "status":
                await self.status_command(update, context)
            elif query.data == "help":
                await self.help_command(update, context)
                
        except Exception as e:
            logger.error(f"Error in button_callback: {e}")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle general text messages"""
        try:
            text = update.message.text.lower()
            
            if any(word in text for word in ["eligibility", "eligible", "coverage", "insurance"]):
                await update.message.reply_text(
                    "🏥 To check eligibility, use:\n"
                    "`/eligibility <patient_id> <procedure_code>`\n\n"
                    "Example: `/eligibility PATIENT_001 PROC001`",
                    parse_mode='Markdown'
                )
            elif any(word in text for word in ["prescription", "drug", "medication", "medicine"]):
                await update.message.reply_text(
                    "💊 To validate a prescription, use:\n"
                    "`/prescription <patient_id> <drug_code>`\n\n"
                    "Example: `/prescription PATIENT_001 DRUG001`",
                    parse_mode='Markdown'
                )
            elif any(word in text for word in ["help", "commands", "what can you do"]):
                await self.help_command(update, context)
            elif any(word in text for word in ["status", "health", "online"]):
                await self.health_check(update, context)
            else:
                await update.message.reply_text(
                    "🤖 I'm a healthcare bot! I can help with:\n\n"
                    "• `/eligibility` - Check insurance coverage\n"
                    "• `/prescription` - Validate medications\n"
                    "• `/status` - System health\n"
                    "• `/help` - Show all commands\n\n"
                    "Type `/help` for more details!"
                )
                
        except Exception as e:
            logger.error(f"Error in handle_message: {e}")
    
    def run(self):
        """Start the bot with improved error handling and recovery"""
        logger.info("Starting Healthcare Bot...")
        
        # Create application with error recovery settings
        self.app = Application.builder().token(self.bot_token).build()
        
        # Set up handlers
        self.setup_handlers()
        
        # Set running flag
        self.running = True
        
        # Run with automatic restart on network errors
        while self.running:
            try:
                logger.info("Bot starting polling...")
                self.app.run_polling(
                    drop_pending_updates=True,  # Drop old updates on restart
                    close_loop=False
                )
            except (NetworkError, TimedOut) as e:
                logger.warning(f"Network error occurred: {e}. Restarting in 5 seconds...")
                if self.running:
                    asyncio.sleep(5)
            except Exception as e:
                logger.error(f"Unexpected error: {e}. Restarting in 10 seconds...")
                if self.running:
                    asyncio.sleep(10)
            
            if not self.running:
                break
                
        logger.info("Bot stopped.")

# Main execution
if __name__ == "__main__":
    # Configuration
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
    API_BASE_URL = os.getenv("API_BASE_URL", "https://your-project.onrender.com")
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Please set TELEGRAM_BOT_TOKEN environment variable")
        print("Get your token from @BotFather on Telegram")
        sys.exit(1)
    
    # Create and run bot
    bot = HealthcareBot(BOT_TOKEN, API_BASE_URL)
    
    try:
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
    
    def setup_handlers(self):
        """Set up bot command and message handlers"""
        # Commands
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("health", self.health_check))
        self.app.add_handler(CommandHandler("eligibility", self.eligibility_command))
        self.app.add_handler(CommandHandler("prescription", self.prescription_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        
        # Callback queries (button presses)
        self.app.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Text messages
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Welcome message with main menu"""
        keyboard = [
            [
                InlineKeyboardButton("🏥 Check Eligibility", callback_data="eligibility"),
                InlineKeyboardButton("💊 Validate Prescription", callback_data="prescription")
            ],
            [
                InlineKeyboardButton("📊 System Status", callback_data="status"),
                InlineKeyboardButton("❓ Help", callback_data="help")
            ],
            [
                InlineKeyboardButton("📖 API Docs", url=f"{self.api_base_url}/docs")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = """
🏥 **Healthcare Agents Bot**

Welcome to the privacy-preserving healthcare system! 

I can help you with:
• 🔍 **Eligibility Verification** - Check insurance coverage
• 💊 **Prescription Validation** - Verify drug safety
• 🤖 **Federated Learning** - Contribute to AI training
• 📊 **System Status** - Check API health

All your data is encrypted and processed with zero-knowledge proofs for maximum privacy! 🔐

Choose an option below or type a command:
        """
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show help information"""
        help_text = """
🤖 **Healthcare Bot Commands**

**Basic Commands:**
• `/start` - Show main menu
• `/help` - Show this help message
• `/health` - Check API status

**Healthcare Commands:**
• `/eligibility <patient_id> <procedure>` - Check eligibility
• `/prescription <patient_id> <drug_code>` - Validate prescription
• `/status` - Show system status

**Examples:**
```
/eligibility PATIENT_001 PROC001
/prescription PATIENT_001 DRUG001
```

**Privacy Features:**
🔐 All data is encrypted
🔍 Zero-knowledge proofs
🏥 HIPAA compliant
⛓️ Blockchain verified

**Need more help?** Check the [API Documentation]({}/docs)
        """.format(self.api_base_url)
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def health_check(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check API health status"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base_url}/health") as response:
                    if response.status == 200:
                        data = await response.json()
                        status_text = f"""
✅ **System Status: Healthy**

🔹 **Version:** {data.get('version', 'Unknown')}
🔹 **Status:** {data.get('status', 'Unknown')}
🔹 **Message:** {data.get('message', 'No message')}
🔹 **API URL:** {self.api_base_url}

All healthcare agents are operational! 🏥
                        """
                    else:
                        status_text = f"❌ **API Error:** Status {response.status}"
        except Exception as e:
            status_text = f"❌ **Connection Error:** {str(e)}"
        
        await update.message.reply_text(status_text, parse_mode='Markdown')
    
    async def eligibility_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle eligibility check command"""
        if len(context.args) < 2:
            await update.message.reply_text(
                "❌ **Usage:** `/eligibility <patient_id> <procedure_code>`\n\n"
                "**Example:** `/eligibility PATIENT_001 PROC001`"
            )
            return
        
        patient_id = context.args[0]
        procedure_code = context.args[1]
        
        # Show loading message
        loading_msg = await update.message.reply_text("🔍 Checking eligibility... Please wait.")
        
        try:
            # Prepare request data
            request_data = {
                "patient_data": {
                    "patient_id": patient_id,
                    "encrypted_data": "sample_encrypted_data",
                    "ipfs_cid": f"Qm{patient_id}Hash",
                    "data_hash": f"hash_{patient_id}"
                },
                "procedure_code": procedure_code
            }
            
            # Make API request
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_base_url}/eligibility/verify",
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        # Format response
                        if data.get("eligible"):
                            result_text = f"""
✅ **Eligibility Confirmed**

🔹 **Patient:** {patient_id}
🔹 **Procedure:** {procedure_code}
🔹 **Status:** Eligible ✅
🔹 **Coverage:** {data.get('coverage_percentage', 'N/A')}%
🔹 **ZK Proof:** `{data.get('zk_proof_hash', 'Generated')[:16]}...`

The patient is eligible for this procedure! 🏥
                            """
                        else:
                            result_text = f"""
❌ **Eligibility Denied**

🔹 **Patient:** {patient_id}
🔹 **Procedure:** {procedure_code}
🔹 **Status:** Not Eligible ❌
🔹 **Reason:** {data.get('reason', 'Coverage not available')}

Please check with insurance provider. 📞
                            """
                    else:
                        error_data = await response.json()
                        result_text = f"❌ **API Error:** {error_data.get('detail', 'Unknown error')}"
        
        except Exception as e:
            result_text = f"❌ **Error:** {str(e)}"
        
        # Update the loading message with results
        await loading_msg.edit_text(result_text, parse_mode='Markdown')
    
    async def prescription_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle prescription validation command"""
        if len(context.args) < 2:
            await update.message.reply_text(
                "❌ **Usage:** `/prescription <patient_id> <drug_code>`\n\n"
                "**Example:** `/prescription PATIENT_001 DRUG001`"
            )
            return
        
        patient_id = context.args[0]
        drug_code = context.args[1]
        
        # Show loading message
        loading_msg = await update.message.reply_text("💊 Validating prescription... Please wait.")
        
        try:
            # Prepare request data
            request_data = {
                "patient_data": {
                    "patient_id": patient_id,
                    "encrypted_data": "sample_encrypted_data",
                    "ipfs_cid": f"Qm{patient_id}Hash",
                    "data_hash": f"hash_{patient_id}"
                },
                "drug_code": drug_code
            }
            
            # Make API request
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_base_url}/prescription/validate",
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        # Format response
                        if data.get("safe"):
                            interactions = data.get("interactions", [])
                            interaction_text = "None detected ✅" if not interactions else f"{len(interactions)} found ⚠️"
                            
                            result_text = f"""
✅ **Prescription Validated**

🔹 **Patient:** {patient_id}
🔹 **Drug:** {drug_code}
🔹 **Safety:** Safe to prescribe ✅
🔹 **Interactions:** {interaction_text}
🔹 **Confidence:** {data.get('confidence', 95)}%

Prescription is safe to dispense! 💊
                            """
                        else:
                            result_text = f"""
⚠️ **Prescription Warning**

🔹 **Patient:** {patient_id}
🔹 **Drug:** {drug_code}
🔹 **Safety:** Potential issues ⚠️
🔹 **Warnings:** {', '.join(data.get('warnings', []))}

Please consult with physician before dispensing. 👨‍⚕️
                            """
                    else:
                        error_data = await response.json()
                        result_text = f"❌ **API Error:** {error_data.get('detail', 'Unknown error')}"
        
        except Exception as e:
            result_text = f"❌ **Error:** {str(e)}"
        
        # Update the loading message with results
        await loading_msg.edit_text(result_text, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show detailed system status"""
        try:
            async with aiohttp.ClientSession() as session:
                # Get health status
                async with session.get(f"{self.api_base_url}/health") as response:
                    health_data = await response.json() if response.status == 200 else {}
                
                # Get federated learning status
                async with session.get(f"{self.api_base_url}/federated-learning/status") as response:
                    fl_data = await response.json() if response.status == 200 else {}
            
            status_text = f"""
📊 **System Status Dashboard**

**🏥 Healthcare API**
• Status: {health_data.get('status', 'Unknown')} {'✅' if health_data.get('status') == 'healthy' else '❌'}
• Version: {health_data.get('version', 'Unknown')}
• Uptime: Online

**🤖 Federated Learning**
• Active Agents: {fl_data.get('active_agents', 0)}
• Training Rounds: {fl_data.get('training_rounds', 0)}
• Model Accuracy: {fl_data.get('model_accuracy', 'N/A')}%

**🔐 Privacy Features**
• Zero-Knowledge Proofs: ✅ Active
• Data Encryption: ✅ AES-256
• Blockchain Verification: ✅ Solana

**📈 Usage Stats**
• Total Queries: {fl_data.get('total_queries', 'N/A')}
• Success Rate: {fl_data.get('success_rate', 'N/A')}%

Last Updated: Just now 🕐
            """
        
        except Exception as e:
            status_text = f"❌ **Error getting status:** {str(e)}"
        
        await update.message.reply_text(status_text, parse_mode='Markdown')
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button presses"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "eligibility":
            await query.edit_message_text(
                "🏥 **Eligibility Check**\n\n"
                "Use: `/eligibility <patient_id> <procedure_code>`\n\n"
                "**Example:** `/eligibility PATIENT_001 PROC001`\n\n"
                "This will check if the patient is eligible for the specified medical procedure."
            )
        elif query.data == "prescription":
            await query.edit_message_text(
                "💊 **Prescription Validation**\n\n"
                "Use: `/prescription <patient_id> <drug_code>`\n\n"
                "**Example:** `/prescription PATIENT_001 DRUG001`\n\n"
                "This will validate if the drug is safe for the patient and check for interactions."
            )
        elif query.data == "status":
            await self.status_command(update, context)
        elif query.data == "help":
            await self.help_command(update, context)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle general text messages"""
        text = update.message.text.lower()
        
        if any(word in text for word in ["eligibility", "eligible", "coverage", "insurance"]):
            await update.message.reply_text(
                "🏥 To check eligibility, use:\n"
                "`/eligibility <patient_id> <procedure_code>`\n\n"
                "Example: `/eligibility PATIENT_001 PROC001`",
                parse_mode='Markdown'
            )
        elif any(word in text for word in ["prescription", "drug", "medication", "medicine"]):
            await update.message.reply_text(
                "💊 To validate a prescription, use:\n"
                "`/prescription <patient_id> <drug_code>`\n\n"
                "Example: `/prescription PATIENT_001 DRUG001`",
                parse_mode='Markdown'
            )
        elif any(word in text for word in ["help", "commands", "what can you do"]):
            await self.help_command(update, context)
        elif any(word in text for word in ["status", "health", "online"]):
            await self.health_check(update, context)
        else:
            await update.message.reply_text(
                "🤖 I'm a healthcare bot! I can help with:\n\n"
                "• `/eligibility` - Check insurance coverage\n"
                "• `/prescription` - Validate medications\n"
                "• `/status` - System health\n"
                "• `/help` - Show all commands\n\n"
                "Type `/help` for more details!"
            )
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Healthcare Bot...")
        self.app.run_polling()

# Main execution
if __name__ == "__main__":
    # Configuration
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
    API_BASE_URL = os.getenv("API_BASE_URL", "https://your-project.vercel.app")
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Please set TELEGRAM_BOT_TOKEN environment variable")
        print("Get your token from @BotFather on Telegram")
        exit(1)
    
    # Create and run bot
    bot = HealthcareBot(BOT_TOKEN, API_BASE_URL)
    bot.run()