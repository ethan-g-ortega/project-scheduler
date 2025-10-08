from app.schemas.weather import WeatherResponse
import time
from app.clients.openweather_client import OpenWeatherClient
from app.core.config import settings

# in-memory cache for POC: {key: {expires_at, payload}}
_cache: dict[str, tuple[float, WeatherResponse]] = {}

class WeatherService:
    def __init__(self, client: OpenWeatherClient | None = None, ttl: int = settings.weather_cache_ttl):
        self.client = client or OpenWeatherClient()
        self.ttl = ttl

    @staticmethod
    def _to_f(c: float) -> float:
        return c * 9 / 5 + 32
    
    def _cache_key(self, city: str, units: str) -> str:
        return f"{city.lower()}|{units}"
    
    async def get_current(self, city: str, units: str ="metric") -> WeatherResponse:
        # Check the cache so we dont waste tokens!
        key = self._cache_key(city, units)
        now = time.time()
        if key in _cache:
            exp, cached = _cache[key]
            if now < exp: 
                return cached.copy(update={"cached": True})
        
        # if not in cache, get from the vendor
        try:
            raw_data = await self.client.current_by_city(city)
        except ValueError as e: #city not found 
            raise self.CityNotFound() from e
        except PermissionError as e:
            raise self.ConfigError() from e
        except RuntimeError as e:
            raise self.UpstreamDown() from e
        
        # Normalize shape
        conditions = (raw_data.get("weather") or [{}])[0].get("description", "unknown").title()
        temp_c = raw_data["main"]["temp"] if units == "metric" else (raw_data["main"]["temp"] - 32) * 5/9
        entity = WeatherResponse(
            city=f'{raw_data.get("name")}, {raw_data.get("sys",{}).get("country","")}'.strip(", "),
            tempC=round(float(temp_c), 1),
            tempF=round(self._to_f(float(temp_c)), 1),
            condition=conditions,
            sourceTs=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(raw_data["dt"])),
            cached=False
        )

        #set cache
        _cache[key] = (now + self.ttl, entity)
        return entity
    
class CityNotFound(Exception):
    pass
class UpstreamDown(Exception):
    pass
class ConfigError(Exception):
    pass
