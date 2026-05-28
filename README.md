TikTok → Instagram Reels Poster
A lightweight desktop app for Linux that lets you paste a TikTok link and automatically post it as an Instagram Reel — no browser, no manual downloading, no transferring files.
Show Image Show Image Show Image

Features

Paste a TikTok link and post to Instagram Reels in one click
Downloads video without watermark using yt-dlp
Saves your default caption so you don't retype it every time
Caches your Instagram session so login is faster after the first time
Clean dark UI built with tkinter
Works great with KDE Connect for instant clipboard sync from your phone


Requirements

Linux (tested on Arch)
Python 3.8+
ffmpeg
tkinter


Installation
1. Install system dependencies
On Arch:
bashsudo pacman -S python python-pip tk ffmpeg
On Ubuntu/Debian:
bashsudo apt install python3 python3-pip python3-tk ffmpeg
2. Clone the repo
bashgit clone https://github.com/sonofgodlike/tiktok-to-reels.git
cd tiktok-to-reels
3. Install Python dependencies
bashpip install yt-dlp instagrapi moviepy==2.2.1 --break-system-packages
4. Run the app
bashpython3 app.py
The app will auto-install any missing dependencies on first run.

Usage

Copy a TikTok link on your phone (Share → Copy Link)
It syncs to your PC clipboard automatically via KDE Connect
Paste it into the app
Enter your Instagram username and password
Write your caption (it saves for next time)
Hit POST TO REELS — done in about 30 seconds
Go to Instagram and add your pinned comment manually


KDE Connect Setup (optional but recommended)
KDE Connect lets you copy a TikTok link on your phone and have it instantly appear on your PC clipboard — no extra steps.
On your PC:
bashsudo pacman -S kdeconnect
kdeconnect-app
On your Android:
Install KDE Connect from the Play Store, pair with your PC, and enable Clipboard Sync in plugin settings.

Troubleshooting
ProblemFixlibtk8.6.so errorsudo pacman -S tkffmpeg not foundsudo pacman -S ffmpegLogin failedTurn off 2FA on Instagram, or wait an hour and retryVideo not found after downloadTikTok link may be private or region-lockedUpload failedInstagram flagged the login — wait an hour and try again

Notes

Your Instagram password is never saved — only a session token is stored locally
Works with Creator and Business Instagram accounts
TikTok videos must be public to download


Built With

yt-dlp — video downloading
instagrapi — Instagram posting
KDE Connect — clipboard sync
tkinter — GUI

