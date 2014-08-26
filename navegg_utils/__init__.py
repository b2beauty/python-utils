#!/usr/bin/python
# coding: utf-8

'''A Navegg package

Author <felipe.a.tomaz@gmail.com>
Created: 27/08/2013
History:
    0.2 <2013-08-28> Add function dictfetchone
    0.3 <2013-09-02> Add decorator function timeit
    0.4 <2014-08-26> Add function to remove especial charters
'''

import time
import connect
#import test

__version__ = '0.1.9.2'


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

def rchar(word):
    vSomeSpecialChars = [ "á", "à", "â", "ã", "ä", "é", "è", "ê", "ë", "í", "ì", "î", "ï", "ó", "ò", "ô", "õ", "ö", "ú", "ù", "û", "ü", "ç","Á", "À", "Â", "Ã", "Ä", "É", "È", "Ê", "Ë", "Í", "Ì", "Î", "Ï", "Ó", "Ò", "Ô", "Õ", "Ö", "Ú", "Ù", "Û", "Ü", "Ç" ]
    vReplacementChars = [ "a", "a", "a", "a", "a", "e", "e", "e", "e", "i", "i", "i", "i", "o", "o", "o", "o", "o", "u", "u", "u", "u", "c","A", "A", "A", "A", "A", "E", "E", "E", "E", "I", "I", "I", "I", "O", "O", "O", "O", "O", "U", "U", "U", "U", "C" ]
    for x in range(len(vSomeSpecialChars)):
        word = word.replace(vSomeSpecialChars[x], vReplacementChars[x] )
    return word

__all__ = [
    'connect',
    'dictfetchall',
    'dictfetchone',
    'timeit',
    'rchar',
#    'test'
]
