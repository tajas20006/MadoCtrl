# -*- coding: utf-8 -*-

# TODO: Replace pywin32 with ctypes.windll

import win32api
import win32con
import win32com.client
import win32ui
import win32gui

from ...constants import WindowType
from ..base import WindowBase, WindowControllerBase

# logging
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())


# Win32API entry point
_shell = win32com.client.Dispatch("WScript.Shell")


def _get_win_type(hwnd):
    # TODO: Improve the conditions
    # Note: No DOCK type

    # Is an invalid window?
    if not win32gui.IsWindowVisible(hwnd) or not win32gui.GetWindowText(hwnd):
        return WindowType.OTHER

    # Is non-application window?
    if win32gui.GetParent(hwnd) != 0:
        # Is dialog class?
        class_name = win32gui.GetClassName(hwnd)
        if class_name == '#32770':
            return WindowType.DIALOG
        else:
            return WindowType.OTHER

    # Is Floating or non-resizable?
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    if ex_style & win32con.WS_EX_TOOLWINDOW or \
       ex_style & win32con.WS_EX_TOPMOST or \
       not style & win32con.WS_SIZEBOX:
        return WindowType.DIALOG
    else:
        return WindowType.NORMAL


class Window(WindowBase):
    '''Abstracted window container for Windows'''

    def __init__(self, hwnd):
        self._hwnd = hwnd

    def get_name(self):
        return win32gui.GetWindowText(self._hwnd)

    def set_forcus(self):
        try:
            # According to https://stackoverflow.com/questions/14295337/\
            #                      win32gui-setactivewindow-error-the-\
            #                      specified-procedure-could-not-be-found
            _shell.SendKeys('%')
            ret = win32gui.SetForegroundWindow(self._hwnd)
            if ret == 0:
                raise
        except Exception:
            logger.warn('Failed to set focus')

    def set_geom(self, x, y, w, h):
        flags = win32con.SWP_NOACTIVATE | win32con.SWP_NOZORDER
        win32gui.SetWindowPos(self._hwnd, 0, x, y, w, h, flags)

    def close(self):
        win32gui.SendMessage(self._hwnd, win32con.WM_CLOSE, 0, 0)

    def set_border(self, width=2, rgb=(255, 0, 0)):
        # TODO: Set border width
        col = win32api.RGB(*rgb)
        win32api.SetSysColors((win32con.COLOR_ACTIVEBORDER,), (col,))

    def set_frame_visib(self, visible):
        style = win32gui.GetWindowLong(self._hwnd, win32con.GWL_STYLE)
        if visible:
            style |= win32con.WS_CAPTION
        else:
            style &= ~win32con.WS_CAPTION
        win32gui.SetWindowLong(self._hwnd, win32con.GWL_STYLE, style)
        win32gui.SetWindowPos(self._hwnd, 0, 0, 0, 0, 0,
                              win32con.SWP_FRAMECHANGED | win32con.SWP_NOMOVE |
                              win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)

    def get_type(self):
        return _get_win_type(self._hwnd)


class WindowController(WindowControllerBase):
    '''Low level interface of controlling windows for Windows'''

    def get_window_list(self, types=[WindowType.NORMAL, WindowType.DIALOG]):
        # TODO: types
        wins = list()

        def enum_handler(hwnd, l_param):
            if _get_win_type(hwnd) in types:
                wins.append(Window(hwnd))

        win32gui.EnumWindows(enum_handler, None)
        return wins

    def get_forcused_window(self):
        hwnd = win32gui.GetForegroundWindow()
        return Window(hwnd)
