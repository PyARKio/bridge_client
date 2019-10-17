# -- coding: utf-8 --
from __future__ import unicode_literals
import threading
import socket
from time import sleep
import time
from datetime import datetime
import json
import pickle
# from queue import Queue
# from collections import deque
from multiprocessing import Queue
from drivers.log_settings import log
from drivers.interrupt import Interrupt
from helpers import Exceptions
from helpers import decorators
from helpers import checkers
import types


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


class CommonQueue:
    CQ = Queue()
    SysCQ = Queue()
    SCQ = Queue()


class Client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        pass


def _init_client(f_object=None):
    log.info(f_object)

    def _f(*object_to_check):
        log.info('init client...')
        log.info(f_object)
        log.info(object_to_check)
        try:
            _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # , 'i')
        except Exception as err:
            log.error(err)
            return False
        else:
            _socket.setblocking(False)
            _socket.settimeout(1)
        log.info('function: <{}>, STATUS: OK'.format(f_object.__name__))
        return f_object(*object_to_check, _socket)
    return _f


@_init_client
def search_ip(host=None, port=None, _socket=None):
    log.info('Connecting to {}:{}:{} ...'.format(host, port, _socket))
    try:
        _socket.connect((host, port))
    except Exception as err:
        log.info('HOST: {} ERROR: {}'.format(host, err))
        CommonQueue.SCQ.put(False)
    else:
        log.info('Connect :) HOST: {}'.format(host))
        _server_identification(host, _socket)


def _server_identification(host, _socket):
    try:
        data = _socket.recv(1024).decode()
    except Exception as err:
        log.info('HOST: {} ERROR: {}'.format(host, err))
        CommonQueue.SCQ.put(False)
    else:
        if data == 'check\r\n':
            _socket.send(bytes('check ok', encoding='UTF-8'))
            CommonQueue.SCQ.put(_socket)
        else:
            CommonQueue.SCQ.put(False)


search_ip('10.8.0.5', 777)



