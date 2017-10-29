# -*- coding: utf-8 -*-

import atexit

import win32gui
import win32con

# logging
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())


class PseudoWorkspace(object):

    def __init__(self, wins=None):
        self._ws_dict = dict()
        self._ws_idx = 0
        self._n_ws = 1
        if wins is not None:
            self.update_wins(wins)

        # Show all windows at exit
        atexit.register(self._show_all_wins)

    def update_win_raw(self, hwnd):
        # Register new window
        if hwnd not in self._ws_dict:
            self.set_win_ws(hwnd, self._ws_idx)
            self._update_win_showing_status(hwnd)  # Update one showing status

    def update_win(self, win):
        self.update_win_raw(win._hwnd)

    def update_wins(self, wins):
        # Register new windows
        for win in wins:
            self.update_win(win)

        # Remove closed windows
        valid_hwnds = list()
        for win in wins:
            valid_hwnds.append(win._hwnd)
        for hwnd in self._ws_dict.keys():
            if hwnd not in valid_hwnds:
                del self._ws_dict[hwnd]

    def get_win_ws(self, hwnd):
        if hwnd in self._ws_dict:
            return self._ws_dict[hwnd]
        else:
            logger.error("PseudoWorkspace dose not control (hwnd: %d)", hwnd)
            return 0

    def set_win_ws(self, hwnd, i):
        if 0 <= i < self._n_ws:
            self._ws_dict[hwnd] = i
            # Update one showing status
            self._update_win_showing_status(hwnd)

    def get_n_workspace(self):
        return self._n_ws

    def set_n_workspace(self, n):
        self._n_ws = n
        # Move to valid workspaces
        for hwnd, i in self._ws_dict.items():
            if self._n_ws <= i:
                self._ws_dict[hwnd] = n - 1
                # Update one showing status
                self._update_win_showing_status(hwnd)

    def get_curr_workspace(self):
        return self._ws_idx

    def set_curr_workspace(self, i):
        if 0 <= i < self._n_ws:
            self._ws_idx = i
            # Update all showing status
            self._update_showing_status()

    def _update_win_showing_status(self, hwnd):
        if self._ws_idx == self.get_win_ws(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_SHOWNA)
        else:
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

    def _update_showing_status(self):
        for hwnd in self._ws_dict.keys():
            self._update_win_showing_status(hwnd)

    def _show_all_wins(self):
        for hwnd in self._ws_dict.keys():
            win32gui.ShowWindow(hwnd, win32con.SW_SHOWNA)
