import os
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sv_ttk
import re
import logging
import json
import darkdetect
import pywinstyles
import winreg
import zipfile
import requests
from collections import deque


class YouTubeDownloader:
    VERSION = "v1.0.0"

    def __init__(self, master):

        self.master = master
        master.title(f"YouTube Downloader by Daniel Calin Stanus - {self.VERSION}")
        master.geometry("1200x900")

        # Set window icon
        try:
            icon_path = resource_path("logo.ico")
            if os.path.exists(icon_path):
                master.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error loading icon: {e}")

        self.center_window()

        # Force Dark Mode Theme
        try:
            sv_ttk.set_theme("dark")
        except Exception as e:
            print(f"Error applying theme in init: {e}")

        # Logging setup
        logging.basicConfig(filename='YouTube_Downloader_by_DS.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        # Check and install FFmpeg in a background thread to not block UI
        threading.Thread(target=self.check_and_install_ffmpeg, daemon=True).start()

        # Create UI
        self.create_widgets()
        self._console_buffer = deque(maxlen=800)
        self._console_log_path = os.path.join(os.path.abspath("."), "console_output.log")

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # YouTube Link Section
        links_label = ttk.Label(main_frame, text="🔗 YouTube Links (one per line):", font=("Helvetica", 16))
        links_label.pack(anchor="w", pady=(0, 5))

        # Container for Text area to simulate borders
        text_container = tk.Frame(main_frame, bg="#333333", padx=1, pady=1)
        text_container.pack(fill="x", pady=(0, 10))

        # Add version label at bottom right of main frame
        version_label = ttk.Label(main_frame, text=self.VERSION, font=("Helvetica", 8), foreground="#666666")
        version_label.place(relx=1.0, rely=1.0, anchor="se", x=15, y=15)

        self.entrada_enlaces = tk.Text(
            text_container,
            height=5,
            font=("Consolas", 14),
            bg="#1c1c1c",
            fg="#ffffff",
            insertbackground="white",
            padx=10,
            pady=10,
            borderwidth=0,
            highlightthickness=1,
            highlightbackground="#333333",
            highlightcolor="#0078d4"  # Windows blue color when focused
        )
        self.entrada_enlaces.pack(fill="x")

        # Download Folder Section
        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(folder_frame, text="📁  Download Folder:", font=("Helvetica", 14)).pack(side="left")

        self.entrada_carpeta = ttk.Entry(folder_frame, width=50)
        self.entrada_carpeta.pack(side="left", padx=(10, 5), expand=True, fill="x")

        # Browse button
        ttk.Button(
            folder_frame,
            text="Browse",
            command=self.browse_folder
        ).pack(side="left")

        # Fixed default download folder
        default_folder = r"C:\DS_YouTubeDownloader"
        os.makedirs(default_folder, exist_ok=True)
        self.entrada_carpeta.insert(0, default_folder)

        # Audio Format
        format_frame = ttk.Frame(main_frame)
        format_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(format_frame, text="🎵  Audio Format:", font=("Helvetica", 14)).pack(side="left")

        self.var_formato = tk.IntVar(value=1)
        ttk.Radiobutton(
            format_frame,
            text="MP3",
            variable=self.var_formato,
            value=1
        ).pack(side="left", padx=(10, 5))

        ttk.Radiobutton(
            format_frame,
            text="Original (best)",
            variable=self.var_formato,
            value=2
        ).pack(side="left")

        # Audio Quality
        quality_frame = ttk.Frame(main_frame)
        quality_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(quality_frame, text="🎵  Audio Quality:", font=("Helvetica", 14)).pack(side="left")

        self.var_calidad = tk.IntVar(value=1)
        quality_options = [
            ("Maximum", 1),
            ("128K", 2),
            ("192K", 3)
        ]

        for text, value in quality_options:
            ttk.Radiobutton(
                quality_frame,
                text=text,
                variable=self.var_calidad,
                value=value
            ).pack(side="left", padx=5)

        # Additional Options
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(options_frame, text="⚙️ Additional Options:", font=("Helvetica", 14)).pack(side="left")

        self.var_metadatos = tk.IntVar(value=1)
        ttk.Checkbutton(
            options_frame,
            text="Include Metadata",
            variable=self.var_metadatos
        ).pack(side="left", padx=(10, 5))

        self.var_miniatura = tk.IntVar(value=1)
        ttk.Checkbutton(
            options_frame,
            text="Include Thumbnail",
            variable=self.var_miniatura
        ).pack(side="left")

        # Video Format
        video_frame = ttk.Frame(main_frame)
        video_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(video_frame, text="🎥  Video Format:", font=("Helvetica", 14)).pack(side="left")

        self.var_video_format = tk.IntVar(value=0)
        ttk.Radiobutton(
            video_frame,
            text="Audio Only",
            variable=self.var_video_format,
            value=0
        ).pack(side="left", padx=(10, 5))

        ttk.Radiobutton(
            video_frame,
            text="Original Video",
            variable=self.var_video_format,
            value=1
        ).pack(side="left", padx=(5, 5))

        ttk.Radiobutton(
            video_frame,
            text="MP4",
            variable=self.var_video_format,
            value=2
        ).pack(side="left", padx=(5, 5))

        # Keep original video option
        self.var_keep_video = tk.IntVar(value=0)
        ttk.Checkbutton(
            video_frame,
            text="Keep Original Video",
            variable=self.var_keep_video
        ).pack(side="left", padx=(20, 5))

        # Video Quality
        video_quality_frame = ttk.Frame(main_frame)
        video_quality_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(video_quality_frame, text="🎥  Video Quality:", font=("Helvetica", 14)).pack(side="left")

        self.var_video_quality = tk.StringVar(value="max")
        quality_options = [
            ("Maximum", "max"),
            ("4K", "2160"),
            ("2K", "1440"),
            ("1080p", "1080"),
            ("720p", "720"),
            ("480p", "480")
        ]

        for text, value in quality_options:
            ttk.Radiobutton(
                video_quality_frame,
                text=text,
                variable=self.var_video_quality,
                value=value
            ).pack(side="left", padx=5)


        # Progress Frame
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill="x", pady=(10, 10))

        self.progress_label = ttk.Label(progress_frame, text="", font=("Helvetica", 12))
        self.progress_label.pack(side="top", fill="x")

        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=100, mode="determinate")
        self.progress_bar.pack(side="top", fill="x")

        # Buttons Frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill="x", pady=(10, 10))

        # Update YT-DLP Button
        self.update_button = ttk.Button(
            buttons_frame,
            text="Update Source",
            command=self.update_ytdlp
        )
        self.update_button.pack(side="left", padx=(0, 10))

        # Open Folder Button
        ttk.Button(
            buttons_frame,
            text="📂 Open Folder",
            command=self.open_download_folder
        ).pack(side="left", padx=(0, 10))

        # Download Button
        self.download_button = ttk.Button(
            buttons_frame,
            text="📥 Start Download",
            command=self.iniciar_descarga,
            style='Accent.TButton'
        )
        self.download_button.pack(side="left", expand=True)

        # Downloaded Songs Treeview
        songs_frame = ttk.Frame(main_frame)
        songs_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        ttk.Label(songs_frame, text="📋 Downloaded Songs:", font=("Helvetica", 14)).pack(anchor="w")

        # Limit height of songs treeview so console has space
        self.songs_tree = ttk.Treeview(
            songs_frame,
            columns=('Title', 'Status'),
            show='headings',
            height=6
        )

        # Define column headings
        self.songs_tree.heading('Title', text='  Song Title', anchor='w')
        self.songs_tree.column('Title', width=300)
        self.songs_tree.heading('Status', text='  Status', anchor='w')
        self.songs_tree.column('Status', width=150, stretch=False)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            songs_frame,
            orient="vertical",
            command=self.songs_tree.yview
        )
        self.songs_tree.configure(yscroll=scrollbar.set)

        self.songs_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Error Label
        self.error_label = ttk.Label(
            main_frame,
            text="",
            foreground="red"
        )
        self.error_label.pack(fill="x", pady=5)

        # Integrated Console Frame
        self.show_console_var = tk.IntVar(value=0)
        ttk.Checkbutton(
            buttons_frame,
            text="Show Console",
            variable=self.show_console_var,
            command=self.toggle_console
        ).pack(side="right")

        self.console_frame = ttk.Frame(main_frame)
        # start hidden; user can enable it
        # self.console_frame.pack(fill="both", expand=True, pady=(10, 0))

        ttk.Label(self.console_frame, text="💻 Console Output:", font=("Helvetica", 14)).pack(anchor="w")

        # Container for Console to simulate borders
        console_container = tk.Frame(self.console_frame, bg="#333333", padx=1, pady=1)
        console_container.pack(fill="both", expand=True)

        self.console_output = tk.Text(
            console_container,
            height=8,
            font=("Consolas", 10),
            bg="#000000",
            fg="#ffffff",
            insertbackground="white",
            padx=10,
            pady=10,
            borderwidth=0,
            state="disabled"
        )
        
        console_scrollbar = ttk.Scrollbar(
            console_container,
            orient="vertical",
            command=self.console_output.yview
        )
        self.console_output.configure(yscroll=console_scrollbar.set)
        
        self.console_output.pack(side="left", fill="both", expand=True)
        console_scrollbar.pack(side="right", fill="y")

    def toggle_console(self):
        show = self.show_console_var.get() == 1
        if show:
            self.console_frame.pack(fill="both", expand=True, pady=(10, 0))
            # dump buffered lines
            try:
                self.console_output.configure(state="normal")
                self.console_output.delete("1.0", "end")
                if self._console_buffer:
                    self.console_output.insert("end", "\n".join(self._console_buffer) + "\n")
                self.console_output.see("end")
                self.console_output.configure(state="disabled")
            except Exception:
                pass
        else:
            try:
                self.console_frame.pack_forget()
            except Exception:
                pass

    def log_to_console(self, message):
        """Store console output and optionally show it in the UI."""
        if not message:
            return

        self._console_buffer.append(str(message))
        try:
            with open(self._console_log_path, "a", encoding="utf-8", errors="replace") as f:
                f.write(f"{message}\n")
        except Exception:
            pass

        if getattr(self, "show_console_var", None) is None or self.show_console_var.get() != 1:
            return

        def update():
            try:
                self.console_output.configure(state="normal")
                self.console_output.insert("end", f"{message}\n")
                self.console_output.see("end")
                self.console_output.configure(state="disabled")
            except Exception:
                pass

        self.master.after(0, update)

    def _set_controls_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        try:
            self.update_button.configure(state=state)
        except Exception:
            pass
        try:
            self.download_button.configure(state=state)
        except Exception:
            pass

    def _show_busy(self, title: str, message: str):
        """
        Simple modal-like progress popup to indicate background work.
        """
        def _create():
            if getattr(self, "_busy_window", None) and self._busy_window.winfo_exists():
                try:
                    self._busy_message_var.set(message)
                    return
                except Exception:
                    pass

            self._busy_window = tk.Toplevel(self.master)
            self._busy_window.title(title)
            self._busy_window.geometry("420x140")
            self._busy_window.transient(self.master)
            self._busy_window.resizable(False, False)
            self._busy_window.protocol("WM_DELETE_WINDOW", lambda: None)

            self._busy_message_var = tk.StringVar(value=message)
            ttk.Label(self._busy_window, textvariable=self._busy_message_var, font=("Helvetica", 11)).pack(
                padx=16, pady=(16, 10), anchor="w"
            )

            self._busy_bar = ttk.Progressbar(self._busy_window, orient="horizontal", mode="indeterminate", length=380)
            self._busy_bar.pack(padx=16, pady=(0, 10), fill="x")
            self._busy_bar.start(12)

            ttk.Label(self._busy_window, text="(No cierres la app)", foreground="#888888").pack(
                padx=16, pady=(0, 12), anchor="w"
            )

            try:
                self._busy_window.grab_set()
            except Exception:
                pass

            self._busy_window.update_idletasks()
            try:
                x = self.master.winfo_x() + (self.master.winfo_width() // 2) - 210
                y = self.master.winfo_y() + (self.master.winfo_height() // 2) - 70
                self._busy_window.geometry(f"+{x}+{y}")
            except Exception:
                pass

        self.master.after(0, _create)

    def _update_busy(self, message: str):
        def _u():
            if getattr(self, "_busy_window", None) and self._busy_window.winfo_exists():
                try:
                    self._busy_message_var.set(message)
                except Exception:
                    pass
        self.master.after(0, _u)

    def _hide_busy(self):
        def _destroy():
            if getattr(self, "_busy_window", None) and self._busy_window.winfo_exists():
                try:
                    self._busy_bar.stop()
                except Exception:
                    pass
                try:
                    self._busy_window.grab_release()
                except Exception:
                    pass
                try:
                    self._busy_window.destroy()
                except Exception:
                    pass
        self.master.after(0, _destroy)

    def _ui_set_progress(self, value: float | int | None = None, text: str | None = None):
        def _u():
            if value is not None:
                try:
                    self.progress_bar.configure(mode="determinate", maximum=100)
                    self.progress_bar["value"] = float(value)
                except Exception:
                    pass
            if text is not None:
                try:
                    self.progress_label.configure(text=text)
                except Exception:
                    pass
        self.master.after(0, _u)

    def _popen_kwargs_hidden(self):
        """
        Ensure subprocesses don't spawn a separate console window on Windows.
        """
        kwargs = {}
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            kwargs["startupinfo"] = startupinfo
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        return kwargs



    def center_window(self):
        # Update the window to ensure accurate dimensions
        self.master.update_idletasks()

        # Get window width and height
        width = self.master.winfo_width()
        height = self.master.winfo_height()

        # Get screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculate position coordinates
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Set the window position
        self.master.geometry(f'+{x}+{y}')

    def check_and_install_ffmpeg(self):
        if os.name != 'nt':
            return  # Only for Windows

        # Check existing FFmpeg installations - fast check first
        ffmpeg_path = r'C:\ffmpeg'
        ffmpeg_exe = os.path.join(ffmpeg_path, 'ffmpeg.exe')
        
        if os.path.exists(ffmpeg_exe):
            self.add_to_path(ffmpeg_path)
            return

        try:
            # Quick check if it's already in PATH without launching a full process if possible
            # but subprocess is the most reliable way
            subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, check=True)
            return
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

        # If we get here, FFmpeg is missing. We need to install it.
        # This part SHOULD be in the main thread or use .after() to create the window
        self.master.after(0, self._show_ffmpeg_install_dialog)

    def _show_ffmpeg_install_dialog(self):
        ffmpeg_path = r'C:\ffmpeg'
        # Create a progress dialog
        progress_window = tk.Toplevel(self.master)
        progress_window.title("FFmpeg Installation")
        progress_window.geometry("300x150")
        progress_window.grab_set()
        progress_window.transient(self.master)

        progress_window.update_idletasks()

        progress_label = ttk.Label(progress_window, text="Downloading FFmpeg...", font=("Helvetica", 12))
        progress_label.pack(pady=10)

        progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=250, mode="indeterminate")
        progress_bar.pack(pady=10)

        progress_window.update()
        progress_bar.start()

        def install_ffmpeg():
            try:
                os.makedirs(ffmpeg_path, exist_ok=True)
                url = 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip'
                response = requests.get(url, stream=True)
                zip_path = os.path.join(ffmpeg_path, 'ffmpeg.zip')

                with open(zip_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    for member in zip_ref.namelist():
                        if member.startswith('ffmpeg-master-latest-win64-gpl/bin/'):
                            zip_ref.extract(member, path=ffmpeg_path)

                inner_bin = os.path.join(ffmpeg_path, 'ffmpeg-master-latest-win64-gpl', 'bin')
                for filename in os.listdir(inner_bin):
                    os.rename(
                        os.path.join(inner_bin, filename),
                        os.path.join(ffmpeg_path, filename)
                    )

                os.remove(zip_path)
                import shutil
                shutil.rmtree(os.path.join(ffmpeg_path, 'ffmpeg-master-latest-win64-gpl'))

                self.add_to_path(ffmpeg_path)

                self.master.after(0, lambda: [progress_window.destroy(), messagebox.showinfo("FFmpeg", "FFmpeg has been successfully installed.")])

            except Exception as e:
                self.master.after(0, lambda: [progress_window.destroy(), messagebox.showerror("FFmpeg Installation Error", str(e))])

        threading.Thread(target=install_ffmpeg, daemon=True).start()

    def add_to_path(self, new_path):
        """
        Add a directory to system PATH if not already present
        """
        try:
            # Get current PATH from environment variables
            current_path = os.environ.get('PATH', '')
            path_dirs = current_path.split(os.pathsep)

            # Normalize paths to handle different path representations
            normalized_path = os.path.normpath(new_path)
            normalized_path_dirs = [os.path.normpath(p) for p in path_dirs]

            # Check if path is already in PATH
            if normalized_path in normalized_path_dirs:
                logging.info(f"Path {new_path} already in system PATH")
                return

            try:
                # Try to update user PATH via registry
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Environment",
                    0,
                    winreg.KEY_ALL_ACCESS
                )

                # Get current PATH from registry
                path_value, _ = winreg.QueryValueEx(key, "Path")

                # Append new path
                updated_path = path_value + f';{new_path}'
                winreg.SetValueEx(
                    key,
                    "Path",
                    0,
                    winreg.REG_EXPAND_SZ,
                    updated_path
                )

                winreg.CloseKey(key)

                # Use setx to update PATH for current session
                subprocess.run(['setx', 'PATH', updated_path], capture_output=True)

                logging.info(f"Added {new_path} to system PATH")

            except Exception as registry_error:
                # Fallback: temporary PATH update for current session
                os.environ['PATH'] = f"{current_path}{os.pathsep}{new_path}"
                logging.warning(f"Temporary PATH update. Registry update failed: {registry_error}")
                messagebox.showwarning(
                    "PATH Update",
                    f"Could not permanently add {new_path} to PATH. Added for current session only."
                )

        except Exception as e:
            logging.error(f"PATH update error: {e}")
            messagebox.showerror("PATH Update Error", str(e))


    def browse_folder(self):
        """Open folder selection dialog"""
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            self.entrada_carpeta.delete(0, tk.END)
            self.entrada_carpeta.insert(0, selected_folder)


    def update_ytdlp(self):
        def update_thread():
            try:
                self.log_to_console("--- Updating YT-DLP engine ---")

                process = subprocess.Popen(
                    ["pip", "install", "-U", "yt-dlp"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    **self._popen_kwargs_hidden()
                )
                
                for line in process.stdout or []:
                    clean_line = line.strip()
                    self.log_to_console(clean_line)
                
                process.wait()
                
                if process.returncode == 0:
                    self.master.after(0, lambda: messagebox.showinfo("Update", "YT-DLP has been updated successfully."))
                else:
                    self.master.after(0, lambda: messagebox.showerror("Update Error", "Failed to update YT-DLP."))
            except Exception as e:
                self.master.after(0, lambda: messagebox.showerror("Update Error", str(e)))

        threading.Thread(target=update_thread, daemon=True).start()

    def open_download_folder(self):
        """Open the download folder"""
        carpeta = self.entrada_carpeta.get().strip()
        if not carpeta:
            carpeta = r"C:\DS_YouTubeDownloader"

        try:
            # Use the appropriate method based on the operating system
            if os.name == 'nt':  # Windows
                os.startfile(carpeta)
            elif os.name == 'posix':  # macOS and Linux
                subprocess.Popen(['xdg-open' if sys.platform.startswith('linux') else 'open', carpeta])
        except Exception as e:
            self.show_error(f"Could not open folder: {e}")

    def parse_progress(self, output):
        """
        Parse yt-dlp progress output
        """
        # Extract download percentage
        match = re.search(r'\[download\]\s+(\d+\.?\d*)%', output)
        extract_match = re.search(r'\[ExtractAudio\]', output)

        if match:
            try:
                progress = float(match.group(1))
                self._ui_set_progress(value=progress)
            except ValueError:
                pass

        # Extract current file name and title
        filename_match = re.search(r'Destination:\s+(.+)', output)
        title_match = re.search(r'\[download\]\s+Downloading\s+video\s+(.+)', output)

        result = {}
        current_filename = None
        if filename_match:
            current_filename = os.path.basename(filename_match.group(1))
            result['filename'] = current_filename
            self._ui_set_progress(text=f"Downloading: {current_filename}")

        if title_match:
            result['title'] = title_match.group(1).strip('"')
            self._ui_set_progress(text=f"Downloading: {result['title']}")

        if extract_match and current_filename:
            self._ui_set_progress(text=f"Extracting Audio: {current_filename}")

        return result

    def download_thread(self, link_info, carpeta, formato, calidad, metadatos, miniatura):
        enlace = link_info['link']
        title = link_info['title']
        artist = link_info['artist']
        display_name = f"{title} - {artist}".strip()

        # Al inicio del método, configura logging
        logging.basicConfig(
            filename='download_log.txt',
            level=logging.INFO,
            format='%(asctime)s - %(message)s'
        )

        # Add to treeview initially as Downloading
        item_id = self.master.after(0, lambda:
        self.songs_tree.insert('', 'end', values=(display_name, '⏳ Downloading', ''))
                                    )

        def sanitize_filename(filename):
            return re.sub(r'[<>:"/\\|?*]', '', filename).strip()

        sanitized_title = sanitize_filename(title)
        sanitized_artist = sanitize_filename(artist)

        # Download all playlists of YouTube channel/user keeping each playlist in separate directory:
        # $ yt - dlp - o "%(uploader)s/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"
        # "https://www.youtube.com/user/TheLinuxFoundation/playlists"

        video_format = self.var_video_format.get()
        keep_video = self.var_keep_video.get()
        video_quality = self.var_video_quality.get()

        # Base command
        comando = ["yt-dlp", "--js-runtimes", "node", "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"]

        if video_format == 0:  # Audio Only
            comando.extend([
                "-x",
                "--audio-format", formato,
                "--audio-quality", calidad,
            ])
        else:  # Video (Original o MP4)
            # Configurar la calidad del video
            if video_quality == "max":
                if video_format == 1:  # Original Video
                    video_format_str = "bestvideo+bestaudio/best"
                else:  # MP4
                    video_format_str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
            else:
                if video_format == 1:  # Original Video
                    video_format_str = f"bestvideo[height<={video_quality}]+bestaudio/best[height<={video_quality}]"
                else:  # MP4
                    video_format_str = f"bestvideo[height<={video_quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={video_quality}][ext=mp4]/best"

            comando.extend([
                "-f", video_format_str,
            ])

        # Output template
        if video_format == 0:
            output_template = f"{carpeta}/{sanitized_title} - {sanitized_artist}.%(ext)s"
        else:
            # Añadir la calidad al nombre del archivo de video
            quality_suffix = "_MAX" if video_quality == "max" else f"_{video_quality}p"
            output_template = f"{carpeta}/{sanitized_title} - {sanitized_artist}{quality_suffix}.%(ext)s"

        comando.extend([
            "-o", output_template,
            "--newline",
            "--progress"
        ])

        # Add metadata and thumbnail options for audio
        # if video_format == 0:
        if metadatos:
            comando.extend(["--embed-metadata", "--add-metadata"])
        if miniatura:
            comando.extend(["--embed-thumbnail", "--convert-thumbnails", "jpg"])

        comando.append(enlace)

        try:
            self._ui_set_progress(value=0, text=f"Downloading: {display_name}")

            # First download with video if needed
            process = subprocess.Popen(
                comando,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                **self._popen_kwargs_hidden()
            )

            current_filepath = None

            # Read output in real-time
            for line in process.stdout or []:
                clean_line = line.strip()
                logging.info(clean_line)
                self.log_to_console(clean_line)
                progress_info = self.parse_progress(line)

                if '[ExtractAudio]' in line:
                    self.master.after(0, lambda:
                    self.update_download_status(display_name, '⏳ Extracting Audio', '')
                                      )
                    self._ui_set_progress(text=f"Extracting Audio: {display_name}")

                dest_match = re.search(r'Destination:\s+(.+)', line)
                if dest_match:
                    current_filepath = dest_match.group(1)

            process.wait()

            # If audio only is selected and keep_video is True, make a copy of the video
            if video_format == 0 and keep_video:
                video_comando = [
                    "yt-dlp",
                    "--js-runtimes", "node",
                    "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                    "-f",
                    f"bestvideo[height<={video_quality}]+bestaudio/best[height<={video_quality}]" if video_quality != "max" else "bestvideo+bestaudio/best",
                    "-o", output_template.replace(".%(ext)s", "_video.%(ext)s"),
                    enlace
                ]
                
                subprocess.Popen(
                    video_comando,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    **self._popen_kwargs_hidden()
                )

            if process.returncode == 0:
                self.master.after(0, lambda:
                self.update_download_status(display_name, '✅ Complete', current_filepath or '')
                                  )
                self._ui_set_progress(value=100, text=f"Download complete: {display_name}")
            else:
                self.master.after(0, lambda:
                self.update_download_status(display_name, '❌ Error', '')
                                  )
                self._ui_set_progress(text=f"Error downloading: {display_name}")

        except Exception as e:
            self.master.after(0, lambda:
            self.update_download_status(display_name, '❌ Error', '')
                              )
            self._ui_set_progress(text=f"Error: {str(e)}")

    def update_download_status(self, link, status, filepath):
        """
        Update the status of a download in the treeview
        """
        # Find the item with the matching link and update its status
        for item in self.songs_tree.get_children():
            if self.songs_tree.item(item)['values'][0] == link:
                self.songs_tree.item(item, values=(link, status, filepath))
                break

    def validate_youtube_links(self, links):
        youtube_regex = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
        validated_links = []

        for link in links:
            # More aggressive cleaning using regex to find the actual URL
            url_match = re.search(r'(https?://[^\s`\'"]+)', link)
            if not url_match:
                continue
            
            link = url_match.group(1).strip()
            if not link:
                continue

            if not re.match(youtube_regex, link):
                self.show_error(f"Invalid link: {link}")
                continue

            try:
                self.log_to_console(f"[INFO] Analizando: {link}")
                # Print diagnostic information
                print(f"Processing link: {link}")

                # Flat playlist extraction
                startupinfo = None
                if os.name == 'nt':
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = subprocess.SW_HIDE

                result = subprocess.run(
                    ["yt-dlp", "--js-runtimes", "node", "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36", "--flat-playlist", "-J", link],
                    capture_output=True,
                    text=True,
                    check=True,
                    startupinfo=startupinfo,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )

                # Print raw JSON for debugging
                print("Raw JSON:", result.stdout)

                data = json.loads(result.stdout)

                # Handle both single video and playlist
                if 'entries' in data:
                    entries = data['entries']
                    print(f"Playlist detected: {len(entries)} entries")
                    self.log_to_console(f"[INFO] Playlist detectada: {len(entries)} elemento(s)")
                else:
                    entries = [data]
                    print("Single video detected")
                    self.log_to_console("[INFO] Vídeo único detectado")

                for entry in entries:
                    video_url = entry.get('url', entry.get('id', ''))
                    if not video_url:
                        print("No video URL found for entry")
                        continue

                    # Detailed video metadata
                    startupinfo_metadata = None
                    if os.name == 'nt':
                        startupinfo_metadata = subprocess.STARTUPINFO()
                        startupinfo_metadata.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                        startupinfo_metadata.wShowWindow = subprocess.SW_HIDE

                    video_result = subprocess.run(
                        ["yt-dlp", "--js-runtimes", "node", "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36", "-J", video_url],
                        capture_output=True,
                        text=True,
                        check=True,
                        startupinfo=startupinfo_metadata,
                        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                    )
                    metadata = json.loads(video_result.stdout)

                    title = metadata.get('title', 'Unknown Title').strip()
                    artist = metadata.get('uploader', 'Unknown Artist').strip()

                    print(f"Found video: {title} by {artist}")
                    self.log_to_console(f"[INFO] Encontrado: {title} - {artist}")

                    validated_links.append({
                        'link': video_url,
                        'title': title,
                        'artist': artist
                    })

            except subprocess.CalledProcessError as e:
                print(f"Subprocess error: {e}")
                print(f"Stderr: {e.stderr}")
                logging.error(f"Metadata extraction error for {link}: {e}")
                if e.stderr:
                    self.log_to_console(f"[ERROR] {e.stderr.strip()}")
                self.show_error(f"Could not process link: {link}")
            except json.JSONDecodeError as e:
                print(f"JSON decoding error: {e}")
                logging.error(f"Invalid JSON response for {link}")
                self.log_to_console("[ERROR] Respuesta JSON inválida al obtener metadatos")
                self.show_error(f"Could not parse metadata for {link}")
            except Exception as e:
                print(f"Unexpected error: {e}")
                logging.error(f"Unexpected error processing {link}: {e}")
                self.log_to_console(f"[ERROR] {str(e)}")
                self.show_error(f"Unexpected error processing {link}")

        if not validated_links:
            self.show_error("No valid YouTube links found")
            return []

        return validated_links

    def show_error(self, message):
        """Display error message"""
        self.error_label.configure(text=message)
        self.master.after(5000, lambda: self.error_label.configure(text=""))
        logging.error(message)

    def iniciar_descarga(self):
        # Reset UI elements (main thread)
        self.error_label.configure(text="")
        for item in self.songs_tree.get_children():
            self.songs_tree.delete(item)

        # Get inputs
        enlaces_raw = self.entrada_enlaces.get("1.0", tk.END).strip().split('\n')
        raw_links = [link.strip() for link in enlaces_raw if link.strip()]
        carpeta = self.entrada_carpeta.get().strip() or r"C:\DS_YouTubeDownloader"

        if not raw_links:
            self.show_error("Please paste at least one YouTube link.")
            return

        self._set_controls_enabled(False)
        self._ui_set_progress(value=0, text="Preparing downloads...")
        self._show_busy("Procesando", "Analizando enlaces y obteniendo metadatos...")

        def _prepare_and_start():
            try:
                # Validate links and get metadata (background thread)
                enlaces = self.validate_youtube_links(raw_links)
                if not enlaces:
                    self.master.after(0, lambda: self._ui_set_progress(text="No valid links found."))
                    return

                # Create download folder
                try:
                    os.makedirs(carpeta, exist_ok=True)
                except Exception as e:
                    self.master.after(0, lambda: self.show_error(f"Could not create download folder: {e}"))
                    return

                # Determine format and quality
                formato = "mp3" if self.var_formato.get() == 1 else "best"
                calidad = "0" if self.var_calidad.get() == 1 else ("128K" if self.var_calidad.get() == 2 else "192K")
                metadatos = self.var_metadatos.get() == 1
                miniatura = self.var_miniatura.get() == 1

                self._update_busy(f"Iniciando descargas ({len(enlaces)} elemento(s))...")

                # Semaphore to limit concurrent downloads
                download_semaphore = threading.Semaphore(3)

                def download_wrapper(link_info):
                    with download_semaphore:
                        self.download_thread(link_info, carpeta, formato, calidad, metadatos, miniatura)

                def download_worker():
                    threads = []
                    for link_info in enlaces:
                        thread = threading.Thread(target=download_wrapper, args=(link_info,), daemon=True)
                        thread.start()
                        threads.append(thread)

                    for thread in threads:
                        thread.join()

                    self.master.after(0, lambda: messagebox.showinfo("Download", "All downloads completed"))
                    self.master.after(0, lambda: self._ui_set_progress(text="All downloads completed."))
                    self.master.after(0, self._hide_busy)
                    self.master.after(0, lambda: self._set_controls_enabled(True))

                # Hide busy popup once downloads are running (UI stays responsive and tree/console update)
                self.master.after(0, self._hide_busy)
                threading.Thread(target=download_worker, daemon=True).start()

            finally:
                # If we exited early due to errors, ensure we re-enable UI and close busy window.
                def _cleanup_if_still_busy():
                    if getattr(self, "_busy_window", None) and self._busy_window.winfo_exists():
                        self._hide_busy()
                        self._set_controls_enabled(True)
                self.master.after(0, _cleanup_if_still_busy)

        threading.Thread(target=_prepare_and_start, daemon=True).start()


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def main():
    start_time = time.time()
    root = tk.Tk()

    # Apply Sun Valley theme once at the beginning
    try:
        sv_ttk.THEME_PATH = resource_path("sv_ttk")
        sv_ttk.set_theme("dark")
        
        # Apply dark title bar for Windows
        try:
            import pywinstyles
            pywinstyles.apply_style(root, "dark")
        except ImportError:
            pass
    except Exception as e:
        print(f"Error applying theme: {e}")

    app = YouTubeDownloader(root)
    
    end_time = time.time()
    print(f"--- [INFO] Startup time: {end_time - start_time:.4f} seconds ---")
    
    root.mainloop()


if __name__ == "__main__":
    main()
