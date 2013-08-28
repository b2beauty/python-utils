#!/usr/bin/python2.7

import logging
import logging.handlers

def log(logname):

    FORMAT = "%(levelname)s %(asctime)s %(filename)s %(funcName)s %(lineno)d %(message)s"
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger(logname)

def logEmail(logname):
    
    formatter = logging.Formatter()
    h1.setFormatter(f)
    h1.setLevel(logging.DEBUG)
    x.addHandler(h1)

    h2 = logging.handlers.SMTPHandler('root', 'root@debra.navegg.com', ['it@navegg.com'], 'CRITICAL log')
    h2.setLevel(logging.CRITICAL)
    h2.setFormatter(f)
    x.addHandler(h2)

