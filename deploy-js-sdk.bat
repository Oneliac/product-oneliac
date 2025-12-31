@echo off
REM Deploy JavaScript SDK to NPM

echo 📦 Deploying Oneliac JavaScript SDK to NPM...
echo.

cd sdk\javascript

echo 🔨 Building TypeScript...
npm run build

echo.
echo 🚀 Publishing to NPM...
echo Make sure you are logged in to NPM: npm login
echo.

npm publish

echo.
echo ✅ JavaScript SDK deployment complete!
echo Install with: npm install oneliac
echo Package page: https://www.npmjs.com/package/oneliac

pause