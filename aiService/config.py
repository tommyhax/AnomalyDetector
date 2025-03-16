import os
from types import SimpleNamespace

config = SimpleNamespace(
    ClientId = os.getenv("CLIENT_ID", "YH7ZX3+Jk0e9B0tw+32oqA=="),
    ClientSecret = os.getenv("CLIENT_SECRET", "Wrvh7L7kBEa6J9RSmaNmkw=="),
    ApiGatewayUrl = os.getenv("API_GATEWAY_URL", "https://localhost:7133"),
    EventHubConnectionString = os.getenv("EVENTHUB_CONNECTIONSTRING", "")
)

config.GetTokenApi = config.ApiGatewayUrl + "/auth/getToken"
config.ValidateTokenApi = config.ApiGatewayUrl + "/auth/validateToken"
config.AnomalyApi = config.ApiGatewayUrl + "/anomaly"
