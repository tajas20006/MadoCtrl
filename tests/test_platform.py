#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import time
import random
import queue

from scripts import log_initializer
from scripts import platforms
from scripts.constants import WindowType, EventType

# logging (root)
from logging import getLogger, DEBUG
log_initializer.set_root_level(DEBUG)
logger = getLogger(__name__)


parser = argparse.ArgumentParser(description='Platform test')
parser.add_argument('--mode', '-m', required=True,
                    choices=['print_wins', 'print_focused', 'focus_loop',
                             'geom_all', 'close_focused', 'frame_toggle',
                             'border_all', 'print_area', 'move_ws',
                             'create_ws', 'print_events'])
args = parser.parse_args()


if __name__ == '__main__':
    mode = args.mode
    logger.info('Start window controller test (mode: %s)', mode)

    # Import all modules for each platform
    platforms.import_modules()

    # Window Controller
    WinController = platforms.window_controller.WindowController

    # Event Handler
    modif = 'Win'
    event_queue = queue.Queue()
    event_handler = platforms.event_handler.EventHandler(event_queue, modif)

    if mode == 'print_wins':
        logger.info('Print all window names and types and working area size')
        wins = WinController.get_window_list([WindowType.NORMAL,
                                              WindowType.DIALOG,
                                              WindowType.DOCK])
        for win in wins:
            logger.debug('Window: "%s"', win.get_name())
            logger.debug('  > Type: %s', win.get_type())

    elif mode == 'print_focused':
        logger.info('Print focused window names and types')
        win = WinController.get_focused_window()
        logger.debug('Window: "%s"', win.get_name())
        logger.debug('  > Type: %s', win.get_type())

    elif mode == 'focus_loop':
        logger.info('Change focus over all windows')
        wins = WinController.get_window_list()
        for win in wins:
            logger.debug(' window name: %s', win.get_name())
            win.set_focus()
            time.sleep(1)

    elif mode == 'geom_all':
        logger.info('Geometries of all windows will be changed randomly')
        wins = WinController.get_window_list()
        for win in wins:
            logger.debug(' window name: %s', win.get_name())
            win.set_geom(random.randint(0, 500), random.randint(0, 500),
                         random.randint(300, 700), random.randint(300, 700))
            time.sleep(0.5)

    elif mode == 'close_focused':
        logger.info('The focused window will be closed after 3 seconds')
        time.sleep(3)
        win = WinController.get_focused_window()
        win.close()

    elif mode == 'frame_toggle':
        logger.info('Frame of the focused window will be hidden and appeared')
        win = WinController.get_focused_window()
        win.set_frame_visib(False)
        time.sleep(1)
        win.set_frame_visib(True)

    elif mode == 'border_all':
        logger.info('Borders of all windows will be changed')
        wins = WinController.get_window_list()
        for win in wins:
            win.set_border()
            time.sleep(1)

    elif mode == 'print_area':
        logger.info('Print working area size')
        working_area = WinController.get_working_area()
        logger.debug('Working area: %s', str(working_area))

    elif mode == 'move_ws':
        logger.info('Move focused window to the next and move back')
        win = WinController.get_focused_window()
        org_ws = win.get_workspace()
        win.set_workspace(org_ws + 1)
        WinController.set_curr_workspace(org_ws + 1)
        time.sleep(1)
        logger.debug('Move back')
        win.set_workspace(org_ws)
        WinController.set_curr_workspace(org_ws)

    elif mode == 'create_ws':
        n_ws = WinController.get_n_workspace()
        org_ws = WinController.get_curr_workspace()
        logger.debug('Create extra workspace (%d -> %d)', n_ws, n_ws + 1)
        WinController.set_n_workspace(n_ws + 1)
        WinController.set_curr_workspace(n_ws)
        logger.debug('n_ws: (%d)', WinController.get_n_workspace())
        time.sleep(1)
        WinController.set_curr_workspace(org_ws)
        WinController.set_n_workspace(n_ws)

    elif mode == 'print_events':
        logger.info('Print all events')
        while True:
            event_type, data = event_queue.get()
            if event_type == EventType.KEY_PRESS:
                logger.debug("keypress: %s", str(data))
            elif event_type == EventType.WIN_CREATE:
                logger.debug("Window is created")
            elif event_type == EventType.WIN_DESTROY:
                logger.debug("Window is destroyed")
