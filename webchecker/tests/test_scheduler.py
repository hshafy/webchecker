#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from webchecker.scheduler import Site

class TestSite:
    def test_dummy(self):
        site = Site(1, 'google', 'https://google.com', 60, '', True)
        assert(str(site) == 'google: https://google.com')

    def test_valid_url(self):
        with pytest.raises(ValueError):
            Site(1, 'google', 'ht.googlecom', 60, '', True)
