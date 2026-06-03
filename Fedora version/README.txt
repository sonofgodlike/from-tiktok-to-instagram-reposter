HOW TO RUN ON BAZZITE
─────────────────────────────────────────────

STEP 1 — Install ffmpeg (one time only)
  Bazzite doesn't use apt-get. Use Homebrew instead:

    brew install ffmpeg

  Don't have Homebrew? Install it first:
    https://brew.sh

  Alternative — install inside Distrobox:
    distrobox-enter
    sudo dnf install ffmpeg

STEP 2 — Make sure Python & tkinter are available
  Bazzite includes Python 3 by default. If the app
  says tkinter is missing, run this and then reboot:

    sudo rpm-ostree install python3-tkinter

STEP 3 — Run the app
  Right-click the folder containing app.py and open
  a terminal there, then run:

    python3 app.py

  The app installs its own Python dependencies
  automatically on first launch (yt-dlp, instagrapi,
  moviepy). No sudo needed for those.

STEP 4 — Use the app
  1. Paste a TikTok link
  2. Enter your Instagram username and password
  3. Write a caption (it's saved for next time)
  4. Hit POST TO REELS and watch the log


CREDITS: Sonofgodlike, Issacphatom69
