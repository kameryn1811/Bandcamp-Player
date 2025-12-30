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
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BandcampPlayer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compress executable (reduces size)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Hide console window - launch silently
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'  # Use the same icon as the main app
)

