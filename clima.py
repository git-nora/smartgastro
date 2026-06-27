"""
SmartGastro - Integración API Clima
Consulta el clima actual de la ciudad donde opera el foodtruck
Lassalle Nora
"""

import requests
import os


def obtener_clima(ciudad="Buenos Aires"):
    """
    Consulta la API de OpenWeatherMap y devuelve
    el clima actual de la ciudad indicada.
    Retorna un diccionario con los datos o un mensaje de error.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        return {
            "error": True,
            "mensaje": "API key no configurada"
        }

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={ciudad}&appid={api_key}&lang=es&units=metric"
    )

    try:
        respuesta = requests.get(url, timeout=5)

        if respuesta.status_code == 401:
            return {
                "error": True,
                "mensaje": "API key inválida"
            }

        if respuesta.status_code == 404:
            return {
                "error": True,
                "mensaje": f"Ciudad '{ciudad}' no encontrada"
            }

        if respuesta.status_code != 200:
            return {
                "error": True,
                "mensaje": "Error al consultar el clima"
            }

        datos = respuesta.json()

        descripcion = datos["weather"][0]["description"]
        temperatura = datos["main"]["temp"]
        humedad = datos["main"]["humidity"]
        icono = datos["weather"][0]["icon"]

        # Detectar si hay lluvia o tormenta
        condicion = datos["weather"][0]["main"].lower()
        hay_lluvia = condicion in ["rain", "drizzle", "thunderstorm"]

        return {
            "error": False,
            "ciudad": ciudad,
            "temperatura": round(temperatura, 1),
            "descripcion": descripcion.capitalize(),
            "humedad": humedad,
            "icono": icono,
            "hay_lluvia": hay_lluvia,
            "alerta": "⚠️ Lluvia prevista. Recomendamos reducir la producción de hoy." if hay_lluvia else None
        }

    except requests.exceptions.Timeout:
        return {
            "error": True,
            "mensaje": "El servicio de clima no respondió a tiempo"
        }
    except requests.exceptions.ConnectionError:
        return {
            "error": True,
            "mensaje": "Sin conexión a internet"
        }
    except Exception:
        return {
            "error": True,
            "mensaje": "Error inesperado al consultar el clima"
        }