# Quick Start - Run the Service in 5 Minutes

## **Option 1: Local (No Docker)**

```bash
# 1. Install dependencies
pip install -r agents/requirements.txt

# 2. Start API server
python -m uvicorn agents.api:app --reload

# 3. Open browser
open http://localhost:8000/docs
```

**Done!** API is live with interactive documentation.

---

## **Option 2: Docker (Recommended)**

```bash
# 1. Build & run
docker-compose up

# 2. Open browser
open http://localhost:8000/docs
```

**Done!** Service is containerized and ready.

---

## **Option 3: Deploy to Cloud (Railway)**

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Deploy (from repo directory)
railway up

# 4. Get URL from Railway console
# https://your-app.up.railway.app
```

**Done!** Service is live on the internet.

---

## **Test the API**

### Health Check
```bash
curl http://localhost:8000/health
```

### Verify Eligibility
```bash
curl -X POST http://localhost:8000/verify-eligibility \
  -H "Content-Type: application/json" \
  -d '{
    "patient_data": {
      "patient_id": "PATIENT_001",
      "encrypted_data": "test_data",
      "ipfs_cid": "QmTest",
      "data_hash": "abc123"
    },
    "procedure_code": "PROC001"
  }'
```

### View API Docs
```
http://localhost:8000/docs       # Swagger UI
http://localhost:8000/redoc      # ReDoc
```

---

## **Python SDK Usage**

```python
from zk_healthcare import EligibilityAgent, PatientData
import asyncio

async def main():
    agent = EligibilityAgent("https://api.devnet.solana.com")
    
    patient = PatientData(
        patient_id="PATIENT_001",
        encrypted_data=b"encrypted",
        ipfs_cid="QmTest",
        data_hash="hash"
    )
    
    result = await agent.check_insurance_coverage(patient, "PROC001")
    print(f"Eligible: {result['eligible']}")
    print(f"Coverage: {result['coverage_pct']}%")

asyncio.run(main())
```

---

## **Next Steps**

1. **For Development**:
   - Read `SDK_GUIDE.md` for integration examples
   - Check `agents/api.py` for endpoint details
   - Run tests: `pytest tests/ -v`

2. **For Deployment**:
   - See `DEPLOYMENT.md` for production setup
   - Configure environment variables
   - Set up monitoring & logging

3. **For Contributions**:
   - See `CONTRIBUTING.md` for guidelines
   - Check GitHub issues for tasks
   - Submit PRs with tests

---

## **Troubleshooting**

### Port Already in Use
```bash
# Use different port
python -m uvicorn agents.api:app --port 8001
```

### Dependencies Missing
```bash
# Reinstall
pip install --upgrade -r agents/requirements.txt
```

### Docker Issues
```bash
# Clean start
docker-compose down
docker-compose up --build
```

---

## **API Endpoints Summary**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health check |
| GET | `/docs` | Interactive API docs |
| GET | `/status` | System status |
| POST | `/verify-eligibility` | Check insurance coverage |
| POST | `/validate-prescription` | Validate drug prescription |
| POST | `/submit-federated-update` | Submit FL training data |

---

**You're ready!** Start coding. 🚀

For questions → Check docs in `/docs` endpoint or read `SDK_GUIDE.md`
