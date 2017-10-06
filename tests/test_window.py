#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import time

from scripts import log_initializer
from scripts import platforms

# logging (root)
from logging import getLogger, DEBUG
log_initializer.set_root_level(DEBUG)
logger = getLogger(__name__)


parser = argparse.ArgumentParser(description='Window controller test')
parser.add_argument('--mode', '-m', required=True,
                    choices=['focus_loop', 'geom_all', 'close_focused', 'frame_toggle', 'border_all'])
args = parser.parse_args()


if __name__ == '__main__':
    mode = args.mode
    logger.info('Start window controller test (mode: %s)', mode)

    platforms.import_modules()

    w_controller = platforms.window_controller.WindowController()

    if mode == 'focus_loop':
        wins = w_controller.get_window_list()
        for win in wins:
            print(win.get_name())
            win.set_forcus()
            time.sleep(1)

    elif mode == 'geom_all':
        wins = w_controller.get_window_list()
        for win in wins:
            print(win.get_name())
            win.set_geom(100, 100, 500, 500)
            time.sleep(0.5)

    elif mode == 'close_focused':
        time.sleep(1)
        win = w_controller.get_forcused_window()
        print(win.get_name())
        win.close()

    elif mode == 'frame_toggle':
        win = w_controller.get_forcused_window()
        print(win.get_name())
        win.set_frame_visib(False)
        time.sleep(1)
        win.set_frame_visib(True)

    elif mode == 'border_all':
        wins = w_controller.get_window_list()
        for win in wins:
            print(win.get_name())
            win.set_border()
            time.sleep(0.01)
