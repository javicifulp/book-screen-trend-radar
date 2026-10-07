import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()
URL = "https://query.wikidata.org/sparql"
HEADERS = {"User-Agent": os.getenv("WIKIDATA_USER_AGENT", "BookScreenTrendRadar/0.1")}
RAW_DIR = Path("data/raw/wikidata")
RAW_DIR.mkdir(parents=True, exist_ok=True)

#película, fecha, ID de Open Library y el ID de IMDb
QUERY = """
SELECT ?adapt ?date ?OL ?IMDb
WHERE {
  ?adapt wdt:P31 wd:Q11424 ; #Entrega el filtro "es una pelicula"
         p:P577/psv: 571 ?date wikibase:timePrecision  ; #Entrega la fecha de estreno
         wdt:P144 ?work ; #Entrega el libro de origen
         wdt:P345 ?IMDb . #Entrega el ID de IMDb de la película como tt...
  ?work wdt:P648 ?OL .    #Entrega el ID de Open Library del libro como OL...W
  FILTER(YEAR(?date) = 2020)
}
LIMIT 20
"""

stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
print("año  total_P144  con_OL  con_OL_e_IMDb  %_con_OL")

for year in range(2018, 2027):
    query = QUERY.replace("{YEAR}", str(year))
    try:
        r = requests.get(URL, params={"query": query, "format": "json"},
                         headers=HEADERS, timeout=70)
        r.raise_for_status()
    except requests.RequestException as e:
        print(year, "falló:", e)
        continue
    data = r.json()
    (RAW_DIR / f"coverage_{year}_{stamp}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    row = data["results"]["bindings"][0]
    total = int(row["total"]["value"])
    con_ol = int(row["con_ol"]["value"])
    con_ol_imdb = int(row["con_ol_imdb"]["value"])
    pct = round(100 * con_ol / total, 1) if total else 0
    print(year, total, con_ol, con_ol_imdb, f"{pct}%")
    time.sleep(2)