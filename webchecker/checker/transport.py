#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Messages Transport module
"""
import abc
from datetime import datetime

from webchecker.logger import logger
from webchecker.settings import TRANSPORT


class Message:
    """
    Message to be sent on the trasnport
    """
    def __init__(self, site_id: int, code: int, response_time: int,
                 created: datetime):
        self.site_id = site_id
        self.code = code
        self.response_time = response_time
        self.created = created


class TransportInterface(metaclass=abc.ABCMeta):
    """
    Transport Interface
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'publish') and
                callable(subclass.publish) or
                NotImplemented)

    @abc.abstractmethod
    def publish(self, topic_name: str, message: Message):
        """Publish a message to a topic"""
        raise NotImplementedError


class Kafka(TransportInterface):
    """
    Kafka Transport
    """
    def publish(self, message: Message):
        # TODO: read topic name from configuration
        pass

class File(TransportInterface):
    """
    File Transport
    """
    def publish(self, message: Message):
        # TODO: read file name from configuration
        line = f'{message.site_id},{message.code},{message.response_time},{message.created}\n'
        filename = 'file_trasnport.txt'
        with open(filename, mode='a') as f:
            f.write(line)


class Console(TransportInterface):
    """
    Console Trasnport
    """
    def publish(self, message: Message):
        print(f'site id: {message.site_id}\n'
              f'status code: {message.code}\n'
              f'response time: {message.response_time}\n'
              f'creation time: {message.created}\n')


def create_trasnport():
    transport_type = TRANSPORT.get('type', 'Console')
    if transport_type == 'File':
        logger.debug('Will use a File trasnport')
        return File()
    if transport_type == 'Kafka':
        logger.debug('Will use Kafka trasnport')
        return Kafka()
        logger.debug('Will only output messages to the Console')
    return Console()
