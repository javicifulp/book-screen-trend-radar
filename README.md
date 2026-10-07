# Book → Screen Trend Radar

Proyecto personal, no comercial, de aprendizaje en Data Engineering,
Data Analytics y Machine Learning.

## Pregunta principal

¿Qué libros están mostrando señales de convertirse en la próxima gran
tendencia audiovisual?

## Fuentes de datos

- **Open Library** (dumps mensuales, consultados con DuckDB)
- **Wikimedia** (API de pageviews)
- **Wikidata** (consultas SPARQL)
- **IMDb** (datasets no comerciales, datasets.imdbws.com)

## Estado

Fase 0: Definición (fuentes, alcance y criterios de éxito).

## Estructura

- `src/`: ingesta, transformación, analítica y ML
- `data/`: datos locales (no se versionan)
- `docs/`: decisiones y documentación
- `sql/`, `notebooks/`, `tests/`, `docker/`

## Cómo preparar el ambiente

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt

Copia `.env.example` a `.env` y completa tus claves.

## Fuentes y atribución

- **Open Library** (proyecto del Internet Archive): dumps de ratings y del
  catálogo de obras, descargados desde https://openlibrary.org/developers/dumps
  (versión del 2026-09-30). Uso limitado a fines académicos y de investigación,
  según los términos del Internet Archive.
- **Wikidata**: datos de adaptaciones obtenidos con SPARQL desde
  https://query.wikidata.org (licencia CC0).
- **IMDb**: Information courtesy of IMDb (https://www.imdb.com). Used with permission.