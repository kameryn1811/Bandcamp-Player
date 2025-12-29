<div align="center">

# <img src="images/icon-title.png" width="32" height="32" alt="Icon"> Bandcamp Player (Python Edition)

[![Download](images/download-button.png)](https://github.com/kameryn1811/Bandcamp-Player/releases/)

</div>

A compact, convenient Python-based mini player for streaming music directly from Bandcamp. Perfect for previewing albums and discovering new music you want to support.

*The main player interface with compact playlist, regular/mini/micro and nano modes.*

<img width="600" alt="screenshot-main" src="images/player modes.png" />

*The main player interface with compact playlist, expanded playlist and detached playlist*

<img width="600" alt="screenshot-main" src="images/playlist modes.png" />

### Shuffle & Repeat Modes

Bandcamp Player offers **4 shuffle modes** and **4 repeat modes**, which can be combined for flexible playback. Cycle through each by clicking the respective button.

**Shuffle Modes**
1. **Off (Mode 0)** – Normal playback order; next/previous work as usual.
2. **Tracks (Mode 1)** – Shuffles tracks within the current album; next/previous navigates shuffled tracks; loops with Repeat Album if active.
3. **Albums (Mode 2)** – Plays albums in random order; moves to a random album when the last track finishes.
4. **Super Shuffle (Mode 3)** – Completely random track and album selection; avoids repeating the last 3 played tracks; works with next/previous buttons.

**Repeat Modes**
1. **Off (Mode 0)** – Plays through the playlist once and stops.
2. **Continuous (Mode 1)** – Plays through the entire playlist, moving to the next album automatically (default).
3. **Album (Mode 2)** – Loops the current album until manually changed.
4. **Track (Mode 3)** – Loops the current track; displays a "1" overlay on the repeat button.

**Mode Combinations**  
Shuffle and Repeat modes can be combined. For example:  
- *Shuffle Tracks + Repeat Album* → randomized tracks that loop within the album  
- *Super Shuffle + Repeat Off* → random tracks that don’t repeat until all have played

<img width="600" alt="screenshot-main" src="images/Playback modes.png" />

## Key Features

* **Executable** - Available in .exe format, simply download and run.
* **Automatic Updates** - Select automatic updates or check now to be notified when there is a new update and accept to install it automatically.
* **Compact Interface** - Minimal window design that stays out of your way.
* **Multiple View Modes** - Regular, Mini, Micro, and Nano modes available for different use cases.
* **Playlist Management** - Create and manage playlists of your favorite Bandcamp albums.
* **Always on Top** - Keep the player visible while working in other applications.
* **Keyboard Shortcuts** - Full keyboard control for play, pause, next, previous, volume, and more.
* **Detachable Playlist** - Detach the playlist window for flexible window management.
* **Autoplay** - Automatically starting playing on startup and when switching albums. 
* **Shuffle & Repeat** - Multiple shuffle and repeat modes for varied listening.
* **Volume Control** - Adjustable volume with visual feedback.
* **Dark Theme** - Beautiful dark interface that's easy on the eyes.

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




