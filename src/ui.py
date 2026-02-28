"""
Keyboard Cleaning App — Zen Dark-Mode UI

Minimal tkinter window with a single toggle button for
locking/unlocking the keyboard.
"""

import tkinter as tk

from . import config as cfg
from .keyboard_blocker import KeyboardBlocker


class App:
    """Main application window — zen dark-mode keyboard locker."""

    def __init__(self):
        self._blocker = KeyboardBlocker()
        self._locked = False

        # ─── Root Window ──────────────────────────────────────────
        self.root = tk.Tk()
        self.root.title(cfg.APP_TITLE)
        self.root.geometry(f"{cfg.WINDOW_WIDTH}x{cfg.WINDOW_HEIGHT}")
        self.root.resizable(cfg.WINDOW_RESIZABLE, cfg.WINDOW_RESIZABLE)
        self.root.configure(bg=cfg.BG_PRIMARY)
        self.root.attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # Center the window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (cfg.WINDOW_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (cfg.WINDOW_HEIGHT // 2)
        self.root.geometry(f"+{x}+{y}")

        # ─── Main Container ──────────────────────────────────────
        container = tk.Frame(self.root, bg=cfg.BG_PRIMARY)
        container.pack(expand=True, fill="both", padx=24, pady=20)

        # ─── Status Icon ──────────────────────────────────────────
        self._icon_label = tk.Label(
            container,
            text=cfg.ICON_ACTIVE,
            font=cfg.FONT_ICON,
            bg=cfg.BG_PRIMARY,
            fg=cfg.TEXT_PRIMARY,
        )
        self._icon_label.pack(pady=(10, 4))

        # ─── Status Text ─────────────────────────────────────────
        self._status_label = tk.Label(
            container,
            text=cfg.STATUS_ACTIVE,
            font=cfg.FONT_STATUS,
            bg=cfg.BG_PRIMARY,
            fg=cfg.TEXT_PRIMARY,
        )
        self._status_label.pack(pady=(0, 16))

        # ─── Toggle Button ───────────────────────────────────────
        self._btn = tk.Button(
            container,
            text=cfg.BTN_TEXT_LOCK,
            font=cfg.FONT_BUTTON,
            bg=cfg.BTN_LOCK_BG,
            fg=cfg.BTN_LOCK_FG,
            activebackground=cfg.BTN_LOCK_HOVER,
            activeforeground=cfg.BTN_LOCK_FG,
            relief="flat",
            cursor="hand2",
            bd=0,
            padx=24,
            pady=10,
            command=self._toggle,
        )
        self._btn.pack(ipadx=12, ipady=4)

        # Hover effects
        self._btn.bind("<Enter>", self._on_btn_enter)
        self._btn.bind("<Leave>", self._on_btn_leave)

        # ─── Hint ────────────────────────────────────────────────
        tk.Label(
            container,
            text=cfg.HINT_TEXT,
            font=cfg.FONT_HINT,
            bg=cfg.BG_PRIMARY,
            fg=cfg.TEXT_SECONDARY,
        ).pack(pady=(12, 0))

    # ─── Public ───────────────────────────────────────────────────

    def run(self) -> None:
        """Start the tkinter main loop."""
        self.root.mainloop()

    # ─── Private ──────────────────────────────────────────────────

    def _toggle(self) -> None:
        """Toggle between locked and unlocked states."""
        if self._locked:
            self._unlock()
        else:
            self._lock()

    def _lock(self) -> None:
        """Lock the keyboard and update the UI."""
        self._blocker.start_blocking()
        self._locked = True

        self._icon_label.config(text=cfg.ICON_LOCKED)
        self._status_label.config(text=cfg.STATUS_LOCKED, fg=cfg.TEXT_LOCKED)
        self._btn.config(
            text=cfg.BTN_TEXT_UNLOCK,
            bg=cfg.BTN_UNLOCK_BG,
            activebackground=cfg.BTN_UNLOCK_HOVER,
        )

    def _unlock(self) -> None:
        """Unlock the keyboard and update the UI."""
        self._blocker.stop_blocking()
        self._locked = False

        self._icon_label.config(text=cfg.ICON_ACTIVE)
        self._status_label.config(text=cfg.STATUS_ACTIVE, fg=cfg.TEXT_PRIMARY)
        self._btn.config(
            text=cfg.BTN_TEXT_LOCK,
            bg=cfg.BTN_LOCK_BG,
            activebackground=cfg.BTN_LOCK_HOVER,
        )

    def _on_close(self) -> None:
        """Clean shutdown — ensure hook is removed before exit."""
        if self._locked:
            self._blocker.stop_blocking()
        self.root.destroy()

    def _on_btn_enter(self, _event) -> None:
        """Mouse enters button — apply hover color."""
        if self._locked:
            self._btn.config(bg=cfg.BTN_UNLOCK_HOVER)
        else:
            self._btn.config(bg=cfg.BTN_LOCK_HOVER)

    def _on_btn_leave(self, _event) -> None:
        """Mouse leaves button — restore normal color."""
        if self._locked:
            self._btn.config(bg=cfg.BTN_UNLOCK_BG)
        else:
            self._btn.config(bg=cfg.BTN_LOCK_BG)
