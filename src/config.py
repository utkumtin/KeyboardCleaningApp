"""
Keyboard Cleaning App — Configuration & Constants

Zen dark-mode color palette, dimensions, and font definitions.
"""

# ─── Window ───────────────────────────────────────────────────────────
APP_TITLE = "Keyboard Cleaner"
WINDOW_WIDTH = 350
WINDOW_HEIGHT = 220
WINDOW_RESIZABLE = False

# ─── Zen Color Palette ───────────────────────────────────────────────
BG_PRIMARY = "#1a1a2e"       # Deep indigo — main background
BG_SECONDARY = "#16213e"     # Slightly lighter — card/frame background
TEXT_PRIMARY = "#e0d6c8"     # Warm sand — primary text
TEXT_SECONDARY = "#8a8a9a"   # Muted lavender — secondary text
TEXT_LOCKED = "#e74c3c"      # Soft red — locked status

BTN_LOCK_BG = "#0f3460"     # Deep blue — lock button
BTN_LOCK_FG = "#e0d6c8"     # Sand — lock button text
BTN_LOCK_HOVER = "#1a4a7a"  # Lighter blue — lock hover

BTN_UNLOCK_BG = "#1b4332"   # Deep green — unlock button
BTN_UNLOCK_FG = "#e0d6c8"   # Sand — unlock button text
BTN_UNLOCK_HOVER = "#2d6a4f" # Lighter green — unlock hover

BORDER_COLOR = "#2a2a4a"     # Subtle border

# ─── Fonts ────────────────────────────────────────────────────────────
FONT_STATUS = ("Segoe UI", 14, "normal")
FONT_ICON = ("Segoe UI Emoji", 28, "normal")
FONT_BUTTON = ("Segoe UI", 11, "bold")
FONT_HINT = ("Segoe UI", 8, "normal")

# ─── Status Messages ─────────────────────────────────────────────────
STATUS_ACTIVE = "Keyboard Active"
STATUS_LOCKED = "Keyboard Locked"
ICON_ACTIVE = "⌨️"
ICON_LOCKED = "🔒"

BTN_TEXT_LOCK = "Lock Keyboard"
BTN_TEXT_UNLOCK = "Unlock Keyboard"

HINT_TEXT = "Mouse always remains active"
