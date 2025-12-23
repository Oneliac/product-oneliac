# Copyright 2025 Raza Ahmad. Licensed under Apache 2.0.
# Mock PyTorch implementation for Python 3.14 compatibility on Windows

import numpy as np
from typing import Any, List, Tuple, Union

class MockTensor:
    """Mock PyTorch tensor using numpy backend"""
    
    def __init__(self, data):
        if isinstance(data, (list, tuple)):
            self.data = np.array(data, dtype=np.float32)
        elif isinstance(data, np.ndarray):
            self.data = data.astype(np.float32)
        else:
            self.data = np.array([data], dtype=np.float32)
    
    def numpy(self):
        return self.data
    
    def cpu(self):
        """Mock cpu() method - returns self since we're already on CPU"""
        return self
    
    def tolist(self):
        """Convert to Python list"""
        return self.data.tolist()
    
    def __add__(self, other):
        if isinstance(other, MockTensor):
            return MockTensor(self.data + other.data)
        return MockTensor(self.data + other)
    
    def __mul__(self, other):
        if isinstance(other, MockTensor):
            return MockTensor(self.data * other.data)
        return MockTensor(self.data * other)
    
    def numel(self):
        return self.data.size
    
    @property
    def shape(self):
        return self.data.shape

def tensor(data):
    """Create a mock tensor"""
    return MockTensor(data)

def randn(*shape):
    """Generate random tensor with normal distribution"""
    return MockTensor(np.random.randn(*shape))

def normal(mean=0.0, std=1.0, size=None):
    """Generate normal distributed tensor"""
    return MockTensor(np.random.normal(mean, std, size))

def mean(tensors, dim=0):
    """Compute mean of tensors"""
    if isinstance(tensors, list):
        arrays = [t.data for t in tensors]
        return MockTensor(np.mean(arrays, axis=dim))
    return MockTensor(np.mean(tensors.data, axis=dim))

def stack(tensors, dim=0):
    """Stack tensors"""
    arrays = [t.data for t in tensors]
    return MockTensor(np.stack(arrays, axis=dim))

class no_grad:
    """Mock no_grad context manager"""
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass

class MockParameter:
    """Mock PyTorch parameter"""
    def __init__(self, data):
        self.data = MockTensor(data) if not isinstance(data, MockTensor) else data
    
    def numel(self):
        return self.data.numel()

class MockModule:
    """Mock PyTorch nn.Module"""
    
    def __init__(self):
        self._parameters = {}
    
    def parameters(self):
        """Return mock parameters"""
        # Return some mock parameters for the model
        return [
            MockParameter(np.random.randn(100, 64)),  # fc1 weight
            MockParameter(np.random.randn(64)),       # fc1 bias
            MockParameter(np.random.randn(64, 10)),   # fc2 weight
            MockParameter(np.random.randn(10))        # fc2 bias
        ]
    
    def state_dict(self):
        """Return mock state dictionary with MockTensor objects"""
        return {
            'fc1.weight': MockTensor(np.random.randn(64, 100)),
            'fc1.bias': MockTensor(np.random.randn(64)),
            'fc2.weight': MockTensor(np.random.randn(10, 64)),
            'fc2.bias': MockTensor(np.random.randn(10))
        }

class MockLinear(MockModule):
    """Mock PyTorch Linear layer"""
    
    def __init__(self, in_features, out_features):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.weight = MockParameter(np.random.randn(out_features, in_features))
        self.bias = MockParameter(np.random.randn(out_features))
    
    def __call__(self, x):
        # Simple linear transformation: y = xW^T + b
        if isinstance(x, MockTensor):
            x_data = x.data
        else:
            x_data = np.array(x)
        
        # Reshape if needed
        if len(x_data.shape) == 1:
            x_data = x_data.reshape(1, -1)
        
        result = np.dot(x_data, self.weight.data.data.T) + self.bias.data.data
        return MockTensor(result)

class MockReLU(MockModule):
    """Mock PyTorch ReLU activation"""
    
    def __call__(self, x):
        if isinstance(x, MockTensor):
            return MockTensor(np.maximum(0, x.data))
        return MockTensor(np.maximum(0, np.array(x)))

# Mock nn module
class nn:
    Module = MockModule
    Linear = MockLinear
    ReLU = MockReLU