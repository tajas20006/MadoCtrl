# -*- coding: utf-8 -*-

import ctypes
import ctypes.wintypes
from ctypes import windll
import win32con
import win32gui

from ...constants import WindowType
from .pseudo_workspace import PseudoWorkspace


# Pseudo workspace
_pseudo_ws = PseudoWorkspace()


# Store default hidden windows
class DefaultHiddenWinows:
    def __init__(self):
        self._wins = list()

        def enum_handler(hwnd, l_param):
            if not win32gui.IsWindowVisible(hwnd):
                self._wins.append(hwnd)
        win32gui.EnumWindows(enum_handler, None)

    def check(self, hwnd):
        return hwnd in self._wins


_default_hidden_wins = DefaultHiddenWinows()


# Window type judger
class TitlebarInfoType(ctypes.Structure):
    pass


TitlebarInfoType._fields_ = [
    ('cbSize', ctypes.wintypes.DWORD),
    ('rcTitleBar', ctypes.wintypes.RECT),
    ('rgstate', ctypes.wintypes.DWORD * 6),
]


def get_win_type(hwnd):
    # TODO: Improve the conditions
    # Note: No DOCK type

    # Is default hidden window?
    if _default_hidden_wins.check(hwnd):
        return WindowType.OTHER

    # Is an invalid window?
    if not win32gui.IsWindow(hwnd) or not win32gui.IsWindowEnabled(hwnd) or \
       not win32gui.GetWindowText(hwnd):
        return WindowType.OTHER

    # Detect desktop and task tray application
    title_info = TitlebarInfoType()
    title_info.cbSize = ctypes.sizeof(title_info)
    ctypes.windll.user32.GetTitleBarInfo(hwnd, ctypes.byref(title_info))
    if title_info.rgstate[0] & win32con.STATE_SYSTEM_INVISIBLE:
        return WindowType.OTHER

    # Is specific class?
    class_name = win32gui.GetClassName(hwnd)
    if class_name == '#32770':  # Dialog
        return WindowType.DIALOG

    # Is non-application window?
    if win32gui.GetParent(hwnd):
        return WindowType.OTHER

    # Is Floating or non-resizable?
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    if not style & win32con.WS_SIZEBOX or \
       ex_style & win32con.WS_EX_TOOLWINDOW or \
       ex_style & win32con.WS_EX_TOPMOST:
        return WindowType.DIALOG
    else:
        return WindowType.NORMAL
