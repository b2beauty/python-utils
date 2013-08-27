#!/usr/bin/python
# coding: utf-8

'''Make connections for all in the world

Author <felipe.a.tomaz@gmail.com>
Created: 27/08/2013
This fragment of the lib is intended to provide all types of connections
projects undertaken in the Naveeg. eg: Database, Queue
History:
'''

import MySQLdb
import pika

def mysql(host,user,password,database=None,autocommit=False):
    '''Connects to a database as parameters informed.
If the database argument is informed only the cursor will be returned, 
but if not informed a database will be returned also the connection to
the database so it can be held to exchange database.

Example of use:

    Informing the database:
    from navegg_utils import connect

    cursor = connect.mysql('host', 'myuser', 'passwd', 'database')

    Without informing the database:

    from navegg_utils import connect
    cursor, connection = connect.mysql ('host', 'myuser', 'passwd')'''
    
    try:
        connection = MySQLdb.connect(host, user, password)
    except MySQLdb.connector.Error as err:
        raise err
        
    cursor = connection.cursor()
    if autocommit:
        cursor.execute('set autocommit = 1')
    if database:
        connection.select_db(database)
        return cursor

    return (cursor,connection)

def queue(host,user,password,queue):
    '''Connects in a row as parameters informed.
You must enter all parameters in function call

Example of use:

    import from navegg_utils connect

    channel = connect.queue ('host', 'myuser', 'passwd', 'queue-name')'''

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,credentials = pika.credentials.PlainCredentials(user, password)))
    except:
        raise
        
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True,exclusive=False)
    
    return channel
