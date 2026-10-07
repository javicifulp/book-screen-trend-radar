import duckdb

RATINGS = "data/raw/openlibrary/ol_dump_ratings_latest.txt.gz"
COLS = "{'work_key':'VARCHAR','edition_key':'VARCHAR','rating':'INTEGER','date':'VARCHAR'}"

con = duckdb.connect()

con.sql(f"""
    SELECT * FROM read_csv('{RATINGS}',
        delim='\\t', header=false, columns={COLS})
    LIMIT 5
""").show()

con.sql(f"""
    SELECT min(date) AS primera ,max (date) AS ultima
    FROM read_csv('{RATINGS}',
        delim='\\t', header=false, columns={COLS})
""").show()

# con.sql(f"""
#     SELECT * FROM read_csv('{RATINGS}',
#         delim='\\t', header=false, columns={COLS})
#     LIMIT 5
# """).show()

# con.sql(f"""
#     SELECT work_key, count(*) AS n, avg(rating) AS promedio
#     FROM read_csv('{RATINGS}',
#         delim='\\t', header=false, columns={COLS})
#     WHERE work_key IN ('/works/OL24829519W', '/works/OL34315810W')
#     GROUP BY work_key
# """).show()

# con.sql(f"""
#     SELECT substr(date, 1, 4) AS anio, count(*) AS n
#     FROM read_csv('{RATINGS}',
#         delim='\\t', header=false, nullstr='\\\\N', columns={COLS})
#     GROUP BY anio
#     ORDER BY anio
# """).show()

# print("Ratings por mes desde 2025")
# con.sql(f"""
#     SELECT substr(date, 1, 7) AS mes, count(*) AS n
#     FROM read_csv('{RATINGS}',
#         delim='\\t', header=false, columns={COLS})
#     WHERE date >= '2025-01'
#     GROUP BY mes
#     ORDER BY mes
# """).show()

# print("Los 10 días con más ratings")
# con.sql(f"""
#     SELECT date, count(*) AS n
#     FROM read_csv('{RATINGS}',
#         delim='\\t', header=false, columns={COLS})
#     GROUP BY date
#     ORDER BY n DESC
#     LIMIT 10
# """).show()

# PICO = "date BETWEEN '2026-07-01' AND '2026-08-31'"
# SRC = f"read_csv('{RATINGS}', delim='\\t', header=false, columns={COLS})"

# print("Ratings y obras distintas: pico vs resto")
# con.sql(f"""
#     SELECT ({PICO}) AS en_pico, count(*) AS ratings,
#            count(DISTINCT work_key) AS obras,
#            round(avg(rating), 2) AS promedio
#     FROM {SRC} GROUP BY en_pico
# """).show()

# print("Distribución de la nota: pico vs resto")
# con.sql(f"""
#     SELECT ({PICO}) AS en_pico, rating, count(*) AS n
#     FROM {SRC} GROUP BY en_pico, rating ORDER BY en_pico, rating
# """).show()

# print("Obras con más ratings durante el pico")
# con.sql(f"""
#     SELECT work_key, count(*) AS n
#     FROM {SRC} WHERE {PICO}
#     GROUP BY work_key ORDER BY n DESC LIMIT 10
# """).show()

# print("Porcentaje de ratings con nota 4, por mes")
# con.sql(f"""
#     SELECT substr(date, 1, 7) AS mes, count(*) AS n,
#            round(100.0 * sum((rating = 4)::INT) / count(*), 1) AS pct_4
#     FROM {SRC} WHERE date >= '2026-04'
#     GROUP BY mes ORDER BY mes
# """).show()

# print("Nota 4 por semana desde abril 2026")
# con.sql(f"""
#     SELECT date_trunc('week', CAST(date AS DATE)) AS semana,
#            count(*) AS n,
#            round(100.0 * sum((rating = 4)::INT) / count(*), 1) AS pct_4
#     FROM {SRC} WHERE date >= '2026-04-01'
#     GROUP BY semana ORDER BY semana
# """).show(max_rows=40)

# print("Días anómalos: más de 50% de nota 4 y al menos 100 ratings")
# con.sql(f"""
#     SELECT date, count(*) AS n,
#            round(100.0 * sum((rating = 4)::INT) / count(*), 1) AS pct_4
#     FROM {SRC} WHERE date >= '2026-04-01'
#     GROUP BY date
#     HAVING count(*) >= 100 AND 100.0 * sum((rating = 4)::INT) / count(*) > 50
#     ORDER BY date
# """).show(max_rows=200)

# print("Bloques anómalos (días marcados separados por <= 7 días se unen)")
# con.sql(f"""
#     WITH marcados AS (
#         SELECT CAST(date AS DATE) AS d
#         FROM {SRC}
#         WHERE date >= '2026-04-01'
#         GROUP BY date
#         HAVING count(*) >= 100
#            AND 100.0 * sum((rating = 4)::INT) / count(*) > 50
#     ),
#     saltos AS (
#         SELECT d, d - LAG(d) OVER (ORDER BY d) AS salto FROM marcados
#     ),
#     bloques AS (
#         SELECT d, sum((salto IS NULL OR salto > 7)::INT)
#                   OVER (ORDER BY d) AS bloque
#         FROM saltos
#     )
#     SELECT bloque, min(d) AS inicio, max(d) AS fin, count(*) AS dias_marcados
#     FROM bloques GROUP BY bloque ORDER BY bloque
# """).show()

# print("Bloques anómalos en toda la historia")
# con.sql(f"""
#     WITH marcados AS (
#         SELECT CAST(date AS DATE) AS d
#         FROM {SRC}
#         GROUP BY date
#         HAVING count(*) >= 100
#            AND 100.0 * sum((rating = 4)::INT) / count(*) > 50
#     ),
#     saltos AS (
#         SELECT d, d - LAG(d) OVER (ORDER BY d) AS salto FROM marcados
#     ),
#     bloques AS (
#         SELECT d, sum((salto IS NULL OR salto > 7)::INT)
#                   OVER (ORDER BY d) AS bloque
#         FROM saltos
#     )
#     SELECT bloque, min(d) AS inicio, max(d) AS fin, count(*) AS dias_marcados
#     FROM bloques GROUP BY bloque ORDER BY bloque
# """).show(max_rows=100)

# print("% de nota 4 y obras distintas por año")
# con.sql(f"""
#     SELECT substr(date, 1, 4) AS anio, count(*) AS n,
#            count(DISTINCT work_key) AS obras,
#            round(100.0 * sum((rating = 4)::INT) / count(*), 1) AS pct_4
#     FROM {SRC} GROUP BY anio ORDER BY anio
# """).show()