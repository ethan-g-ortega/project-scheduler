from pydantic import BaseModel

class WeatherResponse(BaseModel):
    city: str
    tempC: float
    tempF: float
    condition: str
    sourceTs: str
    source: str = "openweather"
    cached: bool = False