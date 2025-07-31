import requests
from django.conf import settings
from datetime import datetime


def buscar_contenido_tmdb(nombre):
    tipos = [("movie", "pelicula"), ("tv", "serie")]
    resultados = []

    for tipo_api, tipo_valor in tipos:
        url = f"https://api.themoviedb.org/3/search/{tipo_api}"
        params = {
            "api_key": settings.TMDB_API_KEY,
            "query": nombre,
            "language": "es-ES"
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            continue

        datos = response.json().get("results", [])
        for resultado in datos:
            titulo = resultado.get("title") or resultado.get("name")
            resumen = resultado.get("overview")
            fecha_raw = resultado.get("release_date") or resultado.get("first_air_date") or None

            fecha_obj = None
            if fecha_raw:
                try:
                    fecha_obj = datetime.strptime(fecha_raw, "%Y-%m-%d").date()
                except ValueError:
                    fecha_obj = None

            imagen = resultado.get("poster_path")
            imagen_url = f"https://image.tmdb.org/t/p/w500{imagen}" if imagen else ""

            resultados.append({
                "titulo": titulo,
                "resumen": resumen,
                "fecha": fecha_obj,
                "imagen": imagen_url,
                "tipo": tipo_valor  # ← aquí se marca si es película o serie
            })

    return resultados
