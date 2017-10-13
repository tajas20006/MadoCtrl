# -*- coding: utf-8 -*-

from ..constants import WindowType


class WindowBase(object):
    '''Abstracted window container for each platform'''

    def get_name(self):
        NotImplemented

    def set_forcus(self):
        NotImplemented

    def set_geom(self, x, y, w, h):
        NotImplemented

    def close(self):
        NotImplemented

    def set_border(self, width=2, rgb=(255, 0, 0)):
        NotImplemented

    def set_frame_visib(self, visible):
        NotImplemented

    def get_type(self):
        NotImplemented


class WindowControllerBase(object):
    '''Low level interface of controlling windows for each platform'''

    def get_window_list(self, types=[WindowType.NORMAL, WindowType.DIALOG]):
        NotImplemented

    def get_forcused_window(self):
        NotImplemented


class EventHandlerBase(object):
    '''Event handler for each platform'''

    def __init__(self, modif_key, event_queue):
        NotImplemented

    def stop(self):
        NotImplemented


class SpecialKeyNames(object):
    '''Key names to avoid ambiguity for each platform'''
    SPACE = 'Space'
    BACKSPACE = 'Backspace'
    TAB = 'Tab'
    ENTER = 'Enter'
    ESC = 'Esc'
    DELETE = 'Del'
    SHIFT = 'Shift'
    CTRL = 'Ctrl'
    ALT = 'Alt'
    WIN = 'Win'
