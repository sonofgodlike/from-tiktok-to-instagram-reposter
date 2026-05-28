# TikTok → Instagram Reels Poster

Paste a TikTok link. It downloads the video and posts it as an Instagram Reel automatically.

---

## Install & Run

**Arch**
```bash
sudo pacman -S python python-pip tk ffmpeg
pip install yt-dlp instagrapi moviepy==2.2.1 --break-system-packages
cd ~/Downloads/TikTok_to_Reels_Arch
python3 app.py
```

**Ubuntu / Debian**
```bash
sudo apt install python3 python3-pip python3-tk ffmpeg
pip3 install yt-dlp instagrapi moviepy==2.2.1 --break-system-packages
cd ~/Downloads/TikTok_to_Reels_Ubuntu
python3 app.py
```

**macOS**
```bash
brew install python ffmpeg
pip3 install yt-dlp instagrapi moviepy==2.2.1
cd ~/Downloads/TikTok_to_Reels_macOS
python3 app.py
```
> Don't have Homebrew? Install it first:
> ```bash
> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
> ```

**Windows**
```
winget install ffmpeg
pip install yt-dlp instagrapi moviepy==2.2.1
cd C:\Users\YourName\Downloads\TikTok_to_Reels_Windows
```
Then double-click `START.bat` or run:
```
python app.py
```
> Replace `YourName` with your actual Windows username.

---

## Built With

[yt-dlp](https://github.com/yt-dlp/yt-dlp) · [instagrapi](https://github.com/subzeroid/instagrapi) · [KDE Connect](https://kdeconnect.kde.org/)
