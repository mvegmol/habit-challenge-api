import httpx
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


async def get_weather(city: str, api_key: str) -> Optional[Dict]:
    """
    Obtiene datos del clima para una ciudad específica usando OpenWeatherMap API.

    Args:
        city: Nombre de la ciudad
        api_key: API key de OpenWeatherMap

    Returns:
        Dict con temperatura, descripción, humedad y velocidad del viento
        None si hay error en la consulta
    """
    logger.info(f"Consultando clima para ciudad: {city}")
    logger.info(f"API Key presente: {bool(api_key)}")
    logger.info(
        f"API Key (primeros 8 caracteres): {api_key[:8] if api_key else 'None'}..."
    )

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",  # Para obtener temperatura en Celsius
            "lang": "es",  # Descripción en español
        }

        logger.info(f"URL: {url}")
        logger.info(f"Parámetros: {params}")

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            logger.info(f"Status code: {response.status_code}")
            response.raise_for_status()

            data = response.json()
            logger.info(f"Respuesta de la API: {data}")

            result = {
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data.get("wind", {}).get("speed", 0),
            }
            logger.info(f"Datos procesados: {result}")
            return result

    except httpx.HTTPError as e:
        logger.error(f"Error al consultar el clima para {city}: {e}")
        return None
    except KeyError as e:
        logger.error(f"Error en la estructura de datos del clima: {e}")
        return None
    except Exception as e:
        logger.error(f"Error inesperado al consultar el clima: {e}")
        return None
