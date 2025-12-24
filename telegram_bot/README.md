# 🤖 Healthcare Telegram Bot

A Telegram bot interface for the Privacy-Preserving Healthcare Agents API.

## 🚀 Features

### For Patients
- **🏥 Eligibility Check**: Verify insurance coverage for procedures
- **💊 Prescription Validation**: Check drug safety and interactions
- **📊 System Status**: Monitor healthcare system health

### For Healthcare Workers
- **Quick Lookups**: Fast patient eligibility verification
- **Drug Safety**: Instant prescription validation
- **System Monitoring**: Real-time API status

## 🛠️ Setup

### 1. Create Telegram Bot

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot`
3. Choose a name: `Healthcare Agents Bot`
4. Choose a username: `your_healthcare_bot`
5. Copy the bot token

### 2. Install Dependencies

```bash
cd telegram_bot
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example config
cp .env.example .env

# Edit with your values
TELEGRAM_BOT_TOKEN=your_bot_token_here
API_BASE_URL=https://your-project.vercel.app
```

### 4. Run the Bot

```bash
python bot.py
```

## 📱 Bot Commands

### Basic Commands
- `/start` - Welcome message and main menu
- `/help` - Show all available commands
- `/health` - Check API system status

### Healthcare Commands
- `/eligibility <patient_id> <procedure>` - Check insurance eligibility
- `/prescription <patient_id> <drug_code>` - Validate prescription safety
- `/status` - Detailed system status

### Example Usage

```
/eligibility PATIENT_001 PROC001
/prescription PATIENT_001 DRUG001
```

## 🎯 Bot Interface

### Main Menu (Inline Buttons)
```
🏥 Check Eligibility    💊 Validate Prescription
📊 System Status        ❓ Help
📖 API Docs
```

### Sample Conversation

**User:** `/start`

**Bot:** 
```
🏥 Healthcare Agents Bot

Welcome to the privacy-preserving healthcare system!

I can help you with:
• 🔍 Eligibility Verification - Check insurance coverage
• 💊 Prescription Validation - Verify drug safety
• 🤖 Federated Learning - Contribute to AI training
• 📊 System Status - Check API health

All your data is encrypted and processed with zero-knowledge proofs! 🔐
```

**User:** `/eligibility PATIENT_001 PROC001`

**Bot:**
```
✅ Eligibility Confirmed

🔹 Patient: PATIENT_001
🔹 Procedure: PROC001
🔹 Status: Eligible ✅
🔹 Coverage: 85%
🔹 ZK Proof: a1b2c3d4e5f6...

The patient is eligible for this procedure! 🏥
```

## 🔐 Privacy Features

- **Zero-Knowledge Proofs**: Patient data privacy guaranteed
- **Encrypted Communication**: All API calls encrypted
- **No Data Storage**: Bot doesn't store sensitive information
- **HIPAA Compliant**: Meets healthcare privacy standards

## 🚀 Deployment Options

### Option 1: Local Development
```bash
python bot.py
```

### Option 2: Cloud Deployment (Heroku)
```bash
# Create Procfile
echo "worker: python bot.py" > Procfile

# Deploy to Heroku
heroku create your-healthcare-bot
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set API_BASE_URL=https://your-api.vercel.app
git push heroku main
```

### Option 3: Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

## 🔧 Advanced Features

### Custom Keyboards
- Inline buttons for quick actions
- Persistent menu for easy navigation
- Context-aware suggestions

### Error Handling
- Graceful API error handling
- User-friendly error messages
- Automatic retry mechanisms

### Logging
- Comprehensive logging for debugging
- User interaction tracking
- API response monitoring

## 📊 Usage Analytics

The bot can track:
- Most used commands
- API response times
- User engagement metrics
- Error rates

## 🛡️ Security Considerations

- **Token Security**: Keep bot token secret
- **Rate Limiting**: Implement to prevent abuse
- **Input Validation**: Sanitize all user inputs
- **Access Control**: Consider user authentication for sensitive operations

## 🔮 Future Enhancements

1. **Voice Messages**: Audio prescription validation
2. **Image Processing**: Scan prescription images
3. **Multi-language**: Support multiple languages
4. **Push Notifications**: Proactive health alerts
5. **Integration**: Connect with EHR systems

## 🆘 Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check bot token is correct
   - Verify API URL is accessible
   - Check internet connection

2. **API errors**
   - Verify Vercel deployment is working
   - Check API endpoint URLs
   - Review error logs

3. **Permission errors**
   - Ensure bot has message permissions
   - Check if bot is added to group (if applicable)

## 📞 Support

- **Bot Issues**: Check logs in `bot.py`
- **API Issues**: Check Vercel function logs
- **Telegram Issues**: Contact [@BotFather](https://t.me/botfather)

---

**Ready to use?** Just run `python bot.py` and start chatting with your healthcare bot! 🏥🤖