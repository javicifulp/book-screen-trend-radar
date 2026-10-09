# Decisiones de Fase 0

Definiciones de Fase 0: ver docs/definiciones.md

## 1. Ventana temporal de los datos
- Los ratings de Open Library empiezan en junio de 2018. Solo se pueden
  estudiar adaptaciones estrenadas desde 2018.
- 2018 y 2019 tienen poco volumen (~80-110 ratings/día) y un % de nota 4
  más bajo (18,6 y 19,3) que 2020-2025 (25,9-28,9). Causa desconocida.
- 2026 está incompleto (año en curso): sus conteos no son comparables
  con años completos.

## 2. Ratings de Open Library con patrón no orgánico
- Línea base (abril-mayo 2026): 14-36% de nota 4 por semana.
- 2018-2025: % anual de nota 4 entre 18,6 y 28,9.
  2026: 92,4.
  Obras/ratings ~0,6-0,7 en 2020-2025 y 0,97 en 2026.
  2020 y 2023 tienen forma normal.
- Proceso sostenido: 13-jun a 7-sep de 2026 (75 días marcados).
  En julio y agosto, ~400 mil ratings, 98% con nota 4 y casi uno por obra, con
  picos de ~12 mil por día. Origen desconocido.
- Ráfaga: 18-20 de mayo de 2026 (3.915 ratings el día 20, 97,1% nota 4).
- Desde la semana del 7 de septiembre vuelve a ~30-40% de nota 4.

**Regla de exclusión:** un día es anómalo si tiene al menos 100 ratings
y más de 50% de nota 4. Los días marcados separados por 7 días o menos
se unen en un bloque, y se excluye el bloque completo (inicio a fin),
incluidos los días intermedios que no superan el umbral.

**Resultado sobre toda la historia (25 bloques):**
- 2018-2020: ninguno.
- 2021-2025: 19 bloques, casi todos de 1 día y aislados (probables
  importaciones individuales; hipótesis).
- 2026: 13-16 mar, 1-abr, 28-abr, 18-20 may, 13-jun a 7-sep, 29-sep.

**Limitaciones:**
- La regla tiene poca potencia en 2018-2019 (volumen diario bajo 100).
- Solo detecta concentración en la nota 4.
- Los promedios no detectan el problema; la distribución de notas sí.
- La agregación mensual ocultó la forma real. Mirar semanal para ubicar
  y diario para fijar bordes.

**Para el pipeline:** los bloques se calculan en cada ejecución, no se
fijan a mano.

**Pendiente:** recalcular 2026 tras excluir los bloques y comprobar que
el % de nota 4 vuelve a ~30%.

## 3. Wikidata: lista de adaptaciones
- Descarga por año (2018-2026) con `src/ingestion/wikidata_list.py`: un
  JSON crudo por año en `data/raw/wikidata/`, con película, fecha,
  precisión, ID de Open Library e ID de IMDb.
- Wikidata puede devolver código 200 con el JSON cortado: el script lo
  informa y sigue con el siguiente año.
- Exigir IMDb deja fuera películas sin ese ID.
- Riesgo detectado: min() sin considerar la precisión elige la fecha falsa.
  Caso Q2095178: tiene 2018-01-01 (precisión 9, solo año) y 2018-09-27
  (precisión 11, día exacto); min() elige 2018-01-01. Pendiente: definir
  cómo elegir la fecha según la precisión.
- 1719 filas -> 662 películas; 151 apariciones repetidas entre años
-Wikidata a veces corta la respuesta (ya pasó en 2022 y 2024).
- Hoy 08/10/2026 un fallo obliga a repetir toda la descarga para mantener un solo stamp.
- Pendiente para el pipeline: reintentos automáticos por año.
- Año de adaptación = min(year(date)), válido con cualquier precisión. Fecha exacta (precisión 11): pendiente para Analytics."

**Duplicados**
- Hay aprox. 2 filas por película (rango 1,8-2,5 según el año) por varias
  fechas, obras o IDs: deduplicar antes del cruce.
