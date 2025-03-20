from pydantic import BaseModel

from entities.data import Data
from entities.prediction import Prediction


class Anomaly(BaseModel):
    data: Data
    prediction: Prediction
