# Copyright 2025 Raza Ahmad. Licensed under Apache 2.0.

"""
FastAPI service wrapper for privacy-preserving healthcare agents.
Provides REST endpoints for eligibility verification, prescription validation, and federated learning.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Optional, List
import asyncio
try:
    import torch.nn as nn
except (ImportError, OSError) as e:
    # Fallback to mock implementation for compatibility issues
    from .torch_mock import nn

from agents.main import (
    PatientData,
    EligibilityAgent,
    PrescriptionAgent,
    FederatedLearningCoordinator,
    DiagnosisModel,
    Fernet,
    hashlib
)

# Pydantic request/response models
class PatientDataRequest(BaseModel):
    """Patient data request model."""
    patient_id: str = Field(..., description="Unique patient identifier")
    encrypted_data: str = Field(..., description="Base64-encoded encrypted patient data")
    ipfs_cid: str = Field(..., description="IPFS content identifier for patient records")
    data_hash: str = Field(..., description="SHA256 hash of patient medical history")


class EligibilityCheckRequest(BaseModel):
    """Request to verify patient insurance eligibility."""
    patient_data: PatientDataRequest
    procedure_code: str = Field(..., description="Medical procedure code (e.g., PROC001)")


class PrescriptionValidationRequest(BaseModel):
    """Request to validate a prescription."""
    patient_data: PatientDataRequest
    drug_code: str = Field(..., description="Drug code (e.g., DRUG001)")


class FederatedLearningRequest(BaseModel):
    """Request to submit federated learning training round."""
    patient_data_list: List[PatientDataRequest] = Field(..., description="List of patient data for training")
    round_number: int = Field(default=0, description="Training round number")


class EligibilityCheckResponse(BaseModel):
    """Response from eligibility check."""
    eligible: bool
    coverage_pct: float = Field(..., description="Coverage percentage (0-100)")
    privacy_preserved: bool
    procedure_code: Optional[str] = None
    requires_authorization: Optional[bool] = None
    zk_proof_verified: bool
    reason: Optional[str] = None


class PrescriptionValidationResponse(BaseModel):
    """Response from prescription validation."""
    valid: bool
    drug_code: str
    interactions_checked: bool
    zk_proof_verified: bool
    cross_chain_oracle: str


class FederatedLearningResponse(BaseModel):
    """Response from federated learning round."""
    round: int
    participants: int
    model_hash: str


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str = "0.1.0"
    message: str = "Healthcare agents API operational"


# Initialize FastAPI app
app = FastAPI(
    title="Privacy-Preserving Healthcare Agents API",
    description="Decentralized medical data analysis with zero-knowledge proofs",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instances (in production, use dependency injection)
solana_endpoint = "https://api.devnet.solana.com"
eligibility_agent = EligibilityAgent(solana_endpoint)
prescription_agent = PrescriptionAgent(solana_endpoint)
diagnosis_model = DiagnosisModel()
fl_coordinator = FederatedLearningCoordinator(diagnosis_model, num_agents=3)


@app.get("/health", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """Health check endpoint."""
    return HealthCheckResponse()


@app.post("/verify-eligibility", response_model=EligibilityCheckResponse)
async def verify_eligibility(request: EligibilityCheckRequest) -> EligibilityCheckResponse:
    """
    Verify patient insurance eligibility using zero-knowledge proofs.
    
    Private inputs (encrypted):
    - Patient ID
    - Medical history hash
    
    Public inputs:
    - Procedure code
    - Insurance provider ID
    
    Returns:
    - Eligibility status
    - Coverage percentage
    - ZK proof verification status
    """
    try:
        # Convert Pydantic request to PatientData
        patient_data = PatientData(
            patient_id=request.patient_data.patient_id,
            encrypted_data=request.patient_data.encrypted_data.encode(),
            ipfs_cid=request.patient_data.ipfs_cid,
            data_hash=request.patient_data.data_hash
        )
        
        # Check coverage
        result = await eligibility_agent.check_insurance_coverage(
            patient_data,
            request.procedure_code
        )
        
        return EligibilityCheckResponse(
            eligible=result["eligible"],
            coverage_pct=result["coverage_pct"],
            privacy_preserved=result["privacy_preserved"],
            procedure_code=result.get("procedure_code"),
            requires_authorization=result.get("requires_authorization"),
            zk_proof_verified=result.get("zk_proof_verified", False),
            reason=result.get("reason")
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eligibility check failed: {str(e)}")


@app.post("/validate-prescription", response_model=PrescriptionValidationResponse)
async def validate_prescription(request: PrescriptionValidationRequest) -> PrescriptionValidationResponse:
    """
    Validate a prescription using drug interaction checking and ZK proofs.
    
    Steps:
    1. Verify patient eligibility (with ZK proof)
    2. Check drug interactions against medical history
    3. Query LayerZero oracle for cross-chain pharmacy verification
    
    Returns:
    - Validity status
    - Interactions checked flag
    - Cross-chain oracle result
    """
    try:
        patient_data = PatientData(
            patient_id=request.patient_data.patient_id,
            encrypted_data=request.patient_data.encrypted_data.encode(),
            ipfs_cid=request.patient_data.ipfs_cid,
            data_hash=request.patient_data.data_hash
        )
        
        result = await prescription_agent.validate_prescription(
            patient_data,
            request.drug_code
        )
        
        return PrescriptionValidationResponse(
            valid=result["valid"],
            drug_code=result["drug_code"],
            interactions_checked=result.get("interactions_checked", False),
            zk_proof_verified=result.get("zk_proof_verified", False),
            cross_chain_oracle=result.get("cross_chain_oracle", "")
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prescription validation failed: {str(e)}")


@app.post("/submit-federated-update", response_model=FederatedLearningResponse)
async def submit_federated_update(request: FederatedLearningRequest) -> FederatedLearningResponse:
    """
    Submit encrypted gradients for federated learning training round.
    
    Process:
    1. Receive encrypted patient data from multiple agents
    2. Compute local gradients with differential privacy noise
    3. Secure aggregate gradients (encrypted)
    4. Update global diagnosis model
    
    Returns:
    - Training round number
    - Participant count
    - New model hash
    """
    try:
        # Convert requests to PatientData objects
        patient_data_list = [
            PatientData(
                patient_id=p.patient_id,
                encrypted_data=p.encrypted_data.encode(),
                ipfs_cid=p.ipfs_cid,
                data_hash=p.data_hash
            )
            for p in request.patient_data_list
        ]
        
        # Run federated learning round
        result = await fl_coordinator.train_round(patient_data_list)
        
        return FederatedLearningResponse(
            round=result["round"],
            participants=result["participants"],
            model_hash=result["model_hash"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Federated learning submission failed: {str(e)}")


@app.get("/status")
async def get_status() -> Dict:
    """Get current system status and agent metrics."""
    return {
        "status": "operational",
        "agents": {
            "eligibility": "active",
            "prescription": "active",
            "diagnosis_model": "trained",
        },
        "federated_learning": {
            "current_round": fl_coordinator.round_number,
            "participants": 0,
        },
        "blockchain": {
            "endpoint": solana_endpoint,
            "network": "devnet"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