- Una película puede aparecer en más de un año (estrenos en distintos
  países), así que los conteos por año no se pueden sumar.
- Método: descargar por año tal cual y quitar duplicados con DuckDB
  (GROUP BY + min() sobre la fecha). Riesgo conocido: filtrar por año en
  la consulta puede falsear la fecha mínima. Alternativa pendiente:
  calcular el mínimo en la propia consulta SPARQL.
  -1719 filas → 662 películas distintas (2018-2026, con OL e IMDb).
  -La suma de distintas por año da 813: 151 apariciones son la misma película en más de un año.

**Fechas de estreno (P577)**
- Tienen precisión variable (9 = año, 10 = mes, 11 = día). Caso
  Q67630363: solo año; la consulta lo muestra como 1 de enero.
- Hay que consultar la precisión (psv:P577 → wikibase:timePrecision) y no
  usar como fecha exacta las de precisión de año.
- Pendiente: medir el porcentaje por precisión y decidir el tratamiento.

**Origen de la adaptación (P144)**
- P144 incluye orígenes que no son libros (cuentos populares, teatro,
  cómics, etc.). Pendiente: medir qué tipos de origen hay y si hace falta
  un filtro por tipo.
- Caso Q63994491 (Gretel & Hansel): una sola declaración "based on"
  (Hansel and Gretel, un cuento, sin referencias). Los dos IDs de Open
  Library vendrían del ítem de origen (por verificar).

## 4. Unión entre fuentes
- Cadena probada con un caso (Twilight): película en Wikidata (Q160071) →
  P144 (Q189378) → P648 (OL5720023W) → Open Library. La prueba partió de
  un ID que venía de TMDB, fuente que luego se descartó.
- Cobertura de P648 en las adaptaciones: pendiente de medir.
- P648 admite IDs de obra (W), edición (M) y autor (A): filtrar por W.
- Las claves de Open Library vienen como `/works/OL...W`; Wikidata
  entrega `OL...W`. Normalizar antes de unir.
- En los dumps, `\N` es un nulo escrito como texto. Declararlo como nulo
  al leer.
- Decisión provisional: la clave del libro es el ítem de Wikidata del
  origen (`?work`), no el ID de Open Library; los OL IDs son atributos.
- Q63994491: sus 2 claves de Open Library (OL24829519W, OL34315810W) tienen
  0 ratings en el dump. Decisión: filtro de calidad por mínimo de ratings.
 
**Resultado del cruce (oct-2026)**
- 1719 filas → 662 películas → 619 con clave W → 584 libros (agrupados por `work`).
- 43 películas (6,5 %) quedan fuera por no tener clave W; en la muestra revisada
  son claves de edición (M). Recuperables con el dump de ediciones (pendiente).
- Ratings limpios: 608.849 de 1.060.973 (se excluyen 452.124 de los 25 bloques).
- Ratings limpios por libro: 0 → 241 (41 %); 1-9 → 182 (31 %);
  10-49 → 94 (16 %); 50 o más → 67 (11,5 %).

**Decisión de umbral:** el rating de un libro se considera confiable con
≥ 10 ratings limpios (161 libros). El umbral no excluye libros: los 584 se
mantienen, y bajo 10 el rating queda como "sin dato confiable".

**Implicancia:** los ratings de Open Library no alcanzan como señal principal.
Probablemente la principal será pageviews de Wikimedia (por confirmar).

**Trampa del JOIN:** unir con una tabla que tiene filas repetidas infla los
conteos sin dar error (un libro con dos películas contaba sus ratings dos veces).
Solución: `SELECT DISTINCT work, work_key` antes de unir.

**Año de adaptación:** min(year(date)), válido con cualquier precisión.
Fecha exacta (precisión 11): pendiente para Analytics.

**Hipótesis "rating alto → más probable que se adapte":** no se puede comprobar
solo con libros adaptados (falta un grupo de comparación) y tiene riesgo de
leakage (muchos ratings son posteriores al estreno). Llevarla a la definición
de "tendencia" y de qué se predice.

