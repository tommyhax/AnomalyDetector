from pydantic import BaseModel, Field

from entities.data import Data


class Feedback(BaseModel):
    data: Data
    is_anomaly: bool = Field(alias="isAnomaly")
