"""
Main entry point for the FastAPI application.

This module sets up and runs a FastAPI server for AI-driven anomaly detection.
It initializes the Autoencoder model, configures event handling, and exposes
API endpoints for interacting with the system.

Autoencoder model:
    - Looks for a pre-trained model
    - Trains and saves a new model if there isn't one
    - Performs anomaly detection on incoming data
    - Re-trains on data which was incorrectly identified as anomalous

Event handling:
    - Receives events from the data hub
        - Submits received data to the Autoencoder for anomaly detection
        - Sends notification of anomaly detection to the API gateway
    - Receives events from the feedback hub
        - If data was incorrectly determined to be anomalous, submits data
          back to the autoencoder for training.

Endpoints:
    /update - Accepts direct feedback of an incorrect anomaly detection and trains
              the Autoencoder model on the given data.  

    /health - Is used by Azure deployment to verify the app is running.
"""

import asyncio

from fastapi import FastAPI, Depends
import uvicorn

from api_gateway import api_gateway
from autoencoder import Autoencoder
from config import config
from entities.data import Data
from entities.feedback import Feedback
from entities.prediction import Prediction
from eventhub_receiver import EventhubReceiver


# set up the AI

model = Autoencoder(
    torchfile="model.pth",
    training_helper_name="gauss5",
    layer_sizes=[5, 3, 5],
    error_threshold=0.05,
)


# set up event hub listeners

async def handle_data_event(json_data):
    """
    Handle data received from the event hub:
        - Get an anomaly prediction from the AI model
        - Send anomaly notification to the API gateway
    """
    data = Data.from_json(json_data)
    prediction = model.predict(data)
    if prediction.is_anomaly:
        api_gateway.post_anomaly(Prediction(data=data, prediction=prediction))

data_receiver = EventhubReceiver(
    config.eventhub_connectionstring_data,
    config.eventhub_consumergroup_data,
    handle_data_event
)

async def handle_feedback_event(json_data):
    """
    Handle feedback received from the event hub:
        - If the data was a false positive, submit it back
          to the AI model for retraining
    """
    feedback = Feedback.from_json(json_data)
    if not feedback.is_anomaly:
        model.update(feedback.data)

feedback_receiver = EventhubReceiver(
    config.eventhub_connectionstring_feedback,
    config.eventhub_consumergroup_feedback,
    handle_feedback_event
)


# set up API endpoints

app = FastAPI()

@app.post("/update")
async def update(feedback: Feedback, _: str = Depends(api_gateway.validate_token)):
    """Get user feedback, update the AI model on false positive."""
    if not feedback.is_anomaly:
        model.update(feedback.data)

@app.get("/health")
async def health():
    """Are we running?"""
    return {"status": "FastAPI is Healthy"}


# Start services

async def main():
    """Start uvicorn and event hub receivers"""

    async def run_uvicorn():
        config = uvicorn.Config("main:app", host="0.0.0.0", port=8000)
        server = uvicorn.Server(config)
        await server.serve()

    async def run_data_receiver():
        await data_receiver.receive(handle_data_event)

    async def run_feedback_receiver():
        await feedback_receiver.receive(handle_feedback_event)

    await asyncio.gather(run_uvicorn(), run_event_hub_receiver())

if __name__ == "__main__":
    asyncio.run(main())
