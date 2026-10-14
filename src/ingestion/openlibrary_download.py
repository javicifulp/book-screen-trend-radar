import requests
from datetime import datetime, timezone
from pathlib import Path


URL_RATINGS = "https://openlibrary.org/data/ol_dump_ratings_latest.txt.gz"


ROOT = Path(__file__).resolve().parents[2]
RAW_OL = ROOT/"data/raw/openlibrary"
print(RAW_OL)
stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


#Solicitar los headers
r = requests.head(URL_RATINGS,allow_redirects=True, timeout=10)
r.raise_for_status()
print(r.url)

#Sacar nombre real
nombre = Path(r.url).name
url_version = r.url
print(nombre)

#Buscar si ya existe
existentes = list(RAW_OL.glob(f"*/{nombre}"))
print(existentes)

if existentes:
    print("Ya existe")
else:
    RUN_DIR = RAW_OL/stamp
    RUN_DIR.mkdir(parents=True, exist_ok=True)

    destino = RUN_DIR/nombre
    print(destino)

    r = requests.get(url_version,stream= True,timeout=30)
    r.raise_for_status()

    with open(destino, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)
        print(nombre,"descargado")

