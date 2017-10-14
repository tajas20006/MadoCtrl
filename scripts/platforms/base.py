# -*- coding: utf-8 -*-

from ..constants import WindowType


class WindowBase(object):
    '''Abstracted window container for each platform'''

    def get_name(self):
        raise NotImplemented

    def get_type(self):
        raise NotImplemented

    def set_focus(self):
        raise NotImplemented

    def set_geom(self, x, y, w, h):
        raise NotImplemented

    def get_workspace(self):
        raise NotImplemented

    def set_workspace(self, i):
        raise NotImplemented

    def close(self):
        raise NotImplemented

    def set_border(self, width=2, rgb=(255, 0, 0)):
        raise NotImplemented

    def set_frame_visib(self, visible):
        raise NotImplemented


class WindowControllerBase(object):
    '''Low level interface of controlling windows for each platform'''

    def get_window_list(self, types=[WindowType.NORMAL, WindowType.DIALOG]):
        raise NotImplemented

    def get_focused_window(self):
        raise NotImplemented

    def get_working_area(self):
        raise NotImplemented

    def get_n_workspace(self):
        raise NotImplemented

    def set_n_workspace(self, n):
        raise NotImplemented

    def get_curr_workspace(self):
        raise NotImplemented

    def set_curr_workspace(self, i):
        raise NotImplemented


class EventHandlerBase(object):
    '''Event handler for each platform'''

    def __init__(self, event_queue, modif_key):
        raise NotImplemented


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
