# -*- coding: utf-8 -*-

from ...constants import SpecialKeyNames

KEYCODE_TABLE = {
    0x08: SpecialKeyNames.BACKSPACE,
    0x09: SpecialKeyNames.TAB,
    0x0D: SpecialKeyNames.ENTER,
    0x10: SpecialKeyNames.SHIFT,
    0x11: SpecialKeyNames.CTRL,
    0x12: SpecialKeyNames.ALT,
    0x1B: SpecialKeyNames.ESC,
    0x20: SpecialKeyNames.SPACE,
    0x2E: SpecialKeyNames.DELETE,
    0x30: '0',
    0x31: '1',
    0x32: '2',
    0x33: '3',
    0x34: '4',
    0x35: '5',
    0x36: '6',
    0x37: '7',
    0x38: '8',
    0x39: '9',
    0x41: 'a',
    0x42: 'b',
    0x43: 'c',
    0x44: 'd',
    0x45: 'e',
    0x46: 'f',
    0x47: 'g',
    0x48: 'h',
    0x49: 'i',
    0x4A: 'j',
    0x4B: 'k',
    0x4C: 'l',
    0x4D: 'm',
    0x4E: 'n',
    0x4F: 'o',
    0x50: 'p',
    0x51: 'q',
    0x52: 'r',
    0x53: 's',
    0x54: 't',
    0x55: 'u',
    0x56: 'v',
    0x57: 'w',
    0x58: 'x',
    0x59: 'y',
    0x5A: 'z',
    0x5B: SpecialKeyNames.WIN,  # left
    0x5C: SpecialKeyNames.WIN,  # right
    0x70: SpecialKeyNames.F1,
    0x71: SpecialKeyNames.F2,
    0x72: SpecialKeyNames.F3,
    0x73: SpecialKeyNames.F4,
    0x74: SpecialKeyNames.F5,
    0x75: SpecialKeyNames.F6,
    0x76: SpecialKeyNames.F7,
    0x77: SpecialKeyNames.F8,
    0x78: SpecialKeyNames.F9,
    0x79: SpecialKeyNames.F10,
    0x7A: SpecialKeyNames.F11,
    0x7B: SpecialKeyNames.F12,
    0x7C: SpecialKeyNames.F13,
    0x7D: SpecialKeyNames.F14,
    0x7E: SpecialKeyNames.F15,
    0x7F: SpecialKeyNames.F16,
    0x80: SpecialKeyNames.F17,
    0x81: SpecialKeyNames.F18,
    0x82: SpecialKeyNames.F19,
    0x83: SpecialKeyNames.F20,
    0x84: SpecialKeyNames.F21,
    0x85: SpecialKeyNames.F22,
    0x86: SpecialKeyNames.F23,
    0x87: SpecialKeyNames.F24,
    0xA0: SpecialKeyNames.SHIFT,  # left
    0xA1: SpecialKeyNames.SHIFT,  # right
    0xA2: SpecialKeyNames.CTRL,  # left
    0xA3: SpecialKeyNames.CTRL,  # right
    0xA4: SpecialKeyNames.ALT,  # left
    0xA5: SpecialKeyNames.ALT,  # right
    0xBB: '+',
    0xBC: ',',
    0xBD: '-',
    0xBE: '.',
    0xBF: '/',
    0xC0: '`',
    0xBA: ';',
    0xDB: '[',
    0xDC: '\\',
    0xDD: ']',
    0xDE: "'",
    0xC0: '`',
}

# Invert KEYCODE ({name: [keycode1, keycode2, ...]})
KEYCODE_TABLE_INV = {}
for key, value in KEYCODE_TABLE.items():
    if value in KEYCODE_TABLE_INV:
        KEYCODE_TABLE_INV[value].append(key)
    else:
        KEYCODE_TABLE_INV[value] = [key]


def interpret_keycode(keycode):
    '''Convert keycode to keyname'''
    if keycode in KEYCODE_TABLE:
        return KEYCODE_TABLE[keycode]
    else:
        return None


def interpret_keyname(keyname):
    '''Convert keyname to list of keycodes'''
    if keyname in KEYCODE_TABLE_INV:
        return KEYCODE_TABLE_INV[keyname]
    else:
        return ['invalid']
