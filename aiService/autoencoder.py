"""
Autoencoder for anomaly detection.

This module implements an autoencoder using PyTorch. It supports training,
loading, and evaluating a simple autoencoder model with a 5-3-5 architecture.
The model detects anomalies based on reconstruction error.

Classes:
    - Autoencoder: Defines the encoder-decoder model, training, and inference.
"""

import logging
import os

import numpy as np
import torch
from torch import nn

from entities.anomaly import Anomaly
from entities.data import Data
from factory_training_helper import get_training_helper


class Autoencoder(nn.Module):
    """
    A simple autoencoder model using PyTorch.

    The model consists of:
    - An encoder that reduces input dimensionality.
    - A decoder that reconstructs the input.
    - A training mechanism using Mean Squared Error (MSE) loss.
    - Anomaly detection based on reconstruction error.

    Attributes:
        torchfile (str): Path to save or load the trained model.
        error_threshold (float): Threshold for anomaly detection.
        training_helper_name (TrainingHelper): Utility class for handling training data.
        encoder (nn.Sequential): The encoding layers of the model.
        decoder (nn.Sequential): The decoding layers of the model.
    """

    def __init__(
        self,
        torchfile: str,
        training_helper_name: str,
        layer_sizes: tuple[int, int, int],
        error_threshold: float,
    ):
        """
        Initialize the autoencoder model.

        Args:
            torchfile (str): File path to save/load the trained model.
            traiing_helper_name (str): The name of a TrainingHelper implementation.
            layer_sizes (tuple[int, int, int]): The size of each layer in the autoencoder.
              - layer_sizes[0]: Input size (number of input features).
              - layer_sizes[1]: Hidden layer size (dimensionality of encoded representation).
              - layer_sizes[2]: Output size (should match input size for reconstruction).
            error_threshold (float): The error threshold for anomaly detection.
        """
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.torchfile = torchfile
        self.error_threshold = error_threshold
        self.training_helper = get_training_helper(training_helper_name)
        self.encoder = nn.Sequential(
            nn.Linear(layer_sizes[0], layer_sizes[1]), nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(layer_sizes[1], layer_sizes[2]), nn.Sigmoid()
        )
        self.load_or_new()

    def train_epoch(self, optimizer, criterion, data):
        """
        Train the model for a single epoch.

        Args:
            optimizer (torch.optim.Optimizer): Optimizer for model training.
            criterion (nn.Module): Loss function (e.g., MSELoss).
            data (torch.Tensor): Training data.

        Returns:
            float: The computed loss value for the epoch.
        """
        optimizer.zero_grad()
        output = self(data)
        loss = criterion(output, data)
        loss.backward()
        optimizer.step()
        return loss

    def load_or_new(self):
        """
        Load an existing model or train a new one if none exists.

        If a saved model is found at `self.torchfile`, it is loaded.
        Otherwise, a new model is trained using available training data.
        """
        if os.path.exists(self.torchfile):
            self.logger.info("Loading model")
            self.load_state_dict(torch.load(self.torchfile))
            self.eval()
        else:
            self.logger.info("No model found; training a new one")
            train_data = self.data_helper.get_training_data()
            train_tensor = torch.tensor(train_data, dtype=torch.float32)
            optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
            criterion = nn.MSELoss()
            self.train()
            num_epochs = 50
            for epoch in range(num_epochs):
                loss = self.train_epoch(optimizer, criterion, train_tensor)
                if epoch % 10 == 0:
                    self.logger.info("Epoch %d, Loss: %f", epoch + 1, loss.item())
            self.save()
            self.eval()

    def save(self):
        """
        Save the trained autoencoder model to a file.

        The model's state dictionary is saved to `self.torchfile` using PyTorch's
        `torch.save` method.
        """
        torch.save(self.state_dict(), self.torchfile)
        self.logger.info("Saved %s", self.torchfile)

    def forward(self, x):
        """
        Perform a forward pass through the autoencoder.

        Args:
            x (torch.Tensor): Input data tensor.

        Returns:
            torch.Tensor: Reconstructed output tensor.
        """
        return self.decoder(self.encoder(x))

    def predict(self, data: Data):
        """
        Perform inference using the autoencoder.

        Args:
            data (Data): Input data instance to be passed through the model.

        Returns:
            Anomaly: The reconstruction errortorch.Tensor: The reconstructed output
            from the autoencoder.
        """
        features = self.data_helper.extract_features(data)
        x = torch.tensor([features], dtype=torch.float32)
        reconstructed = self.forward(x).detach().numpy()
        error = np.mean((np.array(features) - reconstructed) ** 2)
        is_anomaly = error > self.error_threshold
        return Anomaly(error=error, is_anomaly=is_anomaly)

    def update(self, data: Data):
        """
        Update the autoencoder model with new training data.

        Args:
            data (Data): New baseline data used to refine the model.

        Raises:
            RuntimeError: If the model update fails.
        """
        self.logger.info("Updating model")
        train_data = self.data_helper.extract_features(data)
        train_tensor = torch.tensor(train_data, dtype=torch.float32)
        optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
        criterion = nn.MSELoss()
        self.train()
        loss = self.train_epoch(optimizer, criterion, train_tensor)
        self.logger.info("Loss: %f", loss.item())
        self.save()
        self.eval()
