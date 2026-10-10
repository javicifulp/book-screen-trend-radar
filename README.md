# Book → Screen Trend Radar

Proyecto personal, no comercial, de aprendizaje en Data Engineering,
Data Analytics y Machine Learning.

## Pregunta principal

¿Qué libros están mostrando señales de convertirse en la próxima gran
tendencia audiovisual?

En concreto: con los datos disponibles hasta una fecha de corte, ¿qué libros
tendrán una adaptación (película o serie) estrenada en los 5 años siguientes?
Ver `docs/definiciones.md`.

## Estado

**Fase 0: Definición** (casi cerrada, semana 1).

Hecho:
- Descarga de adaptaciones desde Wikidata (2018-2026), con reintentos.
- Cruce Wikidata × Open Library: 662 películas → 584 libros.
- Limpieza de ratings de Open Library (exclusión de bloques anómalos).
- Definiciones de tendencia, target, éxito y alcance.
- Arquitectura y modelo de datos iniciales.

Siguiente: Fase 1, Data Engineering (ingesta de pageviews y libros no adaptados).

## Fuentes de datos

- **Open Library** (dumps mensuales, consultados con DuckDB)
- **Wikimedia** (API de pageviews)
- **Wikidata** (consultas SPARQL)
- **IMDb** (datasets no comerciales, datasets.imdbws.com)

## Arquitectura

Fuentes → `data/raw/` → limpieza con DuckDB → PostgreSQL →
Analytics → ML → Radar.

- **DuckDB:** procesa los dumps grandes (raw → limpio).
- **PostgreSQL:** guarda el modelo de datos final.

Detalle en `docs/arquitectura.md` y `docs/modelo_datos.md`.

## Estructura

- `src/`: ingesta, transformación, analítica y ML
- `data/`: datos locales (no se versionan)
  - `raw/`: archivos tal como llegan de cada fuente
  - `processed/`: datos limpios
- `docs/`: decisiones y documentación
- `sql/`, `notebooks/`, `tests/`, `docker/`

## Cómo preparar el ambiente

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt

Copia `.env.example` a `.env` y completa tus claves.

## Cómo ejecutar

    python src/ingestion/wikidata_list.py        # descarga adaptaciones (Wikidata)
    python src/transformation/cruce_explorar.py  # cruce con Open Library y ratings

Los dumps de Open Library se descargan a mano desde
https://openlibrary.org/developers/dumps y se guardan en `data/raw/`.

## Documentación

- `docs/definiciones.md`: tendencia, target, criterios de éxito y alcance.
- `docs/decisiones.md`: decisiones técnicas, problemas encontrados y pendientes.
- `docs/arquitectura.md`: flujo de datos y rol de cada herramienta.
- `docs/modelo_datos.md`: tablas, grano y claves.

## Fuentes y atribución

- **Open Library** (proyecto del Internet Archive): dumps de ratings y del
  catálogo de obras, descargados desde https://openlibrary.org/developers/dumps
  (versión del 2026-09-30). Uso limitado a fines académicos y de investigación,
  según los términos del Internet Archive.
- **Wikidata**: datos de adaptaciones obtenidos con SPARQL desde
  https://query.wikidata.org (licencia CC0).
- **IMDb**: Information courtesy of IMDb (https://www.imdb.com). Used with permission.
- **Wikimedia pageviews**: pendiente de agregar cuando se use la API
  (confirmar términos).