# -*- coding: utf-8 -*-

from Xlib import XK

from ..base import SpecialKeyNames

# Created with `X11.keysymdef.h`
KEYSYM_TABLE = {
    0x0020: SpecialKeyNames.SPACE,
    0xff08: SpecialKeyNames.BACKSPACE,
    0xff09: SpecialKeyNames.TAB,
    0xff0d: SpecialKeyNames.ENTER,
    0xff1b: SpecialKeyNames.ESC,
    0xffff: SpecialKeyNames.DELETE,
    0xffe1: SpecialKeyNames.SHIFT,  # left
    0xffe2: SpecialKeyNames.SHIFT,  # right
    0xffe3: SpecialKeyNames.CTRL,  # left
    0xffe4: SpecialKeyNames.CTRL,  # right
    0xffe9: SpecialKeyNames.ALT,  # left
    0xffea: SpecialKeyNames.ALT,  # right
    0xffeb: SpecialKeyNames.WIN,  # left
    0xffec: SpecialKeyNames.WIN,  # right
}

# Invert KEYSYM_TABLE ({name: [keycode1, keycode2, ...]})
KEYSYM_TABLE_INV = {}
for key, value in KEYSYM_TABLE.items():
    if value in KEYSYM_TABLE_INV:
        KEYSYM_TABLE_INV[value].append(key)
    else:
        KEYSYM_TABLE_INV[value] = [key]


def interpret_keysym(keysym):
    '''Convert keysym to keyname'''
    if keysym in KEYSYM_TABLE:
        # Special keys
        return KEYSYM_TABLE[keysym]
    else:
        # Other keys (if not found, `None` will be returned)
        return XK.keysym_to_string(keysym)


def interpret_keyname(keyname):
    '''Convert keyname to list of keysyms'''
    if keyname in KEYSYM_TABLE_INV:
        # Special keys
        return KEYSYM_TABLE_INV[keyname]
    else:
        # Other keys
        keysym = XK.string_to_keysym(keyname)
        return [keysym]
