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

        n_ws = WinController.get_n_workspace()

        # Window stack for static order
        wins = WinController.get_window_list()
        self._win_stack = WindowStack(n_ws, wins)

        # Layout
        self._layouts = WorkspaceLayouts(n_ws, layouts)

    def start(self):
        # Event loop
        while True:
            event_type, event_data = self._event_queue.get()
            if event_type in [EventType.WIN_CREATE, EventType.WIN_DESTROY]:
                # A window is changed
                ws_idx = WinController.get_curr_workspace()
                self.arrange(ws_idx)
            elif event_type == EventType.KEY_PRESS:
                # A key is pressed
                self.deal_key_event(event_data)

    def arrange(self, ws_idx):
        # Update window stack
        wins_all = WinController.get_window_list()
        self._win_stack.update(wins_all)
        # Arrange windows
        wins = self._win_stack.get_wins(ws_idx)
        area = WinController.get_working_area()
        self._layouts.arrange(ws_idx, wins, area)

    def change_n_workspaces(self, n):
        self._win_stack.change_n_workspaces(n)
        self._layouts.change_n_workspaces(n)
        WinController.set_n_workspace(n)

    def deal_key_event(self, key):
        # TODO: Make configurable
        if key == 'a':
            # Arrange
            ws_idx = WinController.get_curr_workspace()
            self.arrange(ws_idx)

        elif key == SpecialKeyNames.SPACE:
            # Change layout mode
            ws_idx = WinController.get_curr_workspace()
            self._layouts.next_layout(ws_idx)

        elif key == 'j':
            ws_idx = WinController.get_curr_workspace()
            focused_win = WinController.get_focused_window()
            self._win_stack.change_focus(ws_idx, focused_win, 1)

        elif key == 'k':
            ws_idx = WinController.get_curr_workspace()
            focused_win = WinController.get_focused_window()
            self._win_stack.change_focus(ws_idx, focused_win, -1)

        elif key == 'l':
            ws_idx = WinController.get_curr_workspace()
            n_ws = WinController.get_n_workspace()
            WinController.set_curr_workspace((ws_idx + 1) % n_ws)

        elif key == 'h':
            ws_idx = WinController.get_curr_workspace()
            n_ws = WinController.get_n_workspace()
            WinController.set_curr_workspace((ws_idx - 1) % n_ws)

#         elif key == '9':
#
#         elif key == '0':

        elif key == 'i':
            # Toggle ignoring mode of dialogs
            ws_idx = WinController.get_curr_workspace()
            self._layouts.toggle_dialog_arrange(ws_idx)
            self.arrange(ws_idx)

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
