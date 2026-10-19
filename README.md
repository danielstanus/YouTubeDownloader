# YouTube Downloader Simple v1.0.3

Una herramienta sencilla y potente para descargar videos de YouTube en formato audio (MP3 o calidad original) o video (original o MP4) con una interfaz gráfica moderna.

## 📦 Descarga

Descarga el instalador de la última versión desde la página de [Releases](https://github.com/danielstanus/YouTubeDownloader/releases/latest):

1. Ejecuta `YouTube_Downloader_DS_v1.0.3_Setup.exe` y sigue los pasos.
2. Abre la aplicación desde el acceso directo.

*Nota: La aplicación incluye el motor de descarga (yt-dlp) y puede gestionar FFmpeg automáticamente.*

---

## 🚀 Novedades en v1.0.3

- **Análisis de listas más rápido:** se usan los datos que ya trae la lista (título y autor) y solo se consulta a YouTube el vídeo que no los tiene.
- **Cancelar:** botón Cancel para parar las descargas y el análisis de enlaces. Cerrar la ventana de "Processing" también cancela.
- **yt-dlp actualizable:** el botón "Update Source" descarga la última versión de yt-dlp en `%LOCALAPPDATA%\YouTubeDownloaderDS\bin`. La app también la comprueba al arrancar.
- **Aviso de Node.js:** si Node.js no está instalado, la app avisa al arrancar, porque algunos vídeos lo necesitan.
- **Carpeta por defecto:** `Downloads\DS_YouTubeDownloader`.
- **Idioma:** interfaz e instalador en inglés.

## Características

- 🎥 **Descarga de videos**: Soporta múltiples enlaces y playlists a la vez.
- 🎵 **Formatos de audio**: Elige entre MP3 o el formato original de mejor calidad.
- 🎬 **Formatos de video**: Original o MP4, con calidad de 480p a 4K. Puedes guardar también el video al descargar audio.
- 🎨 **Interfaz Moderna**: Utiliza el tema Sun Valley para una apariencia profesional y agradable.
- ⚙️ **Gestión de FFmpeg**: Verifica e instala automáticamente FFmpeg si no está presente en el sistema.
- 📁 **Carpeta de descargas**: Permite elegir fácilmente dónde guardar tus archivos.

## Requisitos

Para usar el instalador no necesitas nada más. Para ejecutar desde el código:

- Windows
- Python 3.12+
- Node.js (recomendado; algunos vídeos de YouTube no funcionan sin él)
- Bibliotecas necesarias (ver `requirements.txt` o instalar manualmente):
  - `tkinter` (incluido en la mayoría de las instalaciones de Python)
  - `sv_ttk`
  - `darkdetect`
  - `pywinstyles`
  - `requests`
  - `yt-dlp`

## Instalación desde el código

1. Clona el repositorio:
   ```bash
   git clone https://github.com/danielstanus/YouTubeDownloader.git
   cd YouTubeDownloader
   ```

2. Instala las dependencias:
   ```bash
   pip install sv-ttk darkdetect pywinstyles requests yt-dlp
   ```

3. Ejecuta la aplicación:
   ```bash
   python DS_YouTubeDownloader.py
   ```

## Generar el instalador

La versión se define en `version.py`. Al generar el instalador, pásala a Inno Setup:

```powershell
python -m PyInstaller --noconfirm DS_YouTubeDownloader.spec
$v = (Select-String -Path version.py -Pattern 'APP_VERSION = "(.+)"').Matches[0].Groups[1].Value
& "C:\Users\Dani\AppData\Local\Programs\Inno Setup 6\ISCC.exe" "/DMyAppVersion=$v" installer_script.iss
```

## Documentación

Los documentos de decisiones y mejoras están en la carpeta [docs](docs/).

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## Autor

**Daniel Calin Stanus**
- GitHub: [@danielstanus](https://github.com/danielstanus)
