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
}
