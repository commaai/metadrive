"""Minimal gymnasium stubs so metadrive can work without the gymnasium package."""

import numpy as np


class Space:
    """Base space stub."""

    def sample(self):
        raise NotImplementedError

    def contains(self, x):
        return True


class Box(Space):
    def __init__(self, low, high, shape=None, dtype=np.float32):
        self.dtype = np.dtype(dtype)
        if shape is not None:
            self.shape = tuple(shape)
            self.low = np.full(self.shape, low, dtype=self.dtype)
            self.high = np.full(self.shape, high, dtype=self.dtype)
        else:
            self.low = np.asarray(low, dtype=self.dtype)
            self.high = np.asarray(high, dtype=self.dtype)
            self.shape = self.low.shape

    def sample(self):
        return np.random.uniform(self.low, self.high).astype(self.dtype)

    def contains(self, x):
        x = np.asarray(x)
        return x.shape == self.shape and np.all(x >= self.low) and np.all(x <= self.high)


class Discrete(Space):
    def __init__(self, n, start=0):
        self.n = int(n)
        self.start = int(start)

    def sample(self):
        return self.start + np.random.randint(self.n)

    def contains(self, x):
        return isinstance(x, (int, np.integer)) and self.start <= x < self.start + self.n


class MultiDiscrete(Space):
    def __init__(self, nvec):
        self.nvec = np.asarray(nvec, dtype=np.int64)

    def sample(self):
        return np.array([np.random.randint(n) for n in self.nvec])

    def contains(self, x):
        x = np.asarray(x)
        return x.shape == self.nvec.shape and np.all(x >= 0) and np.all(x < self.nvec)


class Dict(Space):
    def __init__(self, spaces=None, **kwargs):
        self.spaces = dict(spaces) if spaces else dict(kwargs)

    def sample(self):
        return {k: v.sample() for k, v in self.spaces.items()}

    def contains(self, x):
        return isinstance(x, dict) and all(k in x and self.spaces[k].contains(x[k]) for k in self.spaces)


class Env:
    """Minimal Env stub — just a base class, no __init__ logic needed."""
    pass


# Expose a 'spaces' namespace so `gym.spaces.Box(...)` etc. work
class _Spaces:
    Space = Space
    Box = Box
    Discrete = Discrete
    MultiDiscrete = MultiDiscrete
    Dict = Dict

    class space:
        Space = Space


spaces = _Spaces()
