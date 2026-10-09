## 1. Definición de "tendencia" (provisional)

Un libro está **en tendencia** en un mes M si se cumplen las dos condiciones:

1. Sus pageviews de Wikipedia en M son **más del doble** del promedio
   mensual de los **12 meses anteriores** a M (sin incluir M).
2. Sus pageviews en M son **≥ 1000**.

- Métrica: pageviews de Wikipedia del artículo del libro, sumadas por mes.
- Por qué B (pico): las tendencias suelen tener un pico y luego se normalizan;
  además permite medir cuánto dura una tendencia.
- Por qué mensual: diluye picos de un solo día (noticias).
- Por qué 12 meses: más estable; evita confundir picos estacionales y
  libros que toman relevancia tiempo después.
- Por qué solo meses anteriores: evitar usar información del futuro.

**Supuestos y pendientes**
- Las pageviews sirven como señal (API de Wikimedia aún sin probar).
- Datos por artículo desde jul-2015 → primer mes evaluable ~jul-2016 (verificar).
- El mínimo de 1000 y el × 2 son provisionales: ajustar en Analytics.
- Un libro sin artículo en Wikipedia no se puede evaluar.

## 2. Qué se predice (provisional)

**Pregunta:** con los datos disponibles hasta una **fecha de corte**, ¿el libro
tendrá una adaptación (película o serie) **estrenada** en los **N = 5 años**
siguientes?

- Target = 1 si el estreno cae dentro de [corte, corte + 5 años); 0 si no.
- Libros adaptados **antes** del corte: se excluyen.
- Features: solo datos anteriores al corte (pageviews, ratings, etc.).
  Nada posterior al corte puede usarse → evita leakage.
- Fecha usada: **estreno** (Wikidata). La fecha de anuncio sería mejor,
  pero Wikidata casi nunca la tiene.
- Rango del corte: entre 2016 (hay pageviews antes) y 2021
  (la ventana de 5 años debe estar completa hoy).

**Por qué fecha de corte y no "X años antes del estreno"**
- Contar desde el estreno solo sirve mirando el pasado: un libro nuevo
  no tiene estreno desde el cual contar.
- Ej.: *La hipótesis del amor* (pub. sep-2021, anuncio oct-2022,
  estreno sep-2026): 3 años antes del estreno ya era después del anuncio.

**Deuda y limitaciones**
- Falta grupo de comparación: libros **no adaptados** → volver a
  Data Engineering (regla 9).
- N = 5 sale de un solo caso: medir en Analytics cuánto tarda
  realmente del anuncio/publicación al estreno.
- Libros publicados poco antes del corte tienen poca historia.

## 3. Criterios de éxito (provisional)

**Objetivo principal:** resultados confiables y un modelo de ML defendible.

| Nivel | Qué debe existir | Cómo se verifica |
|---|---|---|
| Mínimo | Pipeline reproducible: descarga → validación → base de datos | Un comando lo ejecuta de punta a punta sin pasos manuales |
| Esperado | Analytics con hallazgos + modelo que supera un baseline | El modelo gana a la regla "los libros con más pageviews se adaptan" |
| Extra | Radar automatizado en la nube | Se actualiza solo y se ve en un dashboard |

**Confiabilidad**
- Validaciones de calidad en el pipeline.
- Sin leakage: solo datos anteriores a la fecha de corte.
- Evaluación en cortes/años no usados para entrenar.
- Limitaciones y supuestos documentados.

**Punto de control de viabilidad de ML (al cerrar Analytics)**
- Contar libros con target 1 y 0 que tengan pageviews.
- Si hay muy pocos positivos (referencia provisional: < 100), simplificar:
  ranking descriptivo o pregunta más acotada, en vez de forzar el modelo.

## 4. Obligatorio vs. opcional (provisional)

### Fuentes
| Obligatorio | Opcional |
|---|---|
| Wikidata, Open Library, IMDb | NYT Books API (pendiente: revisar términos) |
| Pageviews de Wikimedia (API aún sin probar) | Google Books API (revisar términos) |
| Libros no adaptados como grupo de comparación | |

### Preguntas de Analytics (con fuentes que ya tenemos)
Son candidatas: se validan con los datos disponibles.
1. Género más adaptado, por país de la película y a nivel mundial.
2. Tiempo de publicación a estreno, por género (valida N = 5).
3. Autor ya adaptado antes: ¿aumenta la probabilidad de otra adaptación?
4. Premios literarios: ¿los libros premiados se adaptan más?
5. Película vs. serie: ¿qué géneros van a cada formato?
6. Nota del libro vs. nota de la película (IMDb).
7. Efecto de la adaptación en las pageviews: cuánto suben y cuánto dura.
8. Alcance internacional: ediciones y traducciones (Open Library) y
   pageviews por idioma de Wikipedia.

### Limitaciones conocidas
- "Género más leído por país": sin fuente abierta conocida; el proxy
  es pageviews por idioma, que mide idioma, no país.
- "Buenos ratings no adaptados": es el resultado final del Radar;
  depende del grupo de no adaptados y de la cobertura de ratings.

### Infraestructura y producto
| Obligatorio | Opcional |
|---|---|
| PostgreSQL, Docker, pipeline con validaciones | AWS más allá de lo básico |
| Analytics + punto de control de ML | Radar automatizado |
| Modelo simple + baseline | |