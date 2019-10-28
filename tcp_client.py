# -- coding: utf-8 --
from __future__ import unicode_literals
import threading
from multiprocessing import Queue
from drivers import get_socket
from drivers.log_settings import log
from time import sleep
import time
import socket

# print(sys.version)


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


class CommonQueue:
    CQ = Queue()
    SysCQ = Queue()
    SCQ = Queue()


class Client(threading.Thread):
    def __init__(self, host=None, port=None, auto=False, data_callback=None, system_callback=None):
        log.info('client running...')
        self.host = host
        self.port = port
        self.auto = auto
        self.data_callback = data_callback
        self.system_callback = system_callback
        self.running = True

        threading.Thread.__init__(self)

    def run(self):
        while self.running:
            _sender = None
            _socket = None
            log.info('host circle. _socket: {}'.format(_socket))
            while not _socket:
                _socket = self._get_socket()
            if _socket:
                _sender = self._run_sender(_socket)
            while _socket:
                _socket = self._get_data_from_server(_socket, _sender)

    def _get_socket(self):
        log.info('init search host')
        _socket = get_socket.search_host(pre_host=self.host, port=self.port, auto=self.auto)
        log.info(_socket)
        self.system_callback(_socket)

        return _socket

    @staticmethod
    def _run_sender(_socket):
        _sender = Sender(sender_socket=_socket)
        _sender.start()
        _socket.settimeout(1)

        return _sender

    def _get_data_from_server(self, _socket, _sender):
        # log.info('\n\nREADY to read\n\n')
        try:
            data = _socket.recv(1024).decode()
        except socket.timeout as err:
            pass
            # log.error('GOOD ERROR: {}'.format(err))
        except Exception as err:
            _socket = False
            self._socket_error(err, _sender)
        else:
            if not data:
                log.error('No data from {}'.format(data))
                _socket = False
                self._socket_error(err, _sender)
            else:
                # ADD related to key data from )_sender !!!!
                if _sender.walkie_talkie and data == 'READY TO NEXT':
                    _sender.walkie_talkie = False
                self.data_callback(data)  # .decode('cp1251')
        return _socket

    def _socket_error(self, err, _sender):
        log.info('ERROR: {}'.format(err))
        # STOP SENDER
        _sender.running = False
        CommonQueue.CQ.put(False)
        # SEND TO PARENT
        self.system_callback({'ERROR': '{}'.format(err)})


class Sender(threading.Thread):
    def __init__(self, sender_socket=None, data_callback=None, system_callback=None):
        log.info('start up')
        self.running = True
        self.walkie_talkie = False
        self.sender_socket = sender_socket
        self.data_callback = data_callback
        self.system_callback = system_callback

        threading.Thread.__init__(self)

    def run(self):
        log.info('SENDER running...')
        _delta_on = 0
        while self.running:
            response = Sender.__get_from_queue()
            if response:
                # check data type
                log.info('SEND: {}'.format(response))
                try:
                    self.sender_socket.send(bytes(response, encoding='UTF-8'))
                except Exception as err:
                    log.error('SENDER: {}'.format(err))
                    # self.system_callback()
                else:
                    self.walkie_talkie = True
                    _delta_on = time.time()
                    log.info('WALKIE-TALKIE: {}, _delta_on: {}'.format(self.walkie_talkie, _delta_on))
            else:
                log.info('SENDER: response = {}'.format(response))
                # self.system_callback()

            while self.walkie_talkie:
                sleep(0.05)
                if time.time() - _delta_on > 3:
                    # CALLBACK to write in local db
                    log.debug('TIMEOUT !!!!!!!!!!!!')
                    log.debug(time.time() - _delta_on)
                    self.walkie_talkie = False
            log.info('NEXT @@@@@')

    @staticmethod
    def __get_from_queue():
        try:
            data = CommonQueue.CQ.get()
        except Exception as err:
            log.error(err)
            return False

        return data


def callback_data(response):
    log.info(response)


def callback_system(response):
    log.info(response)
    log.info('START WRITE TO LOCAL DB :)')


if __name__ == '__main__':
    _client = Client(host='192.168.0', port=777, auto=True, data_callback=callback_data, system_callback=callback_system)
    _client.start()

    while True:
        for i in range(500):
            log.info('send to server: {}'.format(bytes('BREAK :) NUMBER: {}'.format(i), encoding='UTF-8')))
            CommonQueue.CQ.put('BREAK :) NUMBER: {}'.format(i))
            sleep(2)


