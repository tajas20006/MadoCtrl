# -*- coding: utf-8 -*-


class WindowType(object):
    NORMAL = 1
    DIALOG = 2
    DOC = 3
    OTHER = 4


class WindowBase(object):
    '''Abstracted window container for each platform'''

    def get_name(self):
        NotImplemented

    def set_forcus(self):
        NotImplemented

    def set_geom(self, x, y, w, h):
        NotImplemented

    def close(self):
        NotImplemented

    def set_border(self, width=2, color_code="#ff0000"):
        NotImplemented

    def set_frame_visib(self, visible):
        NotImplemented

    def get_type(self):
        NotImplemented


class WindowControllerBase(object):
    '''Low level interface of controlling windows for each platform'''

    def get_window_list(self, types=[WindowType.NORMAL, WindowType.DIALOG]):
        NotImplemented

    def get_forcused_window(self):
        NotImplemented
