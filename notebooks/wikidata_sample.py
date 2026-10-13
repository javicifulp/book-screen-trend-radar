import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()
HEADERS = {"User-Agent": os.getenv("WIKIDATA_USER_AGENT", "BookScreenTrendRadar/0.1")}
RAW_DIR = Path("data/raw/wikidata")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def get_entity(qid):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    entity = r.json()["entities"][qid]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    (RAW_DIR / f"{qid}_{stamp}.json").write_text(
        json.dumps(entity, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return entity


def label(entity):
    return entity["labels"].get("en", {}).get("value")


film = get_entity("Q160071")
print("Película:", label(film))

for claim in film["claims"].get("P144", []):
    snak = claim["mainsnak"]
    if "datavalue" not in snak:
        continue
    book_qid = snak["datavalue"]["value"]["id"]
    book = get_entity(book_qid)
    print("Basada en:", book_qid, label(book))
    print("Propiedades del libro:", sorted(book["claims"].keys()))

    for c in book["claims"].get("P648", []):
        print("P648 valor:", c["mainsnak"]["datavalue"]["value"])
    for c in book["claims"].get("P50", []):
        print("P50 valor (autor):", c["mainsnak"]["datavalue"]["value"]["id"])