# -*- coding: utf-8 -*-

# TODO: Replace pywin32 with ctypes.windll

import win32api
import win32con
import win32com.client
import win32ui
import win32gui

from ...constants import WindowType
from ..base import WindowBase, WindowControllerBase
from .common import _pseudo_ws, get_win_type

# logging
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())

# Win32API entry point
_shell = win32com.client.Dispatch("WScript.Shell")


class Window(WindowBase):
    '''Abstracted window container for Windows'''

    def __init__(self, hwnd):
        self._hwnd = hwnd

    def get_name(self):
        return win32gui.GetWindowText(self._hwnd)

    def get_type(self):
        return get_win_type(self._hwnd)

    def set_focus(self):
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

    def get_workspace(self):
        return _pseudo_ws.get_win_ws(self._hwnd)

    def set_workspace(self, i):
        _pseudo_ws.set_win_ws(self._hwnd, i)

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


class WindowController(WindowControllerBase):
    '''Low level interface of controlling windows for Windows'''

    @classmethod
    def get_window_list(cls, types=[WindowType.NORMAL, WindowType.DIALOG]):
        wins = list()

        def enum_handler(hwnd, l_param):
            if get_win_type(hwnd) in types:
                win = Window(hwnd)
                wins.append(win)
        win32gui.EnumWindows(enum_handler, None)

        return wins

    @classmethod
    def get_focused_window(cls):
        hwnd = win32gui.GetForegroundWindow()
        return Window(hwnd)

    @classmethod
    def get_working_area(cls):
        # TODO: Consider multi display
        monitors = win32api.EnumDisplayMonitors(None, None)
        for i, monitor in enumerate(monitors):
            (h_mon, _, (_, _, _, _)) = monitor
            mon = win32api.GetMonitorInfo(h_mon)
            if i == 0:
                left, top, right, bottom = mon['Work']
            else:
                left = min(mon['Work'][0], left)
                top = min(mon['Work'][1], top)
                right = max(mon['Work'][2], right)
                bottom = max(mon['Work'][3], bottom)
        return [left, top, right, bottom]

    @classmethod
    def get_n_workspace(cls):
        return _pseudo_ws.get_n_workspace()

    @classmethod
    def set_n_workspace(cls, n):
        _pseudo_ws.set_n_workspace(n)

    @classmethod
    def get_curr_workspace(cls):
        return _pseudo_ws.get_curr_workspace()

    @classmethod
    def set_curr_workspace(cls, i):
        _pseudo_ws.set_curr_workspace(i)
