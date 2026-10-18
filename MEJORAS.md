# Mejoras propuestas para YouTube Downloader by DS

Lista de mejoras detectadas al revisar el código tras la versión 1.0.1.

## Prioridad alta

> Estado: puntos 1 a 4 implementados en la rama `mejoras-prioridad-alta`, pendientes de prueba. En el punto 4 no quedaban `except:` desnudos (se eliminaron con la actualización de yt-dlp); se han convertido en registro los fallos que se ocultaban en el log de consola y en la limpieza de archivos temporales.

### 1. Ruta fija del usuario en el `.spec`
- **Dónde:** `DS_YouTubeDownloader.spec`, sección `datas`.
- **Problema:** las rutas de `sv_ttk` apuntan a `C:/Users/Dani/AppData/...`. En otro equipo el build de PyInstaller falla.
- **Propuesta:** obtener la ruta de `site-packages` desde Python en lugar de escribirla a mano.

### 2. Dependencia de Node.js
- **Dónde:** todas las llamadas a yt-dlp usan `--js-runtimes node`.
- **Problema:** si el usuario no tiene Node.js instalado, las descargas pueden fallar sin un mensaje claro.
- **Propuesta:** detectar Node.js al arrancar y avisar al usuario, o incluirlo en el instalador.

### 3. Comandos de yt-dlp duplicados
- **Dónde:** los mismos argumentos (`--user-agent`, `--js-runtimes`) aparecen en unas cuatro partes del código.
- **Problema:** cualquier cambio hay que repetirlo en cada sitio.
- **Propuesta:** crear un helper que construya el comando base y lo reutilice.

### 4. Excepciones desnudas (`except:`)
- **Dónde:** varias en la lógica de PATH y de limpieza de archivos.
- **Problema:** ocultan errores reales.
- **Propuesta:** capturar tipos concretos de excepción y registrarlos en el log.

## Usabilidad

### 5. Botón de cancelar descarga
- **Problema:** si una descarga se atasca o es por error, no hay forma de pararla desde la interfaz.
- **Nota:** no se ha verificado si ya existe alguna forma de cancelar. Confirmar antes de implementar.

### 6. Versión en un solo sitio
- **Dónde:** `VERSION` en `DS_YouTubeDownloader.py` y `AppVersion` / `OutputBaseFilename` en `installer_script.iss`.
- **Problema:** hay que cambiarlas a mano en cada release.
- **Propuesta:** leer la versión desde un único archivo.

### 7. Carpeta de descarga por defecto
- **Dónde:** `C:\DS_YouTubeDownloader` está fijada en el código.
- **Propuesta:** usar la carpeta `Descargas` del usuario, que es lo esperado en Windows.

### 8. Mezcla de idiomas
- **Problema:** hay textos en español y en inglés en la interfaz (por ejemplo, "Update Source" y "Iniciando descargas").
- **Propuesta:** unificar los textos en un solo idioma.

## Mantenimiento

### 9. Ruta fija de FFmpeg
- **Dónde:** el instalador y la lógica de FFmpeg asumen `C:\ffmpeg`.
- **Propuesta:** usar la carpeta de la app o el PATH.

### 10. Modificación del PATH con `setx`
- **Dónde:** función de configuración de PATH.
- **Problema:** `setx` trunca el valor a 1024 caracteres y puede romper el PATH del usuario.
- **Propuesta:** usar la API de Windows o no modificar el PATH.

### 11. Log de consola sin límite
- **Problema:** el log se acumula sin límite (ya hay uno de unos 700 KB en `dist/`).
- **Propuesta:** rotar el log o limpiarlo al arrancar.

### 12. `debug_download.py`
- **Problema:** es un script de pruebas que usa `yt-dlp` del PATH.
- **Propuesta:** moverlo a una carpeta de herramientas o eliminarlo.
