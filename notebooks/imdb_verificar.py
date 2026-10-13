import duckdb

#Conteo de filas con DuckDB
duckdb.sql(r""" 
    SELECT COUNT(*)
    FROM read_csv('C:/Users/javic/Documents/book-screen-trend-radar/data/raw/imdb/20261013T212529Z/title.ratings.tsv.gz',
    delim= '\t',nullstr= '\N')

""").show()