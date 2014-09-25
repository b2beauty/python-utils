#!/usr/bin/python
# coding: utf-8

'''Make connections for all in the world
'''

import simplejson
import pika
import MySQLdb
from agendabeleza_utils import cursors, connections


def mysql(host, user, password, database='', port=3306,
          autocommit=True, buffer=True, charset='utf8', dictcursor=False):
    '''Connects to a database as parameters informed.
If the database argument is informed only the cursor will be returned,
but if not informed a database will be returned also the connection to
the database so it can be held to exchange database.

Example of use:

    Informing the database:
    from agendabeleza_utils import connect

    cursor = connect.mysql('host', 'myuser', 'passwd', 'database')

    Without informing the database:

    from agendabeleza_utils import connect
    cursor, connection = connect.mysql('host', 'myuser', 'passwd')'''

    try:
        connection = connections.connect(host=host, user=user,
                                         passwd=password, port=port,
                                         charset=charset, db=database)
    except MySQLdb.Error as err:
        raise err

    if dictcursor:
        if buffer:
            cursor = cursors.DictCursor(connection)
        else:
            cursor = cursors.SSDictCursor(connection)
    else:
        if buffer:
            cursor = cursors.Cursor(connection)
        else:
            cursor = cursors.SSCursor(connection)

    if autocommit:
        connection.autocommit(True)
    if database:
        return cursor

    return (cursor, connection)


def try_reconnect(obj):
    import time
    msg = ''
    delay = 1
    count = 3
    while count > 0:
        try:
            return pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=obj.host,
                    credentials=pika.credentials.PlainCredentials(obj.user,
                                                                  obj.password)
                )
            )
        except Exception as e:
            msg = e
            time.sleep(delay)
            delay += 2
            count -= 1

    raise Exception('Were executed 3 attempt to connect without success: * %s *' % msg)


class SafeExecute(object):

    def __call__(self, fn):

        def do_safe(self, *args, **kwargs):
            try:
                fn(self, *args, **kwargs)
            except (pika.exceptions.AMQPConnectionError,
                    pika.exceptions.ConnectionClosed,
                    pika.exceptions.ChannelClosed) as ex:

                self.connection = try_reconnect(self)
        return do_safe


class Queue(object):
    '''Connects in queue as parameters informed.
You must enter all parameters in function call or use default values

Example of use:

    from agendabeleza_utils import connect

    channel = connect.Queue()
    queue = channel.getQueue('name')'''

    def __init__(self, host='127.0.0.1', user='guest', password='guest'):
        self.host = host
        self.user = user
        self.password = password
        self.__connect()

    def __connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                credentials=pika.credentials.PlainCredentials(self.user,
                                                              self.password)
            )
        )

    def getChannel(self):
        return self.connection.channel()

    def getQueue(self, queue):
        channel = self.getChannel()
        channel.queue_declare(queue=queue, durable=True, exclusive=False)
        return channel

    @SafeExecute()
    def sendPackage(self, channel, route_keys, exchange_name, package):
        '''Send package for one queue connected in server

Example of use:

    from agendabeleza_utils import connect

    package = ['a','b','c']

    channel = connect.Queue()
    queue = channel.getQueue('name')
    channel.sendPackage(channel,'route_keys', 'exchange_name',package)'''

        try:
            if not len(package) and type(package) not in [dict, list, tuple]:
                raise Exception('Type not is dict or list or tuple')

            try:
                json_package = simplejson.dumps(package)
            except Exception as error:
                raise
            channel.basic_publish(exchange=exchange_name, routing_key=route_keys,
                                body=json_package,
                                properties=pika.BasicProperties(
                                    delivery_mode=2))
        except Exception as error:
            raise

    def __loadPackageValue(self, ch, method, properties, body):
        try:
            decoded_body = simplejson.loads(body)
        except Exception:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        self.function(decoded_body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    @SafeExecute()
    def receivePackage(self, channel, queue, function):
        '''receive package for one queue connected in server

Example of use:

    from agendabeleza_utils import connect

    def fn(pack):
        print pack

    channel = connect.Queue()
    queue = channel.getQueue('name')
    channel.receivePackage(queue,fn)'''

        self.function = function
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.__loadPackageValue, queue=queue)
        channel.start_consuming()

    def deleteQueue(self, queue, name):
        '''Delete a queue

Example of use:

    from agendabeleza_utils import connect

    connection = connect.Queue()
    channel = connection.getQueue('')
    connection.deleteQueue(channel,'name')'''

        queue.deleteQueue(name)
