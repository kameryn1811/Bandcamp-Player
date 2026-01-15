"""
Bandcamp Player - Launcher
Self-contained launcher that bundles Python and auto-updates the main script.
"""

# Launcher version (update this when releasing a new launcher.exe)
__version__ = "2.0.0"

import sys
import os
import threading
import time
import runpy
import subprocess
from pathlib import Path
import json
import shutil

# GitHub repository information
REPO_OWNER = "kameryn1811"
REPO_NAME = "Bandcamp-Player"
SCRIPT_NAME = "bandcamp_pl_gui.py"
LAUNCHER_EXE_NAME = "BandcampPlayer.exe"

# Get launcher directory (where launcher.exe is located)
if hasattr(sys, 'frozen'):
    # Running as PyInstaller bundle
    LAUNCHER_DIR = Path(sys.executable).parent
    # In PyInstaller, bundled files are extracted to sys._MEIPASS
    # The script is bundled as a data file, so we need to copy it from _MEIPASS if it doesn't exist
    BUNDLED_SCRIPT = Path(sys._MEIPASS) / SCRIPT_NAME if hasattr(sys, '_MEIPASS') else None
else:
    # Running as script
    LAUNCHER_DIR = Path(__file__).resolve().parent
    BUNDLED_SCRIPT = None

SCRIPT_PATH = LAUNCHER_DIR / SCRIPT_NAME
SETTINGS_FILE = LAUNCHER_DIR / "launcher_settings.json"
GUI_SETTINGS_FILE = LAUNCHER_DIR / "settings.json"  # GUI's settings file
UPDATE_STATUS_FILE = LAUNCHER_DIR / "update_status.json"
UPDATE_DOWNLOAD_FLAG = LAUNCHER_DIR / "update_download_flag.json"  # Flag file to trigger download from GUI
LAUNCHER_EXE_PATH = Path(sys.executable) if hasattr(sys, 'frozen') else None


def show_error_dialog(title, message, details=None):
    """Show an error dialog, trying multiple methods to ensure it's visible.
    
    Args:
        title: Dialog title
        message: Main error message
        details: Optional detailed error information (traceback, etc.)
    """
    # Try tkinter first (most reliable)
    try:
        import tkinter.messagebox as messagebox
        import tkinter as tk
        
        # Create root window if it doesn't exist (hidden)
        try:
            root = tk._default_root
            if root is None:
                root = tk.Tk()
                root.withdraw()  # Hide the root window
        except:
            root = tk.Tk()
            root.withdraw()
        
        # Combine message and details if provided
        full_message = message
        if details:
            full_message = f"{message}\n\nDetails:\n{details}"
        
        messagebox.showerror(title, full_message)
        return
    except Exception:
        pass  # Fall through to next method
    
    # Try Windows MessageBox as fallback
    try:
        import ctypes
        from ctypes import wintypes
        
        # Combine message and details if provided
        full_message = message
        if details:
            full_message = f"{message}\n\nDetails:\n{details}"
        
        # Truncate if too long (Windows MessageBox has limits)
        if len(full_message) > 1000:
            full_message = full_message[:1000] + "\n\n... (truncated)"
        
        ctypes.windll.user32.MessageBoxW(
            0,
            full_message,
            title,
            0x10 | 0x0  # MB_ICONERROR | MB_OK
        )
        return
    except Exception:
        pass  # Fall through to last resort
    
    # Last resort: try to write to a log file
    try:
        log_file = LAUNCHER_DIR / "crash_log.txt"
        with open(log_file, 'a', encoding='utf-8') as f:
            from datetime import datetime
            f.write(f"\n{'='*60}\n")
            f.write(f"Crash at {datetime.now()}\n")
            f.write(f"Title: {title}\n")
            f.write(f"Message: {message}\n")
            if details:
                f.write(f"Details:\n{details}\n")
            f.write(f"{'='*60}\n")
    except Exception:
        pass  # If even logging fails, we're out of options


