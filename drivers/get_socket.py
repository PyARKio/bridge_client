# -- coding: utf-8 --
from __future__ import unicode_literals
import threading
import socket
from time import sleep
import time
from multiprocessing import Queue
from drivers.log_settings import log


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


class CommonQueue:
    CQ = Queue()
    SysCQ = Queue()
    SCQ = Queue()


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
            CommonQueue.SCQ.put(False)
            return False
        else:
            _socket.setblocking(False)
            _socket.settimeout(1)
        log.info('function: <{}>, host: {}, STATUS: OK'.format(f_object.__name__, object_to_check[0]))
        return f_object(*object_to_check, _socket)
    return _f


@_init_client
def check_host(host=None, port=None, _socket=None):
    log.info('Connecting to {}:{}:{} ...'.format(host, port, _socket))
    try:
        _socket.connect((host, port))
    except Exception as err:
        log.error('HOST: {} ERROR: {}'.format(host, err))
        CommonQueue.SCQ.put(False)
    else:
        log.info('Connect :) HOST: {}'.format(host))
        _server_identification(host, _socket)


def _server_identification(host, _socket):
    log.info('for host: {}'.format(host))
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
            # data = _socket.recv(1024).decode()
            # while True:
            #     sleep(10)
        else:
            CommonQueue.SCQ.put(False)


# PRE_HOST: is not correct method !!!
# @CHECK_args !!!
def search_host(pre_host=None, port=None, _socket_connect=None, auto=False, word=[None, None]):
    _socket = False

    if auto:
        log.info('AUTO MODE')
        point = time.time()
        for f in range(0, 256, 4):
            for i in range(f, f + 4):
                host = '{}.{}'.format(pre_host, i)
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
                log.info(time.time() - point)
                log.info(_socket)
                break

        # for i in range(5):
        #     log.info('send to server: {}'.format(bytes('BREAK :)', encoding='UTF-8')))
        #     _socket.send(bytes('BREAK :)', encoding='UTF-8'))
        #     sleep(5)
        # data = _socket.recv(10000)
        # _socket = None
    else:
        log.info('MANUAL MODE')
        check_host(pre_host, port)
        _socket = CommonQueue.SCQ.get()

    return _socket


# search_host(pre_host='10.8.0', port=777, auto=True)
