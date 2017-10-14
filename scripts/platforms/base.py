# -*- coding: utf-8 -*-

from ..constants import WindowType


class WindowBase(object):
    '''Abstracted window container for each platform'''

    def get_name(self):
        NotImplemented

    def get_type(self):
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


class WindowControllerBase(object):
    '''Low level interface of controlling windows for each platform'''

    def get_window_list(self, types=[WindowType.NORMAL, WindowType.DIALOG]):
        NotImplemented

    def get_forcused_window(self):
        NotImplemented


class EventHandlerBase(object):
    '''Event handler for each platform'''

    def __init__(self, event_queue, modif_key):
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
    F1 = 'F1'
    F2 = 'F2'
    F3 = 'F3'
    F4 = 'F4'
    F5 = 'F5'
    F6 = 'F6'
    F7 = 'F7'
    F8 = 'F8'
    F9 = 'F9'
    F10 = 'F10'
    F11 = 'F11'
    F12 = 'F12'
    F13 = 'F13'
    F14 = 'F14'
    F15 = 'F15'
    F16 = 'F16'
    F17 = 'F17'
    F18 = 'F18'
    F19 = 'F19'
    F20 = 'F20'
    F21 = 'F21'
    F22 = 'F22'
    F23 = 'F23'
    F24 = 'F24'