def setup_global_exception_handler():
    """Set up global exception handler to catch unhandled exceptions."""
    def exception_handler(exc_type, exc_value, exc_traceback):
        """Handle unhandled exceptions by showing error dialog."""
        if exc_type is KeyboardInterrupt:
            # Don't show dialog for user-initiated interrupts
            sys.exit(0)
        
        try:
            import traceback
            error_msg = f"An unexpected error occurred:\n\n{exc_type.__name__}: {exc_value}"
            traceback_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            
            show_error_dialog(
                "Bandcamp Player - Error",
                error_msg,
                traceback_str
            )
        except Exception:
            # If showing error dialog fails, at least try to log it
            try:
                log_file = LAUNCHER_DIR / "crash_log.txt"
                with open(log_file, 'a', encoding='utf-8') as f:
                    from datetime import datetime
                    import traceback
                    f.write(f"\n{'='*60}\n")
                    f.write(f"Fatal crash at {datetime.now()}\n")
                    f.write(f"Exception type: {exc_type.__name__}\n")
                    f.write(f"Exception value: {exc_value}\n")
                    f.write(f"Traceback:\n{''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))}\n")
                    f.write(f"{'='*60}\n")
            except Exception:
                pass
        
        # Exit with error code
        sys.exit(1)
    
    # Set the global exception handler
    sys.excepthook = exception_handler


def get_launcher_version():
    """Get version of the current launcher executable.
    
    Returns:
        Version string if found, None otherwise
    """
    # If running as script (not frozen), return version from this file
    if not hasattr(sys, 'frozen'):
        return __version__
    
    # If running as exe, try to get version from embedded data or file
    try:
        # Try to read version from launcher.py if it exists in the directory
        launcher_py = LAUNCHER_DIR / "launcher.py"
        if launcher_py.exists():
            with open(launcher_py, 'r', encoding='utf-8') as f:
                content = f.read()
                for line in content.split('\n'):
                    if '__version__' in line and '=' in line:
                        version = line.split('=')[1].strip().strip('"').strip("'")
                        return version
    except Exception:
        pass
    
    # Fallback: return embedded version (this is the version compiled into the exe)
    return __version__


