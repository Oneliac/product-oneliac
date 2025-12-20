# SDK Guide - For Developers

This guide covers how developers can integrate the zk-healthcare system into their applications.

---

## **Installation**

### Python

```bash
pip install zk-healthcare
```

### JavaScript/TypeScript

```bash
npm install @zk-healthcare/solana-client
```

---

## **Python SDK**

### Basic Usage

```python
from zk_healthcare import EligibilityAgent, PatientData
import asyncio

async def check_eligibility():
    # Initialize agent
    agent = EligibilityAgent(solana_endpoint="https://api.devnet.solana.com")
    
    # Create patient data
    patient = PatientData(
        patient_id="PATIENT_001",
        encrypted_data=b"encrypted_data_bytes",
        ipfs_cid="QmXxxx...",
        data_hash="sha256_hash"
    )
    
    # Check coverage
    result = await agent.check_insurance_coverage(patient, "PROC001")
    
    print(f"Eligible: {result['eligible']}")
    print(f"Coverage: {result['coverage_pct']}%")
    print(f"Privacy: {result['privacy_preserved']}")

# Run
asyncio.run(check_eligibility())
```

### Prescription Validation

```python
from zk_healthcare import PrescriptionAgent

async def validate_rx():
    agent = PrescriptionAgent("https://api.devnet.solana.com")
    
    result = await agent.validate_prescription(patient, "DRUG001")
    
    return {
        "valid": result["valid"],
        "drug": result["drug_code"],
        "zk_proof": result["zk_proof_verified"],
        "cross_chain": result["cross_chain_oracle"]
    }
```

### Federated Learning

```python
from zk_healthcare import FederatedLearningCoordinator, DiagnosisModel

async def train_model():
    # Initialize coordinator
    model = DiagnosisModel(input_size=100, hidden_size=64, output_size=10)
    coordinator = FederatedLearningCoordinator(model, num_agents=5)
    
    # Submit training data
    patients = [patient1, patient2, patient3, ...]
    
    result = await coordinator.train_round(patients)
    
    print(f"Round: {result['round']}")
    print(f"Participants: {result['participants']}")
    print(f"Model hash: {result['model_hash']}")
```

### Zero-Knowledge Proofs

```python
from zk_healthcare import ZKProofGenerator

async def generate_proof():
    generator = ZKProofGenerator("./circuits/eligibility.circom")
    
    # Private inputs (patient data)
    private_inputs = {
        "patientID": "PATIENT_001",
        "dateOfBirth": 631152000,  # Unix timestamp
        "insurancePolicyNum": 123456,
        "medicalHistoryHash": "0x..."
    }
    
    # Public inputs (criteria)
    public_inputs = {
        "requiredAge": 18,
        "insuranceProviderID": "INS123",
        "currentTimestamp": 1733529600
    }
    
    # Generate proof
    proof = await generator.generate_proof(private_inputs, public_inputs)
    
    # Verify proof
    is_valid = await generator.verify_proof(proof, public_inputs)
    
    return proof if is_valid else None
```

---

## **REST API Client**

### Base URL
```
https://api.your-healthcare-service.com
```

### Health Check
```bash
GET /health

Response:
{
  "status": "healthy",
  "version": "0.1.0",
  "message": "Healthcare agents API operational"
}
```

### Verify Eligibility

```bash
POST /verify-eligibility

Request:
{
  "patient_data": {
    "patient_id": "PATIENT_001",
    "encrypted_data": "base64_encoded_data",
    "ipfs_cid": "QmXxxx...",
    "data_hash": "sha256_hash"
  },
  "procedure_code": "PROC001"
}

Response:
{
  "eligible": true,
  "coverage_pct": 80.0,
  "privacy_preserved": true,
  "procedure_code": "PROC001",
  "requires_authorization": true,
  "zk_proof_verified": true
}
```

### Validate Prescription

```bash
POST /validate-prescription

Request:
{
  "patient_data": { ... },
  "drug_code": "DRUG001"
}

Response:
{
  "valid": true,
  "drug_code": "DRUG001",
  "interactions_checked": true,
  "zk_proof_verified": true,
  "cross_chain_oracle": "LayerZero confirmed: DRUG001 available on Ethereum bridge"
}
```

### Submit Federated Update

```bash
POST /submit-federated-update

Request:
{
  "patient_data_list": [
    { "patient_id": "...", ... },
    { "patient_id": "...", ... }
  ],
  "round_number": 1
}

Response:
{
  "round": 1,
  "participants": 3,
  "model_hash": "sha256_hash_of_model"
}
```

---

## **JavaScript/TypeScript SDK**

### Installation & Setup

```typescript
import { HealthcareClient } from '@zk-healthcare/solana-client';

const client = new HealthcareClient({
  endpoint: "https://api.devnet.solana.com",
  programId: "HEALth11111111111111111111111111111111111"
});
```

### Verify Eligibility

```typescript
const result = await client.verifyEligibility({
  patientData: {
    patientId: "PATIENT_001",
    encryptedData: Buffer.from("..."),
    ipfsCid: "QmXxxx...",
    dataHash: "0x..."
  },
  procedureCode: "PROC001"
});

console.log(`Eligible: ${result.eligible}`);
console.log(`Coverage: ${result.coveragePct}%`);
```

