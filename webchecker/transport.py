#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Messages Transport module
"""
import abc
import json

from datetime import datetime

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError

from webchecker.logger import logger
from webchecker.settings import TRANSPORT


class Message:
    """
    Message to be sent on the trasnport
    """
    def __init__(self, site_id: int, status_code: int, response_time: int,
                 created: datetime, passed: bool):
        self.site_id = site_id
        self.status_code = status_code
        self.response_time = response_time
        self.created = created
        self.passed = passed

    def asdict(self):
        return {'site_id': self.site_id,
                'status_code': self.status_code,
                'response_time': self.response_time,
                'created': self.created.isoformat(),
                'passed': self.passed}

    def __repr__(self):
        return json.dumps(self.asdict())

    def asbytes(self):
        return str(self).encode('utf-8')

    @classmethod
    def from_bytes(klass, value):
        """Creates a Message object from bytes"""
        value_str = value.decode('utf-8')
        value_dict = json.loads(value_str)
        value_dict['created'] = datetime.fromisoformat(value_dict['created'])
        return klass(**value_dict)
        

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
    def __init__(self, cons=False):
        self.host = TRANSPORT.get('host', 'localhost')
        self.port = TRANSPORT.get('port', 9002)
        self.topic_name = TRANSPORT.get('topic_name', 'defaulttopic')
        # TODO: use same client accross multiple calls
        if not cons:
            self.producer = KafkaProducer(bootstrap_servers=[f'{self.host}:{self.port}'])

    def publish(self, message: Message):
        if not self.producer:
            raise Exception('No producer found!')
        try:
            logger.error('test debugger4')
            self.producer.send(self.topic_name,
                               message.asbytes())
        except KafkaError as err:
            logger.error(err)
            logger.debug(f'Error trying to publish a message to kafka, \
                          message: {message.asdict()}, not sent!')
    def get_consumer(self):
        # FIXME: this is bad!
        return KafkaConsumer(self.topic_name,
                             bootstrap_servers=[f'{self.host}:{self.port}'])



class File(TransportInterface):
    """
    File Transport
    """
    def publish(self, message: Message):
        # TODO: read file name from configuration
        line = (f'{message.site_id},{message.status_code},'
                f'{message.response_time},{message.created},'
                f'{message.passed}')
        filename = TRANSPORT.get('file_name', 'file_trasnport.txt')
        with open(filename, mode='a') as f:
            f.write(line)


class Console(TransportInterface):
    """
    Console Trasnport
    """
    def publish(self, message: Message):
        print(f'site id: {message.site_id}\n'
              f'status code: {message.status_code}\n'
              f'response time: {message.response_time}\n'
              f'creation time: {message.created}\n')


def create_trasnport():
    transport_type = TRANSPORT.get('type', 'Console')
    if transport_type == 'File':
        logger.debug('Will use a File trasnport')
        return File()

    if transport_type == 'Kafka':
        logger.debug('Will use Kafka trasnport')
        try:
            kafka = Kafka()
        except KafkaError as err:
            logger.error(err)
            logger.debug('Error trying to create kafka client, will fallback\
                         to the console')
            return Console()
        except TypeError as err:
            logger.error(err)
            logger.debug('Error trying to create kafka client, will fallback\
                         to the console')
            return Console()
        return kafka

    logger.debug('Will only output messages to the Console')
    return Console()
