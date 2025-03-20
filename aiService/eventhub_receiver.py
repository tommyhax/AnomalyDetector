"""
EventHub Receiver Module.

This module provides an asynchronous event receiver for Azure Event Hub.
It listens for incoming events and processes them using a user-defined JSON handler.

Classes:
    EventhubReceiver: Handles event reception from Azure Event Hub.
"""

import logging

from azure.eventhub.aio import EventHubConsumerClient

class EventhubReceiver:
    """
    Asynchronous receiver for Azure Event Hub.

    This class listens for events from an Azure Event Hub and processes them
    using a callback function provided via the constructor. Events are logged
    and checkpoints are updated to track processed messages.

    Attributes:
        connectionstring (str): Connection String for the event hub
        consumergroup (str): Consumer Group for the event hub
        event_handler: Function to process events when they are received
        logger (logging.Logger): Logger for event processing logs.

    Methods:
        receive(json_handler): Asynchronously receives events, logs the receipt,
                               and calls a provided handler to process them.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, connectionstring: str, consumergroup: str, event_handler):
        self.connectionstring = connectionstring
        self.consumergroup = consumergroup
        self.event_handler = event_handler
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    async def receive(self):
        """
        Receive events from Azure Event Hub.

        This method sets up an `EventHubConsumerClient` to listen for events asynchronously.
        Each received event is processed using the event_handler function.
        """
        client = EventHubConsumerClient.from_connection_string(
            self.connectionstring, self.eventhub_consumergroup
        )

        async def on_event(self, partition_context, event):
            self.logger.info("Received event")
            await partition_context.update_checkpoint(event)
            await self.event_handler(event.body_as_json())

        async with client:
            await client.receive(
                on_event=on_event,
                starting_position="-1",
            )
