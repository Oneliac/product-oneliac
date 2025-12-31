// Copyright 2025 Raza Ahmad. Licensed under Apache 2.0.

/**
 * Healthcare Agents SDK Models
 * 
 * Data models for API requests and responses.
 */

import * as CryptoJS from 'crypto-js';
import { PatientDataInput, RawPatientData } from './types';
import { ValidationError } from './exceptions';

export class PatientData {
  public patientId: string;
  public encryptedData: string;
  public ipfsCid: string;
  public dataHash: string;

  constructor(data: PatientDataInput) {
    this.patientId = data.patientId;
    this.encryptedData = data.encryptedData;
    this.ipfsCid = data.ipfsCid;
    this.dataHash = data.dataHash;
  }

  /**
   * Create PatientData from raw patient information
   * 
   * @param patientId - Unique patient identifier
   * @param rawData - Raw patient data object
   * @param encryptionKey - Optional encryption key (uses default if not provided)
   * @returns PatientData instance with encrypted data
   */
  static create(patientId: string, rawData: RawPatientData, encryptionKey?: string): PatientData {
    // Convert raw data to JSON string (sorted for consistent hashing)
    const dataJson = JSON.stringify(rawData, Object.keys(rawData).sort());
    
    // Create hash of the data
    const dataHash = CryptoJS.SHA256(dataJson).toString();
    
    // For demo purposes, use base64 encoding as "encryption"
    // In production, use proper encryption
    const encryptedData = btoa(dataJson);
    
    // Generate mock IPFS CID
    const ipfsCid = `Qm${dataHash.substring(0, 32)}`;
    
    return new PatientData({
      patientId,
      encryptedData,
      ipfsCid,
      dataHash
    });
  }

  /**
   * Convert to dictionary for API requests
   */
  toDict(): PatientDataInput {
    return {
      patientId: this.patientId,
      encryptedData: this.encryptedData,
      ipfsCid: this.ipfsCid,
      dataHash: this.dataHash
    };
  }
}

export class EligibilityRequest {
  public patientData: PatientData;
  public procedureCode: string;

  constructor(patientData: PatientData, procedureCode: string) {
    this.patientData = patientData;
    this.procedureCode = procedureCode;
  }

  /**
   * Validate the request data
   */
  validate(): void {
    if (!this.patientData.patientId) {
      throw new ValidationError('Patient ID is required');
    }
    if (!this.procedureCode) {
      throw new ValidationError('Procedure code is required');
    }
  }
}

export class PrescriptionRequest {
  public patientData: PatientData;
  public drugCode: string;

  constructor(patientData: PatientData, drugCode: string) {
    this.patientData = patientData;
    this.drugCode = drugCode;
  }

  /**
   * Validate the request data
   */
  validate(): void {
    if (!this.patientData.patientId) {
      throw new ValidationError('Patient ID is required');
    }
    if (!this.drugCode) {
      throw new ValidationError('Drug code is required');
    }
  }
}

export class FederatedLearningRequest {
  public patientDatasets: PatientData[];

  constructor(patientDatasets: PatientData[]) {
    this.patientDatasets = patientDatasets;
  }

  /**
   * Validate the request data
   */
  validate(): void {
    if (!this.patientDatasets || this.patientDatasets.length === 0) {
      throw new ValidationError('At least one patient dataset is required');
    }
    
    for (const pd of this.patientDatasets) {
      if (!pd.patientId) {
        throw new ValidationError('All patient datasets must have patient_id');
      }
    }
  }
}