# -- coding: utf-8 --
from __future__ import unicode_literals
import threading
from multiprocessing import Queue
from drivers import get_socket
from drivers.log_settings import log
from time import sleep


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
        threading.Thread.__init__(self)

        self.host = host
        self.port = port
        self.auto = auto
        self.data_callback = data_callback
        self.system_callback = system_callback
        self.running = True

    def run(self):
        while self.running:
            _socket = False
            while not _socket:
                _socket = get_socket.search_host(pre_host=self.host, port=self.port, auto=self.auto)
                log.info(_socket)
                self.system_callback(_socket)

            while _socket:
                log.info('\n\nREAD\n\n')
                _socket.setblocking(True)
                try:
                    data = _socket.recv(10000)
                except Exception as err:
                    log.info('ERROR: {}'.format(err))
                    # _socket = None
                else:
                    self.data_callback(data.decode('cp1251'))
                    # _socket.setblocking(False)

                # for i in range(5):
                # log.info('send to server: {}'.format(bytes('BREAK :)', encoding='UTF-8')))
                # _socket.send(bytes('BREAK :)', encoding='UTF-8'))
                #     sleep(5)
                # _socket = None


class Sender(threading.Thread):
    def __init__(self, sender_socket=None):
        threading.Thread.__init__(self)
        self.running = True
        self.sender_socket = sender_socket

    def run(self):
        while self.running:
            data = CommonQueue.CQ.get()
            # check data type
            self.sender_socket.send(bytes(data, encoding='UTF-8'))


def callback_data(response):
    log.info(response)


def callback_system(response):
    log.info(response)


if __name__ == '__main__':
    # host='10.8.0'
    _client = Client(host='192.168.1', port=777, auto=True, data_callback=callback_data, system_callback=callback_system)
    _client.start()

    while True:
        sleep(10)


