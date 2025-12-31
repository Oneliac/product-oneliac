// Copyright 2025 Raza Ahmad. Licensed under Apache 2.0.

/**
 * Healthcare Agents SDK Exceptions
 * 
 * Custom exception classes for the Healthcare Agents SDK.
 */

export class HealthcareAgentsError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'HealthcareAgentsError';
  }
}

export class APIError extends HealthcareAgentsError {
  public statusCode?: number;

  constructor(message: string, statusCode?: number) {
    super(message);
    this.name = 'APIError';
    this.statusCode = statusCode;
  }
}

export class ValidationError extends HealthcareAgentsError {
  constructor(message: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

export class AuthenticationError extends HealthcareAgentsError {
  constructor(message: string) {
    super(message);
    this.name = 'AuthenticationError';
  }
}

export class RateLimitError extends HealthcareAgentsError {
  constructor(message: string) {
    super(message);
    this.name = 'RateLimitError';
  }
}

export class NetworkError extends HealthcareAgentsError {
  constructor(message: string) {
    super(message);
    this.name = 'NetworkError';
  }
}