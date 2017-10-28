# -*- coding: utf-8 -*-

from ewmh import EWMH
from Xlib import Xatom
from Xlib.error import BadWindow

from ...constants import WindowType

# Common entry point
_ewmh = EWMH()
_display = _ewmh.display


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


def get_win_type(xwin):
    prop = _display.intern_atom('_NET_WM_WINDOW_TYPE')
    try:
        data = xwin.get_full_property(prop, Xatom.ATOM)
    except BadWindow:
        return WindowType.OTHER
    if data is None:
        return WindowType.OTHER

    for win_type in data.value:
        if win_type in _win_normal_types:
            return WindowType.NORMAL
        elif win_type in _win_dialog_types:
            return WindowType.DIALOG
        elif win_type in _win_dock_types:
            return WindowType.DOCK
        elif win_type in _win_other_types:
            return WindowType.OTHER
    # Unknown type
    return WindowType.OTHER
