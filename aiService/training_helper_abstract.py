"""
Abstract base class for training data providers.

This module defines `TrainingHelper`, an abstract base class (ABC) for
custom training data providers. Subclasses must implement methods for:

- Retrieving training data from various sources (files, event hubs, log streams, etc.).
- Extracting numerical features from raw text-based data.

Classes:
    TrainingHelper (ABC): Base class for training data providers.
"""

from abc import ABC, abstractmethod


class TrainingHelper(ABC):
    """
    Abstract base class for custom training data providers.

    This class defines the interface for retrieving training data and extracting
    numerical features from raw data. Implementing subclasses must provide methods
    for:

    - Fetching training data from a source (e.g., files, event hubs, log streams).
    - Extracting numerical features from text-based or structured data.

    Subclasses should override:
        - `get_data()`: Retrieve raw training data.
        - `extract_features(data)`: Convert raw data into numerical feature vectors.
    """

    @abstractmethod
    def get_data(self):
        """
        Retrieve raw training data.

        Returns: list[Data]: A list of data instances.
        """

    @abstractmethod
    def extract_features(self, data):
        """
        Convert raw data into numerical feature vectors.

        Args:
            data (list[Data] or Data): The input data, which may be a single Data instance
                                       or a list of instances.

        Returns:
            list[list[float]]: A list of feature vectors extracted from the input data.
        """
