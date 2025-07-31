import requests


def buscar_contenido_tmdb(titulo, tipo="movie"):  # tipo puede ser 'movie' o 'tv'
    api_key = "e11b180671fd9354dbe7bb0a8ae26919"
    url = f"https://api.themoviedb.org/3/search/{tipo}"
    params = {
        "api_key": api_key,
        "query": titulo,
        "language": "es-MX"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["results"]:
        resultado = data["results"][0]
        titulo = resultado.get("title") or resultado.get("name")  # 'title' para películas, 'name' para series
        resumen = resultado.get("overview")
        fecha = resultado.get("release_date") or resultado.get("first_air_date")
        imagen = f"https://image.tmdb.org/t/p/w500{resultado.get('poster_path')}" if resultado.get("poster_path") else "Sin imagen"

        print(f"Título: {titulo}")
        print(f"Resumen: {resumen}")
        print(f"Fecha de lanzamiento: {fecha}")
        print(f"Imagen: {imagen}")
    else:
        print("No se encontraron resultados.")


buscar_contenido_tmdb("Inception", tipo="movie")
buscar_contenido_tmdb("Breaking Bad", tipo="tv")


