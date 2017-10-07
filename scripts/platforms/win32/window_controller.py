# -*- coding: utf-8 -*-

import win32api
import win32con
import win32com.client
import win32ui
import win32gui

from ..common import WindowType, WindowBase, WindowControllerBase

# logging
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())


# Win32API entry point
_shell = win32com.client.Dispatch("WScript.Shell")


# Raw window types of Xlib


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
        pass


class WindowController(WindowControllerBase):
    '''Low level interface of controlling windows for Windows'''

    def get_window_list(self, types=[WindowType.NORMAL, WindowType.DIALOG]):
        # TODO: types
        wins = list()

        def enum_handler(hwnd, l_param):
            if win32gui.IsWindowVisible(hwnd):
                wins.append(Window(hwnd))

        win32gui.EnumWindows(enum_handler, None)
        return wins

    def get_forcused_window(self):
        hwnd = win32gui.GetForegroundWindow()
        return Window(hwnd)
