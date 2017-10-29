# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class LayoutBase(metaclass=ABCMeta):
    '''Layout class which arrange windows in a workspace'''

    @abstractmethod
    def arrange(self, wins, area):
        pass
