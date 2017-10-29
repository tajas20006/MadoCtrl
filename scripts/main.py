#!/usr/bin/python
# -*- coding: utf-8 -*-

import queue

from scripts import log_initializer
from scripts import layouts
from scripts import platforms
from scripts.constants import EventType, SpecialKeyNames
from scripts.window_stack import WindowStack
from scripts.workspace_layouts import WorkspaceLayouts

# logging (root)
from logging import getLogger, DEBUG
log_initializer.set_root_level(DEBUG)
logger = getLogger(__name__)

# Import all modules for each platform
platforms.import_modules()
WinController = platforms.window_controller.WindowController
EventHandler = platforms.event_handler.EventHandler


class MadoCtrl(object):
    def __init__(self, modif, layouts):
        # Event handler
        self._event_queue = queue.Queue()
        self._event_handler = EventHandler(self._event_queue, modif)

        # Window stack for static order
        n_ws = WinController.get_n_workspace()
        wins = WinController.get_window_list()
        self._win_stack = WindowStack(n_ws, wins)

        # Layout for each workspace
        self._layouts = WorkspaceLayouts(n_ws, layouts)

    def start(self):
        # Event loop
        while True:
            event_type, event_data = self._event_queue.get()
            logger.debug('Get new event (%d, %s)', event_type, str(event_data))
            if event_type == EventType.WIN_CREATE:
                # A window is created
                ws_idx = WinController.get_curr_workspace()
                self._win_stack.update_new_window(event_data, ws_idx)
                self.arrange()
            elif event_type == EventType.WIN_DESTROY:
                # A window is destroyed
                self._win_stack.update_old_window(event_data)
                self.arrange()
            elif event_type == EventType.KEY_PRESS:
                # A key is pressed
                self.deal_key_event(event_data)

    def arrange(self):
#         # Update window stack
#         wins_all = WinController.get_window_list()
#         self._win_stack.update(wins_all)
        # Arrange windows
        ws_idx = WinController.get_curr_workspace()
        wins = self._win_stack.get_wins(ws_idx)
        area = WinController.get_working_area()
        self._layouts.arrange(ws_idx, wins, area)

    def change_n_workspaces(self, n):
        self._win_stack.change_n_workspaces(n)
        self._layouts.change_n_workspaces(n)
        WinController.set_n_workspace(n)

    def change_workspace(self, step):
        ws_idx = WinController.get_curr_workspace()
        n_ws = WinController.get_n_workspace()
        WinController.set_curr_workspace((ws_idx + step) % n_ws)

    def change_focus(self, step):
        ws_idx = WinController.get_curr_workspace()
        focused_win = WinController.get_focused_window()
        self._win_stack.change_focus(ws_idx, focused_win, step)

    def deal_key_event(self, key):
        # TODO: Make configurable
        if key == 'a':
            self.arrange()

        elif key == SpecialKeyNames.SPACE:
            # Change layout mode
            ws_idx = WinController.get_curr_workspace()
            self._layouts.next_layout(ws_idx)

        elif key == 'j':
            self.change_focus(1)

        elif key == 'k':
            self.change_focus(-1)

        elif key == 'l':
            self.change_workspace(1)

        elif key == 'h':
            self.change_workspace(-1)

#         elif key == '9':
#
#         elif key == '0':

        elif key == 'i':
            # Toggle ignoring mode of dialogs
            ws_idx = WinController.get_curr_workspace()
            self._layouts.toggle_dialog_arrange(ws_idx)
            self.arrange()

        else:
            # Change workspace with number key
            try:
                ws_idx = (int(key) - 1) % 10
                WinController.set_curr_workspace(ws_idx)
            except ValueError:
                pass


if __name__ == '__main__':
    modif_key = SpecialKeyNames.WIN
    layout_set = [layouts.TallLayout(), layouts.OriginalLayout()]

    mado = MadoCtrl(modif_key, layout_set)
    mado.change_n_workspaces(13)
    mado.start()
