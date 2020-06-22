#!/usr/bin/env python
# -*- coding: utf-8 -*-
from webchecker.scheduler import Site

class TestSite:
    def test_dummy(self):
        site = Site(1, 'google', 'google.com', 60, '')
        assert(str(site) == 'google: google.com')

