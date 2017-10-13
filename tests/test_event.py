#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import time
import queue

from scripts import log_initializer
from scripts import platforms
from scripts.constants import EventType

# logging (root)
from logging import getLogger, DEBUG
log_initializer.set_root_level(DEBUG)
logger = getLogger(__name__)


parser = argparse.ArgumentParser(description='Event handler test')
parser.add_argument('--mode', '-m', required=True, choices=['print_all'])
args = parser.parse_args()


if __name__ == '__main__':
    mode = args.mode
    logger.info('Start event handler test (mode: %s)', mode)

    # Import all modules for each platform
    platforms.import_modules()

    # Create a handler instance
    modif = 'Win'
    event_queue = queue.Queue()
    event_handler = platforms.event_handler.EventHandler(event_queue, modif)

    if mode == 'print_all':
        logger.info('Print all events')
        while True:
            event_type, data = event_queue.get()
            if event_type == EventType.KEY_PRESS:
                logger.debug("keypress: %s", str(data))
            elif event_type == EventType.WIN_CREATE:
                logger.debug("Window is created")
            elif event_type == EventType.WIN_DESTROY:
                logger.debug("Window is destroyed")
