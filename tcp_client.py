# -- coding: utf-8 --
from __future__ import unicode_literals
import threading
from multiprocessing import Queue
from drivers import get_socket
from drivers.log_settings import log
from time import sleep
import time
import socket
import pickle


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
            # check back-up files (mistake: two lines upper)
            while _socket:
                _socket = self._get_data_from_server(_socket, _sender)

    def _get_socket(self):
        log.info('init search host')
        _socket = get_socket.search_host(pre_host=self.host, port=self.port, auto=self.auto)
        log.info(_socket)
        self.system_callback(_socket)

        return _socket

    def _run_sender(self, _socket):
        _sender = Sender(sender_socket=_socket, system_callback=self.system_callback)
        _sender.start()
        _socket.settimeout(1)
        return _sender

    def _get_data_from_server(self, _socket, _sender):
        try:
            data = _socket.recv(1024).decode()
        except socket.timeout:
            if not _sender.running:
                _socket = False
                log.info('_socket: {}'.format(_socket))
        except Exception as err:
            _socket = False
            self._socket_error(err, _sender)
        else:
            if not data:
                log.error('No data from {}'.format(data))
                _socket = False
                self._socket_error('No data', _sender)
            else:
                # ADD related to key data from )_sender !!!!
                if _sender.walkie_talkie_runner and data == 'READY TO NEXT':
                    _sender.walkie_talkie_runner = False
                self.data_callback(data)
        return _socket

    def _socket_error(self, err, _sender):
        log.info('ERROR: {}'.format(err))
        _sender.running = False
        self.system_callback({'ERROR: {}'.format(err)})


class Sender(threading.Thread):
    CYCLE = 0

    def __init__(self, sender_socket=None, data_callback=None, system_callback=None):
        log.info('start up')
        self.running = True
        self.walkie_talkie_runner = False
        self.sender_socket = sender_socket
        self.data_callback = data_callback
        self.system_callback = system_callback

        threading.Thread.__init__(self)

    def run(self):
        _delta_on = 0
        while self.running:
            response = Sender.__get_from_queue(self)
            if response:
                # check data type
                log.info('SEND: {}'.format(response))
                try:
                    self.sender_socket.send(bytes(response, encoding='UTF-8'))
                except Exception as err:
                    log.error('SENDER: {}'.format(err))
                    self.system_callback({'ERROR: {}'.format(err)})
                    self._back_up()
                else:
                    self.walkie_talkie_runner = True
                    _delta_on = time.time()
                    log.info('WALKIE-TALKIE: {}, _delta_on: {}'.format(self.walkie_talkie_runner, _delta_on))
            self.walkie_talkie(_delta_on)

    def walkie_talkie(self, _delta_on):
        while self.walkie_talkie_runner:
            sleep(0.05)
            if time.time() - _delta_on > 3:
                self.system_callback('LOST CONNECTION WITH SERVER')
                self._back_up()
        Sender.CYCLE += 1

    @staticmethod
    def __get_from_queue(self):
        log.info('RUNNING... CYCLE: {}'.format(Sender.CYCLE))
        while CommonQueue.CQ.empty() and self.running:
            sleep(0.01)
        try:
            data = CommonQueue.CQ.get(block=False)
        except Exception as err:
            log.error(err)
            return False
        if data != 'SAVE':
            return data
        return False

    def _back_up(self):
        self.walkie_talkie_runner = False
        self.running = False
        temp_queue = CommonQueue.CQ.put('SAVE', block=True)
        pickle.dump(temp_queue, open('pyark_{}_.io'.format(time.time()), 'wb'), 2)


def callback_data(response):
    log.info(response)


def callback_system(response):
    log.info(response)
    log.info('START WRITE TO LOCAL DB :)')


if __name__ == '__main__':
    _client = Client(host='192.168.1', port=777, auto=True, data_callback=callback_data, system_callback=callback_system)
    _client.start()

    while True:
        # sleep(15)
        for i in range(500):
            log.info('send to server: {}'.format(bytes('BREAK :) NUMBER: {}'.format(i), encoding='UTF-8')))
            CommonQueue.CQ.put('BREAK :) NUMBER: {}'.format(i), block=False)
            sleep(1)


