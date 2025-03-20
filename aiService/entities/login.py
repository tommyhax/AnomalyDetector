from pydantic import BaseModel, Field

class Login(BaseModel):
    client_id: str = Field(alias="clientId")
    client_secret: str = Field(alias="clientSecret")

    class Config:
        populate_by_name = True
