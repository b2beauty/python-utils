#!/usr/bin/python
# coding: utf-8

'''Make connections for all in the world

Author Tomaz Felipe <felipe.a.tomaz@gmail.com>
Reviser:
     Viero Rafael <frnakyviero@gmail.com
Created: 27/08/2013
This fragment of the lib is intended to provide all types of connections
projects undertaken in the Naveeg. eg: Database, Queue
History:
    0.2 <2013-08-28> Add Queue class
    0.3 <2013-08-29> Alter methods on Queue class to private, documented
    function and add option for unbuffer cursor in mysql connection
    0.4 <2013-08-28> <Viero> Add port argument in mysql connection function
    0.5 <2013-09-02> Add exception in json loader if body not one json
    0.6 <2014-07-17> Add suport to dictcursor and charset in mysql function
    and use custom cursors class to safe errors in execution
    0.7 <2014-07-21> Add Queue decorator to safe connection
'''

import simplejson
import pika
import MySQLdb
from navegg_utils import cursors, connections


def mysql(host, user, password, database='', port=3306,
          autocommit=True, buffer=True, charset='utf8', dictcursor=False):
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

    from navegg_utils import connect

    channel = connect.Queue()
    queue = channel.getQueue('name')'''

    def __init__(self, host='quinn.nvg.im', user='guest', password='guest'):
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

    def __getChannel(self):
        return self.connection.channel()

    def getQueue(self, queue):
        channel = self.__getChannel()
        channel.queue_declare(queue=queue, durable=True, exclusive=False)
        return channel

    @SafeExecute()
    def sendPackage(self, queue, name, package):
        '''Send package for one queue connected in server

Example of use:

    from navegg_utils import connect

    package = ['a','b','c']

    channel = connect.Queue()
    queue = channel.getQueue('name')
    channel.sendPackage(queue,'name',package)'''

        try:
            if not len(package) and type(package) not in [dict, list, tuple]:
                raise Exception('Type not is dict or list or tuple')

            try:
                json_package = simplejson.dumps(package)
            except Exception as error:
                raise
            queue.basic_publish(exchange='', routing_key=name,
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
    def receivePackage(self, queue, name, function):
        '''receive package for one queue connected in server

Example of use:

    from navegg_utils import connect

    def fn(pack):
        print pack

    channel = connect.Queue()
    queue = channel.getQueue('name')
    channel.receivePackage(queue,'name',fn)'''

        self.function = function
        queue.basic_qos(prefetch_count=1)
        queue.basic_consume(self.__loadPackageValue, queue=name)
        queue.start_consuming()
