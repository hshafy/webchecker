#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.config

logging.config.fileConfig('logging.conf')

logger = logging.getLogger('webchecker')
