#!/usr/bin/env python3

# LG generate some numbers about moodle 

from sys import exit
from time import time

try:
    import click
except:
    print('No click module found. Debian install: apt install python3-click')
    exit(1)

try:
    import pymysql.cursors
except:
    print('No pymysql module found. Debian install: apt install python3-pymysql')

@click.command()
@click.option('--host', '-h', default='127.0.0.1', help='SQL Host', show_default=True)
@click.option('--user', '-u', default='moodlechecker', help='Username', show_default=True)
@click.option('--password', '-p', prompt=True, hide_input=True)
@click.option('--database', '-d', default='moodle', help='SQL Database', show_default=True)
@click.option('--table', '-t', default='mdl_', help='Moodle table prefix', show_default=True)
@click.option('--debug/--no-debug', default=False, help='Debug mode', show_default=True)
@click.option('--statistic', '-s', default='users_live', show_default=True, type=click.Choice(['users_live', 'users_hour', 'users_day', 'file_count', 'active_accounts'], case_sensitive=False))


def m_cli(host, user, password, database, table, debug, statistic):

    """Get moodle statistics, and/or check moodle thresholds."""

    if debug:
        click.echo('Debug mode is %s' % ('on' if debug else 'off'))
        print(f"SQL Host: {host}")
        print(f"SQL User: {user}")
        #print(f"SQL Pass: {password}")
        print(f"SQL DB: {database}")
        print(f"Moodle table prefix: {table}")

    m_call(host, user, password, database, table, debug, statistic)


def m_call(host, user, password, database, table, debug, statistic):

    """Check the statistic and call the function, return the value."""

    call = statistic

    if call == 'users_live':
        seconds = 300
        m_users(host, user, password, database, table, debug, statistic, seconds)
    elif call == 'users_hour':
        seconds = 7200
        m_users(host, user, password, database, table, debug, statistic, seconds)
    elif call == 'users_day':
        seconds = 86400
        m_users(host, user, password, database, table, debug, statistic, seconds)
    elif call == 'file_count':
        m_files(host, user, password, database, table, debug, statistic)
    elif call == 'active_accounts':
        m_accounts(host, user, password, database, table, debug, statistic)
    else:
        print ('Run with --help, should never get here!')


def m_users(host, user, password, database, table, debug, statistic, seconds):

    """Query the database, return number of users over time."""

    table_name = table+'user'
    epoch = int(time())
    offset = seconds
    moodle_secs = (epoch - offset)

    if debug:
        print(f"Moodle table name: {table_name}")
        print(f"Epoch time: {epoch}")
        print(f"Offset Seconds: {offset}")
        print(f"Moodle seconds to check: {moodle_secs}")
    
    connection = pymysql.connect(host=host, user=user,
                                 password=password, db=database,
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT count(id) AS users FROM (%s) WHERE lastaccess > (%s)' % \
            (table_name,moodle_secs))
            result = cursor.fetchone()
            if debug:
                print (result)
            print (result['users'])
    finally:
        connection.close()


def m_accounts(host, user, password, database, table, debug, statistic):

    """Query the database, return number of active accounts."""

    table_name = table+'user'

    if debug:
        print(f"Moodle table name: {table_name}")
    
    connection = pymysql.connect(host=host, user=user,
                                 password=password, db=database,
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT COUNT(id) AS accounts FROM (%s) WHERE confirmed = 1 AND NOT (deleted = 1 OR suspended = 1)' % \
            (table_name,))
            result = cursor.fetchone()
            if debug:
                print (result)
            print (result['accounts'])
    finally:
        connection.close()


def m_files(host, user, password, database, table, debug, statistic):

    """Query the database, return number of user files."""

    table_name = table+'files'

    if debug:
        print(f"Moodle table name: {table_name}")
    
    connection = pymysql.connect(host=host, user=user,
                                 password=password, db=database,
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT count(id) AS files FROM (%s)' % \
            (table_name,))
            result = cursor.fetchone()
            if debug:
                print (result)
            print (result['files'])
    finally:
        connection.close()


def main():
    m_cli()


if __name__ == '__main__':
    main()
