from uuid import UUID

from pydantic import BaseModel


class Data(BaseModel):
    id: UUID
    timestamp: str
    value: str
