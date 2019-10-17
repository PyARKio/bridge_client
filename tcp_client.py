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
def check_host(host=None, port=None, _socket=None):
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
    log.info('')
    try:
        data = _socket.recv(1024).decode()
    except Exception as err:
        log.info('HOST: {} ERROR: {}'.format(host, err))
        CommonQueue.SCQ.put(False)
    else:
        log.info('response from server: {}'.format(data))
        if data == 'check\r\n':
            log.info('send to server: {}'.format(bytes('check ok', encoding='UTF-8')))
            _socket.send(bytes('check ok', encoding='UTF-8'))
            CommonQueue.SCQ.put(_socket)
        else:
            CommonQueue.SCQ.put(False)


# check_host('10.8.0.5', 777)


def auto_search_host(pre_host, port):
    point = time.time()
    _socket = False
    for f in range(0, 256, 4):
        for i in range(f, f + 4):
            host = '{}.{}'.format(pre_host, i)
            # host = '192.168.1.{}'.format(i)
            assistant_start = threading.Thread(target=check_host, args=(host, port, ))
            assistant_start.start()

        index = 0
        while index < 4:
            if not _socket:
                _socket = CommonQueue.SCQ.get()
            else:
                CommonQueue.SCQ.get()
            index += 1

        if _socket:
            log.info('BREAK')
            break

        log.info(time.time() - point)
        log.info(_socket)
    for i in range(5):
        log.info('send to server: {}'.format(bytes('BREAK :)', encoding='UTF-8')))
        _socket.send(bytes('BREAK :)', encoding='UTF-8'))
        sleep(5)
    _socket = None


auto_search_host('10.8.0', 777)


