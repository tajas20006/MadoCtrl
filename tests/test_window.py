#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import time
import random

from scripts import log_initializer
from scripts import platforms
from scripts.platforms.common import WindowType

# logging (root)
from logging import getLogger, DEBUG
log_initializer.set_root_level(DEBUG)
logger = getLogger(__name__)


parser = argparse.ArgumentParser(description='Window controller test')
parser.add_argument('--mode', '-m', required=True,
                    choices=['print_all', 'print_focused', 'focus_loop',
                             'geom_all', 'close_focused', 'frame_toggle',
                             'border_all'])
args = parser.parse_args()


if __name__ == '__main__':
    mode = args.mode
    logger.info('Start window controller test (mode: %s)', mode)

    platforms.import_modules()

    w_controller = platforms.window_controller.WindowController()

    if mode == 'print_all':
        logger.info('Print all window names and types')
        wins = w_controller.get_window_list([WindowType.NORMAL,
                                             WindowType.DIALOG,
                                             WindowType.DOCK])
        for win in wins:
            logger.debug('Window: "%s"', win.get_name())
            logger.debug('  > Type: %s', win.get_type())

    elif mode == 'print_focused':
        logger.info('Print focused window names and types')
        win = w_controller.get_forcused_window()
        logger.debug('Window: "%s"', win.get_name())
        logger.debug('  > Type: %s', win.get_type())

    elif mode == 'focus_loop':
        logger.info('Change focus over all windows')
        wins = w_controller.get_window_list()
        for win in wins:
            logger.debug(' window name: %s', win.get_name())
            win.set_forcus()
            time.sleep(1)

    elif mode == 'geom_all':
        logger.info('Geometries of all windows will be changed randomly')
        wins = w_controller.get_window_list()
        for win in wins:
            logger.debug(' window name: %s', win.get_name())
            win.set_geom(random.randint(0, 500), random.randint(0, 500),
                         random.randint(300, 700), random.randint(300, 700))
            time.sleep(0.5)

    elif mode == 'close_focused':
        logger.info('The focused window will be closed after 3 seconds')
        time.sleep(3)
        win = w_controller.get_forcused_window()
        win.close()

    elif mode == 'frame_toggle':
        logger.info('Frame of the focused window will be hidden and appeared')
        win = w_controller.get_forcused_window()
        win.set_frame_visib(False)
        time.sleep(1)
        win.set_frame_visib(True)

    elif mode == 'border_all':
        logger.info('Borders of all windows will be changed')
        wins = w_controller.get_window_list()
        for win in wins:
            win.set_border()
            time.sleep(1)
