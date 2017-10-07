# -*- coding: utf-8 -*-

from Xlib import Xatom, X
from ewmh import EWMH

from ..common import WindowType, WindowBase, WindowControllerBase

# logging
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())


# Xlib entry point
_ewmh = EWMH()
_display = _ewmh.display
_colormap = _display.screen().default_colormap


# Raw window types of Xlib
_win_normal_types = [_display.intern_atom('_NET_WM_WINDOW_TYPE_NORMAL'),
                     _display.intern_atom('_NET_WM_WINDOW_TYPE_DND')]
_win_dialog_types = [_display.intern_atom('_NET_WM_WINDOW_TYPE_TOOLBAR'),
                     _display.intern_atom('_NET_WM_WINDOW_TYPE_MENU'),
                     _display.intern_atom('_NET_WM_WINDOW_TYPE_UTILITY'),
                     _display.intern_atom('_NET_WM_WINDOW_TYPE_SPLASH'),
                     _display.intern_atom('_NET_WM_WINDOW_TYPE_DIALOG'),
                     _display.intern_atom('_NET_WM_WINDOW_TYPE_DROPDOWN_MENU'),
                     _display.intern_atom('_NET_WM_WINDOW_TYPE_POPUP_MENU'),
                     _display.intern_atom('_NET_WM_WINDOW_TYPE_NOTIFICATION'),
                     _display.intern_atom('_NET_WM_WINDOW_TYPE_COMBO')]
_win_dock_types = [_display.intern_atom('_NET_WM_WINDOW_TYPE_DOCK')]
_win_other_types = [_display.intern_atom('_NET_WM_WINDOW_TYPE_DESKTOP')]


def _get_win_type(x_win):
    prop = _display.intern_atom('_NET_WM_WINDOW_TYPE')
    data = x_win.get_full_property(prop, Xatom.ATOM)
    win_type = data.value[0]
    if win_type in _win_normal_types:
        return WindowType.NORMAL
    elif win_type in _win_dialog_types:
        return WindowType.DIALOG
    elif win_type in _win_dock_types:
        return WindowType.DOC
    elif win_type in _win_other_types:
        return WindowType.OTHER
    else:
        logger.warn('Invalid window type is detected: {}', win_type)
        return -1


def _flush():
    '''Flush window events forcibly'''
    _display.flush()


class Window(WindowBase):
    '''Abstracted window container for X Window System'''

    def __init__(self, x_win):
        self._x_win = x_win  # Xlib.display.Window

    def get_name(self):
        return self._x_win.get_wm_name()

    def set_forcus(self):
        _ewmh.setActiveWindow(self._x_win)
        _flush()

    def set_geom(self, x, y, w, h):
        _ewmh.setMoveResizeWindow(self._x_win, 0, x, y, w, h)
        _flush()

    def close(self):
        _ewmh.setCloseWindow(self._x_win)
        _flush()

    def set_border(self, width=2, color_code="#ff0000"):
        color = _colormap.alloc_named_color(color_code).pixel
        self._x_win.configure(border_width=width)
        self._x_win.change_attributes(None, border_pixel=color)
        _flush()

    def set_frame_visib(self, visible):
        prop = _display.intern_atom('_MOTIF_WM_HINTS')
        if visible:
            data = [2, 0, 1, 0, 0]  # [HINTS_DECORATIONS, 0, ON, 0, 0]
        else:
            data = [2, 0, 0, 0, 0]  # [HINTS_DECORATIONS, 0, OFF, 0, 0]
        self._x_win.change_property(prop, prop, 32, data, X.PropModeReplace)
        _flush()

    def get_type(self):
        return _get_win_type(self._x_win)


class WindowController(WindowControllerBase):
    '''Low level interface of controlling windows for X Window System'''

    def get_window_list(self, types=[WindowType.NORMAL, WindowType.DIALOG]):
        x_wins = _ewmh.getClientListStacking()  # [Xlib.display.Window]
        return [Window(x_win) for x_win in x_wins
                if _get_win_type(x_win) in types]

    def get_forcused_window(self):
        x_win = _ewmh.getActiveWindow()  # Xlib.display.Window
        return Window(x_win)
