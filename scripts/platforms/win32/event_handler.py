# -*- coding: utf-8 -*-

import threading

from ...constants import EventType
from ..base import EventHandlerBase

# logging
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())


class EventHandler(EventHandlerBase):
    '''Event handler for Windows'''

    def grab_key_event(self, event_queue, keys):
        NotImplemented

    def grab_win_event(self, event_queue):
        NotImplemented
