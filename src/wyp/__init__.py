"""
WYP? — What's Your Problem?
It's Deterministically Solved!

AUF2026 / FAURE_CORE_2026

Public application interface for the WYP deterministic engine.
"""

from .engine import DeterministicEngine
from .api import solve

__all__ = [
    "DeterministicEngine",
    "solve",
]

__version__ = "1.0.0"
__author__ = "Alain Faure"
__system__ = "WYP? — What's Your Problem? It's Deterministically Solved!"
