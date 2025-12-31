# Oneliac JavaScript SDK

[![npm version](https://badge.fury.io/js/oneliac.svg)](https://badge.fury.io/js/oneliac)
[![TypeScript](https://img.shields.io/badge/%3C%2F%3E-TypeScript-%230074c1.svg)](http://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A JavaScript/TypeScript client library for the Privacy-Preserving Healthcare Agents API. Enables secure medical data analysis with zero-knowledge proofs and federated learning.

## 🚀 Features

- **🔐 Zero-Knowledge Proofs**: Patient privacy guaranteed mathematically
- **🏥 Eligibility Verification**: Check insurance coverage without exposing data
- **💊 Prescription Validation**: Verify drug safety with encrypted medical history
- **🤖 Federated Learning**: Participate in collaborative AI training
- **⛓️ Blockchain Integration**: Solana-based proof verification
- **🔒 HIPAA Compliant**: Meets healthcare privacy standards
- **📝 TypeScript Support**: Full type definitions included
- **🌐 Browser & Node.js**: Works in both environments

## 📦 Installation

```bash
npm install oneliac
```

Or with yarn:

```bash
yarn add oneliac
```

## 🔧 Quick Start

### TypeScript/ES6 Modules

```typescript
import { 
  HealthcareAgentsClient, 
  PatientData, 
  EligibilityRequest 
} from 'oneliac';

// Initialize client
const client = new HealthcareAgentsClient({
  baseUrl: 'https://healthcare-agents-api.onrender.com',
  apiKey: 'your-api-key', // Optional
  timeout: 30000 // 30 seconds
});

async function main() {
  try {
    // Check API health
    const health = await client.healthCheck();
    console.log(`API Status: ${health.status}`);
    
    // Create patient data
    const patientData = PatientData.create('PATIENT_001', {
      age: 45,
      insuranceId: 'INS123456',
      medicalConditions: ['diabetes', 'hypertension']
    });
    
    // Check eligibility
    const eligibilityRequest = new EligibilityRequest(patientData, 'PROC001');
    const result = await client.verifyEligibility(eligibilityRequest);
    
    console.log(`Eligible: ${result.eligible}`);
    console.log(`Coverage: ${result.coveragePercentage}%`);
    
  } catch (error) {
    console.error('Error:', error.message);
  }
}

main();
```

### CommonJS (Node.js)

```javascript
const { 
  HealthcareAgentsClient, 
  PatientData, 
  EligibilityRequest 
} = require('healthcare-agents-sdk');

// Initialize client
const client = new HealthcareAgentsClient({
  baseUrl: 'https://healthcare-agents-api.onrender.com'
});

async function main() {
  // Check API health
  const health = await client.healthCheck();
  console.log(`API Status: ${health.status}`);
  
  // Create patient data
  const patientData = PatientData.create('PATIENT_001', {
    age: 45,
    insuranceId: 'INS123456',
    medicalConditions: ['diabetes', 'hypertension']
  });
  
  // Check eligibility
  const eligibilityRequest = new EligibilityRequest(patientData, 'PROC001');
  const result = await client.verifyEligibility(eligibilityRequest);
  
  console.log(`Eligible: ${result.eligible}`);
}

main().catch(console.error);
```

### Browser Usage

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://unpkg.com/healthcare-agents-sdk@latest/dist/index.js"></script>
</head>
<body>
  <script>
    const { HealthcareAgentsClient, PatientData, EligibilityRequest } = HealthcareAgentsSDK;
    
    const client = new HealthcareAgentsClient({
      baseUrl: 'https://healthcare-agents-api.onrender.com'
    });
    
    async function checkEligibility() {
      const patientData = PatientData.create('PATIENT_001', {
        age: 45,
        insuranceId: 'INS123456'
      });
      
      const request = new EligibilityRequest(patientData, 'PROC001');
      const result = await client.verifyEligibility(request);
      
      document.getElementById('result').innerText = 
        `Eligible: ${result.eligible}, Coverage: ${result.coveragePercentage}%`;
    }
  </script>
  
  <button onclick="checkEligibility()">Check Eligibility</button>
  <div id="result"></div>
</body>
</html>
```

## 📚 API Reference

### Client Configuration

```typescript
interface ClientConfig {
  baseUrl: string;        // API base URL
  apiKey?: string;        // Optional API key
  timeout?: number;       // Request timeout in milliseconds (default: 30000)
}

const client = new HealthcareAgentsClient({
  baseUrl: 'https://healthcare-agents-api.onrender.com',
  apiKey: 'your-api-key',
  timeout: 30000
});
```

### Patient Data Creation

```typescript
// Create from raw data
const patientData = PatientData.create('PATIENT_001', {
  age: 45,
  insuranceId: 'INS123456',
  medicalConditions: ['diabetes', 'hypertension'],
  allergies: ['penicillin'],
  currentMedications: ['metformin', 'lisinopril']
});

// Manual creation
const patientData = new PatientData({
  patientId: 'PATIENT_001',
  encryptedData: 'base64-encoded-data',
  ipfsCid: 'QmHash...',
  dataHash: 'sha256-hash'
});
```

### Eligibility Verification

```typescript
import { EligibilityRequest } from 'healthcare-agents-sdk';

const request = new EligibilityRequest(patientData, 'PROC001');
const result = await client.verifyEligibility(request);

// Result type
interface EligibilityResponse {
  eligible: boolean;
  coveragePercentage?: number;
  zkProofHash: string;
  reason?: string;
}
```

### Prescription Validation

```typescript
import { PrescriptionRequest } from 'healthcare-agents-sdk';

const request = new PrescriptionRequest(patientData, 'DRUG001');
const result = await client.validatePrescription(request);

// Result type
interface PrescriptionResponse {
  safe: boolean;
  interactions: string[];
  confidence: number;
  warnings: string[];
}
```

### Federated Learning

```typescript
import { FederatedLearningRequest } from 'healthcare-agents-sdk';

// Train with multiple patient datasets
const request = new FederatedLearningRequest([
  patientData1, 
  patientData2, 
  patientData3
]);

const result = await client.federatedLearningTrain(request);

// Check system status
const status = await client.federatedLearningStatus();
```

## 🏥 Healthcare Integration Examples

### Hospital Management System

```typescript
class HospitalSystem {
  private client: HealthcareAgentsClient;
  
  constructor(apiUrl: string) {
    this.client = new HealthcareAgentsClient({ baseUrl: apiUrl });
  }
  
  async checkPatientEligibility(patientId: string, procedureCode: string) {
    const patientData = await this.getPatientData(patientId);
    const request = new EligibilityRequest(patientData, procedureCode);
    return await this.client.verifyEligibility(request);
  }
  
  async validatePrescription(patientId: string, drugCode: string) {
    const patientData = await this.getPatientData(patientId);
    const request = new PrescriptionRequest(patientData, drugCode);
    return await this.client.validatePrescription(request);
  }
  
  private async getPatientData(patientId: string): Promise<PatientData> {
    // Fetch patient data from your database
    const rawData = await this.database.getPatient(patientId);
    return PatientData.create(patientId, rawData);
  }
}
```

### Pharmacy Integration

```typescript
class PharmacySystem {
  private client: HealthcareAgentsClient;
  
  constructor() {
    this.client = new HealthcareAgentsClient({
      baseUrl: 'https://healthcare-agents-api.onrender.com'
    });
  }
  
  async dispenseMedication(patientId: string, drugCode: string) {
    try {
      const patientData = await this.getPatientData(patientId);
      const request = new PrescriptionRequest(patientData, drugCode);
      const result = await this.client.validatePrescription(request);
      
      if (result.safe) {
        return await this.dispenseDrug(drugCode);
      } else {
        return {
          error: 'Prescription validation failed',
          warnings: result.warnings,
          interactions: result.interactions
        };
      }
    } catch (error) {
      return { error: `Validation error: ${error.message}` };
    }
  }
}
```

### React Component Example

```tsx
import React, { useState } from 'react';
import { HealthcareAgentsClient, PatientData, EligibilityRequest } from 'healthcare-agents-sdk';

const EligibilityChecker: React.FC = () => {
  const [result, setResult] = useState<string>('');
  const [loading, setLoading] = useState(false);
  
  const client = new HealthcareAgentsClient({
    baseUrl: 'https://healthcare-agents-api.onrender.com'
  });
  
  const checkEligibility = async () => {
    setLoading(true);
    try {
      const patientData = PatientData.create('PATIENT_001', {
        age: 45,
        insuranceId: 'INS123456'
      });
      
      const request = new EligibilityRequest(patientData, 'PROC001');
      const response = await client.verifyEligibility(request);
      
      setResult(`Eligible: ${response.eligible}, Coverage: ${response.coveragePercentage}%`);
    } catch (error) {
      setResult(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div>
      <button onClick={checkEligibility} disabled={loading}>
        {loading ? 'Checking...' : 'Check Eligibility'}
      </button>
      <p>{result}</p>
    </div>
  );
};
```

## 🔐 Privacy & Security

### Data Encryption

```typescript
// Patient data is automatically encrypted when created
const patientData = PatientData.create('PATIENT_001', {
  ssn: '123-45-6789',  // Sensitive data
  medicalHistory: ['surgery_2020', 'allergy_penicillin']
});

console.log(patientData.encryptedData); // Base64 encoded encrypted data
console.log(patientData.dataHash);      // SHA256 hash for verification
```

### Zero-Knowledge Proofs

```typescript
const result = await client.verifyEligibility(request);

// ZK proof hash verifies computation without revealing data
console.log(`ZK Proof: ${result.zkProofHash}`);
```

## 🔧 Error Handling

```typescript
import { APIError, ValidationError, NetworkError } from 'healthcare-agents-sdk';

try {
  const result = await client.verifyEligibility(request);
} catch (error) {
  if (error instanceof APIError) {
    console.error(`API Error: ${error.message} (Status: ${error.statusCode})`);
  } else if (error instanceof ValidationError) {
    console.error(`Validation Error: ${error.message}`);
  } else if (error instanceof NetworkError) {
    console.error(`Network Error: ${error.message}`);
  } else {
    console.error(`Unexpected Error: ${error.message}`);
  }
}
```

## 🧪 Testing

```bash
# Install dependencies
npm install

# Run tests
npm test

# Run tests in watch mode
npm run test:watch

# Build the project
npm run build
```

## 📖 Documentation

- **API Documentation**: [https://healthcare-agents-api.onrender.com/docs](https://healthcare-agents-api.onrender.com/docs)
- **TypeDoc**: Generated from source code
- **GitHub Repository**: [https://github.com/razaahmad9222/healthcare-agents-sdk-js](https://github.com/razaahmad9222/healthcare-agents-sdk-js)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Run tests: `npm test`
5. Build: `npm run build`
6. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/razaahmad9222/healthcare-agents-sdk-js/issues)
- **Discussions**: [GitHub Discussions](https://github.com/razaahmad9222/healthcare-agents-sdk-js/discussions)
- **Email**: raza@healthcare-agents.com

---

**Built with ❤️ for privacy-preserving healthcare**