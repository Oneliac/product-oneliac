# Deployment Guide - Privacy-Preserving Healthcare Agents

This guide covers deploying the zk-healthcare system for developers and services.

---

## **Table of Contents**
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Smart Contract Deployment](#smart-contract-deployment)
5. [SDK Distribution](#sdk-distribution)

---

## **Local Development**

### Prerequisites
- Python 3.9+
- Rust 1.70+ (for Solana contracts)
- Solana CLI
- Node.js (for Circom/snarkjs, optional for dev)

### Setup

```bash
# Clone repository
git clone https://github.com/razaahmad9222/zk-healthcare-agents-solana.git
cd zk-healthcare-agents-solana

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r agents/requirements.txt

# Run tests
pytest tests/ -v

# Start API server locally
python -m uvicorn agents.api:app --reload
```

API will be available at `http://localhost:8000`
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## **Docker Deployment**

### Build & Run Locally

```bash
# Build image
docker build -t zk-healthcare-api:latest .

# Run container
docker run -p 8000:8000 \
  -e SOLANA_ENDPOINT=https://api.devnet.solana.com \
  zk-healthcare-api:latest

# Or use docker-compose
docker-compose up -d
```

### Push to Registry

```bash
# Tag image
docker tag zk-healthcare-api:latest your-registry/zk-healthcare-api:latest

# Push
docker push your-registry/zk-healthcare-api:latest
```

---

## **Cloud Deployment**

### Option 1: Railway (Recommended for MVP)

1. **Create account**: https://railway.app
2. **Connect GitHub repo**
3. **Add environment variables**:
   ```
   SOLANA_NETWORK=devnet
   SOLANA_ENDPOINT=https://api.devnet.solana.com
   ```
4. **Deploy**:
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login
   railway login
   
   # Deploy
   railway up
   ```

**Cost**: ~$5/month for starter tier
**URL**: Auto-generated, e.g., https://zk-healthcare-api-prod.up.railway.app

### Option 2: Fly.io

```bash
# Install Fly CLI
curl https://fly.io/install.sh | sh

# Login
flyctl auth login

# Launch app
flyctl launch

# Deploy
flyctl deploy
```

**Cost**: ~$3/month (free tier available)

### Option 3: AWS Lambda (Serverless)

```bash
# Install Zappa
pip install zappa

# Initialize
zappa init

# Deploy
zappa deploy production

# Update
zappa update production
```

**Cost**: Pay-per-request (~$0.0000002 per invocation)

### Option 4: DigitalOcean App Platform

1. Connect GitHub repo in DigitalOcean console
2. Select `Dockerfile` as build type
3. Configure environment variables
4. Deploy

**Cost**: ~$5-12/month

---

## **Smart Contract Deployment**

### Build

```bash
cd programs/zk_healthcare

# Install Rust (if needed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Build contract
cargo build

# Or use Anchor
anchor build
```

### Deploy to Devnet

```bash
# Set RPC endpoint
solana config set --url https://api.devnet.solana.com

# Airdrop SOL (if needed)
solana airdrop 2 --url devnet

# Deploy
anchor deploy --provider.cluster devnet
```

Output will show:
```
Program deployed to: <PROGRAM_ID>
```

### Deploy to Mainnet-Beta (Production)

```bash
# ⚠️ Requires real SOL
solana config set --url https://api.mainnet-beta.solana.com

# Build with optimizations
cargo build --release

# Deploy (costs ~0.5 SOL ≈ $5-20)
anchor deploy --provider.cluster mainnet
```

---

## **SDK Distribution**

### Python Package (PyPI)

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Upload to PyPI
twine upload dist/*
```

Then users can install:
```bash
pip install zk-healthcare
```

### TypeScript/JavaScript Package (NPM)

Create `packages/js-client/package.json`:
```json
{
  "name": "@zk-healthcare/solana-client",
  "version": "0.1.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "dependencies": {
    "@solana/web3.js": "^1.91.0"
  }
}
```

Publish:
```bash
npm publish
```

Users can then use:
```bash
npm install @zk-healthcare/solana-client
```

---

## **Environment Variables**

Configure these for your deployment:

```bash
# Blockchain
SOLANA_NETWORK=devnet|testnet|mainnet
SOLANA_ENDPOINT=https://api.devnet.solana.com

# API
API_PORT=8000
API_HOST=0.0.0.0
LOG_LEVEL=info|debug|warning|error

# Security (future)
JWT_SECRET=your-secret-key
ENCRYPTION_KEY=your-encryption-key

# Monitoring
SENTRY_DSN=https://...  # Error tracking
DATADOG_API_KEY=...      # Observability
```

---

## **Monitoring & Observability**

### Health Check

```bash
curl http://your-api-url/health
```

Response:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "message": "Healthcare agents API operational"
}
```

### Logs

```bash
# Docker
docker logs zk-healthcare-api

# Railway
railway logs

# Fly.io
flyctl logs
```

### Metrics

Add monitoring for:
- API response times
- Proof verification success rate
- Smart contract transaction costs
- Federated learning convergence

---

## **Testing Deployment**

After deploying to cloud, test endpoints:

```bash
# Health check
curl https://your-api-url/health

# Eligibility check
curl -X POST https://your-api-url/verify-eligibility \
  -H "Content-Type: application/json" \
  -d '{
    "patient_data": {
      "patient_id": "PATIENT_001",
      "encrypted_data": "...",
      "ipfs_cid": "Qm...",
      "data_hash": "abc123..."
    },
    "procedure_code": "PROC001"
  }'

# Interactive docs
https://your-api-url/docs
```

---

## **Scaling Considerations**

### Horizontal Scaling
- Use load balancer (AWS ALB, Nginx)
- Run multiple API instances
- Separate database for state (future)

### Performance Optimization
- Cache proof verification keys
- Use Redis for session management
- Batch federated learning updates

### Cost Optimization
- Use Solana devnet for testing (free)
- Cache circuit artifacts
- Use serverless for sporadic traffic

---

## **Security Checklist**

- [ ] Use HTTPS in production
- [ ] Enable CORS appropriately
- [ ] Add API authentication (JWT)
- [ ] Rotate encryption keys regularly
- [ ] Monitor for unusual verification patterns
- [ ] Use hardware security modules for key storage
- [ ] Regular security audits of Solana contract

---

## **Support & Troubleshooting**

### Common Issues

**"Proof verification failed"**
- Ensure circuit artifacts are correct
- Check proof format (should be 256 bytes)
- Verify verifying key is loaded on-chain

**"Connection timeout"**
- Check Solana RPC endpoint availability
- Verify network configuration
- Check firewall rules

**"OutOfMemory errors"**
- Reduce batch size for federated learning
- Implement pagination for large datasets
- Use streaming for IPFS data

For more help, see [CONTRIBUTING.md](CONTRIBUTING.md) or open an issue on GitHub.

---

## **Next Steps**

1. **Deploy to Railway** (5 min): Fastest path to production
2. **Configure DNS**: Point domain to cloud deployment
3. **Set up monitoring**: Add error tracking and logging
4. **Package SDK**: Publish to PyPI/NPM for developers
5. **Document API**: Keep OpenAPI/Swagger docs updated
