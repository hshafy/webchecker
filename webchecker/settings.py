#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Settings
"""

TRANSPORT = {
    # Trasnport type, can be one of File, Console or Kafka
    "type": "Kafka",

    # Topic name, only in Kafka
    "topic_name": "checks",
    "host": "kafka",
    "port": 9092,

    # Only for File
    "file_name": "file_trasnport.txt",
}

DATABASE = {
    # TODO: move this to env variable
    "db_conn": "postgresql://postgres:postgres@db:5432",
    "host": "db",
    "port": 5432,
    "db_name": "writer",
    "user": "postgres",
    "password": "postgres",
}

SCHEDULE = [
    {
        "site_id": 1,
        "name": "google",
        "url": "https://google.com",
        "period": 60,  # seconds
        "regex_check": None,
        "pass_code": 200,
    },
    {
        "site_id": 2,
        "name": "microsift",
        "url": "https://microsoft.com",
        "period": 30,  # seconds
        "regex_check": None,
        "pass_code": 200,
    }
]
