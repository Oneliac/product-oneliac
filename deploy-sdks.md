# 📦 Deploy Oneliac SDKs - Step by Step Guide

## 🐍 Deploy Python SDK to PyPI

### Step 1: Create PyPI Account
1. Go to [pypi.org](https://pypi.org/account/register/)
2. Create account and verify email
3. Enable 2FA (required for publishing)

### Step 2: Generate API Token
1. Go to [Account Settings](https://pypi.org/manage/account/) → API tokens
2. Click "Add API token"
3. Token name: `oneliac-sdk`
4. Scope: "Entire account" (or create project first)
5. Copy the token (starts with `pypi-`)

### Step 3: Configure Credentials
```bash
# Option A: Use .pypirc file (recommended)
# Create ~/.pypirc file:
[distutils]
index-servers = pypi

[pypi]
username = __token__
password = pypi-your-token-here

# Option B: Use environment variable
export TWINE_PASSWORD=pypi-your-token-here
```

### Step 4: Upload to PyPI
```bash
cd sdk/python

# Upload to PyPI
python -m twine upload dist/*

# You'll see:
# Uploading distributions to https://upload.pypi.org/legacy/
# Uploading oneliac-0.1.0-py3-none-any.whl
# Uploading oneliac-0.1.0.tar.gz
```

### Step 5: Verify Upload
```bash
# Install from PyPI
pip install oneliac

# Test import
python -c "from healthcare_agents import HealthcareAgentsClient; print('✅ Success!')"
```

## 📦 Deploy JavaScript SDK to NPM

### Step 1: Create NPM Account
1. Go to [npmjs.com](https://www.npmjs.com/signup)
2. Create account and verify email
3. Enable 2FA (recommended)

### Step 2: Login to NPM
```bash
cd sdk/javascript

# Login to NPM
npm login
# Enter username, password, email, and 2FA code
```

### Step 3: Build Package
```bash
# Build TypeScript (already done)
npm run build

# Verify build
ls dist/
# Should show: index.js, index.d.ts, client.js, etc.
```

### Step 4: Publish to NPM
```bash
# Publish package
npm publish

# You'll see:
# npm notice package: oneliac@0.1.0
# npm notice === Tarball Contents ===
# npm notice package size: X.X kB
# npm notice unpacked size: X.X kB
# npm notice total files: XX
# + oneliac@0.1.0
```

### Step 5: Verify Upload
```bash
# Install from NPM
npm install oneliac

# Test import
node -e "const {HealthcareAgentsClient} = require('oneliac'); console.log('✅ Success!');"
```

## 🚀 Automated Deployment Scripts

### Python Deployment Script
```bash
#!/bin/bash
# deploy-python-sdk.sh

cd sdk/python

echo "🐍 Deploying Python SDK to PyPI..."

# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build package
echo "📦 Building package..."
python -m build

# Upload to PyPI
echo "🚀 Uploading to PyPI..."
python -m twine upload dist/*

echo "✅ Python SDK deployed successfully!"
echo "Install with: pip install oneliac"
```

### JavaScript Deployment Script
```bash
#!/bin/bash
# deploy-js-sdk.sh

cd sdk/javascript

echo "📦 Deploying JavaScript SDK to NPM..."

# Build TypeScript
echo "🔨 Building TypeScript..."
npm run build

# Publish to NPM
echo "🚀 Publishing to NPM..."
npm publish

echo "✅ JavaScript SDK deployed successfully!"
echo "Install with: npm install oneliac"
```

## 🔄 Update Existing Packages

### Update Python SDK
```bash
cd sdk/python

# 1. Update version in setup.py
# version="0.1.1"

# 2. Build and upload
python -m build
python -m twine upload dist/*
```

### Update JavaScript SDK
```bash
cd sdk/javascript

# 1. Update version
npm version patch  # or minor/major

# 2. Build and publish
npm run build
npm publish
```

## 📊 Monitor Your Packages

### PyPI Statistics
- **Package page**: https://pypi.org/project/oneliac/
- **Download stats**: https://pypistats.org/packages/oneliac
- **Dependencies**: Shows who depends on your package

### NPM Statistics
- **Package page**: https://www.npmjs.com/package/oneliac
- **Download stats**: Built into NPM dashboard
- **Dependencies**: Shows dependent packages

## 🔧 Troubleshooting

### Common PyPI Issues

#### 1. Package name already exists
```bash
# Error: The user 'username' isn't allowed to upload to project 'oneliac'
# Solution: Choose a different name or contact current owner
```

#### 2. Authentication failed
```bash
# Error: Invalid or non-existent authentication information
# Solution: Check your API token and .pypirc file
```

#### 3. Version already exists
```bash
# Error: File already exists
# Solution: Increment version number in setup.py
```

### Common NPM Issues

#### 1. Package name taken
```bash
# Error: You do not have permission to publish "oneliac"
# Solution: Use scoped package @yourusername/oneliac
```

#### 2. Not logged in
```bash
# Error: You must be logged in to publish packages
# Solution: Run npm login
```

#### 3. Version already published
```bash
# Error: You cannot publish over the previously published versions
# Solution: Run npm version patch
```

## 📋 Pre-Deployment Checklist

### Python SDK
- [ ] Tests pass: `python -m pytest`
- [ ] Package builds: `python -m build`
- [ ] Version updated in `setup.py`
- [ ] README.md is complete
- [ ] Dependencies listed in `requirements.txt`
- [ ] PyPI account set up with 2FA
- [ ] API token configured

### JavaScript SDK
- [ ] Tests pass: `npm test`
- [ ] TypeScript builds: `npm run build`
- [ ] Version updated in `package.json`
- [ ] README.md is complete
- [ ] Dependencies listed in `package.json`
- [ ] NPM account set up
- [ ] Logged in: `npm whoami`

## 🎯 Post-Deployment

### Update Documentation
1. Update main README with installation instructions
2. Add badges for PyPI and NPM versions
3. Update examples with new package names
4. Create changelog for version history

### Announce Release
1. GitHub release with changelog
2. Social media announcement
3. Developer community posts
4. Update project website

### Monitor Usage
1. Check download statistics
2. Monitor for issues/bug reports
3. Respond to user questions
4. Plan next version features

---

## 🎉 Ready to Deploy!

Your SDKs are built and ready for deployment:

### Python SDK ✅
- **Built**: `oneliac-0.1.0-py3-none-any.whl`
- **Ready for**: `python -m twine upload dist/*`
- **Install command**: `pip install oneliac`

### JavaScript SDK ✅
- **Built**: TypeScript compiled to `dist/`
- **Ready for**: `npm publish`
- **Install command**: `npm install oneliac`

**Deploy now and make Oneliac available to developers worldwide!** 🚀