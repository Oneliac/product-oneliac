# Copyright 2025 Raza Ahmad. Licensed under Apache 2.0.
# Lightweight PyTorch mock for Vercel deployment

import numpy as np

class MockTensor:
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
        return self
    
    def tolist(self):
        return self.data.tolist()
    
    def __add__(self, other):
        if isinstance(other, MockTensor):
            return MockTensor(self.data + other.data)
        return MockTensor(self.data + other)
    
    def numel(self):
        return self.data.size

def tensor(data):
    return MockTensor(data)

def randn(*shape):
    return MockTensor(np.random.randn(*shape))

def normal(mean=0.0, std=1.0, size=None):
    return MockTensor(np.random.normal(mean, std, size))

def mean(tensors, dim=0):
    if isinstance(tensors, list):
        arrays = [t.data for t in tensors]
        return MockTensor(np.mean(arrays, axis=dim))
    return MockTensor(np.mean(tensors.data, axis=dim))

def stack(tensors, dim=0):
    arrays = [t.data for t in tensors]
    return MockTensor(np.stack(arrays, axis=dim))

class no_grad:
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass

class MockModule:
    def __init__(self):
        pass
    
    def parameters(self):
        return []
    
    def state_dict(self):
        return {}

class MockLinear(MockModule):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
    
    def __call__(self, x):
        if isinstance(x, MockTensor):
            x_data = x.data
        else:
            x_data = np.array(x)
        result = np.random.randn(*x_data.shape[:-1], self.out_features)
        return MockTensor(result)

class MockReLU(MockModule):
    def __init__(self):
        super().__init__()
    
    def __call__(self, x):
        if isinstance(x, MockTensor):
            return MockTensor(np.maximum(0, x.data))
        return MockTensor(np.maximum(0, np.array(x)))

class nn:
    Module = MockModule
    Linear = MockLinear
    ReLU = MockReLU