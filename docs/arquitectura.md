# Arquitectura (provisional)

## Flujo

Wikidata · Open Library (dumps) · IMDb (datasets) · Wikimedia pageviews (API)
        ↓
Ingesta (src/ingestion/) → data/raw/ (archivos tal como llegan)
        ↓
Transformación y validación con DuckDB (src/transformation/)
        ↓
data/processed/ (datos limpios)
        ↓
Carga en PostgreSQL (modelo de datos final)
        ↓
Vistas/datasets de Analytics (SQL sobre PostgreSQL)
        ↓
Dataset de ML → modelo → predicciones (se guardan en PostgreSQL)
        ↓
Radar (dashboard que lee PostgreSQL)

## Roles de cada base de datos
- **DuckDB:** procesar los dumps grandes (raw → limpio). Lee JSON/CSV
  directo y es rápido para consultas analíticas.
- **PostgreSQL:** guardar el modelo final. Claves y restricciones que
  validan los datos, varias conexiones a la vez (pipeline + dashboard),
  y es la base que usarán Docker (semana 6) y AWS (semana 7).
- Motivo adicional: PostgreSQL es objetivo de aprendizaje de la guía.

## Pendientes
- Formato de data/processed/ (decidir en semana 3-4).
- Cómo se cargan los datos de DuckDB a PostgreSQL (semana 3).
- Herramienta del dashboard (Fase 2).