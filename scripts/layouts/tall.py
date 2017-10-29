# -*- coding: utf-8 -*-
from .base import LayoutBase


class TallLayout(LayoutBase):
    '''TallLayout
    '''

    def arrange(self, wins, area):
        n_wins = len(wins)
        x, y, w, h = area
        if n_wins == 0:
            return
        elif n_wins == 1:
            wins[0].set_geom(x, y, w, h)
        else:
            w_half = int(w / 2)
            h_one = int(h / (n_wins - 1))
            wins[0].set_geom(x, y, w_half, h)
            curr_y = y
            for i in range(1, n_wins):
                wins[i].set_geom(x + w_half, curr_y, w_half, h_one)
                curr_y += h_one
