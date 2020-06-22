#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scheduler module
"""
import time

from webchecker import checker

SCHEDULE = [
    {
        "site_id": 1,
        "name": "google",
        "url": "https://google.com",
        "period": 60,  # seconds
        "regex_check": None,
    },
    {
        "site_id": 2,
        "name": "microsift",
        "url": "https://microsoft.com",
        "period": 30,  # seconds
        "regex_check": None,
    }
]


class Site(object):
    """
    Site Class
    """
    def __init__(self, site_id, name, url, period, regex_check):
        self.site_id = site_id
        self.name = name
        self.url = url
        self.period = period
        self.regex_check = regex_check

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
        checker.start(site)
        time.sleep(5)


if __name__ == '__main__':
    sites = _fetch_schedule()
    start_scheduler(sites[1])
