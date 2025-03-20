"""
API Gateway Interface

This module provides authentication and authorization functions for interacting
with the API Gateway. It supports bearer token validation and token retrieval.
"""

import logging

from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx

from config import config
from entities.anomaly import Anomaly
from entities.login import Login


class ApiGateway:
    """
    API Gateway client.

    This class handles authentication and calls to the gateway, and validation of
    tokens sent by our own API clients.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.login = Login(
            client_id=config.client_id, client_secret=config.client_secret
        )

    async def validate_token(
        self, credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())
    ):
        """
        Validate the bearer token of a connecting client.

        Args:
            credentials (HTTPAuthorizationCredentials): The HTTP Bearer token to validate.

        Returns:
            str: The valid token if authentication is successful.

        Raises:
            HTTPException: If token validation fails.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                config.token_validate_api, json={"token": credentials.credentials}
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Token validation failed"
            )

        return credentials.credentials

    async def get_token(self):
        """
        Authenticate and obtain a bearer token from the gateway.

        Returns:
            str: A new bearer token if authentication is successful.

        Raises:
            HTTPException: If authenticatin fails.
        """
        async with httpx.AsyncClient as client:
            response = await client.post(
                config.token_get_api, json=self.login.model_dump()
            )

            if response.status_code == 200:
                return response.json()["access_token"]

            raise httpx.HTTPStatusError(
                f"Failed to retrieve token: {response.text}",
                request=response.request,
                response=response,
            )

    async def post_anomaly(self, anomaly: Anomaly):
        """
        Send an anomaly notification via the gateway.

        Args:
            Anomaly: The notification payload.

        Raises:
            HTTPException: If the attempt fails.
        """
        token = await self.get_token()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                config.anomaly_api,
                json=anomaly,
                headers={"Authorization": f"Bearer {token}"},
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Anomaly notification failed"
            )


api_gateway = ApiGateway()
