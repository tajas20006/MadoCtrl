#!/usr/bin/python
# -*- coding: utf-8 -*-

import log_initializer
import platforms

# logging (root)
from logging import getLogger, DEBUG
log_initializer.set_root_level(DEBUG)
logger = getLogger(__name__)


if __name__ == '__main__':
    logger.info(platforms.window_controller)
