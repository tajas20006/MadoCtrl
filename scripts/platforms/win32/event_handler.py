# -*- coding: utf-8 -*-

import threading
import atexit

import ctypes
import ctypes.wintypes
from ctypes import windll
import win32con
import win32gui

from ...constants import EventType, WindowType
from ..base import EventHandlerBase
from .key_converter import interpret_keycode, interpret_keyname
from .common import _pseudo_ws, get_win_type
from .window_controller import WindowController

# logging
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())


WinEventFuncType = ctypes.WINFUNCTYPE(
    None,
    ctypes.wintypes.HANDLE,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.HWND,
    ctypes.wintypes.LONG,
    ctypes.wintypes.LONG,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.DWORD
)

WinHookFuncType = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_void_p)
)

KEY_DOWN_TYPES = [0x100, 0x104]  # WM_KeyDown (normal), WM_SYSKEYDOWN (alt)
KEY_UP_TYPES = [0x101, 0x105]  # WM_KeyUp (normal), WM_SYSKEYUP (alt)


class KeyEventHandler(object):
    '''Sub event handler for Windows to capture key event'''

    def __init__(self, event_queue, modif_key):
        # Modifier
        self._modif_keycodes = interpret_keyname(modif_key)
        self._is_modif_down = False

        # Output queue
        self._out_event_queue = event_queue

    def _key_callback(self, n_code, w_param, l_param):
        # memo: l_param = [key_code, scan_code, alt_pressed (& 32), time)

        # Determine event type (up or down)
        key_code = l_param[0]
        if w_param in KEY_DOWN_TYPES:
            is_down = True
        elif w_param in KEY_UP_TYPES:
            is_down = False
        else:
            logger.warn('Unknown key event type: {}', w_param)

        # Update modifier status
        if key_code in self._modif_keycodes:
            self._is_modif_down = is_down

        # Check modifier is down
        if not self._is_modif_down:
            # Ignore this event
            return windll.user32.CallNextHookEx(self._key_hook_id, n_code,
                                                w_param, l_param)

        # Send key event
        if is_down:
            key_name = interpret_keycode(key_code)
            if key_name is not None:
                self._out_event_queue.put((EventType.KEY_PRESS, key_name))
            else:
                logger.debug('Unknown key is pressed (keycode: %d)', key_code)
        return True

    def register_hook(self):
        # Wrap and avoid auto-releasing
        self._key_event_callback = WinHookFuncType(self._key_callback)

        # Set key event hook
        self._key_hook_id = windll.user32.SetWindowsHookExA(
            0x00D, self._key_event_callback,
            windll.kernel32.GetModuleHandleW(None), 0)

        # Unhook at exit
        atexit.register(windll.user32.UnhookWindowsHookEx, self._key_hook_id)


class WindowEventHandler(object):
    '''Sub event handler for Windows to capture window event'''

    def __init__(self, event_queue):
        # Output queue
        self._out_event_queue = event_queue

        # Update pseudo workspace initially
        wins = WindowController.get_window_list()
        _pseudo_ws.update_wins(wins)

    def _win_callback(self, h_win_event_hook, event, hwnd, id_object, id_child,
                      dw_event_thread, dwms_event_time):
        # Ignore non application windows
        if get_win_type(hwnd) in [WindowType.OTHER, WindowType.DOCK]:
            return

        # Update pseudo workspace
        _pseudo_ws.update_win_raw(hwnd)

        # Send create / destroy event
        if event == win32con.EVENT_OBJECT_CREATE:
            self._out_event_queue.put((EventType.WIN_CREATE, None))
        elif event == win32con.EVENT_OBJECT_DESTROY:
            self._out_event_queue.put((EventType.WIN_DESTROY, None))

    def register_hook(self):
        # Wrap and avoid auto-releasing
        self._win_event_callback = WinEventFuncType(self._win_callback)

        # Set window event hook
        event_types = [
            win32con.EVENT_OBJECT_CREATE,
            win32con.EVENT_OBJECT_DESTROY,
        ]
        for event_type in event_types:
            h = windll.user32.SetWinEventHook(event_type, event_type, 0,
                                              self._win_event_callback, 0, 0,
                                              win32con.WINEVENT_OUTOFCONTEXT)
            if h:
                # Unhook at exit
                atexit.register(windll.user32.UnhookWinEvent, h)
            else:
                logger.warn("SetWinEventHook is failed (type: %d)", event_type)


class EventHandler(EventHandlerBase):
    '''Event handler for Windows'''

    def __init__(self, event_queue, modif_key):
        logger.debug('Create EventHandler instance (modif: "%s")', modif_key)

        # Create for each handler
        self._key_event_handler = KeyEventHandler(event_queue, modif_key)
        self._win_event_handler = WindowEventHandler(event_queue)

        # Start event capturing loop
        self._thread = threading.Thread(target=self._event_loop, daemon=True)
        self._thread.start()

    def _event_loop(self):
        logger.debug('Start event loop')

        self._key_event_handler.register_hook()
        self._win_event_handler.register_hook()

        while True:
            msg = windll.user32.GetMessageW(None, 0, 0, 0)
            windll.user32.TranslateMessage(byref(msg))
            windll.user32.DispatchMessageW(byref(msg))
