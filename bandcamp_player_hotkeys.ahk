#Requires AutoHotkey v2.0
#SingleInstance Force

; Bandcamp Player Global Hotkeys
; Auto-generated script for Bandcamp Player
; This script enables global hotkeys for Bandcamp Player even when the window is not focused.
; 
; INSTRUCTIONS:
; 1. Install AutoHotkey v2 from https://www.autohotkey.com/download/
; 2. Right-click this script and select "Run Script" or double-click it
; 3. The script will run in the background and enable global hotkeys
; 4. To stop, right-click the AutoHotkey icon in the system tray and select "Exit"

; Set custom icon (if icon-hotkeys.ico exists in the same directory as this script)
iconPath := A_ScriptDir . "\icon-hotkeys.ico"
if (FileExist(iconPath)) {
    try {
        TraySetIcon(iconPath)
    } catch {
        ; Silently fail if icon can't be set
    }
}

; Media keys (hardware media keys)
$Media_Play_Pause::SendBandcampPlayerCommand("playpause")
$Media_Next::SendBandcampPlayerCommand("next")
$Media_Prev::SendBandcampPlayerCommand("prev")

; Bandcamp Player specific shortcuts
; Media controls
^!Right::SendBandcampPlayerCommand("next")          ; Next Track: Ctrl+Alt+Right
^!Left::SendBandcampPlayerCommand("prev")           ; Previous Track: Ctrl+Alt+Left
^!Space::SendBandcampPlayerCommand("playpause")    ; Play/Pause: Ctrl+Alt+Space

; Album navigation
^+!Right::SendBandcampPlayerCommand("next_album")   ; Next Album: Ctrl+Shift+Alt+Right
^+!Left::SendBandcampPlayerCommand("prev_album")   ; Previous Album: Ctrl+Shift+Alt+Left

; Volume controls
^+Up::SendBandcampPlayerCommand("volume_up")       ; Volume Up: Ctrl+Shift+Up
^+Down::SendBandcampPlayerCommand("volume_down")    ; Volume Down: Ctrl+Shift+Down
^+m::SendBandcampPlayerCommand("mute")              ; Mute: Ctrl+Shift+M

; Playlist and UI controls
^!p::SendBandcampPlayerCommand("toggle_playlist")              ; Toggle Playlist: Ctrl+Alt+P
^+!p::SendBandcampPlayerCommand("toggle_playlist_expand")     ; Toggle Playlist Expand: Ctrl+Shift+Alt+P
^!m::SendBandcampPlayerCommand("cycle_app_mode")               ; Cycle App Mode: Ctrl+Alt+M

; Function to send commands to Bandcamp Player via named pipe
SendBandcampPlayerCommand(command) {
    pipeName := "\\.\pipe\BandcampPlayerIPC"
    
    ; Try to connect to named pipe and send command
    ; GENERIC_WRITE = 0x40000000, OPEN_EXISTING = 3
    ; INVALID_HANDLE_VALUE = -1 (0xFFFFFFFF)
    pipe := DllCall("CreateFile", "Str", pipeName, "UInt", 0x40000000, "UInt", 0, "Ptr", 0, "UInt", 3, "UInt", 0, "Ptr", 0, "Ptr")
    INVALID_HANDLE_VALUE := -1
    if (pipe != INVALID_HANDLE_VALUE && pipe != 0) {
        ; Successfully connected - send command with newline
        bytesWritten := 0
        commandWithNewline := command . "`n"
        commandBytes := Buffer(StrLen(commandWithNewline) + 1, 0)
        StrPut(commandWithNewline, commandBytes, "UTF-8")
        success := DllCall("WriteFile", "Ptr", pipe, "Ptr", commandBytes.Ptr, "UInt", StrLen(commandWithNewline), "UInt*", &bytesWritten, "Ptr", 0)
        DllCall("FlushFileBuffers", "Ptr", pipe)  ; Ensure data is sent
        DllCall("CloseHandle", "Ptr", pipe)
        if (success) {
            return true  ; Successfully sent via named pipe
        }
    }
    return false  ; Failed to connect or send
}
