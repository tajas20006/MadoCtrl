# -*- coding: utf-8 -*-

# logging
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())


class WindowStack(object):
    def __init__(self, n_ws, wins):
        self._win_stacks = list()  # [workspace, window]
        # First Call
        self.change_n_workspaces(n_ws)
        self.update(wins)

    def change_n_workspaces(self, n):
        logger.debug('Change the number of workspaces (%d)', n)
        # Allocate for lacking workspaces
        n_lack = n - len(self._win_stacks)
        for i in range(n_lack):
            self._win_stacks.append(list())

    def update_new_window(self, new_win, default_ws):
        # Register new window
        logger.debug('Register a new window')
        try:
            ws_idx = new_win.get_workspace()
        except Exception:
            logger.debug('Failed to get workspace, so use default one')
            ws_idx = default_ws
        self._win_stacks[ws_idx].append(new_win)

    def update_old_window(self, old_win):
        for ws_idx, wins in enumerate(self._win_stacks):
            try:
                old_win_idx = wins.index(old_win)
                # Remove old window
                logger.debug('Remove an old window')
                del wins[old_win_idx]
                break
            except ValueError:
                continue

    def update(self, curr_wins):
        logger.debug('Update window stacks')
        for ws_idx, wins in enumerate(self._win_stacks):
            for w_idx, win in enumerate(wins):
                try:
                    # Check a previous window still exists
                    w_idx_new = curr_wins.index(win)
                except ValueError:
                    # Remove old window
                    logger.debug('Remove an old window')
                    del self._win_stacks[ws_idx][w_idx]
                    continue

                ws_idx_new = curr_wins[w_idx_new].get_workspace()
                if ws_idx != ws_idx_new:
                    # Workspace is changed
                    logger.debug('Moved between workspaces')
                    del self._win_stacks[ws_idx][w_idx]
                    continue

                # Except non-new windows
                del curr_wins[w_idx_new]

        # Register new windows
        for new_win in curr_wins:
            logger.debug('Register a new window')
            ws_idx = new_win.get_workspace()
            self._win_stacks[ws_idx].append(new_win)

    def get_wins(self, ws_idx):
        return self._win_stacks[ws_idx]

    def change_focus(self, ws_idx, focused_win, step):
        logger.debug('Change focus')
        win_stack = self._win_stacks[ws_idx]
        try:
            # Check there is a valid focused window
            w_idx = win_stack.index(focused_win)
        except ValueError:
            # Focus the master window
            if len(win_stack) >= 1:
                win_stack[0].set_focus()
            return
        # Do focus
        win_stack[(w_idx + step) % len(win_stack)].set_focus()
