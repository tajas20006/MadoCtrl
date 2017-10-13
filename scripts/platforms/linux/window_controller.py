# -*- coding: utf-8 -*-

from Xlib import Xatom, X

from ...constants import WindowType
from ..base import WindowBase, WindowControllerBase
from .common import _ewmh

# logging
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())

# Xlib entry point
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


def _get_win_type(xwin):
    prop = _display.intern_atom('_NET_WM_WINDOW_TYPE')
    data = xwin.get_full_property(prop, Xatom.ATOM)
    win_type = data.value[0]
    if win_type in _win_normal_types:
        return WindowType.NORMAL
    elif win_type in _win_dialog_types:
        return WindowType.DIALOG
    elif win_type in _win_dock_types:
        return WindowType.DOCK
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

    def __init__(self, xwin):
        self._xwin = xwin  # Xlib.display.Window

    def get_name(self):
        return self._xwin.get_wm_name()

    def set_forcus(self):
        _ewmh.setActiveWindow(self._xwin)
        _flush()

    def set_geom(self, x, y, w, h):
        _ewmh.setMoveResizeWindow(self._xwin, 0, x, y, w, h)
        _flush()

    def close(self):
        _ewmh.setCloseWindow(self._xwin)
        _flush()

    def set_border(self, width=2, rgb=(255, 0, 0)):
        color_code = '#%02x%02x%02x' % rgb
        col = _colormap.alloc_named_color(color_code).pixel
        self._xwin.configure(border_width=width)
        self._xwin.change_attributes(None, border_pixel=col)
        _flush()

    def set_frame_visib(self, visible):
        prop = _display.intern_atom('_MOTIF_WM_HINTS')
        if visible:
            data = [2, 0, 1, 0, 0]  # [HINTS_DECORATIONS, 0, ON, 0, 0]
        else:
            data = [2, 0, 0, 0, 0]  # [HINTS_DECORATIONS, 0, OFF, 0, 0]
        self._xwin.change_property(prop, prop, 32, data, X.PropModeReplace)
        _flush()

    def get_type(self):
        return _get_win_type(self._xwin)


class WindowController(WindowControllerBase):
    '''Low level interface of controlling windows for X Window System'''

    def get_window_list(self, types=[WindowType.NORMAL, WindowType.DIALOG]):
        xwins = _ewmh.getClientListStacking()
        return [Window(xwin) for xwin in xwins
                if _get_win_type(xwin) in types]

    def get_forcused_window(self):
        xwin = _ewmh.getActiveWindow()
        return Window(xwin)
