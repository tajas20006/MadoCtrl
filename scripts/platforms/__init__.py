# -*- coding: utf-8 -*-
import sys
import importlib

module_names = ['window_controller', 'key_listener']


def import_modules(platform_name=None):
    ''' Import modules for each platform
         @param platform_name: Name of a module corresponding to the directory.
    '''

    if platform_name is None:
        platform_name = sys.platform

    for module_name in module_names:
        import_path = '{}.{}.{}'.format(__name__, platform_name, module_name)
        globals()[module_name] = importlib.import_module(import_path)
