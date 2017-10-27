# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

from ..constants import WindowType


class WindowBase(metaclass=ABCMeta):
    '''Abstracted window container for each platform'''

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def set_focus(self):
        pass

    @abstractmethod
    def set_geom(self, x, y, w, h):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def get_workspace(self):
        pass

    @abstractmethod
    def set_workspace(self, i):
        pass

    @abstractmethod
    def set_border(self, width=2, rgb=(255, 0, 0)):
        pass

    @abstractmethod
    def set_frame_visib(self, visible):
        pass


class WindowControllerBase(metaclass=ABCMeta):
    '''Low level interface of controlling windows for each platform'''

    @staticmethod
    @abstractmethod
    def get_window_list(self, types=[WindowType.NORMAL, WindowType.DIALOG]):
        pass

    @staticmethod
    @abstractmethod
    def get_focused_window(self):
        pass

    @staticmethod
    @abstractmethod
    def get_working_area(self):
        pass

    @staticmethod
    @abstractmethod
    def get_n_workspace(self):
        pass

    @staticmethod
    @abstractmethod
    def set_n_workspace(self, n):
        pass

    @staticmethod
    @abstractmethod
    def get_curr_workspace(self):
        pass

    @staticmethod
    @abstractmethod
    def set_curr_workspace(self, i):
        pass


class EventHandlerBase(metaclass=ABCMeta):
    '''Event handler for each platform'''

    @abstractmethod
    def __init__(self, event_queue, modif_key):
        pass
