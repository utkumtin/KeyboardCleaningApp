# 🧹 Keyboard Cleaning App

A minimal Windows utility that temporarily disables keyboard input while you clean your keyboard.

## Features

- **One-click lock/unlock** — Toggle keyboard input with a single button
- **Zen dark-mode UI** — Distraction-free, minimal interface
- **Zero dependencies** — Uses only Python standard library
- **Lightweight** — Minimal system resource usage

## Requirements

- Windows 10/11
- Python 3.8+
- **Administrator privileges** (required for keyboard hooks)

## Usage

### Option 1: Double-click
Run `run.bat` — it will automatically request admin privileges.

### Option 2: Command line
```bash
python -m src.main
```

## How It Works

The app uses Windows' low-level keyboard hook (`SetWindowsHookEx` with `WH_KEYBOARD_LL`) to intercept and suppress all keyboard input while locked. The hook is cleanly removed when unlocked or when the app is closed.

## Safety

- The mouse always remains active, so you can always unlock or close the app
- Closing the window automatically removes the keyboard hook
- The app requires admin privileges to install keyboard hooks
