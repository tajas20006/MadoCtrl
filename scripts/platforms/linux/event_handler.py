# -*- coding: utf-8 -*-

import threading

import Xlib
from Xlib import Xatom, X, XK

from ...constants import EventType
from ..base import EventHandlerBase
from .common import _ewmh
from .key_converter import interpret_keysym, interpret_keyname

# logging
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())

# Xlib entry point
_display = _ewmh.display
_root = _display.screen().root


def _register_key_grab(keysyms):
    '''Register a modifier key to enable event capturing'''
    for keysym in keysyms:
        keycodes_map = _display.keysym_to_keycodes(keysym)
        keycodes = [keycode for keycode, _ in keycodes_map]
        for keycode in keycodes:
            _root.grab_key(keycode, 0, True, X.GrabModeAsync, X.GrabModeAsync)


class EventHandler(EventHandlerBase):
    '''Event handler for X Window System'''

    def __init__(self, event_queue, modif_key):
        logger.debug('Create EventHandler instance (modif: "%s")', modif_key)

        # Enable key-press and window notifications
        event_mask = X.KeyPressMask | X.SubstructureNotifyMask
        _root.change_attributes(event_mask=event_mask)

        # Enable to grab keys with specific modifiers
        modif_keysyms = interpret_keyname(modif_key)
        _register_key_grab(modif_keysyms)

        # Output queues
        self._out_event_queue = event_queue

        # Start event capturing loop
        self._thread = threading.Thread(target=self._event_loop, daemon=True)
        self._thread.start()

    def _event_loop(self):
        logger.debug('Start event loop')

        while True:
            # Get next event
            event = _display.next_event()
            if isinstance(event, Xlib.protocol.event.KeyPress):
                # Convert keycode to key name
                keycode = event.detail
                keysym = _display.keycode_to_keysym(keycode, 0)
                # Interpret keysyms
                key_name = interpret_keysym(keysym)
                # Send press event
                if key_name is not None:
                    self._out_event_queue.put((EventType.KEY_PRESS, key_name))
                else:
                    logger.debug('Unknown key is pressed (keysym: %d}', keysym)

            elif isinstance(event, Xlib.protocol.event.CreateNotify):
                # Send create event
                self._out_event_queue.put((EventType.WIN_CREATE, None))

            elif isinstance(event, Xlib.protocol.event.DestroyNotify):
                # Send destroy event
                self._out_event_queue.put((EventType.WIN_DESTROY, None))

            # Release queued events
            _display.allow_events(Xlib.X.AsyncKeyboard, Xlib.X.CurrentTime)
