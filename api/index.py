# Copyright 2025 Raza Ahmad. Licensed under Apache 2.0.

"""
Vercel serverless entry point for healthcare agents API.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up torch mock before importing agents
try:
    import torch
except (ImportError, OSError):
    # Use local torch mock for Vercel
    from . import torch_mock
    sys.modules['torch'] = torch_mock
    sys.modules['torch.nn'] = torch_mock

from agents.api import app

# Export for Vercel
handler = app