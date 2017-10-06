# -*- coding: utf-8 -*-

from Xlib import Xatom, X
from ewmh import EWMH

# logging
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())


# Xlib entry point
_ewmh = EWMH()
_display = _ewmh.display
_colormap = _display.screen().default_colormap

def _flush():
    '''Flush window events forcibly'''
    _display.flush()


class Window(object):
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

    def set_frame_visib(self, visible):
        prop = _display.intern_atom('_NET_WM_WINDOW_TYPE')
        if visible:
            data = [0]
        else:
            data = [_display.intern_atom('_NET_WM_WINDOW_TYPE_DOCK')]
        self._x_win.change_property(prop, Xatom.ATOM, 32, data,
                                    X.PropModeReplace)
        _flush()

    def set_border(self, width=2, color_code="#ff0000"):
        color = _colormap.alloc_named_color(color_code).pixel
        self._x_win.configure(border_width=width)
        self._x_win.change_attributes(None, border_pixel=color)
        _flush()


class WindowController():
    '''Low level interface of controlling windows for X Window System'''

    def get_window_list(self):
        x_wins = _ewmh.getClientListStacking()  # [Xlib.display.Window]
        return [Window(x_win) for x_win in x_wins]

    def get_forcused_window(self):
        x_win = _ewmh.getActiveWindow()  # Xlib.display.Window
        return Window(x_win)
