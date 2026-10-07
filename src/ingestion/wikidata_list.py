import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

URL = "https://query.wikidata.org/sparql"
HEADERS = {
    "User-Agent": os.getenv(
        "WIKIDATA_USER_AGENT",
        "BookScreenTrendRadar/0.1"
    )
}

RAW_DIR = Path("data/raw/wikidata")
RAW_DIR.mkdir(parents=True, exist_ok=True)

# película, fecha, ID de Open Library e ID de IMDb
QUERY = """
SELECT ?adapt ?date ?OL ?IMDb ?precision
WHERE {
  ?adapt wdt:P31 wd:Q11424 ;
         p:P577/psv:P577 ?nodo ;
         wdt:P144 ?work ;
         wdt:P345 ?IMDb .

  ?nodo wikibase:timeValue ?date ;
        wikibase:timePrecision ?precision .

  ?work wdt:P648 ?OL .

  FILTER(YEAR(?date) = {YEAR})
}
"""

stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

print("año  filas peliculas")

for year in range(2018, 2027):

    query = QUERY.replace("{YEAR}", str(year))

    try:
        r = requests.get(
            URL,
            params={"query": query, "format": "json"},
            headers=HEADERS,
            timeout=70
        )
        r.raise_for_status()
        data = r.json()
        
    except requests.RequestException as e:
        print(year, "falló:", e)
        continue

    
    peliculas= set() #coleccion sin  repetidos

    #Por cada fila de la lista, agrega a peliculas el valor de la película.
    for fila in data["results"]["bindings"]:
        peliculas.add(fila["adapt"]["value"])
        
    cantidad_peliculas= len(peliculas)

    # Guardar respuesta completa
    (RAW_DIR / f"list_{year}_{stamp}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    # Cantidad de filas devueltas por Wikidata
    total = len(data["results"]["bindings"])

    print(year, total, cantidad_peliculas)

    time.sleep(2)