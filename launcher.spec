# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Bandcamp Player Launcher
This creates a self-contained launcher.exe that bundles Python and can download/update the main script.
"""

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('bandcamp_pl_gui.py', '.'),  # Bundle the script as a fallback (will be updated from GitHub)
        ('icon.ico', '.'),  # Bundle icon.ico (will be extracted to launcher directory on first run)
        ('bandcamp_player_hotkeys.ahk', '.'),  # Bundle AutoHotkey script (will be extracted to launcher directory on first run)
        ('icon-hotkeys.ico', '.'),  # Bundle AutoHotkey icon (will be extracted to launcher directory on first run)
        ('Logo/bandcamp-button-circle-line-aqua-128.png', 'Logo'),  # Bundle logo (will be extracted to Logo directory on first run)
    ],
    hiddenimports=[
        'requests',  # Required for GitHub API calls
        'json',
        'pathlib',
        'subprocess',
        'threading',
        # Standard library modules used by bandcamp_pl_gui.py
        'webbrowser',
        'tempfile',
        'hashlib',
        'ctypes',
        'ctypes.wintypes',
        'urllib.request',
        'urllib.parse',
        'urllib.error',
        'tkinter',
        'tkinter.messagebox',
        # PyQt6 modules required by bandcamp_pl_gui.py
        # Even though launcher.py doesn't import them, the script does
        # PyInstaller needs these to bundle PyQt6 with the launcher
        'PyQt6',
        'PyQt6.QtWidgets',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWebEngineWidgets',
        'PyQt6.QtWebEngineCore',
        'PyQt6.QtNetwork',
        'qtawesome',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size and scan time
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'PIL._tkinter_finder',  # Not needed for launcher
        'test',
        'unittest',
        'pydoc',
        'doctest',
        # PyQt6 modules not used by this app (conservative list)
        # Note: QtWebEngine is still bundled (size is dominated by Chromium).
        'PyQt6.QtMultimedia',
        'PyQt6.QtMultimediaWidgets',
        'PyQt6.QtSql',
        'PyQt6.QtTest',
        'PyQt6.QtDesigner',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    [],
    name='BandcampPlayer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Faster startup (avoid UPX decompression / AV overhead)
    runtime_tmpdir=None,  # Use default temp dir (faster than custom location for antivirus)
    console=False,  # Hide console window - launch silently
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',  # Use the same icon as the main app
    exclude_binaries=True,  # onedir: collect binaries separately (no onefile extraction)
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='BandcampPlayer'
)

