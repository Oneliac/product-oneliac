# Circom Circuit Artifacts

## Development Status
These are **mock artifacts** for development/testing. For production deployment:

### Build Real Artifacts
```bash
# Install dependencies
npm install -g circom snarkjs

# Compile circuit
circom eligibility.circom --r1cs --wasm --sym

# Download Powers of Tau (one-time)
wget https://hermez.s3-eu-west-1.amazonaws.com/powersOfTau28_hez_final_10.ptau

# Generate proving key (Phase 1)
snarkjs groth16 setup eligibility.r1cs powersOfTau28_hez_final_10.ptau eligibility_0000.zkey

# Contribute to ceremony (Phase 2)
snarkjs zkey contribute eligibility_0000.zkey eligibility_final.zkey -n="Your contribution"

# Export verification key
snarkjs groth16 export-verification-key eligibility_final.zkey verification_key.json
```

## Circuit Structure
- **Inputs (private)**: patientID, dateOfBirth, insurancePolicyNum, medicalHistoryHash
- **Inputs (public)**: requiredAge, insuranceProviderID, currentTimestamp
- **Output**: isEligible (1 if patient meets age + insurance criteria, 0 otherwise)
- **Components**: Poseidon hash (insurance validation), GreaterEqThan (age check)

## Files
- `eligibility.circom`: Circuit source code
- `build/verification_key.json`: Groth16 verification key (mock)
- `build/circuit_metadata.json`: Circuit metadata
