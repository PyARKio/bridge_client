# -- coding: utf-8 --
from __future__ import unicode_literals
import os
import socket
from time import sleep
import json


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


host = '192.168.0.49'
port = 4040

_connecting = True
mySocket = socket.socket()
print('Connecting...')
while _connecting:
    try:
        mySocket.connect((host, port))
    except Exception as err:
        print(err)
        sleep(30)
    else:
        _connecting = False
        print('Connect :)')

while True:
    message = json.dumps({'manufacturer': get_manufacturer(),
                          'model_name': get_model_name(),
                          'serial_number': get_serial_number(),
                          'type': get_type(),
                          'volt': get_volt(),
                          'capacity': get_capacity(),
                          'current': get_current(),
                          'status': get_status(),
                          'technology': get_technology(),
                          'temp': get_temp(),
                          'present': get_present(),
                          'health': get_health(),
                          'charge_control_limit': get_charge_control_limit(),
                          'charge_control_limit_max': get_charge_control_limit_max(),
                          'charge_control_start_threshold': get_charge_control_start_threshold(),
                          'charge_control_end_threshold': get_charge_control_end_threshold(),
                          'charge_type': get_charge_type()
                          })

    mySocket.send(message)
    sleep(1.5)