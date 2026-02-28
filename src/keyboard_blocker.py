"""
Keyboard Cleaning App — Low-Level Keyboard Blocker

Uses Windows SetWindowsHookEx with WH_KEYBOARD_LL to intercept
and suppress all keyboard input.
"""

import ctypes
import ctypes.wintypes
import threading

# ─── Windows API Constants ────────────────────────────────────────────
WH_KEYBOARD_LL = 13
WM_QUIT = 0x0012
HC_ACTION = 0

# ─── Correct types for 32-bit AND 64-bit Windows ─────────────────────
# LRESULT is pointer-sized (LONG_PTR): 32-bit on x86, 64-bit on x64.
# Using LPARAM (which is also LONG_PTR) gives us the right size.
LRESULT = ctypes.wintypes.LPARAM

# WINFUNCTYPE = __stdcall (required for Windows callbacks)
# CFUNCTYPE = __cdecl (wrong for hook callbacks)
HOOKPROC = ctypes.WINFUNCTYPE(
    LRESULT,                   # LRESULT return
    ctypes.c_int,              # nCode
    ctypes.wintypes.WPARAM,    # wParam
    ctypes.wintypes.LPARAM,    # lParam
)

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# ─── API Signatures ──────────────────────────────────────────────────
user32.SetWindowsHookExW.restype = ctypes.wintypes.HHOOK
user32.SetWindowsHookExW.argtypes = [
    ctypes.c_int,
    HOOKPROC,
    ctypes.wintypes.HINSTANCE,
    ctypes.wintypes.DWORD,
]

user32.CallNextHookEx.restype = LRESULT
user32.CallNextHookEx.argtypes = [
    ctypes.wintypes.HHOOK,
    ctypes.c_int,
    ctypes.wintypes.WPARAM,
    ctypes.wintypes.LPARAM,
]

user32.UnhookWindowsHookEx.restype = ctypes.wintypes.BOOL
user32.UnhookWindowsHookEx.argtypes = [ctypes.wintypes.HHOOK]

user32.GetMessageW.argtypes = [
    ctypes.POINTER(ctypes.wintypes.MSG),
    ctypes.wintypes.HWND,
    ctypes.wintypes.UINT,
    ctypes.wintypes.UINT,
]

user32.TranslateMessage.argtypes = [ctypes.POINTER(ctypes.wintypes.MSG)]
user32.DispatchMessageW.argtypes = [ctypes.POINTER(ctypes.wintypes.MSG)]

user32.PostThreadMessageW.argtypes = [
    ctypes.wintypes.DWORD,
    ctypes.wintypes.UINT,
    ctypes.wintypes.WPARAM,
    ctypes.wintypes.LPARAM,
]

kernel32.GetModuleHandleW.restype = ctypes.wintypes.HMODULE
kernel32.GetModuleHandleW.argtypes = [ctypes.wintypes.LPCWSTR]

kernel32.GetCurrentThreadId.restype = ctypes.wintypes.DWORD


class KeyboardBlocker:
    """Blocks all keyboard input using a Windows low-level keyboard hook.

    The hook runs in a dedicated thread with its own message pump,
    so tkinter's main loop remains responsive.
    """

    def __init__(self):
        self._hook_handle = None
        self._hook_thread = None
        self._thread_id = None
        self._callback = None  # prevent garbage collection of the callback
        self._lock = threading.Lock()

    @property
    def is_blocking(self) -> bool:
        """True if the keyboard hook is currently installed."""
        return self._hook_handle is not None

    def start_blocking(self) -> bool:
        """Install the low-level keyboard hook in a background thread.

        Returns True if the hook was installed successfully.
        """
        with self._lock:
            if self._hook_handle is not None:
                return True  # already blocking

            ready_event = threading.Event()
            self._hook_thread = threading.Thread(
                target=self._hook_thread_func,
                args=(ready_event,),
                daemon=True,
            )
            self._hook_thread.start()
            ready_event.wait(timeout=5.0)
            return self._hook_handle is not None

    def stop_blocking(self) -> None:
        """Remove the keyboard hook and stop the message pump thread."""
        with self._lock:
            if self._hook_handle is None:
                return  # not blocking

            # Post WM_QUIT to the hook thread's message pump
            if self._thread_id is not None:
                user32.PostThreadMessageW(
                    self._thread_id, WM_QUIT, 0, 0
                )

        # Wait for thread to finish (outside lock to avoid deadlock)
        if self._hook_thread is not None:
            self._hook_thread.join(timeout=3.0)

        with self._lock:
            self._hook_handle = None
            self._hook_thread = None
            self._thread_id = None

    def _hook_thread_func(self, ready_event: threading.Event) -> None:
        """Thread entry: install hook, run message pump, cleanup on exit."""
        self._thread_id = kernel32.GetCurrentThreadId()

        # Create the callback — prevent GC for the lifetime of the hook
        self._callback = HOOKPROC(self._low_level_handler)

        h_mod = kernel32.GetModuleHandleW(None)

        h_hook = user32.SetWindowsHookExW(
            WH_KEYBOARD_LL,
            self._callback,
            h_mod,
            0,
        )

        if not h_hook:
            err = ctypes.get_last_error()
            print(f"[KeyboardBlocker] SetWindowsHookExW failed (error {err})")
            ready_event.set()
            return

        self._hook_handle = h_hook
        ready_event.set()

        # Message pump — REQUIRED for low-level hooks.
        # The OS delivers hook callbacks via the thread message queue,
        # so we must pump messages for the hook to fire.
        msg = ctypes.wintypes.MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

        # Cleanup
        user32.UnhookWindowsHookEx(h_hook)

    def _low_level_handler(self, n_code, w_param, l_param):
        """Hook callback — suppress all keyboard events."""
        try:
            if n_code == HC_ACTION:
                # Return 1 to swallow the key event (don't pass it along)
                return 1
        except Exception:
            pass
        return user32.CallNextHookEx(self._hook_handle, n_code, w_param, l_param)
