# Decisiones de Fase 0

## 1. Ventana temporal de los datos
- Los ratings de Open Library empiezan en junio de 2018. Solo se pueden
  estudiar adaptaciones estrenadas desde 2018.
- 2018 y 2019 tienen poco volumen (~80-110 ratings/día) y un % de nota 4
  más bajo (18,6 y 19,3) que 2020-2025 (25,9-28,9). Causa desconocida.

## 2. Ratings de Open Library con patrón no orgánico
- Línea base (abril-mayo 2026): 14-36% de nota 4 por semana.
- 2018-2025: % anual de nota 4 entre 18,6 y 28,9. 2026: 92,4.
  Obras/ratings ~0,6-0,7 en 2020-2025 y 0,97 en 2026. 2020 y 2023
  tienen forma normal.
- Proceso sostenido: 13-jun a 7-sep de 2026 (75 días marcados). En julio
  y agosto, ~400 mil ratings, 98% con nota 4 y casi uno por obra, con
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

## 3. Unión entre fuentes
- Cadena probada con un caso (Twilight): película en Wikidata (Q160071) →
  P144 (Q189378) → P648 (OL5720023W) → Open Library. La prueba partió de
  un ID que venía de TMDB, fuente que luego se descartó.
- Cobertura de P648 en las adaptaciones: pendiente de medir.
- Las claves de Open Library vienen como `/works/OL...W`; Wikidata
  entrega `OL...W`. Normalizar antes de unir.
- En los dumps, `\N` es un nulo escrito como texto. Declararlo como nulo
  al leer.

## 4. Fotos del día y series de tiempo
- IMDb (ratings, votos) es una foto del día de la descarga, sin historia.
  Si se quiere una serie propia, guardar copias periódicas de
  `title.ratings` con la fecha en el nombre (pendiente de decidir).
- Las series con historia vienen de los ratings con fecha de Open Library
  (desde jun-2018) y de pageviews de Wikimedia; posiblemente del ranking
  del NYT más adelante.
- Los ratings de Open Library son pocos (Twilight: 448 en total). Usarlos
  como indicador relativo, no como medida del mercado.

## 5. Fuentes y condiciones
Base (uso abierto):
- Wikidata: CC0 (verificado en la página de licencias de Wikimedia).
- Open Library: La página de Licensing del Developer Center dice que el
  Internet Archive no reclama nuevos derechos sobre el material de la base,
  con advertencia de posibles derechos preexistentes en algunas
  contribuciones y jurisdicciones. No nombra una licencia formal, no
  menciona los dumps de ratings/reading log ni impone restricciones de ML.
  Los dumps no traen identificadores de usuario. Riesgo bajo. 
  Pendiente opcional: leer los Terms of Service del Internet Archive.
  Reglas de uso de la API (oct-2026): para volumen usar los dumps; si se
  usa la API, identificarse con User-Agent y correo, máximo 3 req/s,
  guardar en caché, sin scraping de HTML ni cientos de consultas por
  libro. Sin mención de ML.
- Wikimedia pageviews: datasets de Analytics en CC0 salvo indicación
  contraria. Pendiente: confirmar los términos específicos de la API.
Complemento:
- IMDb (datasets gratuitos): solo uso personal y no comercial, sin publicar
  ni crear bases de datos de películas fuera del uso individual; atribución
  con la frase exigida. El artículo de ayuda no menciona ML; no leí la
  licencia completa. Uso privado y local; el modelo debe funcionar sin IMDb.

  Pendientes de revisar: NYT Books API (términos oficiales) y Google Books API.
  Descartadas:
- TMDB: prohíbe usar su contenido en aplicaciones de ML y limita la caché
  a 6 meses. Datos y claves eliminados del proyecto.
- Goodreads: sin API oficial; el scraping contradice las reglas del proyecto.
- API de IMDb (AWS Data Exchange): condiciones desconocidas.