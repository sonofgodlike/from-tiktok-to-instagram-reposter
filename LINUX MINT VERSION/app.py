import tkinter as tk
from tkinter import messagebox
import threading
import subprocess
import sys
import os
import json

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

def save_config(username, caption):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"username": username, "default_caption": caption}, f)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}

def install_deps(log):
    log("checking dependencies...")
    pkgs = ["yt-dlp", "instagrapi", "moviepy==2.2.1"]
    for pkg in pkgs:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--quiet", "--upgrade", "--break-system-packages", pkg],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            # fallback: try without --break-system-packages (older pip)
            result2 = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--quiet", "--upgrade", pkg],
                capture_output=True, text=True
            )
            if result2.returncode != 0:
                log(f"failed to install {pkg}: {result2.stderr.strip()[:120]}")
                return False
        log(f"{pkg.split('==')[0]} ready")

    # check ffmpeg — use apt on Debian/Ubuntu/Mint
    import shutil
    if shutil.which("ffmpeg"):
        log("ffmpeg found")
    else:
        log("ffmpeg not found — trying apt-get install...")
        result = subprocess.run(
            ["sudo", "apt-get", "install", "-y", "ffmpeg"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            log("could not auto-install ffmpeg. run: sudo apt-get install ffmpeg")
            return False
        log("ffmpeg installed")

    return True

def download_tiktok(url, output_path, log):
    import yt_dlp
    log("downloading tiktok video...")
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'http_headers': {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'TikTok video')
        log(f"downloaded: {title[:60]}")
        return title

def post_to_instagram(video_path, caption, username, password, log):
    import shutil, os
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path
        os.environ["FFMPEG_BINARY"] = ffmpeg_path
    from instagrapi import Client
    log("logging into instagram...")
    cl = Client()
    cl.delay_range = [1, 3]
    session_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"session_{username}.json")
    try:
        if os.path.exists(session_file):
            cl.load_settings(session_file)
            cl.login(username, password)
            log("logged in (cached session)")
        else:
            cl.login(username, password)
            cl.dump_settings(session_file)
            log("logged in")
    except Exception as e:
        log(f"login failed: {e}")
        return False
    log("uploading reel... this may take a minute")
    try:
        cl.clip_upload(video_path, caption)
        log("posted! go add your pinned gif comment.")
        return True
    except Exception as e:
        log(f"upload failed: {e}")
        return False

# ── colors ──────────────────────────────────────────────
BG       = "#0f0f0f"
SURFACE  = "#1a1a1a"
SURFACE2 = "#242424"
BORDER   = "#2e2e2e"
TEXT     = "#f0f0f0"
MUTED    = "#666666"
ACCENT   = "#ff3366"
ACCENT_H = "#e0254f"
GREEN    = "#22c55e"
LOG_BG   = "#111111"
LOG_FG   = "#4ade80"

class PlaceholderEntry(tk.Entry):
    def __init__(self, master, placeholder, show_char=None, **kw):
        super().__init__(master, **kw)
        self.placeholder = placeholder
        self.show_char = show_char
        self._active = False
        self.configure(fg=MUTED)
        self.insert(0, placeholder)
        self.bind("<FocusIn>", self._on_in)
        self.bind("<FocusOut>", self._on_out)

    def _on_in(self, e):
        if not self._active:
            self._active = True
            self.delete(0, "end")
            self.configure(fg=TEXT)
            if self.show_char:
                self.configure(show=self.show_char)

    def _on_out(self, e):
        if not self.get():
            self._active = False
            if self.show_char:
                self.configure(show="")
            self.configure(fg=MUTED)
            self.insert(0, self.placeholder)

    def real_value(self):
        val = self.get()
        return "" if val == self.placeholder else val


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("reels poster")
        self.geometry("520x700")
        self.resizable(False, False)
        self.configure(bg=BG)
        self._build()
        cfg = load_config()
        if cfg.get("username"):
            self.username_entry.delete(0, "end")
            self.username_entry.insert(0, cfg["username"])
            self.username_entry.configure(fg=TEXT)
            self.username_entry._active = True
        if cfg.get("default_caption"):
            self.caption_box.delete("1.0", "end")
            self.caption_box.insert("1.0", cfg["default_caption"])
            self.caption_box.configure(fg=TEXT)
            self.caption_box._active = True

    def _section(self, label):
        f = tk.Frame(self, bg=BG)
        f.pack(fill="x", padx=28, pady=(18, 4))
        tk.Label(f, text=label.upper(), font=("DejaVu Sans", 9, "bold"),
                 fg=MUTED, bg=BG).pack(anchor="w")
        return f

    def _field(self, placeholder, show_char=None):
        frame = tk.Frame(self, bg=SURFACE, highlightbackground=BORDER,
                         highlightthickness=1)
        frame.pack(fill="x", padx=28, pady=2)
        e = PlaceholderEntry(frame, placeholder, show_char=show_char,
                             bg=SURFACE, relief="flat", bd=0,
                             font=("DejaVu Sans", 12), insertbackground=TEXT,
                             highlightthickness=0)
        e.pack(fill="x", ipady=10, padx=12)

        def on_enter(w):
            frame.configure(highlightbackground=ACCENT)
        def on_leave(w):
            frame.configure(highlightbackground=BORDER)
        e.bind("<Enter>", on_enter)
        e.bind("<Leave>", on_leave)
        e.bind("<FocusIn>", lambda ev: frame.configure(highlightbackground=ACCENT))
        e.bind("<FocusOut>", lambda ev: frame.configure(highlightbackground=BORDER))
        return e

    def _build(self):
        # ── logo bar ──
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=28, pady=(32, 0))
        tk.Label(top, text="●", font=("DejaVu Sans", 18), fg=ACCENT, bg=BG).pack(side="left")
        tk.Label(top, text="  reels poster", font=("DejaVu Sans", 18, "bold"),
                 fg=TEXT, bg=BG).pack(side="left")

        tk.Label(self, text="paste a tiktok link. it posts itself.",
                 font=("DejaVu Sans", 11), fg=MUTED, bg=BG).pack(anchor="w", padx=28, pady=(4, 0))

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=28, pady=20)

        # ── fields ──
        self._section("tiktok link")
        self.link_entry = self._field("https://www.tiktok.com/@user/video/...")

        self._section("instagram username")
        self.username_entry = self._field("your_username")

        self._section("instagram password")
        # Use "*" instead of "•" to avoid font rendering issues on some Linux setups
        self.password_entry = self._field("password", show_char="*")

        self._section("caption")
        cap_frame = tk.Frame(self, bg=SURFACE, highlightbackground=BORDER, highlightthickness=1)
        cap_frame.pack(fill="x", padx=28, pady=2)

        class PlaceholderText(tk.Text):
            def __init__(self, master, placeholder, **kw):
                super().__init__(master, **kw)
                self.placeholder = placeholder
                self._active = False
                self.configure(fg=MUTED)
                self.insert("1.0", placeholder)
                self.bind("<FocusIn>", self._on_in)
                self.bind("<FocusOut>", self._on_out)
            def _on_in(self, e):
                if not self._active:
                    self._active = True
                    self.delete("1.0", "end")
                    self.configure(fg=TEXT)
            def _on_out(self, e):
                if not self.get("1.0", "end-1c").strip():
                    self._active = False
                    self.delete("1.0", "end")
                    self.insert("1.0", self.placeholder)
                    self.configure(fg=MUTED)
            def real_value(self):
                val = self.get("1.0", "end-1c")
                return "" if val == self.placeholder else val

        self.caption_box = PlaceholderText(
            cap_frame, "write your caption here... (saved for next time)",
            height=3, bg=SURFACE, relief="flat", bd=0,
            font=("DejaVu Sans", 12), insertbackground=TEXT,
            highlightthickness=0, wrap="word"
        )
        self.caption_box.pack(fill="x", padx=12, pady=8)
        cap_frame.bind("<Enter>", lambda e: cap_frame.configure(highlightbackground=ACCENT))
        cap_frame.bind("<Leave>", lambda e: cap_frame.configure(highlightbackground=BORDER))
        self.caption_box.bind("<FocusIn>", lambda e: cap_frame.configure(highlightbackground=ACCENT))
        self.caption_box.bind("<FocusOut>", lambda e: cap_frame.configure(highlightbackground=BORDER))

        # ── post button ──
        self.post_btn = tk.Button(
            self, text="POST TO REELS",
            font=("DejaVu Sans", 13, "bold"),
            bg=ACCENT, fg=TEXT,
            activebackground=ACCENT_H, activeforeground=TEXT,
            relief="flat", cursor="hand2", bd=0,
            command=self._start_post
        )
        self.post_btn.pack(fill="x", padx=28, pady=(22, 0), ipady=13)

        # ── log ──
        log_outer = tk.Frame(self, bg=LOG_BG, highlightbackground=BORDER, highlightthickness=1)
        log_outer.pack(fill="both", expand=True, padx=28, pady=(14, 24))

        self.log_text = tk.Text(
            log_outer, bg=LOG_BG, fg=LOG_FG,
            font=("DejaVu Sans Mono", 10), relief="flat",
            padx=12, pady=10, state="disabled", wrap="word",
            highlightthickness=0
        )
        self.log_text.pack(fill="both", expand=True)

    def log(self, msg):
        # Marshal to main thread via after() — required for thread safety on Linux
        self.after(0, self._append_log, msg)

    def _append_log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"> {msg}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def _start_post(self):
        link     = self.link_entry.real_value().strip()
        username = self.username_entry.real_value().strip()
        password = self.password_entry.real_value().strip()
        caption  = self.caption_box.real_value().strip()

        if not link:
            messagebox.showerror("missing", "paste a tiktok link first.")
            return
        if not username:
            messagebox.showerror("missing", "enter your instagram username.")
            return
        if not password:
            messagebox.showerror("missing", "enter your instagram password.")
            return

        save_config(username, caption)

        self.post_btn.config(state="disabled", text="posting...")
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")

        def worker():
            try:
                if not install_deps(self.log):
                    self.log("setup failed. run: sudo apt-get install ffmpeg python3-pip")
                    return
                VIDEO_EXTS = (".mp4", ".webm", ".mkv", ".mov", ".avi")
                base_dir   = os.path.dirname(os.path.abspath(__file__))
                video_base = os.path.join(base_dir, "download")
                for f in os.listdir(base_dir):
                    if f.startswith("download") and f.endswith(VIDEO_EXTS):
                        os.remove(os.path.join(base_dir, f))

                title = download_tiktok(link, video_base, self.log)

                actual_path = None
                for f in sorted(os.listdir(base_dir)):
                    if f.startswith("download") and f.endswith(VIDEO_EXTS):
                        actual_path = os.path.join(base_dir, f)
                        self.log(f"found video: {f}")
                        break

                if not actual_path:
                    self.log(f"files in dir: {[f for f in os.listdir(base_dir) if not f.startswith('.')]}")
                    self.log("video not found. trying forced mp4 download...")
                    import yt_dlp as ytdl2
                    out = video_base + "_forced.mp4"
                    ydl_opts2 = {
                        'outtmpl': out,
                        'format': 'mp4/best',
                        'quiet': False,
                        'merge_output_format': 'mp4',
                        'http_headers': {'User-Agent': 'Mozilla/5.0'}
                    }
                    with ytdl2.YoutubeDL(ydl_opts2) as ydl2:
                        ydl2.download([link])
                    if os.path.exists(out):
                        actual_path = out
                        self.log("forced download succeeded.")
                    else:
                        self.log("download failed. link may be private or region-locked.")
                        return

                final_caption = caption if caption else (title[:200] if title else "via tiktok")
                success = post_to_instagram(actual_path, final_caption, username, password, self.log)

                if success:
                    os.remove(actual_path)
                    self.log("temp file cleaned up.")
            except Exception as e:
                self.log(f"unexpected error: {e}")
            finally:
                self.after(0, lambda: self.post_btn.config(state="normal", text="POST TO REELS"))

        threading.Thread(target=worker, daemon=True).start()

if __name__ == "__main__":
    # Friendly error if tkinter isn't installed (common on minimal Linux installs)
    try:
        import tkinter
    except ImportError:
        print("tkinter not found. Install it with: sudo apt-get install python3-tk")
        sys.exit(1)

    app = App()
    app.mainloop()
