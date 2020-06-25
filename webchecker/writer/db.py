#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DB Module
"""
import psycopg2
from psycopg2 import sql

from webchecker.logger import logger
from webchecker.settings import DATABASE


def init_db():
    """
    Create database and tables if db not there
    """
    # TODO: get params from a function
    db_name = DATABASE.get('db_name', 'writer')
    try:
        conn = connection(use_db=False)
        cur = conn.cursor()
        if db_exists(cur, db_name):
            return True
        logger.debug('DB not found, will create it...')
        create_db(cur, db_name)
    except psycopg2.Error as err:
        logger.error(err)
        return False
    finally:
        cur.close()
        conn.close()

    logger.debug('Switching to created DB...')
    try:
        writer_conn = connection()
        writer_cur = writer_conn.cursor()
        create_tables(writer_cur)
    except psycopg2.Error as err:
        logger.error(err)
        return False
    finally:
        writer_cur.close()
        writer_conn.close()
    logger.debug('Database initialization suceeded.')
    return True


def db_exists(cursor, db_name):
    """Check if database exists"""
    cursor.execute('SELECT 1 FROM pg_catalog.pg_database '
                   ' WHERE datname = %s;', [db_name])
    return cursor.fetchone() is not None


def create_db(cursor, db_name):
    """Create database"""
    logger.debug('Creating database...')
    cursor.execute(
        sql.SQL('CREATE DATABASE {};').format(sql.Identifier(db_name)))
    logger.debug('Database creation suceeded.')


def create_tables(cursor):
    """Create tables"""
    tables = tables_creation_sqls()
    for table in tables:
        logger.debug('Creating table...')
        cursor.execute(table)
    logger.debug('Tables creation suceeded.')


def tables_creation_sqls():
    """
    Get tables creations sqls
    """
    sql_statements = []
    check_table = ('CREATE TABLE checks('
                   '    site_id integer NOT NULL,'
                   '    created timestamp with time zone NOT NULL,'
                   '    status_code smallint NOT NULL,'
                   '    response_time integer NOT NULL,'
                   '    passed boolean NOT NULL,'
                   '    CONSTRAINT checks_pkey PRIMARY KEY (site_id,created))')
    sql_statements.append(check_table)
    return sql_statements


def connection(use_db=True):
    """
    Get db connection with autocommit=True for
    simplicity
    """
    # TODO: use the connection pool
    # TODO: get params from a function
    host = DATABASE.get('host', 'localhost')
    port = DATABASE.get('port', 5432)
    user = DATABASE.get('user')
    password = DATABASE.get('password')
    db_name = DATABASE.get('db_name', 'writer')
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


def execute(*args, **kwargs):
    """
    A wrapper around psycopg2.execute function

    all params will be passed as is
    """
    conn = connection()
    cur = conn.cursor()
    try:
        cur.execute(*args, **kwargs)
    except psycopg2.Error as err:
        logger.error(err)
    finally:
        cur.close()
        conn.close()
