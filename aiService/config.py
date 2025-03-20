"""
Set up configuration from the environment or default values
"""

import os
from types import SimpleNamespace

DEFAULT_CLIENT_ID = "YH7ZX3+Jk0e9B0tw+32oqA=="
DEFAULT_CLIENT_SECRET = "Wrvh7L7kBEa6J9RSmaNmkw=="
DEFAULT_API_GATEWAY_URL = "https://localhost:7133"
DEFAULT_EVENTHUB_CONNECTIONSTRING = ""
DEFAULT_EVENTHUB_CONSUMERGROUP = "$Default"

config = SimpleNamespace(
    client_id=os.getenv("CLIENT_ID", DEFAULT_CLIENT_ID),
    client_secret=os.getenv("CLIENT_SECRET", DEFAULT_CLIENT_SECRET),
    api_gateway_url=os.getenv("API_GATEWAY_URL", DEFAULT_API_GATEWAY_URL),
    eventhub_connectionstring_data=os.getenv(
        "EVENTHUB_CONNECTIONSTRING", DEFAULT_EVENTHUB_CONNECTIONSTRING
    ) + f";EntityPath=data",
    eventhub_connectionstring_feedback=os.getenv(
        "EVENTHUB_CONNECTIONSTRING", DEFAULT_EVENTHUB_CONNECTIONSTRING
    ) + f";EntityPath=feedback",
    eventhub_consumergroup_data=os.getenv(
        "EVENTHUB_CONSUMERGROUP_DATA", DEFAULT_EVENTHUB_CONSUMERGROUP
    ),
    eventhub_consumergroup_feedback=os.getenv(
        "EVENTHUB_CONSUMERGROUP_FEEDBACK", DEFAULT_EVENTHUB_CONSUMERGROUP
    ),
)

config.token_get_api = config.api_gateway_url + "/auth/getToken"
config.token_validate_api = config.api_gateway_url + "/auth/validateToken"
config.anomaly_api = config.api_gateway_url + "/anomaly"

