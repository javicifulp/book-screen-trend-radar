import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

URL = "https://query.wikidata.org/sparql"
#Leer el User-Agent desde el env. (sin valor por defecto)
user_agent=os.getenv("WIKIDATA_USER_AGENT")

#Si no existe, detener el script con un error claro
if user_agent is None:
    raise RuntimeError("Falta WIKIDATA_USER_AGENT en el archio .env")
                     
HEADERS = {"User-Agent": user_agent}

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT/"data/raw/wikidata"
stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

#Ruta de carpeta
RUN_DIR = RAW_DIR/stamp
RUN_DIR.mkdir(parents=True, exist_ok=True)

# película, fecha, ID de Open Library e ID de IMDb y títulos de Wikipedia (en/es).
QUERY = """
SELECT ?adapt ?date ?OL ?IMDb ?precision ?work ?titulo_en ?titulo_es
WHERE {
  ?adapt wdt:P31 wd:Q11424 ;
         p:P577/psv:P577 ?nodo ;
         wdt:P144 ?work ;
         wdt:P345 ?IMDb .

  ?nodo wikibase:timeValue ?date ;
        wikibase:timePrecision ?precision .

  ?work wdt:P648 ?OL .

  OPTIONAL{
  ?art_en schema:about ?work .
  ?art_en schema:isPartOf <https://en.wikipedia.org/>.
  ?art_en schema:name ?titulo_en .
  }
    # Bloque 2: artículo en español (si existe)
  OPTIONAL {
    ?art_es schema:about ?work .
    ?art_es schema:isPartOf <https://es.wikipedia.org/> .
    ?art_es schema:name ?titulo_es .
  }

  FILTER(YEAR(?date) = {YEAR})
}
"""
print("año  filas peliculas")

for year in range(2018, 2027):

    query = QUERY.replace("{YEAR}", str(year))
    data = None

    #Si falla, entraal except imprime error y espera 30 seg
    #Si el siguiente intento sale bien, data queda con datos y hace break
    #Si llega a "if data is None" y datda tiene datos, NO entra al continue
    #Sigue normal..cuenta pelis y guarda archivo del año

    for intento in range(1,4):
        try:
            r = requests.get(
                URL,
                params={"query": query, "format": "json"},
                headers=HEADERS,
                timeout=70
            )
            r.raise_for_status()
            data = r.json()
            break 
        
        except requests.RequestException as e:
            print(year, "intento",intento, "falló:", e)
            time.sleep(30)
    
    #Se revisa para ver si falló los 3 intentos
    if data is None:
        continue

    
    peliculas= set() #coleccion sin  repetidos

    #Por cada fila de la lista, agrega a peliculas el valor de la película.
    for fila in data["results"]["bindings"]:
        peliculas.add(fila["adapt"]["value"])
        
    cantidad_peliculas= len(peliculas)

    # Guardar respuesta como list_{year}.json dentro de RUN_DIR
    (RUN_DIR / f"list_{year}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    # Cantidad de filas devueltas por Wikidata
    total = len(data["results"]["bindings"])

    print(year, total, cantidad_peliculas)

    time.sleep(2)