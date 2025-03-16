import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import httpx

clientId = os.getenv("CLIENT_ID", "YH7ZX3+Jk0e9B0tw+32oqA==")
clientSecret = os.getenv("CLIENT_SECRET", "Wrvh7L7kBEa6J9RSmaNmkw==")
apiGatewayUrl = os.getenv("API_GATEWAY_URL", "https://localhost:7133")
eventHubConnectionString = os.getenv("EVENTHUB_CONNECTIONSTRING", "")

validateTokenApi = "/auth/validateToken"
getTokenApi = "/auth/getToken"
anomalyApi = "/anomaly"

app = FastAPI()

bearer_scheme = HTTPBearer()

async def validateToken(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    async with httpx.AsyncClient() as client:
        response = await client.post(apiGatewayUrl + validateTokenApi, json={"token": credentials.credentials})

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return credentials.credentials

@app.post("/update")
async def update_route(valid_token: str = Depends(validateToken)):
    return {"message": "Access granted to /update endpoint"}

@app.get("/health")
async def health_check():
    return {"status": "FastAPI is Healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

