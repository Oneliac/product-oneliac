// Copyright 2025 Raza Ahmad. Licensed under Apache 2.0.

/**
 * Healthcare Agents JavaScript/TypeScript SDK
 * 
 * A client library for the Privacy-Preserving Healthcare Agents API.
 * Provides easy access to eligibility verification, prescription validation,
 * and federated learning capabilities with zero-knowledge proofs.
 */

export { HealthcareAgentsClient } from './client';
export { 
  PatientData, 
  EligibilityRequest, 
  PrescriptionRequest, 
  FederatedLearningRequest 
} from './models';
export { 
  HealthcareAgentsError, 
  APIError, 
  ValidationError, 
  AuthenticationError,
  RateLimitError,
  NetworkError 
} from './exceptions';
export * from './types';