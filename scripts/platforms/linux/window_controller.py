# -*- coding: utf-8 -*-

# TODO: Replace ewmh with xlib

from Xlib import Xatom, X

from ...constants import WindowType
from ..base import WindowBase, WindowControllerBase
from .common import _ewmh, get_win_type

# logging
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())

# Xlib entry point
_display = _ewmh.display
_colormap = _display.screen().default_colormap


def _flush():
    '''Flush window events forcibly'''
    _display.flush()


class Window(WindowBase):
    '''Abstracted window container for X Window System'''

    def __init__(self, xwin):
        self._xwin = xwin  # Xlib.display.Window

    def get_name(self):
        return _ewmh.getWmName(self._xwin).decode('utf-8')

    def get_type(self):
        return get_win_type(self._xwin)

    def set_focus(self):
        _ewmh.setActiveWindow(self._xwin)
        _flush()

    def set_geom(self, x, y, w, h):
        _ewmh.setMoveResizeWindow(self._xwin, 0, x, y, w, h)
        _flush()

    def close(self):
        _ewmh.setCloseWindow(self._xwin)
        _flush()

    def get_workspace(self):
        return _ewmh.getWmDesktop(self._xwin)

    def set_workspace(self, i):
        _ewmh.setWmDesktop(self._xwin, i)
        _flush()

    def set_border(self, width=2, rgb=(255, 0, 0)):
        # TODO: Dose not work in xfce4
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


class WindowController(WindowControllerBase):
    '''Low level interface of controlling windows for X Window System'''

    @classmethod
    def get_window_list(cls, types=[WindowType.NORMAL, WindowType.DIALOG]):
        xwins = _ewmh.getClientListStacking()
        return [Window(xwin) for xwin in xwins
                if get_win_type(xwin) in types]

    @classmethod
    def get_focused_window(cls):
        xwin = _ewmh.getActiveWindow()
        return Window(xwin)

    @classmethod
    def get_working_area(cls):
        # TODO: Consider multi display
        area = _ewmh.getWorkArea()
        if area is None or len(area) == 0 or len(area) % 4 != 0:
            # Not supported
            logger.critical('Failed to get working area size (Not supported)' +
                            ' (data: %s)', str(area))
            return [0, 0, 0, 0]
        elif len(area) == 4:
            # Single size
            return area
        else:
            # Select current workspace size
            i = cls.get_curr_workspace()
            if len(area) < (i + 1) * 4:
                logger.critical('Unknown format of working area size' +
                                ' (data: %s)', str(area))
                return [0, 0, 0, 0]
            else:
                return area[4 * i: 4 * (i + 1)]

    @classmethod
    def get_n_workspace(cls):
        return _ewmh.getNumberOfDesktops()

    @classmethod
    def set_n_workspace(cls, n):
        '''Set the number of workspaces
            This method cannot work in some window manager such as Unity.
        '''
        _ewmh.setNumberOfDesktops(n)
        _flush()

    @classmethod
    def get_curr_workspace(cls):
        return _ewmh.getCurrentDesktop()

    @classmethod
    def set_curr_workspace(cls, i):
        _ewmh.setCurrentDesktop(i)
        _flush()
