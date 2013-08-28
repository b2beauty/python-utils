#!/usr/bin/python
# coding: utf-8

'''Make connections for all in the world

Author <felipe.a.tomaz@gmail.com>
Created: 27/08/2013
This fragment of the lib is intended to provide all types of connections
projects undertaken in the Naveeg. eg: Database, Queue
History:
    0.2 <2013-08-28> Add Queue class
'''

import simplejson
import MySQLdb
import pika

def mysql(host,user,password,database=None,autocommit=True):
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
    
class Queue(object):
    '''Connects in queue as parameters informed.
You must enter all parameters in function call or use default values

Example of use:

    from navegg_utils import connect

    channel = connect.Queue()
    queue = channel.getQueue('name')'''
    
    def __init__(self,host='quinn.nvg.im',user='guest',password='guest'):
        self.host = host
        self.user = user
        self.password = password
        self.__connect()

    def __connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                credentials=pika.credentials.PlainCredentials(self.user, self.password)
            )
        )

    def getChannel(self):
        return self.connection.channel()

    def getQueue(self,queue):
        channel = self.getChannel()
        channel.queue_declare(queue=queue, durable=True,exclusive=False)
        return channel
        
    def sendPackage(self,queue,name,package):
        try:
            if not len(package) and type(package) not in [dict,list,tuple]:
                raise Exception('Type not is dict or list or tuple')
                
            json_package = simplejson.dumps(package)
            queue.basic_publish(exchange='',routing_key=name,
                                body=json_package,
                                properties=pika.BasicProperties(
                                   delivery_mode = 2,
                                ))
        except Exception as error:
            raise
            
    def loadPackageValue(self,ch,method,properties,body):
        decoded_body = simplejson.loads(body)
        self.function(decoded_body)
        ch.basic_ack(delivery_tag = method.delivery_tag)

    def receivePackage(self,queue,name,function):
        self.function = function
        queue.basic_qos(prefetch_count=1)
        queue.basic_consume(self.loadPackageValue,queue=name)
        queue.start_consuming()
