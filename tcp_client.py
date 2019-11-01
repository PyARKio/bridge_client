# -- coding: utf-8 --
from __future__ import unicode_literals
import threading
from multiprocessing import Queue
from drivers import get_socket
from drivers.log_settings import log
from drivers import db
from time import sleep
import time
import socket
from datetime import datetime


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
        self.db_conn = None
        self.db_cursor = None

        threading.Thread.__init__(self)

    def db_init(self):
        # self.db_name = '{} {}'.format(self.battery_name, time.time())
        log.info('DB name: PyARKio.io')

        self.db_conn, self.db_cursor = db.init_db('PyARKio.io')
        log.info('DB_conn: {};  DB_cursor: {}'.format(self.db_conn, self.db_cursor))

        if self.db_conn and self.db_cursor:
            log.info(db.select_all_table(self.db_cursor))
            if not db.create_table_in_db(self.db_cursor):
                log.info('Can not create table <data>')
                log.info('SYSTEM STOP')
                # sys.exit(0)
            if not db.commit_changes(self.db_conn):
                log.info('Can not commit')
                log.info('SYSTEM STOP')
                # sys.exit(0)
        else:
            log.info('Can not init db')
            log.info('SYSTEM STOP')
            # sys.exit(0)

    def run(self):
        self.db_init()
        while self.running:
            _sender = None
            _socket = None
            log.info('host circle. _socket: {}'.format(_socket))
            while not _socket:
                _socket = self._get_socket()
            self._recover()
            if _socket:
                _sender = self._run_sender(_socket)
            while _socket:
                _socket = self._get_data_from_server(_socket, _sender)

    def _get_socket(self):
        log.info('init search host')
        _socket = get_socket.search_host(pre_host=self.host, port=self.port, auto=self.auto)
        log.info(_socket)
        # self.system_callback({'START': _socket})

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
                if _sender.walkie_talkie_runner and data == 'READY TO NEXT\r\n':
                    _sender.walkie_talkie_runner = False
                self.data_callback(data)
        return _socket

    def _socket_error(self, err, _sender):
        log.info('ERROR: {}'.format(err))
        _sender.running = False
        self.system_callback({'ERROR': err})

    def _recover(self):
        back_up_data = db.select_from_db(self.db_cursor, name_table_in_db='data')
        log.info(back_up_data)
        for data in back_up_data:
            log.debug('PUT IN QUEUE {}'.format(data[3]))
            CommonQueue.CQ.put(data[3], block=False)
            db.delete_from_table_in_db(self.db_cursor, data[0])
            db.commit_changes(self.db_conn)
        back_up_data = db.select_from_db(self.db_cursor, name_table_in_db='data')
        log.info(back_up_data)
        self.system_callback({'START': 'RECOVER DONE'})


class Sender(threading.Thread):
    CYCLE = 0

    def __init__(self, sender_socket=None, data_callback=None, system_callback=None):
        log.info('start up')
        self.running = True
        self.walkie_talkie_runner = False
        self.sender_socket = sender_socket
        self.data_callback = data_callback
        self.system_callback = system_callback
        self.db_conn = None
        self.db_cursor = None

        threading.Thread.__init__(self)

    def run(self):
        self.db_conn, self.db_cursor = db.init_db('PyARKio.io')
        _delta_on = 0
        while self.running:
            response = Sender.__get_from_queue(self, wait=True)
            if response:
                # check data type
                log.info('SEND: {}'.format(response))
                try:
                    self.sender_socket.send(bytes(response, encoding='UTF-8'))
                except Exception as err:
                    log.error('SENDER: {}'.format(err))
                    self.system_callback({'ERROR': err})
                    self._back_up()
                else:
                    self.walkie_talkie_runner = True
                    _delta_on = time.time()
                    log.info('WALKIE-TALKIE: {}, _delta_on: {}'.format(self.walkie_talkie_runner, _delta_on))
            elif not self.running:
                self.system_callback({'ERROR': 'SOMEBODY STOP SENDER'})
                self._back_up()
            self.walkie_talkie(_delta_on)

    def walkie_talkie(self, _delta_on):
        while self.walkie_talkie_runner:
            sleep(0.05)
            if time.time() - _delta_on > 3:
                self.system_callback({'ERROR': 'LOST CONNECTION WITH SERVER'})
                self._back_up()
        Sender.CYCLE += 1

    @staticmethod
    def while_empty(self):
        log.info('RUNNING... CYCLE: {}'.format(Sender.CYCLE))
        while CommonQueue.CQ.empty() and self.running:
            sleep(0.01)

    @staticmethod
    def __get_from_queue(self, wait=False):
        if wait:
            Sender.while_empty(self)
        try:
            data = CommonQueue.CQ.get(block=False)
        except Exception as err:
            log.error(err)
            return False
        if data != 'SAVE':
            return data
        return False

    def _back_up(self):
        log.info('BACK-UP running...')
        self.walkie_talkie_runner = False
        self.running = False
        while not CommonQueue.CQ.empty():
            data = Sender.__get_from_queue(self)
            db.insert_into_db(self.db_cursor, time.time(), datetime.now(), data)
            db.commit_changes(self.db_conn)
        log.info('BACK-UP: ok')


def callback_data(response):
    log.info(response)


def callback_system(response):
    log.info(response)
    log.info('START WRITE TO LOCAL DB :)')


if __name__ == '__main__':
    _client = Client(host='10.8.0', port=777, auto=True, data_callback=callback_data, system_callback=callback_system)
    _client.start()

    while True:
        # sleep(15)
        for i in range(500):
            log.info('send to server: {}'.format(bytes('BREAK :) NUMBER: {}'.format(i), encoding='UTF-8')))
            CommonQueue.CQ.put('BREAK :) NUMBER: {}'.format(i), block=False)
            sleep(1)


