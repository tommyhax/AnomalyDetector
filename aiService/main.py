import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import httpx

app = FastAPI()

bearer_scheme = HTTPBearer()

async def validateToken(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    authValidateUrl = os.getenv("AUTH_VALIDATE_URL", "https://localhost:7133/validateToken")

    async with httpx.AsyncClient() as client:
        response = await client.post(authValidateUrl, json={"token": credentials.credentials})

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return token

@app.post("/update")
async def update_route(valid_token: str = Depends(validateToken)):
    return {"message": "Access granted to /update endpoint"}

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)

