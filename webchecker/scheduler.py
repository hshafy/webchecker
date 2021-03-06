#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scheduler module
"""
import time

import validators

from webchecker.checker import worker
from webchecker.settings import SCHEDULE


class Site(object):
    """
    Site Class
    """
    def __init__(self, site_id, name, url, period, regex_check, pass_code=200):
        if not validators.url(url):
            raise ValueError

        self.site_id = site_id
        self.name = name
        self.url = url
        self.period = period
        self.regex_check = regex_check
        self.pass_code = pass_code

    def __repr__(self):
        return f'{self.name}: {self.url}'


def _fetch_schedule():
    sites = []
    for sch in SCHEDULE:
        sites.append(Site(**sch))
    return sites


def start_scheduler(site):
    """
    System entry point, manages the schedule, fetch site urls and
    enqueue them periodically

    TODO:
    1- Owns the schedule data structure
    2- checks it periodically to find the next one to process
    3- fire the checker.check_site [maybe in a different thread/process]
        or chcker.check_site can be a worker that consumes scheduler tasks
    """
    while True:
        worker.start(site)
        time.sleep(5)


def start():
    sites = _fetch_schedule()
    start_scheduler(sites[1])
