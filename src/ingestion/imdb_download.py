import time
from datetime import datetime, timezone
from pathlib import Path
import requests
import duckdb

BASE_URL = "https://datasets.imdbws.com/"
FILES = ["title.basics.tsv.gz","title.ratings.tsv.gz"]

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT/"data/raw/imdb"
stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

#Ruta de carpeta
RUN_DIR = RAW_DIR/stamp
RUN_DIR.mkdir(parents=True, exist_ok=True)

#Recorrer la lista
for nombre in FILES:
    URL = BASE_URL + nombre
    destino = RUN_DIR / nombre
    print(URL)
    print(destino)

#Descargar por parte "chunks"
    r = requests.get(URL,stream= True,timeout=30)
    r.raise_for_status()

    with open(destino, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)
        print(nombre,"descargado")