## 5. Fotos del día y series de tiempo
- IMDb (ratings, votos) es una foto del día de la descarga, sin historia.
  Si se quiere una serie propia, guardar copias periódicas de
  `title.ratings` con la fecha en el nombre (pendiente de decidir).
- Las series con historia vienen de los ratings con fecha de Open Library
  (desde jun-2018) y de pageviews de Wikimedia; posiblemente del ranking
  del NYT más adelante.
- Los ratings de Open Library son pocos (Twilight: 448 en total). Usarlos
  como indicador relativo, no como medida del mercado.

## 6. Fuentes y condiciones

### Base (uso abierto)
- **Wikidata:** CC0 (verificado en la página de licencias de Wikimedia).
- **Open Library:**
  - La página de Licensing del Developer Center dice que el Internet
    Archive no reclama nuevos derechos sobre el material de la base, con
    advertencia de posibles derechos preexistentes en algunas
    contribuciones y jurisdicciones. No nombra una licencia formal, no
    menciona los dumps de ratings/reading log ni impone restricciones de ML.
  - Términos de uso del Internet Archive (leídos oct-2026; aplican porque
    los dumps se descargan desde archive.org):
    - El acceso se otorga solo para fines académicos y de investigación.
      El uso actual (aprendizaje, portfolio) calza. El uso comercial no
      está cubierto: habría que pedir permiso o revisar de nuevo los
      términos. Como no calza del todo con la página de Licensing, se
      toma el texto más restrictivo. **Limitación conocida.**
    - Prohíbe recolectar o guardar datos personales. Los dumps no traen
      identificadores de usuario, así que se cumple. No agregar datos de
      usuarios desde ninguna fuente.
    - Pide (no exige) citar al Archive en publicaciones. Decisión: citar
      al Internet Archive / Open Library en el README.
  - Riesgo bajo para el uso actual.
  - Reglas de uso de la API (oct-2026): para volumen usar los dumps; si se
    usa la API, identificarse con User-Agent y correo, máximo 3 req/s,
    guardar en caché, sin scraping de HTML ni cientos de consultas por
    libro. Sin mención de ML.
- **Wikimedia pageviews:** datasets de Analytics en CC0 salvo indicación
  contraria. Pendiente: confirmar los términos específicos de la API.

### Complemento
- **IMDb (datasets gratuitos):** solo uso personal y no comercial, sin
  publicar ni crear bases de datos de películas fuera del uso individual;
  atribución con la frase exigida. El artículo de ayuda no menciona ML; no
  leí la licencia completa. Uso privado y local; el modelo debe funcionar
  sin IMDb.

### Pendientes de revisar
- NYT Books API (términos oficiales).
- Google Books API.

### Descartadas
- **TMDB:** prohíbe usar su contenido en aplicaciones de ML y limita la
  caché a 6 meses. Datos y claves eliminados del proyecto.
- **Goodreads:** sin API oficial; el scraping contradice las reglas del
  proyecto.
- **API de IMDb (AWS Data Exchange):** condiciones desconocidas.

### Atribución
- El README tendrá una sección "Fuentes y atribución" con cada fuente y lo
  que pide: Internet Archive / Open Library (cita), IMDb (frase exigida),
  Wikidata (CC0, cita opcional como buena práctica).

## 7. Resumen de pendientes
- Recalcular 2026 sin bloques anómalos (sección 2).
- Medir el porcentaje de fechas por precisión (sección 3).
- Medir los tipos de origen en P144 (sección 3).
- Decidir si el mínimo de fecha se calcula en SPARQL (sección 3).
- Medir la cobertura de P648 (sección 4).
- Decidir si se guardan copias periódicas de IMDb (sección 5).
- Confirmar términos de la API de pageviews (sección 6).
- Revisar NYT Books API y Google Books API (sección 6).
- Crear la sección "Fuentes y atribución" en el README (sección 6).
- Conseguir libros no adaptados como grupo de comparación (definiciones, parte 2).
- Probar la API de pageviews de Wikimedia (definiciones, parte 1).
- Medir el tiempo de publicación/anuncio a estreno para validar N = 5.
