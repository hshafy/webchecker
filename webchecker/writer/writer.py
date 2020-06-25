#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
writer module
"""
import time

from webchecker.checker.transport import Message, Kafka
from webchecker.writer.models import Checks
from webchecker.logger import logger

def run_worker():

    """
    Start a worker to process messages

    1- fetch message from kafka
    2- convert received message to known type
    3- save_result()
    """
    logger.debug('Starting writer worker.')
    # FIXME: bitte
    kafka = Kafka(cons=True)
    consumer = None
    while not consumer:
        logger.debug('Attempting to connect to Kafka')
        consumer = kafka.get_consumer()
        time.sleep(10)
    
    logger.debug('Kafka consumer acquired')
    while True:
        for msg in consumer:
            try:
                converted_msg = Message.from_bytes(msg.value)
                save_result(converted_msg)
            except Exception as err:
                logger.error(err)


def save_result(message: Message):
    """
    Saves result to db
    """
    record = Checks(site_id=message.site_id,
                    status_code=message.code,
                    response_time=message.response_time,
                    created=message.created)
    record.save()
