import duckdb

con = duckdb.connect()

wikidata = "data/raw/wikidata/list_*_20261008T130410Z.json"



con.sql(f"""
    CREATE TABLE adaptaciones AS
    SELECT 
    fila.adapt.value AS adapt, fila.work.value AS work,
    fila.OL.value AS OL, fila.IMDb.value AS IMDb, 
    fila.date.value AS date, 
    fila.precision.value AS precision
    FROM(
    SELECT unnest (results.bindings) AS fila
    FROM read_json ('{wikidata}'))
""")

#Una fila por pelicula    
con.sql(f"""
    CREATE TABLE peliculas AS
    SELECT adapt, min(year(date)) AS anio, COUNT(*) AS filas
    FROM adaptaciones
    GROUP BY adapt
""")
#Verificacion debe dar 662
# Una fila por película, con su año más temprano (662 filas)
con.sql(f"""
    SELECT COUNT(*) FROM peliculas
""").show()

con.sql(f"""
    CREATE TABLE peliculas_libros AS 
    SELECT DISTINCT adapt, work, '/works/' || OL AS work_key
    FROM adaptaciones
    WHERE OL LIKE 'OL%W'
""")

# con.sql(f"""
#     SELECT COUNT(DISTINCT adapt) FROM peliculas_libros
# """).show()

# con.sql(f"""
#     SELECT OL FROM adaptaciones WHERE OL NOT LIKE 'OL%W' LIMIT 10
# """).show()

RATINGS = "data/raw/openlibrary/ol_dump_ratings_latest.txt.gz"
COLS = "{'work_key':'VARCHAR','edition_key':'VARCHAR','rating':'INTEGER','date':'VARCHAR'}"

con.sql(f"""
    CREATE TABLE ratings AS 
    SELECT work_key, rating, edition_key,CAST(date AS DATE) AS date
    FROM read_csv('{RATINGS}',
        delim='\\t', header=false, nullstr='\\\\N', columns={COLS})
""")

# con.sql(f"""
#     SELECT COUNT(*) FROM ratings
# """).show()


#print("Bloques anómalos en toda la historia")
con.sql(f"""
    CREATE TABLE bloques AS
    WITH marcados AS (
        SELECT CAST(date AS DATE) AS d
        FROM ratings
        GROUP BY date
        HAVING count(*) >= 100
           AND 100.0 * sum((rating = 4)::INT) / count(*) > 50
    ),
    saltos AS (
        SELECT d, d - LAG(d) OVER (ORDER BY d) AS salto FROM marcados
    ),
    numerados AS (
        SELECT d, sum((salto IS NULL OR salto > 7)::INT)
                  OVER (ORDER BY d) AS bloque
        FROM saltos
    )
    SELECT bloque, min(d) AS inicio, max(d) AS fin, count(*) AS dias_marcados
    FROM numerados GROUP BY bloque ORDER BY bloque
""")

# con.sql(f"""SELECT * FROM bloques""").show(max_rows=30)

#Ratings limpios

con.sql(""" 
    CREATE TABLE ratings_limpios AS
    SELECT * FROM ratings
    WHERE NOT EXISTS (
    SELECT 1 FROM bloques
    WHERE ratings.date BETWEEN bloques.inicio AND bloques.fin
    )
""")

# con.sql(f"""SELECT COUNT(*) FROM ratings_limpios""").show()

##608849 ratingslimpios

#Unir libros con ratings, cuantos ratings limpios tienen clave de OL de mis peliculas
#Se unen 2 tablas por la columna que comparten "work_key"
#LEFT JOIN 

# 584 libros
con.sql(f"""
    CREATE TABLE libros_ratings AS
    SELECT pl.work, count(r.work_key) AS n_ratings
    FROM (SELECT DISTINCT work, work_key FROM peliculas_libros) AS pl
    LEFT JOIN ratings_limpios AS r
    ON pl.work_key = r.work_key
    GROUP BY pl.work
""")

# con.sql(f"""SELECT * FROM libros_ratings ORDER BY n_ratings DESC LIMIT 10""").show()
# con.sql(f"""SELECT COUNT(*) FROM libros_ratings""").show()
# con.sql(f"""SELECT * FROM peliculas_libros LIMIT 5""").show()

#El umbral
con.sql(f"""
SELECT
CASE
    WHEN n_ratings = 0 THEN '0'
    WHEN n_ratings < 10 THEN '1-9'
    WHEN n_ratings < 50 THEN '10-49'
    ELSE '50 o más'
END AS rango, COUNT(*) AS libros
FROM libros_ratings
GROUP BY rango
ORDER BY rango
""").show()