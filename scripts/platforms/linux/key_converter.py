# -*- coding: utf-8 -*-

from Xlib import XK

from ...constants import SpecialKeyNames

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
    0xffbe: SpecialKeyNames.F1,
    0xffbf: SpecialKeyNames.F2,
    0xffc0: SpecialKeyNames.F3,
    0xffc1: SpecialKeyNames.F4,
    0xffc2: SpecialKeyNames.F5,
    0xffc3: SpecialKeyNames.F6,
    0xffc4: SpecialKeyNames.F7,
    0xffc5: SpecialKeyNames.F8,
    0xffc6: SpecialKeyNames.F9,
    0xffc7: SpecialKeyNames.F10,
    0xffc8: SpecialKeyNames.F11,
    0xffc9: SpecialKeyNames.F12,
    0xffca: SpecialKeyNames.F13,
    0xffcb: SpecialKeyNames.F14,
    0xffcc: SpecialKeyNames.F15,
    0xffcd: SpecialKeyNames.F16,
    0xffce: SpecialKeyNames.F17,
    0xffcf: SpecialKeyNames.F18,
    0xffd0: SpecialKeyNames.F19,
    0xffd1: SpecialKeyNames.F20,
    0xffd2: SpecialKeyNames.F21,
    0xffd3: SpecialKeyNames.F22,
    0xffd4: SpecialKeyNames.F23,
    0xffd5: SpecialKeyNames.F24,
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
