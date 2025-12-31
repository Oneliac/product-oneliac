// Copyright 2025 Raza Ahmad. Licensed under Apache 2.0.

/**
 * Healthcare Agents API Client
 * 
 * Main client class for interacting with the Healthcare Agents API.
 */

import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { 
  ClientConfig, 
  EligibilityResponse, 
  PrescriptionResponse, 
  FederatedLearningResponse,
  FederatedLearningStatus,
  HealthStatus 
} from './types';
import { EligibilityRequest, PrescriptionRequest, FederatedLearningRequest } from './models';
import { APIError, NetworkError } from './exceptions';

export class HealthcareAgentsClient {
  private client: AxiosInstance;
  private baseUrl: string;
  private apiKey?: string;

  /**
   * Initialize the Healthcare Agents client
   * 
   * @param config - Client configuration
   */
  constructor(config: ClientConfig) {
    this.baseUrl = config.baseUrl.replace(/\/$/, '');
    this.apiKey = config.apiKey;

    this.client = axios.create({
      baseURL: this.baseUrl,
      timeout: config.timeout || 30000,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'healthcare-agents-js-sdk/0.1.0',
        ...(this.apiKey && { Authorization: `Bearer ${this.apiKey}` })
      }
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response: AxiosResponse) => response,
      (error) => {
        if (error.response) {
          // API returned an error response
          const message = error.response.data?.detail || `HTTP ${error.response.status}`;
          throw new APIError(message, error.response.status);
        } else if (error.request) {
          // Network error
          throw new NetworkError('Network error: Unable to reach the API');
        } else {
          // Other error
          throw new APIError(`Request error: ${error.message}`);
        }
      }
    );
  }

  /**
   * Check API health status
   * 
   * @returns Health status information
   */
  async healthCheck(): Promise<HealthStatus> {
    const response = await this.client.get<HealthStatus>('/health');
    return response.data;
  }

  /**
   * Verify patient eligibility for a medical procedure
   * 
   * @param request - Eligibility verification request
   * @returns Eligibility verification result with ZK proof
   */
  async verifyEligibility(request: EligibilityRequest): Promise<EligibilityResponse> {
    request.validate();
    
    const data = {
      patient_data: request.patientData.toDict(),
      procedure_code: request.procedureCode
    };

    const response = await this.client.post<EligibilityResponse>('/eligibility/verify', data);
    return response.data;
  }

  /**
   * Validate prescription safety and check for drug interactions
   * 
   * @param request - Prescription validation request
   * @returns Prescription validation result with safety information
   */
  async validatePrescription(request: PrescriptionRequest): Promise<PrescriptionResponse> {
    request.validate();
    
    const data = {
      patient_data: request.patientData.toDict(),
      drug_code: request.drugCode
    };

    const response = await this.client.post<PrescriptionResponse>('/prescription/validate', data);
    return response.data;
  }

  /**
   * Participate in federated learning training round
   * 
   * @param request - Federated learning training request
   * @returns Training result with model updates
   */
  async federatedLearningTrain(request: FederatedLearningRequest): Promise<FederatedLearningResponse> {
    request.validate();
    
    const data = {
      patient_datasets: request.patientDatasets.map(pd => pd.toDict())
    };

    const response = await this.client.post<FederatedLearningResponse>('/federated-learning/train', data);
    return response.data;
  }

  /**
   * Get federated learning system status
   * 
   * @returns Current status of federated learning system
   */
  async federatedLearningStatus(): Promise<FederatedLearningStatus> {
    const response = await this.client.get<FederatedLearningStatus>('/federated-learning/status');
    return response.data;
  }
}