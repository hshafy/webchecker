#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Testing Trasnport
"""
from datetime import datetime

from webchecker.transport import Message


class TestMessage:
    def _create_message(self):
        message = Message(site_id=1,
                          code=200,
                          response_time=120,
                          created=datetime(year=2020,
                                           month=2,
                                           day=22,
                                           hour=4,
                                           minute=15,
                                           second=30))
        return message

    def test_serlialize_message(self):
        message = self._create_message()
        serialized = str(message)
        expected = '{"site_id": 1, "status_code": 200, "response_time": 120, "created": "2020-02-22T04:15:30"}'
        assert serialized == expected

    def test_asbytes(self):
        message = self._create_message()
        assert isinstance(message.asbytes(), bytes)
