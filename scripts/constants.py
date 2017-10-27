# -*- coding: utf-8 -*-


class WindowType(object):
    NORMAL = 1
    DIALOG = 2
    DOCK = 3
    OTHER = 4


class EventType(object):
    KEY_PRESS = 1
    WIN_CREATE = 2
    WIN_DESTROY = 3


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
