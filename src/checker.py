#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
checker module
"""

from datetime import datetime

import requests


class CheckResult(object):
    """
    Results Class
    """
    def __init__(self, site, response):
        self.site = site
        self.code = response.status_code
        self.elapsed = response.elapsed.total_seconds() * 1000
        self.created = datetime.now()


def _check_site(site):
    """
    check site and add results to kafka topic

    NOTE:
    1- should perform non blocking request or handle request in a different
    process/thread [for diffrent sites]
    2- checks for same site has to be handled in order
    3- overlapping checks for same site shouldn't be allowed
    """
    response = requests.get(site.url)
    return CheckResult(site, response)


def _push_results(result):
    """
    Pushes results to Kafka (storage - backend)
    """
    print(f'{result.created}: {result.site} - {result.code} - {result.elapsed} ms')


def start(site):
    """
    checker entry point
    """
    result = _check_site(site)
    _push_results(result)
