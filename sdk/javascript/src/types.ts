// Copyright 2025 Raza Ahmad. Licensed under Apache 2.0.

/**
 * Type definitions for Healthcare Agents SDK
 */

export interface ClientConfig {
  baseUrl: string;
  apiKey?: string;
  timeout?: number;
}

export interface PatientDataInput {
  patientId: string;
  encryptedData: string;
  ipfsCid: string;
  dataHash: string;
}

export interface RawPatientData {
  [key: string]: any;
}

export interface EligibilityResponse {
  eligible: boolean;
  coveragePercentage?: number;
  zkProofHash: string;
  reason?: string;
}

export interface PrescriptionResponse {
  safe: boolean;
  interactions: string[];
  confidence: number;
  warnings: string[];
}

export interface FederatedLearningResponse {
  modelUpdated: boolean;
  trainingRound: number;
  modelAccuracy: number;
  participants: number;
}

export interface FederatedLearningStatus {
  activeAgents: number;
  trainingRounds: number;
  modelAccuracy: number;
  totalQueries?: number;
  successRate?: number;
}

export interface HealthStatus {
  status: string;
  version: string;
  message: string;
}