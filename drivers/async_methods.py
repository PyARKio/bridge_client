# -- coding: utf-8 --
from __future__ import unicode_literals
import asyncio
import socket
import threading
import queue
from time import sleep
import time


port = 777
rtt = None
find_q = queue.Queue()


async def call_url(host):
    print('Starting {}'.format(host))
    print('Connecting to {}:{} ...'.format(host, port))
    _connecting = True
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.setblocking(False)
    mySocket.settimeout(2)

    # while _connecting:
    try:
        mySocket.connect((host, port))
    except Exception as err:
        # _connecting = False
        print('HOST: {} ERROR: {}'.format(host, err))
    else:
        # _connecting = False
        print('Connect :) HOST: {}'.format(host))


futures = [call_url('10.8.0.{}'.format(i)) for i in range(255)]
# mySocket.connect(('10.8.0.5', port))
point = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(futures))
print(time.time() - point)


# def _init_client():
#     log.info('init client...')
#     try:
#         _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     except Exception as err:
#         log.error(err)
#         return False
#     else:
#         _socket.setblocking(False)
#         _socket.settimeout(1)
#     log.info('STATUS: OK')
#     return _socket
#
#
# def search_ip(host):
#     global rtt
#     print('Connecting to {}:{} ...'.format(host, port))
#     _socket = _init_client()
#
#     try:
#         _socket.connect((host, port))
#     except Exception as err:
#         print('HOST: {} ERROR: {}'.format(host, err))
#         find_q.put(False)
#     else:
#         print('Connect :) HOST: {}'.format(host))
#         try:
#             data = _socket.recv(1024).decode()
#         except Exception as err:
#             print('HOST: {} ERROR: {}'.format(host, err))
#             find_q.put(False)
#         else:
#             if data == 'check\r\n':
#                 _socket.send(bytes('check ok', encoding='UTF-8'))
#                 rtt = _socket
#                 find_q.put(rtt)
#             else:
#                 find_q.put(False)
#
#
# point = time.time()
# for f in range(0, 256, 4):
#     for i in range(f, f+4):
#         ip = '10.8.0.{}'.format(i)
#         # ip = '192.168.1.{}'.format(i)
#         assistant_start = threading.Thread(target=search_ip, args=(ip, ))
#         assistant_start.start()
#
#     index = 0
#     while index < 4:
#         find_q.get()
#         index += 1
#
#     if rtt:
#         print('BREAK')
#         break
#
# print(time.time() - point)
# print(rtt)
# for i in range(5):
#     rtt.send(bytes('BREAK :)', encoding='UTF-8'))
#     sleep(5)
# rtt = None
#
#
# while True:
#     sleep(100)



