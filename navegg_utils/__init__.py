#!/usr/bin/python
# coding: utf-8

'''A Navegg package

Author <felipe.a.tomaz@gmail.com>
Created: 27/08/2013
History:
    0.2 <2013-08-28> Add function dictfetchone
    0.3 <2013-09-02> Add decorator function timeit
'''

import time
import connect
#import test

__version__ = '0.1.9'


def dictfetchall(cursor):
    '''Returns all rows from a cursor as a dict

Example of use:

    from navegg_utils import connect, dictfetchall

    cursor = connect.mysql('host', 'myuser', 'passwd', 'database')
    cursor.execute('show tables')
    rows = dictfetchall(cursor)'''

    try:
        return [
            dict(zip([col[0] for col in cursor.description], row))
            for row in cursor.fetchall()
        ]
    except:
        return []


def dictfetchone(cursor):
    '''Returns one row from a cursor as a dict

Example of use:

    from navegg_utils import connect, dictfetchaone

    cursor = connect.mysql('host', 'myuser', 'passwd', 'database')
    cursor.execute('show tables')
    row = dictfetchone(cursor)'''

    try:
        return dict(
            zip(
                [col[0] for col in cursor.description],
                cursor.fetchone()
            ))
    except:
        return {}


def timeit(method):
    '''Decorator to calculate execute time for a function

Example of use:

    from navegg_utils import timeit

    class a(object):
        @timeit
        def b(self,c,d):
            return c+d

    if __name__ == '__main__':
        e = a()
        e.b(5,4)

Out of execute is:

    Time to execute 'b': 0.000002 sec'''

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print 'Time to execute %r: %f sec' % (method.__name__, te-ts)
        return result

    return timed

__all__ = [
    'connect',
    'dictfetchall',
    'dictfetchone',
    'timeit',
#    'test'
]
