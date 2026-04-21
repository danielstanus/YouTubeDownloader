# YouTube Downloader Simple v1.0.0

Una herramienta sencilla y potente para descargar videos de YouTube en formato audio (MP3 o calidad original) con una interfaz gráfica moderna.

## 🚀 Versión v1.0.0 (Actual)
Esta versión incluye:
- Modo oscuro nativo forzado.
- Interfaz mejorada con bordes definidos y feedback visual de foco.
- Optimización de arranque (comprobación de FFmpeg en segundo plano).
- Limpieza inteligente de URLs mediante Regex.
- Soporte de User-Agent de Chrome para evitar bloqueos de YouTube.

## Características

- 🎥 **Descarga de videos**: Soporta múltiples enlaces a la vez.
- 🎵 **Formatos de audio**: Elige entre MP3 o el formato original de mejor calidad.
- 🎨 **Interfaz Moderna**: Utiliza el tema Sun Valley para una apariencia profesional y agradable.
- ⚙️ **Gestión de FFmpeg**: Verifica e instala automáticamente FFmpeg si no está presente en el sistema.
- 📁 **Carpeta de descargas**: Permite elegir fácilmente dónde guardar tus archivos.

## Requisitos

- Python 3.12+
- Bibliotecas necesarias (ver `requirements.txt` o instalar manualmente):
  - `tkinter` (incluido en la mayoría de las instalaciones de Python)
  - `sv_ttk`
  - `darkdetect`
  - `pywinstyles`
  - `requests`
  - `yt-dlp` (necesario para la descarga, asegúrate de tenerlo instalado)

## Instalación

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

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## Autor

**Daniel Calin Stanus**
- GitHub: [@danielstanus](https://github.com/danielstanus)
