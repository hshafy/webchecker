#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DB Models
"""
from datetime import datetime

from webchecker.writer import db
from webchecker.logger import logger


class Checks:
    """
    Checks model
    """
    _table_name = 'checks'

    def __init__(self, site_id: int, status_code: int,
                 response_time: int, created: datetime):
        self.rid = None
        self.site_id = site_id
        self.status_code = status_code
        self.response_time = response_time
        self.created = created

    def astuple(self):
        return (self.site_id,
                self.status_code,
                self.response_time,
                self.created)

    def save(self):
        if not self.rid:
            # no record id then perfrom insert operation
            logger.debug('Attempt to insert checks record...')
            db.execute(f'INSERT INTO {self._table_name}'
                       f'(site_id, status_code, response_time, created)'
                       f' VALUES (%s, %s, %s, %s)', self.astuple())
            logger.debug('Checks Record saved.')