def get_auto_check_updates_setting():
    """Read the auto-check updates setting from GUI's settings.json file.
    
    Returns:
        True if auto-check is enabled, False if disabled, True by default if setting not found
    """
    try:
        if GUI_SETTINGS_FILE.exists():
            with open(GUI_SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                return settings.get("auto_check_updates", True)  # Default to True if not found
    except Exception:
        pass  # If can't read settings, default to True
    return True  # Default to enabled if settings file doesn't exist


def get_local_version():
    """Get version from local script file."""
    if not SCRIPT_PATH.exists():
        return None
    
    try:
        with open(SCRIPT_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for __version__ = "x.x.x"
            for line in content.split('\n'):
                if '__version__' in line and '=' in line:
                    # Extract version string
                    version = line.split('=')[1].strip().strip('"').strip("'")
                    return version
    except Exception:
        pass
    
    return None


def get_latest_launcher_version():
    """Get latest launcher.exe version from launcher_manifest.json on GitHub.
    
    Returns:
        Tuple of (version_string, release_url, file_size) or (None, None, None) if error
        Note: release_url is the GitHub release page URL, not a direct download URL
    """
    try:
        import requests
        import json
        
        # Get manifest from GitHub main branch
        manifest_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/launcher_manifest.json"
        response = requests.get(manifest_url, timeout=10)
        response.raise_for_status()
        manifest = json.loads(response.text)
        
        version = manifest.get('version')
        # Use release_url if available, otherwise fall back to download_url
        release_url = manifest.get('release_url')
        if not release_url:
            # Fallback to download_url for backwards compatibility
            release_url = manifest.get('download_url')
        file_size = manifest.get('file_size', 0)
        
        if not version or not release_url:
            print("Warning: Invalid launcher manifest (missing version or release_url)")
            return None, None, None
        
        return version, release_url, file_size
    except ImportError:
        print("Warning: 'requests' library not found. Launcher update checking disabled.")
        return None, None, None
    except json.JSONDecodeError as e:
        print(f"Error parsing launcher manifest: {e}")
        return None, None, None
    except Exception as e:
        print(f"Error checking for launcher updates: {e}")
        return None, None, None


def get_latest_version():
    """Get latest version by reading directly from main branch file (not from releases)."""
    try:
        import requests
        import re
        # Get version directly from main branch file (not from releases)
        # This way we don't depend on releases being created/updated
        download_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/{SCRIPT_NAME}"
        response = requests.get(download_url, timeout=10)
        response.raise_for_status()
        file_content = response.text
        
        # Extract version from the file
        version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', file_content)
        if not version_match:
            print("Warning: Could not find version number in main branch file.")
            return None, None, None
        
        latest_version = version_match.group(1)
        
        # Return version, download URL, and None for release_data (not needed anymore)
        return latest_version, download_url, None
    except ImportError:
        print("Warning: 'requests' library not found. Update checking disabled.")
        return None, None, None
    except Exception as e:
        print(f"Error checking for updates: {e}")
        return None, None, None


def compare_versions(version1, version2):
    """Compare two version strings.
    
    Returns:
        -1 if version1 < version2
         0 if version1 == version2
         1 if version1 > version2
    """
    def version_tuple(v):
        parts = []
        for part in v.split('.'):
            try:
                parts.append(int(part))
            except ValueError:
                parts.append(0)
        return tuple(parts)
    
    v1_tuple = version_tuple(version1)
    v2_tuple = version_tuple(version2)
    
    max_len = max(len(v1_tuple), len(v2_tuple))
    v1_tuple = v1_tuple + (0,) * (max_len - len(v1_tuple))
    v2_tuple = v2_tuple + (0,) * (max_len - len(v2_tuple))
    
    if v1_tuple < v2_tuple:
        return -1
    elif v1_tuple > v2_tuple:
        return 1
    else:
        return 0


def write_update_status(message, version=None):
    """Write update status to file for GUI to read.
    
    Appends to existing messages if file exists, otherwise creates new.
    """
    try:
        messages = []
        if UPDATE_STATUS_FILE.exists():
            try:
                with open(UPDATE_STATUS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    messages = data.get("messages", [])
            except Exception:
                messages = []
        
        messages.append({
            "message": message,
            "version": version,
            "timestamp": time.time()
        })
        
        status = {
            "messages": messages,
            "latest_version": version
        }
        with open(UPDATE_STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(status, f)
    except Exception:
        pass  # Don't fail if we can't write status


def clear_update_status():
    """Clear update status file."""
    try:
        if UPDATE_STATUS_FILE.exists():
            UPDATE_STATUS_FILE.unlink()
    except Exception:
        pass


def download_script(download_url, expected_version=None):
    """Download the latest script from GitHub.
    
    Args:
        download_url: URL to download the script from
        expected_version: Expected version string to verify (optional)
    
    Returns:
        Script content as string, or None if error
    """
    try:
        import requests
        import re
        # Only log if we're actually updating (expected_version provided)
        if expected_version:
            write_update_status(f"Downloading v{expected_version} from GitHub...", expected_version)
        response = requests.get(download_url, timeout=30)
        response.raise_for_status()
        script_content = response.text
        
        # Verify the downloaded file's version if expected_version is provided
        if expected_version:
            version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', script_content)
            if version_match:
                downloaded_version = version_match.group(1)
                if downloaded_version != expected_version:
                    write_update_status(f"DEBUG: Downloaded file version: {downloaded_version}, Expected: {expected_version}", downloaded_version)
                if compare_versions(downloaded_version, expected_version) < 0:
                    write_update_status(f"Warning: Downloaded file version ({downloaded_version}) is older than expected ({expected_version})", downloaded_version)
        
        return script_content
    except Exception as e:
        write_update_status(f"Error downloading script: {e}")
        print(f"Error downloading script: {e}")
        return None


def check_and_update_script(silent=False):
    """Check for updates and download if needed.
    
    Args:
        silent: If True, don't print messages (for background check)
    
    Returns:
        True if update was downloaded, False otherwise
    """
    local_version = get_local_version()
    latest_version, download_url, _ = get_latest_version()
    
    if not latest_version:
        if not silent:
            print("Could not check for updates.")
        return False
    
    # If no local script, download it
    if not local_version:
        if not silent:
            print(f"Downloading script (v{latest_version})...")
        script_content = download_script(download_url, expected_version=latest_version)
        if script_content:
            SCRIPT_PATH.write_text(script_content, encoding='utf-8')
            write_update_status(f"Successfully updated to v{latest_version}!", latest_version)
            if not silent:
                print(f"Downloaded v{latest_version}")
            return True
        clear_update_status()
        return False
    
    # Compare versions
    if compare_versions(latest_version, local_version) > 0:
        if not silent:
            print(f"Update available: v{local_version} -> v{latest_version}")
        script_content = download_script(download_url, expected_version=latest_version)
        if script_content:
            # Create backup
            backup_path = SCRIPT_PATH.with_suffix('.py.backup')
            if SCRIPT_PATH.exists():
                import shutil
                shutil.copy2(SCRIPT_PATH, backup_path)
            
            # Write new version
            SCRIPT_PATH.write_text(script_content, encoding='utf-8')
            write_update_status(f"Successfully updated to v{latest_version}!", latest_version)
            if not silent:
                print(f"Updated to v{latest_version}")
            return True
        clear_update_status()
    elif not silent:
        print(f"Already up to date (v{local_version})")
        clear_update_status()
    
    return False


def run_script_directly():
    """Run the script directly in the current Python process (self-contained).
    
    This uses the embedded Python that's bundled with PyInstaller.
    """
    if not SCRIPT_PATH.exists():
        return False
    
    try:
        # Hide console window immediately if running as frozen exe (launcher mode)
        # This must happen BEFORE launching the script to prevent console flash
        if hasattr(sys, 'frozen') and sys.platform == 'win32':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                hwnd = kernel32.GetConsoleWindow()
                if hwnd:
                    # Free the console completely (removes it entirely)
                    kernel32.FreeConsole()
            except Exception:
                pass  # Silently fail if console hiding doesn't work
        
        # Set environment variable to indicate launcher mode
        os.environ['BANDCAMP_PLAYER_LAUNCHER'] = '1'
        # Set launcher version in environment variable for GUI to read
        launcher_version = get_launcher_version()
        if launcher_version:
            os.environ['BANDCAMP_PLAYER_LAUNCHER_VERSION'] = launcher_version
        
        # Change to script directory so relative imports work
        original_cwd = os.getcwd()
        os.chdir(LAUNCHER_DIR)
        
        try:
            # Use runpy.run_path to execute the script properly
            # This handles __name__ == '__main__' blocks correctly
            runpy.run_path(str(SCRIPT_PATH), run_name='__main__')
            return True
        finally:
            # Restore original working directory
            os.chdir(original_cwd)
            
    except Exception as e:
        # If direct execution fails, show error using our error dialog function
        import traceback
        error_msg = f"Error launching script:\n{str(e)}"
        traceback_str = traceback.format_exc()
        show_error_dialog("Launch Error", error_msg, traceback_str)
        return False


def check_launcher_update(silent=False):
    """Check for launcher.exe updates.
    
    When an update is available, opens the browser to the GitHub release page
    where the user can manually download and replace the .exe file.
    The .exe is large (~200MB), so manual download is preferred.
    
    Args:
        silent: If True, don't show dialogs (for background check)
    
    Returns:
        False (always returns False since we no longer auto-download)
    """
    if not hasattr(sys, 'frozen'):
        # Not running as exe, skip launcher update check
        return False
    
    try:
        current_version = get_launcher_version()
        latest_version, release_url, file_size = get_latest_launcher_version()
        
        if not latest_version or not release_url:
            if not silent:
                write_update_status(f"Could not check for launcher updates (version: {current_version})")
            return False
        
        # Compare versions
        comparison = compare_versions(latest_version, current_version)
        if comparison > 0:
            # Update available
            if not silent:
                # Show update dialog that opens browser to release page
                show_launcher_update_dialog(current_version, latest_version, release_url)
            # Note: We no longer auto-download the .exe (it's ~200MB)
            # User must manually download and replace it
            return False
        elif not silent:
            write_update_status(f"Launcher is up to date (v{current_version})")
        
        return False
    except Exception as e:
        error_msg = f"Error checking for launcher updates: {e}"
        if not silent:
            write_update_status(error_msg)
        return False


def show_launcher_update_dialog(current_version, latest_version, release_url):
    """Show dialog for launcher update and open browser to release page.
    
    Args:
        current_version: Current launcher version
        latest_version: Latest available version
        release_url: URL to GitHub release page where user can download the .exe
    """
    try:
        import tkinter.messagebox as messagebox
        import webbrowser
        
        message = (
            f"A new launcher version is available!\n\n"
            f"Current version: v{current_version}\n"
            f"Latest version: v{latest_version}\n\n"
            f"The launcher file is large (~200MB), so please download it manually from GitHub.\n\n"
            f"Would you like to open the release page in your browser now?\n\n"
            f"After downloading, simply replace the old BandcampPlayer.exe with the new one."
        )
        
        response = messagebox.askyesno("Launcher Update Available", message)
        
        if response:
            # Open browser to release page
            try:
                webbrowser.open(release_url)
                write_update_status(f"Opened release page for launcher v{latest_version}")
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Could not open browser.\n\nPlease visit:\n{release_url}\n\nmanually."
                )
                write_update_status(f"Error opening browser: {e}")
        else:
            write_update_status(f"Launcher update available (v{latest_version}) - user declined")
    except Exception as e:
        write_update_status(f"Error showing launcher update dialog: {e}")


# Installing dialog removed - was causing blank window issues
# Extraction now happens silently before GUI is created


def main():
    """Main launcher entry point."""
    # Set up global exception handler FIRST (before hiding console)
    # This ensures errors are shown even when console is hidden
    setup_global_exception_handler()
    
    # Hide console window immediately if running as frozen exe
    # This must happen early, but after exception handler setup
    if hasattr(sys, 'frozen') and sys.platform == 'win32':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            hwnd = kernel32.GetConsoleWindow()
            if hwnd:
                # Free the console completely (removes it entirely)
                kernel32.FreeConsole()
        except Exception:
            pass  # Silently fail if console hiding doesn't work
    
    # Extract bundled files to launcher directory if needed
    def extract_bundled_files():
        """Extract bundled files in background to avoid blocking startup."""
        if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
            bundle_dir = Path(sys._MEIPASS)
            
            # Extract icon.ico from bundle if it doesn't exist
            icon_path = LAUNCHER_DIR / "icon.ico"
            if not icon_path.exists():
                bundled_icon = bundle_dir / "icon.ico"
                if bundled_icon.exists():
                    try:
                        shutil.copy2(bundled_icon, icon_path)
                    except Exception:
                        pass
            
            # Extract bandcamp_player_hotkeys.ahk from bundle if it doesn't exist
            ahk_path = LAUNCHER_DIR / "bandcamp_player_hotkeys.ahk"
            if not ahk_path.exists():
                bundled_ahk = bundle_dir / "bandcamp_player_hotkeys.ahk"
                if bundled_ahk.exists():
                    try:
                        shutil.copy2(bundled_ahk, ahk_path)
                    except Exception:
                        pass
            
            # Extract icon-hotkeys.ico from bundle if it doesn't exist
            hotkeys_icon_path = LAUNCHER_DIR / "icon-hotkeys.ico"
            if not hotkeys_icon_path.exists():
                bundled_hotkeys_icon = bundle_dir / "icon-hotkeys.ico"
                if bundled_hotkeys_icon.exists():
                    try:
                        shutil.copy2(bundled_hotkeys_icon, hotkeys_icon_path)
                    except Exception:
                        pass
            
            # Extract logo from bundle if it doesn't exist
            logo_dir = LAUNCHER_DIR / "Logo"
            logo_path = logo_dir / "bandcamp-button-circle-line-aqua-128.png"
            if not logo_path.exists():
                bundled_logo = bundle_dir / "Logo" / "bandcamp-button-circle-line-aqua-128.png"
                if bundled_logo.exists():
                    try:
                        # Create Logo directory if it doesn't exist
                        logo_dir.mkdir(exist_ok=True)
                        shutil.copy2(bundled_logo, logo_path)
                    except Exception:
                        pass
    
    # Extract files in background thread (non-blocking)
    extraction_thread = threading.Thread(target=extract_bundled_files, daemon=True)
    extraction_thread.start()
    
    # If script doesn't exist, extract immediately (required for app to run)
    # Extract silently - no dialog to avoid blank window issues
    if not SCRIPT_PATH.exists() and BUNDLED_SCRIPT and BUNDLED_SCRIPT.exists():
        try:
            # Extract script (this can take a moment on first run)
            shutil.copy2(BUNDLED_SCRIPT, SCRIPT_PATH)
        except Exception as e:
            # Show error if extraction fails (only if GUI is available)
            try:
                import tkinter.messagebox as messagebox
                messagebox.showerror(
                    "Extraction Error",
                    f"Failed to extract {SCRIPT_NAME}:\n{str(e)}\n\nPlease try again."
                )
            except:
                pass
            sys.exit(1)
    
    # Launch the script immediately (using bundled version if available)
    # Check for updates in background AFTER launching (non-blocking, delayed)
    # Only check if auto-check updates is enabled in settings
    # Note: Script updates are now handled by the GUI after URL loads to avoid
    # interfering with JavaScript initialization. Only launcher updates are checked here.
    def check_updates_background():
        # Delay significantly to avoid interfering with JavaScript initialization
        # On first launch, JavaScript injection happens at 2s, 4s, 6s, 8s after page load
        # We delay until well after this period to ensure no interference
        time.sleep(15)
        
        # Check if auto-update is enabled in GUI settings
        auto_check_enabled = get_auto_check_updates_setting()
        if not auto_check_enabled:
            return
        
        # Script updates are now handled by the GUI after a URL loads
        # (see bandcamp_pl_gui.py on_page_loaded method)
        # This ensures the update dialog doesn't interfere with JavaScript initialization
        
        # Check for launcher updates (show dialog if update available)
        # This is delayed to avoid interfering with app initialization
        check_launcher_update(silent=False)
    
    def check_download_flag():
        """Check if GUI requested download and process it."""
        if UPDATE_DOWNLOAD_FLAG.exists():
            try:
                with open(UPDATE_DOWNLOAD_FLAG, 'r', encoding='utf-8') as f:
                    flag_data = json.load(f)
                    if flag_data.get('download', False):
                        # User approved download - proceed with update
                        check_and_update_script(silent=True)
                    # Clean up flag file
                    UPDATE_DOWNLOAD_FLAG.unlink()
            except Exception:
                # If flag file is invalid, just delete it
                try:
                    UPDATE_DOWNLOAD_FLAG.unlink()
                except:
                    pass
    
    # Check for download flag periodically (every 2 seconds)
    def monitor_download_flag():
        while True:
            # No need to poll aggressively; user-triggered updates are infrequent.
            time.sleep(5)
            check_download_flag()
    
    # Start flag monitor in background
    flag_monitor_thread = threading.Thread(target=monitor_download_flag, daemon=True)
    flag_monitor_thread.start()
    
    # Start update check in background (non-blocking)
    auto_check_enabled = get_auto_check_updates_setting()
    if auto_check_enabled:
        update_thread = threading.Thread(target=check_updates_background, daemon=True)
        update_thread.start()
    
    # Also copy icon.ico from parent if it doesn't exist (for development)
    icon_path = LAUNCHER_DIR / "icon.ico"
    if not icon_path.exists():
        parent_icon = LAUNCHER_DIR.parent / "icon.ico"
        if parent_icon.exists():
            try:
                shutil.copy2(parent_icon, icon_path)
            except Exception:
                pass
    
    # Launch the script immediately (uses embedded Python - truly self-contained)
    launch_script()


def launch_script():
    """Launch the main script directly in the current Python process (self-contained)."""
    if not SCRIPT_PATH.exists():
        show_error_dialog(
            "Error",
            f"{SCRIPT_NAME} not found!\n\nPlease ensure the script is downloaded."
        )
        return
    
    # Run the script directly in the current embedded Python process
    success = run_script_directly()
    
    # If script completes, exit launcher
    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Catch any errors during main() execution
        # This is a fallback in case the global exception handler wasn't set up yet
        try:
            setup_global_exception_handler()
            show_error_dialog(
                "Fatal Error",
                f"Failed to start Bandcamp Player:\n\n{str(e)}",
                str(e)
            )
        except Exception:
            # Last resort: try to write to log file
            try:
                log_file = Path(__file__).parent / "crash_log.txt" if not hasattr(sys, 'frozen') else LAUNCHER_DIR / "crash_log.txt"
                with open(log_file, 'a', encoding='utf-8') as f:
                    from datetime import datetime
                    import traceback
                    f.write(f"\n{'='*60}\n")
                    f.write(f"Fatal startup crash at {datetime.now()}\n")
                    f.write(f"Error: {str(e)}\n")
                    f.write(f"Traceback:\n{traceback.format_exc()}\n")
                    f.write(f"{'='*60}\n")
            except Exception:
                pass
        sys.exit(1)
