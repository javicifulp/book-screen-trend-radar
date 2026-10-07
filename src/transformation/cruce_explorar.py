import duckdb

con = duckdb.connect()

wikidata = "data/raw/wikidata/list_*_20261007T133350Z.json"

con.sql(f"""
    SELECT 
    fila.adapt.value AS adapt, 
    fila.OL.value AS OL, fila.IMDb.value AS IMDb, 
    fila.date.value AS date, 
    fila.precision.value AS precision
    FROM(
    SELECT unnest (results.bindings) AS fila
    FROM read_json ('{wikidata}'))

    LIMIT 5
""").show()
    
con.sql(f"""
    SELECT COUNT(*) FROM (
    SELECT unnest (results.bindings) AS fila
    FROM read_json ('{wikidata}'))
""").show()