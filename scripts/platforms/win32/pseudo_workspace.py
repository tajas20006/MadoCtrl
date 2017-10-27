# -*- coding: utf-8 -*-

import win32gui
import win32con

# logging
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())


class PseudoWorkspace(object):

    def __init__(self):
        self._ws_dict = dict()
        self._ws_idx = 0
        self._n_ws = 1

    def update_win(self, win):
        # Register new window
        if win._hwnd not in self._ws_dict:
            self.set_win_ws(win._hwnd, self._ws_idx)
            self._update_win_showing_status(win._hwnd)

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
        return self._ws_dict[hwnd]

    def set_win_ws(self, hwnd, i):
        self._ws_dict[hwnd] = i
        self._update_win_showing_status(hwnd)  # Update one showing status

    def get_n_workspace(self):
        return self._n_ws

    def set_n_workspace(self, n):
        self._n_ws = n

    def get_curr_workspace(self):
        return self._ws_idx

    def set_curr_workspace(self, i):
        self._ws_idx = i
        self._update_showing_status()  # Update all showing status

    def _update_win_showing_status(self, hwnd):
        flags = win32con.SWP_NOACTIVATE | win32con.SWP_NOMOVE | \
                win32con.SWP_NOSIZE | win32con.SWP_NOZORDER
        if self._ws_idx == self.get_win_ws(hwnd):
            win32gui.SetWindowPos(hwnd, 0, 0, 0, 0, 0,
                                  win32con.SWP_SHOWWINDOW | flags)
        else:
            win32gui.SetWindowPos(hwnd, 0, 0, 0, 0, 0,
                                  win32con.SWP_HIDEWINDOW | flags)

    def _update_showing_status(self):
        for hwnd in self._ws_dict.keys():
            self._update_win_showing_status(hwnd)
