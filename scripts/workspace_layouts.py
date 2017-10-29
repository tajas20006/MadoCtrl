# -*- coding: utf-8 -*-

from scripts.constants import WindowType

# logging
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())


class LayoutParams(object):
    def __init__(self):
        self.l_idx = 0
        self.ignore_dialogs = True


class WorkspaceLayouts(object):
    def __init__(self, n_ws, layouts):
        self._layout_params = list()
        self._layouts = layouts
        # First Call
        self.change_n_workspaces(n_ws)

    def _get_params(self, ws_idx):
        return self._layout_params[ws_idx]

    def change_n_workspaces(self, n):
        # Allocate for lacking workspaces
        n_lack = n - len(self._layout_params)
        for i in range(n_lack):
            self._layout_params.append(LayoutParams())

    def arrange(self, ws_idx, wins, area):
        params = self._get_params(ws_idx)
        # Extract valid windows
        if params.ignore_dialogs:
            valid_wins = list()
            for win in wins:
                if win.get_type() == WindowType.NORMAL:
                    valid_wins.append(win)
        else:
            valid_wins = wins

        # Arrange
        self._layouts[params.l_idx].arrange(valid_wins, area)

    def next_layout(self, ws_idx):
        params = self._get_params(ws_idx)
        params.l_idx = (params.l_idx + 1) % len(self._layouts)

    def toggle_dialog_arrange(self, ws_idx):
        params = self._get_params(ws_idx)
        params.ignore_dialogs = not params.ignore_dialogs

    def call_layout_method(self, ws_idx, method_name, *args, **kwargs):
        l_idx = self._get_params(ws_idx).l_idx
        # Fetch layout's method
        try:
            method = getattr(self._layouts[l_idx], method_name)
        except AttributeError:
            return
        method(*args, **kwargs)
