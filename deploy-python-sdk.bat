@echo off
REM Deploy Python SDK to PyPI

echo 🐍 Deploying Oneliac Python SDK to PyPI...
echo.

cd sdk\python

echo 📦 Building package...
python -m build

echo.
echo 🚀 Uploading to PyPI...
echo Make sure you have:
echo 1. PyPI account created at pypi.org
echo 2. API token generated
echo 3. Token configured in ~/.pypirc or TWINE_PASSWORD env var
echo.

python -m twine upload dist/*

echo.
echo ✅ Python SDK deployment complete!
echo Install with: pip install oneliac
echo Package page: https://pypi.org/project/oneliac/

pause