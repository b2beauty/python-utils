#!/usr/bin/python
# coding: utf-8

'''A Navegg package

Author <felipe.a.tomaz@gmail.com>
Created: 27/08/2013
History:
    0.2 <2013-08-28> Add function dictfetchone
'''

def dictfetchall(cursor):
    '''Returns all rows from a cursor as a dict

Example of use:

    from navegg_utils import connect, dictfetchall

    cursor = connect.mysql('host', 'myuser', 'passwd', 'database')
    cursor.execute('show tables')
    rows = dictfetchall(cursor)'''
    
    return [
        dict(zip([col[0] for col in cursor.description], row))
        for row in cursor.fetchall()
    ]
    
def dictfetchone(cursor):
    '''Returns one row from a cursor as a dict

Example of use:

    from navegg_utils import connect, dictfetchaone

    cursor = connect.mysql('host', 'myuser', 'passwd', 'database')
    cursor.execute('show tables')
    row = dictfetchone(cursor)'''
    
    return dict(
        zip(
            [col[0] for col in cursor.description],
            cursor.fetchaone()
        ))

__all__ = [
    'connect',
    'logging',
    'dictfetchall',
]
