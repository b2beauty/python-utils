#!/usr/bin/python
# coding: utf-8

'''A Navegg package

Author <felipe.a.tomaz@gmail.com>
Created: 27/08/2013
History:
'''

def dictfetchall(cursor):
    '''Returns all rows from a cursor as a dict

Example of use:

    from navegg_utils import connect, dictfetchall

    cursor = connect.mysql('host', 'myuser', 'passwd', 'database')
    cursor.execute('show tables')
    rows = dictfetchall(cursor)'''
    
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

__all__ = [
    'connect',
    'logging',
    'dictfetchall',
]
