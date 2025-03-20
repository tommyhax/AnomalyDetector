"""
TrainingHelper Factory.

This module provides a factory function to dynamically retrieve a `TrainingHelper`
implementation based on a given name. Currently, it supports:

- `gauss5`: Returns an instance of `TrainingHelperGauss5`.

Functions:
    get_training_helper(name: str)
        Factory function that returns the appropriate `TrainingHelper` subclass
        based on the provided name.
"""

from training_helper_abstract import TrainingHelper
from training_helper_gauss5 import TrainingHelperGauss5


def get_training_helper(name: str) -> TrainingHelper:
    """
    Factory function to get a TrainingHelper implementation.

    Args:
        name (str): A short name representing the implementation.

    Raises:
        ValueError: If an unknown name is provided.
    """
    if name == "gauss5":
        return TrainingHelperGauss5()
    raise ValueError(f"Unknown TrainingHelper implementation: {name}")
