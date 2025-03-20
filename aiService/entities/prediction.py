from pydantic import BaseModel, Field


class Prediction(BaseModel):
    error: float
    is_anomaly: bool = Field(alias="isAnomaly")
