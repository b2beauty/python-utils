#!/usr/bin/python
# coding: utf-8
"""

This module implements connections for MySQLdb. Presently there is
only one class: Connection. Others are unlikely. However, you might
want to make your own subclasses. In most cases, you will probably
override Connection.default_cursor with a non-standard Cursor class.

Changed by Navegg - <it@navegg.com>"""

from MySQLdb.connections import Connection
from navegg_utils import cursors


class Connection(Connection):

    """MySQL Database Connection Object

    Changed by Navegg - <it@navegg.com>"""

    default_cursor = cursors.Cursor
    host = None
    user = None
    passwd = None
    port = 3306
    charset = 'utf8'
    db = ''

    def __init__(self, *args, **kwargs):

        kwargs2 = kwargs.copy()
        self.host = kwargs2.pop('host', None)
        self.user = kwargs2.pop('user', None)
        self.passwd = kwargs2.pop('passwd', None)
        self.port = kwargs2.pop('port', 3306)
        self.charset = kwargs2.pop('charset', 'utf8')
        self.db = kwargs2.pop('db', '')

        return super(Connection, self).__init__(*args, **kwargs)


connect = Connection
