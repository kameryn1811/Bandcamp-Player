<div align="center">

# <img src="images/icon-title.png" width="32" height="32" alt="Icon"> Bandcamp Player (Python Edition)

[![Download](images/download-button.png)](https://github.com/kameryn1811/Bandcamp-Player/releases/)

</div>

A compact, convenient Python-based mini player for streaming music directly from Bandcamp. Perfect for previewing albums and discovering new music you want to support.

## Key Features

* **Executable** - Available in .exe format, simply download and run.
* **Automatic Updates** - Select automatic updates or check now to be notified when there is a new update and accept to install it automatically.
* **Compact Interface** - Minimal window design that stays out of your way.
* **Multiple View Modes** - Regular, Mini, Micro, and Nano modes available for different use cases.
* **Playlist Management** - Create and manage playlists of your favorite Bandcamp albums.
* **Detachable Playlist** - Detach the playlist window for flexible window management.
* **Always on Top** - Keep the player visible while working in other applications.
* **Keyboard Shortcuts** - Full keyboard control for play, pause, next, previous, volume, and more.
* **Autoplay** - Automatically starting playing on startup and when switching albums. 
* **Shuffle & Repeat** - Multiple shuffle and repeat modes for varied listening.
* **Volume Control** - Adjustable volume with visual feedback.
* **Dark Theme** - Beautiful dark interface that's easy on the eyes.

*The main player interface with compact playlist, regular/mini/micro and nano modes.*

*Note: Mini mode features optional player autohide so the artwork is fully viewable*

*Note: Nano mode features optional autohide when docked to the top or bottom of the screen*

<img width="600" alt="main-player-interface" src="images/player modes.png" />

## Technology & Approach

Bandcamp doesn’t provide a public API for music playback, playlists, or track data (its official APIs are limited to sales and merchandise for artists and labels). As a work around Bandcamp Player embeds Bandcamp’s own mobile web player in a desktop app, preserving the Bandcamp experience while adding lightweight desktop features.

### Core Stack

- **PyQt6** – Cross-platform desktop framework for window management, system tray integration, and media keys  
- **PyQt6-WebEngine** – Embedded Chromium browser used to load Bandcamp’s mobile site with full DOM access  
- **qtawesome** – FontAwesome icons with emoji fallback

## Quick Start

**Installation**

1. Download [BandcampPlayer.exe](https://github.com/kameryn1811/Bandcamp-Player/releases/tag/Launcher_v1.0.0) and run it! (everything else is automatic)
2. **Note:** You may see a Windows Defender SmartScreen Warning, see [Troubleshooting](#troubleshooting) for more information. 
3. What it Does:
   - Downloads the latest `bandcamp_pl_gui.py` script from GitHub and Launches it
   - Checks for updates on startup
   - Self-contained - No Python installation needed
   - Automatically installs any dependencies

## Usage

1. **Add URLs**: Drag and drop Bandcamp URLs into the main window or playlist, or use the add button.
2. **Play Music**: Click on any item in the playlist to start playing.
3. **Controls**: Use the player controls or keyboard shortcuts to navigate tracks.
4. **Modes**: Switch between Regular, Mini, Micro, and Nano modes from the settings menu.
5. **Playlists**: Create multiple playlists and switch between them using the playlist menu.

## Shuffle & Repeat Modes  <img alt="shuffle-repeat" src="images/shuffle-repeat.png" />

- <img alt="shuffle-tracks" src="images/shuffle-tracks.png" /> **Shuffle Tracks** – shuffle tracks within the current album  
- <img alt="shuffle-album" src="images/shuffle-album.png" /> **Shuffle Albums** – play albums in random order  
- <img alt="super-shuffle" src="images/super-shuffle.png" /> **Super Shuffle** – completely random tracks and albums; avoids recent repeats  
- <img alt="continuous" src="images/continuous.png" /> **Continuous Repeat** – plays through entire playlist (default)  
- <img alt="repeat-album" src="images/repeat-album.png" /> **Repeat Album** – loops current album  
- <img alt="repeat-1" src="images/repeat-1.png" /> **Repeat Track** – loops current track (shows "1" on button)  

**Combinations:** Shuffle and Repeat work together (e.g., *Shuffle Tracks + Repeat Album* loops shuffled tracks; *Super Shuffle + Repeat Off* plays random tracks without immediate repeats).

## Keyboard Shortcuts

* **Space** - Play/Pause
* **Left Arrow** - Previous track
* **Right Arrow** - Next track
* **Up Arrow** - Volume up
* **Down Arrow** - Volume down
* **F12** - Developer Tools
* And more... (see Settings > Keyboard Shortcuts)

## Troubleshooting

**Windows SmartScreen Warning**
- When you open BandcampPlayer.exe for the first time, Windows might say: "Windows protected your PC"
- This happens because the app isn't code-signed (certificates are pricey, and this is a free open-source project).
- No worries, it's safe to run. The EXE is the same code you can read on GitHub.
- **To continue:** Click "More info" and "Run anyway", Windows won't nag you again for the same .exe. 
- **Want extra peace of mind?** - You can review the code, build it yourself, or use the standalone Python script like in Option 2.

**"Python not found"**
- Reinstall Python and ensure "Add Python to PATH" is checked
- Or manually add Python to your system PATH

**Windows 7: Missing DLL or Failed to load Python Errors**
- If the app won't launch on Windows 7 and you see errors like "api-ms-win-core-path-l1-1-0.dll not found" or "Failed to load Python DLL," Windows 7 is missing a DLL required by Python 3.11+.
- Fix it with the latest compatibility patch from nalexandru: https://github.com/nalexandru/api-ms-win-core-path-HACK/releases
- Download the latest release and copy the DLLs to the following locations:
  - x86 → C:\Windows\SysWOW64
  - x64 → C:\Windows\System32 (Admin rights may be needed)
- Launch the app!
- Thanks to @alabx for this [fix](https://github.com/kameryn1811/Bandcamp-Downloader/issues/6)! 

**"Player not responding"**
- Check your internet connection
- Verify the Bandcamp URL is valid and accessible
- Try refreshing the page

**"Playlist not saving"**
- Check that the Playlists folder exists in the app directory
- Verify write permissions for the app directory

**Media keys not working**
- Media key support requires Windows
- Ensure no other application is capturing media keys
- Try restarting the application

## Credits & Inspiration

This project provides a convenient way to stream music from Bandcamp in a compact, always-accessible player interface.

## Legal & Ethical Use

This tool is designed for:
* Streaming freely available music from Bandcamp
* Personal use of music you own or have permission to stream
* Building a local playlist of your favorite Bandcamp content

Please respect copyright laws and Bandcamp's terms of service. Support artists by purchasing music when possible.

## Disclaimer

This software is provided as-is for educational and personal use. The developers are not responsible for misuse. Please use responsibly and support the artists whose music you enjoy.















