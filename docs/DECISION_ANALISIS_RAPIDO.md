# Decisión: cómo acelerar el análisis de listas de YouTube

## Problema

Al pegar un enlace de playlist o varios enlaces, la app tarda mucho antes de empezar a descargar.

**Causa:** por cada vídeo, la app lanza una consulta separada a yt-dlp (`-J <url>`) para obtener el título y el autor. Una lista de 100 vídeos son 100 consultas que se hacen una detrás de otra.

Los tiempos de abajo son **estimaciones**. Hay que medirlos en tu equipo antes de decidir (ver la sección final).

---

## Opciones

### Opción A: No cambiar nada

- **Beneficio:** cero riesgo. Los datos son siempre completos.
- **Desventaja:** listas largas siguen tardando mucho.
- **Cuándo elegirla:** si casi nunca descargas listas grandes.

### Opción B: Hacer las consultas en paralelo (3 a la vez)

- **Cómo:** en lugar de una consulta detrás de otra, lanzar 3 a la vez (el mismo límite que ya tienen las descargas).
- **Beneficio:** el tiempo de análisis baja aprox. a un tercio. Es un cambio pequeño y los datos son los mismos.
- **Riesgos:**
  - YouTube puede limitar las peticiones si se hacen demasiadas seguidas (error 429 o "Sign in to confirm you're not a bot").
  - Cada consulta sigue siendo lenta por sí sola.
- **Esfuerzo:** bajo.

### Opción C: Usar los datos de la consulta de la lista y pedir detalles solo si faltan

- **Cómo:** la consulta de la lista (`--flat-playlist -J`) ya devuelve el título y, en muchos casos, el autor de cada vídeo. Solo se haría una consulta extra por vídeo cuando falte algún dato.
- **Beneficio:** en el caso normal, una lista de 100 vídeos tardaría como **una sola consulta** más unas pocas extra. Es la mejora más grande.
- **Riesgos:**
  - Algunos campos (sobre todo el autor) pueden venir vacíos en la consulta de lista, así que habrá casos con consulta extra igualmente.
  - Hay que comprobar que los nombres de autor sean los mismos que antes; si cambian, los archivos descargados tendrían nombres distintos.
- **Esfuerzo:** medio. Hay que probar con varias listas reales.

### Opción D: Combinar C + B

- **Cómo:** usar los datos de la lista y, cuando falte algo, hacer las consultas extra en paralelo (3 a la vez).
- **Beneficio:** es la opción más rápida en el caso general.
- **Riesgos:** los de C, más el riesgo de límite de peticiones de B, pero mucho menor porque se hacen muchas menos consultas.
- **Esfuerzo:** medio-alto.

---

## Comparación rápida

| Opción | Velocidad (lista de 100 vídeos, estimado) | Riesgo | Esfuerzo |
|---|---|---|---|
| A. Sin cambios | ~100 consultas seguidas | Ninguno | Ninguno |
| B. Paralelo (3) | ~33 consultas en tandas | Límite de YouTube | Bajo |
| C. Datos de lista | ~1 consulta + extras necesarias | Datos incompletos o nombres distintos | Medio |
| D. C + B | ~1 consulta + pocas extras en paralelo | Igual que C, menor | Medio-alto |

---

## Qué hay que medir antes de decidir

1. **Tiempo actual:** cronometrar el análisis de una lista real de 20 o 50 vídeos.
2. **Datos de la lista:** comprobar en 2 o 3 listas si la consulta de lista trae título y autor de todos los vídeos.
3. **Límites:** probar la opción B con una lista larga y ver si aparecen errores de YouTube.

## Recomendación inicial

Empezar por la **opción C**. Da la mayor mejora con cambios moderados y no aumenta el número de peticiones a YouTube. Si después sigue siendo lento, añadir la **opción B** encima.

## Decisión

- [ ] A. No cambiar nada
- [ ] B. Paralelo (3)
- [x] C. Datos de la lista, consulta extra solo si falta (implementada en v1.0.3; la prueba de velocidad fue positiva)
- [ ] D. C + B