### Submit Proof to Solana

```typescript
const txSignature = await client.submitProof({
  proof: proofBytes,
  publicInputs: publicInputsBytes,
  ipfsHash: "QmXxxx..."
});

console.log(`Confirmed: ${txSignature}`);
```

---

## **Data Privacy & Encryption**

### Encrypt Patient Data

```python
from cryptography.fernet import Fernet
import json

# Generate key (store securely!)
key = Fernet.generate_key()
cipher = Fernet(key)

# Patient data
patient_data = {
    "ssn": "123-45-6789",
    "dateOfBirth": "1980-01-01",
    "medicalHistory": ["Diabetes", "Hypertension"]
}

# Encrypt
encrypted = cipher.encrypt(json.dumps(patient_data).encode())

# Decrypt
decrypted = json.loads(cipher.decrypt(encrypted))
```

### Upload to IPFS

```python
import requests

# Using public IPFS gateway
files = {'file': encrypted_data}
response = requests.post('https://ipfs.io/api/v0/add', files=files)
ipfs_cid = response.json()['Hash']

print(f"IPFS CID: {ipfs_cid}")
```

---

## **Error Handling**

### API Errors

```python
import httpx

async def safe_verify_eligibility():
    try:
        result = await agent.check_insurance_coverage(patient, "PROC001")
        return result
    
    except httpx.TimeoutException:
        print("Request timeout - retry later")
    
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 500:
            print("Server error - check logs")
        elif e.response.status_code == 400:
            print(f"Invalid request: {e.response.text}")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
```

### Proof Verification Failures

```python
try:
    is_valid = await generator.verify_proof(proof, public_inputs)
    if not is_valid:
        print("Proof verification failed")
        # Retry with fresh proof generation
        proof = await generator.generate_proof(private_inputs, public_inputs)
except Exception as e:
    print(f"Proof generation error: {e}")
```

---

## **Testing**

### Unit Tests

```python
import pytest
from zk_healthcare import EligibilityAgent, PatientData

@pytest.mark.asyncio
async def test_eligibility_check():
    agent = EligibilityAgent("http://localhost:8000")
    
    patient = PatientData(
        patient_id="TEST_001",
        encrypted_data=b"test",
        ipfs_cid="QmTest",
        data_hash="hash"
    )
    
    result = await agent.check_insurance_coverage(patient, "PROC001")
    
    assert result["eligible"] == True
    assert result["privacy_preserved"] == True
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_full_workflow():
    # 1. Generate ZK proof
    proof = await generate_eligibility_proof(patient)
    
    # 2. Submit to blockchain
    tx = await submit_proof_to_solana(proof)
    
    # 3. Verify on-chain
    assert await verify_on_chain(tx) == True
    
    # 4. Check eligibility
    result = await check_coverage(patient)
    assert result["zk_proof_verified"] == True
```

---

## **Best Practices**

### Key Management
```python
# ❌ DON'T
key = "hardcoded_key_123"

# ✅ DO
import os
key = os.getenv("ENCRYPTION_KEY")
if not key:
    raise ValueError("ENCRYPTION_KEY not set")
```

### Async/Await
```python
# ❌ Avoid blocking calls
result = agent.check_insurance_coverage(patient, "PROC001")  # Blocks!

# ✅ Use async
result = await agent.check_insurance_coverage(patient, "PROC001")
```

### Error Handling
```python
# ❌ Ignore errors
await agent.verify_eligibility(patient)

# ✅ Handle errors
try:
    result = await agent.verify_eligibility(patient)
except Exception as e:
    logger.error(f"Verification failed: {e}")
    # Implement retry logic
```

### Rate Limiting
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def verify_with_retry(patient):
    return await agent.verify_eligibility(patient)
```

---

## **Examples & Tutorials**

Check `notebooks/` directory for Jupyter notebooks:
- `eligibility_check.ipynb`: Step-by-step eligibility verification
- `prescription_validation.ipynb`: Drug interaction checking
- `federated_learning.ipynb`: Privacy-preserving model training
- `zk_circuits.ipynb`: Understanding zk-SNARK circuits

---

## **Troubleshooting**

### "Module not found: zk_healthcare"
```bash
# Reinstall SDK
pip install --upgrade zk-healthcare

# Or install from source
pip install -e .
```

### "Proof verification timeout"
- Increase timeout: `PROOF_TIMEOUT=30s`
- Check circuit artifacts in `circuits/build/`
- Verify Solana RPC endpoint is responsive

### "IPFS gateway timeout"
- Use alternative gateway
- Store IPFS CID locally and pin to your node
- Cache encrypted data

---

## **Support**

- **Docs**: https://docs.zk-healthcare.io
- **GitHub**: https://github.com/razaahmad9222/zk-healthcare-agents-solana
- **Discord**: https://discord.gg/zk-healthcare
- **Email**: support@zk-healthcare.io

---

## **API Reference**

Full OpenAPI specification available at:
```
https://api.your-healthcare-service.com/openapi.json
```

Interactive documentation:
```
https://api.your-healthcare-service.com/docs
```
