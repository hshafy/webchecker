#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
checker module
"""

from datetime import datetime

import requests

from webchecker.logger import logger
from webchecker.transport import create_trasnport, Message


class CheckResult(object):
    """
    Results Class
    """
    def __init__(self, site, response):
        self.site = site
        self.status_code = response.status_code
        self.elapsed = response.elapsed.total_seconds() * 1000
        self.created = datetime.now()
        self.passed = response.status_code == site.pass_code


def _check_site(site) -> CheckResult:
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
    logger.debug(f'{result.site} - {result.status_code} - {result.elapsed} ms')
    transport = create_trasnport()
    message = Message(site_id=result.site.site_id,
                      status_code=result.status_code,
                      response_time=result.elapsed,
                      created=result.created,
                      passed=result.passed)
    transport.publish(message=message)


def start(site):
    """
    checker entry point
    """
    result = _check_site(site)
    _push_results(result)
