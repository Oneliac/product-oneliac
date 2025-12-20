pragma circom 2.0.0.0;

include "circomlib/poseidon.circom";
include "circomlib/comparators.circom";

// Patient eligibility verification circuit
template PatientEligibility() {
    // Private inputs (patient data)
    signal input patientID;
    signal input dateOfBirth;
    signal input insurancePolicyNum;
    signal input medicalHistoryHash;
    
    // Public inputs (verification criteria)
    signal input requiredAge;
    signal input insuranceProviderID;
    signal input currentTimestamp;
    
    // Output: 1 if eligible, 0 otherwise
    signal output isEligible;
    
    // Intermediate signals
    signal ageInYears;
    signal ageCheck;
    signal insuranceCheck;
    signal policyValidHash;
    signal timeDiff;
    
    // Age calculation (simplified: time difference in seconds / seconds per year)
    timeDiff <== currentTimestamp - dateOfBirth;
    ageInYears <== timeDiff / 31557600;  // Seconds per year (365.25 days)
    
    // Age verification (ageInYears >= requiredAge)
    component ageComparator = GreaterEqThan(32);
    ageComparator.in[0] <== ageInYears;
    ageComparator.in[1] <== requiredAge;
    ageCheck <== ageComparator.out;
    
    // Insurance verification (hash-based using Poseidon)
    component policyHasher = Poseidon(2);
    policyHasher.inputs[0] <== insurancePolicyNum;
    policyHasher.inputs[1] <== insuranceProviderID;
    policyValidHash <== policyHasher.out;
    
    // Check if policy hash matches medical history hash
    component insuranceValidator = IsEqual();
    insuranceValidator.in[0] <== policyValidHash;
    insuranceValidator.in[1] <== medicalHistoryHash;
    insuranceCheck <== insuranceValidator.out;
    
    // Final eligibility: AND gate (both checks must pass)
    // Note: This requires both ageCheck and insuranceCheck to be 1
    signal ageCheckConstraint;
    signal insuranceCheckConstraint;
    
    ageCheckConstraint <== ageCheck * (ageCheck - 1);  // ageCheck must be 0 or 1
    insuranceCheckConstraint <== insuranceCheck * (insuranceCheck - 1);  // insuranceCheck must be 0 or 1
    
    // Final result: both must be 1
    isEligible <== ageCheck * insuranceCheck;
}

component main = PatientEligibility();
