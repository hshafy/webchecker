#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DB Module
"""
import psycopg2

from webchecker.settings import DATABASE
from webchecker.logger import logger


def init_db():
    """
    Create database and tables
    """
    logger.debug('Initializing database...')
    create_db()
    create_tables()
    logger.debug('Database initialization suceeded.')


def create_db():
    """
    Create database
    """
    # TODO: check if db exists before
    conn = connection(use_db=False)
    cur = conn.cursor()
    try:
        logger.debug('Creating database...')
        cur.execute('CREATE DATABASE writer;')
    except psycopg2.Error as err:
        logger.error(err)
    finally:
        cur.close()
        conn.close()
    logger.debug('Database creation suceeded.')


def create_tables():
    """
    Create tables
    """
    conn = connection()
    cur = conn.cursor()
    try:
        tables = tables_creation_sqls()
        for table in tables:
            logger.debug('Creating table...')
            cur.execute(table)
    except psycopg2.Error as err:
        logger.error(err)
    finally:
        cur.close()
        conn.close()
    logger.debug('Tables creation suceeded.')


def tables_creation_sqls():
    """
    Get tables creations sqls
    """
    sql = []
    check_table = ('CREATE TABLE checks('
                   '  id serial PRIMARY KEY,'
                   '  site_id INTEGER NOT NULL,'
                   '  status_code INTEGER NOT NULL,'
                   '  response_time INTEGER NOT NULL,'
                   '  created TIMESTAMP)')
    sql.append(check_table)
    return sql


def connection(use_db=True):
    """
    Get db connection
    """
    # TODO: use the connection pool
    host = DATABASE.get("host", 'localhost')
    port = DATABASE.get("port", 5432)
    user = DATABASE.get("user")
    password = DATABASE.get("password")
    db_name = DATABASE.get("db_name")
    if not use_db:
        db_name = 'postgres'

    assert all([host, port, db_name, user, password])
    conn = None
    try:
        conn = psycopg2.connect(host=host, port=port, user=user,
                                password=password, dbname=db_name)
        conn.set_session(autocommit=True)
        return conn
    except psycopg2.Error as err:
        logger.error(err)
        if hasattr(conn, 'close') and callable(getattr(conn, 'close')):
            conn.close()
