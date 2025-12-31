# 📦 Oneliac SDK Deployment Guide

Complete guide for publishing Python (PyPI) and JavaScript (NPM) SDKs for the Oneliac Healthcare API.

## 🐍 Python SDK (PyPI)

### Package Name: `oneliac`

### Publishing Commands

```bash
cd sdk/python

# Build package
python -m build

# Upload to PyPI
twine upload dist/*
```

### Installation Commands

After publishing, users can install with:

```bash
# Latest version
pip install oneliac

# Specific version
pip install oneliac==0.1.0

# With development dependencies
pip install oneliac[dev]
```

## 📦 JavaScript SDK (NPM)

### Package Name: `oneliac`

### Publishing Commands

```bash
cd sdk/javascript

# Build TypeScript
npm run build

# Publish to NPM
npm publish
```

### Installation Commands

After publishing, users can install with:

```bash
# Latest version
npm install oneliac

# Specific version
npm install oneliac@0.1.0

# With Yarn
yarn add oneliac
```

## 🔄 Automated Publishing (GitHub Actions)

### Python SDK CI/CD

Create `.github/workflows/python-sdk.yml`:

```yaml
name: Python SDK

on:
  push:
    tags:
      - 'python-v*'
  pull_request:
    paths:
      - 'sdk/python/**'

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        cd sdk/python
        pip install -r requirements.txt
        pip install pytest black flake8 mypy
    
    - name: Lint with flake8
      run: |
        cd sdk/python
        flake8 healthcare_agents/
    
    - name: Type check with mypy
      run: |
        cd sdk/python
        mypy healthcare_agents/
    
    - name: Test with pytest
      run: |
        cd sdk/python
        pytest

  publish:
    needs: test
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/python-v')
    
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install build tools
      run: pip install build twine
    
    - name: Build package
      run: |
        cd sdk/python
        python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        cd sdk/python
        twine upload dist/*
```

### JavaScript SDK CI/CD

Create `.github/workflows/javascript-sdk.yml`:

```yaml
name: JavaScript SDK

on:
  push:
    tags:
      - 'js-v*'
  pull_request:
    paths:
      - 'sdk/javascript/**'

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]
    
    steps:
    - uses: actions/checkout@v4
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
    
    - name: Install dependencies
      run: |
        cd sdk/javascript
        npm ci
    
    - name: Lint
      run: |
        cd sdk/javascript
        npm run lint
    
    - name: Build
      run: |
        cd sdk/javascript
        npm run build
    
    - name: Test
      run: |
        cd sdk/javascript
        npm test

  publish:
    needs: test
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/js-v')
    
    steps:
    - uses: actions/checkout@v4
    - name: Use Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        registry-url: 'https://registry.npmjs.org'
    
    - name: Install dependencies
      run: |
        cd sdk/javascript
        npm ci
    
    - name: Build
      run: |
        cd sdk/javascript
        npm run build
    
    - name: Publish to NPM
      env:
        NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
      run: |
        cd sdk/javascript
        npm publish
```

## 📋 Release Checklist

### Before Publishing

- [ ] Update version numbers in `setup.py` and `package.json`
- [ ] Update `CHANGELOG.md` with new features
- [ ] Test SDKs against live API
- [ ] Run all tests locally
- [ ] Update documentation
- [ ] Create GitHub release notes

### Python SDK Release

```bash
# 1. Update version in setup.py
# 2. Tag release
git tag python-v0.1.0
git push origin python-v0.1.0

# 3. GitHub Actions will automatically:
#    - Run tests
#    - Build package
#    - Publish to PyPI
```

### JavaScript SDK Release

```bash
# 1. Update version in package.json
npm version patch  # or minor/major

# 2. Tag release
git tag js-v0.1.0
git push origin js-v0.1.0

# 3. GitHub Actions will automatically:
#    - Run tests
#    - Build TypeScript
#    - Publish to NPM
```

## 📊 Usage Analytics

### PyPI Downloads

Monitor at: https://pypistats.org/packages/healthcare-agents

### NPM Downloads

Monitor at: https://www.npmjs.com/package/healthcare-agents-sdk

## 🔧 Maintenance

### Updating Dependencies

```bash
# Python SDK
cd sdk/python
pip-compile requirements.in  # If using pip-tools

# JavaScript SDK
cd sdk/javascript
npm update
npm audit fix
```

### Version Management

Follow semantic versioning (semver):
- **Patch** (0.1.1): Bug fixes
- **Minor** (0.2.0): New features, backward compatible
- **Major** (1.0.0): Breaking changes

## 📖 Documentation

### Python SDK Docs

```bash
cd sdk/python
sphinx-build -b html docs/ docs/_build/
```

### JavaScript SDK Docs

```bash
cd sdk/javascript
npm run docs  # Generates TypeDoc documentation
```

## 🆘 Support

### Common Issues

1. **PyPI Upload Fails**
   - Check API token permissions
   - Ensure version number is incremented
   - Verify package name availability

2. **NPM Publish Fails**
   - Check NPM authentication: `npm whoami`
   - Ensure package name is available
   - Verify build completed successfully

3. **Import Errors**
   - Check Python path configuration
   - Verify all dependencies are listed
   - Test in clean virtual environment

### Getting Help

- **Python SDK**: [GitHub Issues](https://github.com/razaahmad9222/healthcare-agents-sdk-python/issues)
- **JavaScript SDK**: [GitHub Issues](https://github.com/razaahmad9222/healthcare-agents-sdk-js/issues)
- **General**: raza@healthcare-agents.com

---

**Ready to publish?** Follow the checklists above to get your SDKs live on PyPI and NPM! 📦🚀