#vendor adapter with single responsibility - make the HTTP call
import httpx, time, logging
from app.core.config import settings

log = logging.getLogger("weather")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

class OpenWeatherClient:
    def __init__(self, time_ms: int = settings.weather_timeout_ms):
        self._timeout = httpx.Timeout(time_ms / 1000.0)

    async def current_by_city(self, city: str, units: str = "metric") -> dict:
        #The vendor params: q, units, appid
        params = {"q": city, "units": units, "appid": settings.openweather_api_key}


        t0 = time.perf_counter()
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            #retry if failed
            try:
                resp = await client.get(BASE_URL, params=params)
                if resp.status_code >= 500:
                    resp = await client.get(BASE_URL, params=params)
            except httpx.HTTPError as e:
                raise RuntimeError("Upstream_unreachable") from e
            finally:
                log.info("openweather_latency_ms=%d", int((time.perf_counter()-t0)*1000))
            
        if resp.status_code == 404:
            raise ValueError("City_not_found")
        if resp.status_code == 401:
            raise PermissionError("bad_api_key")
        if not resp.is_success:
            raise RuntimeError(f"upstream_error_{resp.status_code}")
        return resp.json()
