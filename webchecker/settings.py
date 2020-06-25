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
