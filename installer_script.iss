; Script de Inno Setup para YouTube Downloader by DS
; Desarrollado por Daniel Calin Stanus

[Setup]
AppId={{C7A4E3B1-D2B9-487D-9A6A-13A6A4DA43F8}
AppName=YouTube Downloader by DS
AppVersion=1.0.0
AppPublisher=Daniel Calin Stanus
AppPublisherURL=https://github.com/danielstanus/YouTubeDownloader
AppSupportURL=https://github.com/danielstanus/YouTubeDownloader
AppUpdatesURL=https://github.com/danielstanus/YouTubeDownloader
DefaultDirName={autopf}\YouTubeDownloaderDS
DisableProgramGroupPage=yes
; El instalador final se guardará en la carpeta Output del proyecto
OutputDir=C:\YTDS\DS_YouTubeDownloader_Simple\installer_output
OutputBaseFilename=YouTube_Downloader_DS_v1.0.0_Setup
SetupIconFile=C:\YTDS\DS_YouTubeDownloader_Simple\logo.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Ejecutable principal
Source: "C:\YTDS\DS_YouTubeDownloader_Simple\dist\YouTube Downloader by DS.exe"; DestDir: "{app}"; Flags: ignoreversion
; Dependencias incluidas en el ZIP definitivo
Source: "C:\ffmpeg\ffmpeg.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\ffmpeg\ffprobe.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\ffmpeg\yt-dlp.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\YTDS\DS_YouTubeDownloader_Simple\logo.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\YouTube Downloader by DS"; Filename: "{app}\YouTube Downloader by DS.exe"
Name: "{autodesktop}\YouTube Downloader by DS"; Filename: "{app}\YouTube Downloader by DS.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\YouTube Downloader by DS.exe"; Description: "{cm:LaunchProgram,YouTube Downloader by DS}"; Flags: nowait postinstall skipifsilent
