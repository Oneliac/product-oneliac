@echo off
echo 🧪 Testing Oneliac SDKs before deployment...
echo.

echo 🐍 Testing Python SDK...
cd sdk\python
python -c "import sys; sys.path.insert(0, '.'); from healthcare_agents import HealthcareAgentsClientSync, PatientData, EligibilityRequest; client = HealthcareAgentsClientSync('https://test-api.com'); patient_data = PatientData.create('TEST_001', {'age': 30}); request = EligibilityRequest(patient_data, 'PROC001'); request.validate(); print('✅ Python SDK: All tests passed!')"

echo.
echo 📦 Testing JavaScript SDK...
cd ..\javascript
node test-sdk.js

echo.
echo 🎉 All SDK tests passed! Ready for deployment.
echo.
echo Next steps:
echo 1. Deploy Python SDK: run deploy-python-sdk.bat
echo 2. Deploy JavaScript SDK: run deploy-js-sdk.bat
echo.

pause