import requests
from pathlib import Path
from datetime import datetime
import os


URL = "https://openlibrary.org/data/ol_dump_works_latest.txt.gz"
#r.url = ol_dump_works_2026-09-30.txt.gz

r = requests.head(URL, allow_redirects=True)
print(r.url)
print(r.headers)
