# Modelo de datos (provisional)

Base: PostgreSQL. Los datos llegan ya limpios desde DuckDB.
Clave del libro: ítem de Wikidata del origen (`work`), decidido en la semana 1.
Las claves de cada fuente (ol_key, titulo_articulo) se traducen a `work`
en la transformación, porque un libro puede tener varias. Así todas las
tablas se unen por `work`. ratings_ol.work = pageviews.work = libros.work

## Tablas del núcleo

### libros
- **Una fila es:** un libro (adaptado o no).
- **Clave:** `work`
- **Columnas:** work, titulo, fecha_publicacion, precision_fecha
- **Fuente:** Wikidata
- **Nota:** no se guarda una columna "adaptado": se obtiene de
  `libros_adaptaciones`, para no tener el mismo dato en dos lugares.

### libros_ol
- **Una fila es:** una clave de obra de Open Library de un libro.
- **Clave:** (work, ol_key)
- **Columnas:** work, ol_key (formato OL...W, normalizado)
- **Fuente:** Wikidata P648, solo claves W
- **Por qué existe:** un libro puede tener varias claves de Open Library.

### libros_wikipedia
- **Una fila es:** el artículo de un libro en una Wikipedia (un idioma).
- **Clave:** (work, idioma)
- **Columnas:** work, idioma, titulo_articulo
- **Fuente:** Wikidata (enlaces a Wikipedia del ítem)
- **Por qué existe:** la API de pageviews pide el título del artículo,
  y el título cambia según el idioma.

### adaptaciones
- **Una fila es:** una película o serie.
- **Clave:** `adaptacion` (ítem de Wikidata)
- **Columnas:** adaptacion, titulo, tipo (película/serie), fecha_estreno,
  precision_fecha, imdb_id
- **Fuente:** Wikidata (+ IMDb para el ID)
- **Nota:** una sola fecha por adaptación (la mínima; regla de
  precisión pendiente, ver decisiones.md sección 3).

### libros_adaptaciones
- **Una fila es:** la relación entre un libro y una adaptación.
- **Clave:** (work, adaptacion)
- **Fuente:** Wikidata P144
- **Por qué existe:** un libro puede tener varias adaptaciones y una
  adaptación puede venir de varios libros.

### ratings_ol
- **Una fila es:** los ratings limpios de un libro en un mes.
- **Clave:** (work, mes)
- **Columnas:** work, mes, n_ratings, nota_1, nota_2, nota_3, nota_4, nota_5
- **Fuente:** dump de ratings de Open Library, unido por `libros_ol`
- **Notas:**
  - Los bloques anómalos se excluyen por día en DuckDB, antes de agrupar.
  - Se guarda la distribución de notas, no solo el promedio.
  - Confiable si el libro tiene ≥ 10 ratings limpios (no se filtra).

### pageviews
- **Una fila es:** las visitas al artículo de un libro, en un mes y un idioma.
- **Clave:** (work, mes, idioma)
- **Columnas:** work, mes, idioma, visitas
- **Fuente:** API de pageviews de Wikimedia (aún sin probar)

## Relaciones

libros ─┬─ libros_ol ──────────── (ratings del dump) → ratings_ol
        ├─ libros_wikipedia ───── (API) → pageviews
        └─ libros_adaptaciones ── adaptaciones

## Pendientes
- Tablas para Analytics: género, autor, premios, ediciones/traducciones.
- Cómo se consigue la lista de libros **no adaptados** (definiciones, parte 2).
- Regla para elegir la fecha según la precisión.