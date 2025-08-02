import httpx
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


async def get_coordinates_from_city(
    city: str, api_key: str
) -> Optional[Tuple[float, float]]:
    """
    Obtiene las coordenadas (lat, lon) de una ciudad usando Geocoding API.

    Args:
        city: Nombre de la ciudad
        api_key: API key de OpenWeatherMap

    Returns:
        Tuple con (latitud, longitud) o None si hay error
    """
    try:
        url = "https://api.openweathermap.org/geo/1.0/direct"
        params = {"q": city, "limit": 1, "appid": api_key}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            if data and len(data) > 0:
                location = data[0]
                return (location["lat"], location["lon"])
            return None

    except Exception as e:
        logger.error(f"Error al obtener coordenadas para {city}: {e}")
        return None


async def get_weather_v3(city: str, api_key: str) -> Optional[Dict]:
    """
    Obtiene datos del clima usando One Call API 3.0.

    Args:
        city: Nombre de la ciudad
        api_key: API key de OpenWeatherMap

    Returns:
        Dict con temperatura, descripción, humedad y velocidad del viento
        None si hay error en la consulta
    """
    try:
        # Primero obtener coordenadas
        coordinates = await get_coordinates_from_city(city, api_key)
        if not coordinates:
            logger.error(f"No se pudieron obtener coordenadas para {city}")
            return None

        lat, lon = coordinates

        # Llamada a One Call API 3.0
        url = "https://api.openweathermap.org/data/3.0/onecall"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric",  # Para obtener temperatura en Celsius
            "lang": "es",  # Descripción en español
            "exclude": "minutely,hourly,daily,alerts",  # Solo datos actuales
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            current = data["current"]

            return {
                "temperature": current["temp"],
                "description": current["weather"][0]["description"],
                "humidity": current["humidity"],
                "wind_speed": current["wind_speed"],
            }

    except httpx.HTTPError as e:
        logger.error(f"Error al consultar el clima para {city}: {e}")
        return None
    except KeyError as e:
        logger.error(f"Error en la estructura de datos del clima: {e}")
        return None
    except Exception as e:
        logger.error(f"Error inesperado al consultar el clima: {e}")
        return None


# Función compatible con el código existente
async def get_weather(city: str, api_key: str) -> Optional[Dict]:
    """
    Función wrapper para mantener compatibilidad.
    Usa la API 2.5 por defecto, pero puedes cambiar a v3 aquí.
    """
    # Para usar la nueva API 3.0, descomenta la siguiente línea:
    # return await get_weather_v3(city, api_key)

    # API 2.5 (actual) - mantiene compatibilidad
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",
            "lang": "es",
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            return {
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data.get("wind", {}).get("speed", 0),
            }

    except httpx.HTTPError as e:
        logger.error(f"Error al consultar el clima para {city}: {e}")
        return None
    except KeyError as e:
        logger.error(f"Error en la estructura de datos del clima: {e}")
        return None
    except Exception as e:
        logger.error(f"Error inesperado al consultar el clima: {e}")
        return None
