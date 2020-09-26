# syd
![syd-1](https://user-images.githubusercontent.com/35954251/94338969-ba3fc300-fff6-11ea-9f1c-1b90b509c9f9.png)  
A very simple YouTube to MP3 downloader.

# Installation
1. Clone or download the repository
2. Install `tkinter`:
    - Fedora: `sudo dnf install python3-tkinter`
    - Arch/Manjaro: `sudo pacman -S tk`
    - Ubuntu/Debian: `sudo apt-get install python3-tk`
3. Navigate to repository root directory
4. Install: `chmod +x install syd; ./install`
5. Run: 
    - from terminal `./syd`
    - with Application launcher (.desktop file gets generated with install)

# Instructions
- Paste a YouTube link into the text box with Ctrl+V
- Click the download button or press Enter
- Single videos are downloaded to `~/Music/syd-music/`
- Playlists are downloaded to `~/Music/syd-music/<playlist-name>/`

# About
This project is dedicated to:
- my mom in hopes of simplifying her YouTube-to-MP3 struggles
- my sister and dad for the same reasons

Made with:
- [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI)
- [YoutubeDL](https://github.com/ytdl-org/youtube-dl)

# To do
- Windows support