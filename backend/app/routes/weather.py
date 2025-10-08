# FastAPI router (request/response schemas)
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.weather import WeatherResponse
from app.services.weather_service import WeatherService

router = APIRouter(prefix="/api", tags=["weather"])

@router.get("/weather/", response_model=WeatherResponse)
async def get_weather(city: str=Query(..., min_length=1), units: str = Query("metric", pattern="^(metric|imperial)$")):
    svc = WeatherService()
    try:
        return await svc.get_current(city=city, units=units)
    except WeatherService.CityNotFound:
        raise HTTPException(status_code=422, detail="Invalid or unknown city")
    except WeatherService.UpstreamDown:
        raise HTTPException(status_code=503, detail="Weather provider unavailable")
    except WeatherService.ConfigError:
        raise HTTPException(status_code=500, detail="Server misconfigured (API Key)")