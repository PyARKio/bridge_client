# -- coding: utf-8 --
from __future__ import unicode_literals
import os
import socket
from time import sleep
import json
from log_settings import log


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


# https://www.kernel.org/doc/Documentation/ABI/testing/sysfs-class-power

# ===== General Properties =====
manufacturer_path = '/sys/class/power_supply/battery/manufacturer'
model_name_path = '/sys/class/power_supply/battery/model_name'
serial_number_path = '/sys/class/power_supply/battery/serial_number'
type_path = '/sys/class/power_supply/battery/type'
# ===== Battery Properties =====
status_path = '/sys/class/power_supply/battery/status'
capacity_path = '/sys/class/power_supply/battery/capacity'
volt_path = '/sys/class/power_supply/battery/voltage_now'
current_path = '/sys/class/power_supply/battery/current_now'
technology_path = '/sys/class/power_supply/battery/technology'
temp_path = '/sys/class/power_supply/battery/temp'
present_path = '/sys/class/power_supply/battery/present'
health_path = '/sys/class/power_supply/battery/health'
charge_control_limit_path = '/sys/class/power_supply/battery/charge_control_limit'
charge_control_limit_max_path = '/sys/class/power_supply/battery/charge_control_limit_max'
charge_control_start_threshold_path = '/sys/class/power_supply/battery/charge_control_start_threshold'
charge_control_end_threshold_path = '/sys/class/power_supply/battery/charge_control_end_threshold'
charge_type_path = '/sys/class/power_supply/battery/charge_type'


# ===== General Properties =====
def get_manufacturer():
    """
    What:		/sys/class/power_supply/<supply_name>/manufacturer
    Date:		May 2007
    Contact:	linux-pm@vger.kernel.org
    Description:
            Reports the name of the device manufacturer.

            Access: Read
            Valid values: Represented as string
    :return:
    """
    response = 0
    if os.path.exists(manufacturer_path):
        with open(manufacturer_path, 'r') as f:
            response = f.readline().rstrip()
    return response


def get_model_name():
    """
    What:		/sys/class/power_supply/<supply_name>/model_name
    Date:		May 2007
    Contact:	linux-pm@vger.kernel.org
    Description:
            Reports the name of the device model.

            Access: Read
            Valid values: Represented as string
    :return:
    """
    response = 0
    if os.path.exists(model_name_path):
        with open(model_name_path, 'r') as f:
            response = f.readline().rstrip()
    return response


def get_serial_number():
    """
    What:		/sys/class/power_supply/<supply_name>/serial_number
    Date:		January 2008
    Contact:	linux-pm@vger.kernel.org
    Description:
            Reports the serial number of the device.

            Access: Read
            Valid values: Represented as string
    :return:
    """
    response = 0
    if os.path.exists(serial_number_path):
        with open(serial_number_path, 'r') as f:
            response = f.readline().rstrip()
    return response


def get_type():
    """
    What:		/sys/class/power_supply/<supply_name>/type
    Date:		May 2010
    Contact:	linux-pm@vger.kernel.org
    Description:
            Describes the main type of the supply.

            Access: Read
            Valid values: "Battery", "UPS", "Mains", "USB"
    :return:
    """
    response = 0
    if os.path.exists(type_path):
        with open(type_path, 'r') as f:
            response = f.readline().rstrip()
    return response


# ===== Battery Properties =====

def get_capacity():
    """
    What:		/sys/class/power_supply/<supply_name>/capacity
    Date:		May 2007
    Contact:	linux-pm@vger.kernel.org
    Description:
            Fine grain representation of battery capacity.
            Access: Read
            Valid values: 0 - 100 (percent)
    """
    response = 0
    if os.path.exists(capacity_path):
        with open(capacity_path, 'r') as f:
            response = f.readline().rstrip()
    return response


def get_volt():
    """
    What:		/sys/class/power_supply/<supply_name>/voltage_now,
    Date:		May 2007
    Contact:	linux-pm@vger.kernel.org
    Description:
            Reports an instant, single VBAT voltage reading for the battery.
            This value is not averaged/smoothed.

            Access: Read
            Valid values: Represented in microvolts
    """
    response = 0
    if os.path.exists(volt_path):
        with open(volt_path, 'r') as f:
          response = f.readline().rstrip()
          response = float(response) / 1000000.0
    return response


def get_current():
    """
    What:		/sys/class/power_supply/<supply_name>/current_now
    Date:		May 2007
    Contact:	linux-pm@vger.kernel.org
    Description:
            Reports an instant, single IBAT current reading for the battery.
            This value is not averaged/smoothed.

            Access: Read
            Valid values: Represented in microamps
    """
    response = 0
    if os.path.exists(current_path):
        with open(current_path, 'r') as f:
            response = f.readline().rstrip()
            response = float(response) / 1000.0
    return response


def get_status():
    """
    What:		/sys/class/power_supply/<supply_name>/status
    Date:		May 2007
    Contact:	linux-pm@vger.kernel.org
    Description:
            Represents the charging status of the battery. Normally this
            is read-only reporting although for some supplies this can be
            used to enable/disable charging to the battery.

            Access: Read, Write
            Valid values: "Unknown", "Charging", "Discharging",
                    "Not charging", "Full"
    """
    with open(status_path) as f:
        response = f.readline().rstrip()
    return response


def get_technology():
    """
    What:		/sys/class/power_supply/<supply_name>/technology
    Date:		May 2007
    Contact:	linux-pm@vger.kernel.org
    Description:
            Describes the battery technology supported by the supply.

            Access: Read
            Valid values: "Unknown", "NiMH", "Li-ion", "Li-poly", "LiFe",
                    "NiCd", "LiMn"
    """
    response = 0
    if os.path.exists(technology_path):
        with open(technology_path, 'r') as f:
            response = f.readline().rstrip()
    return response


def get_temp():
    """
    What:		/sys/class/power_supply/<supply_name>/temp
    Date:		May 2007
    Contact:	linux-pm@vger.kernel.org
    Description:
            Reports the current TBAT battery temperature reading.

            Access: Read
            Valid values: Represented in 1/10 Degrees Celsius
    """
    response = 0
    if os.path.exists(temp_path):
        with open(temp_path, 'r') as f:
            response = f.readline().rstrip()
            response = float(response) / 10.0
    return response


def get_present():
    """
    What:		/sys/class/power_supply/<supply_name>/present
    Date:		May 2007
    Contact:	linux-pm@vger.kernel.org
    Description:
            Reports whether a battery is present or not in the system.

            Access: Read
            Valid values:
                0: Absent
                1: Present
    """
    response = 0
    if os.path.exists(present_path):
        with open(present_path, 'r') as f:
            response = f.readline().rstrip()
    return response


def get_health():
    """
    What:		/sys/class/power_supply/<supply_name>/health
    Date:		May 2007
    Contact:	linux-pm@vger.kernel.org
    Description:
            Reports the health of the battery or battery side of charger
            functionality.

            Access: Read
            Valid values: "Unknown", "Good", "Overheat", "Dead",
                        "Over voltage", "Unspecified failure", "Cold",
                        "Watchdog timer expire", "Safety timer expire"
    """
    response = 0
    if os.path.exists(health_path):
        with open(health_path, 'r') as f:
            response = f.readline().rstrip()
    return response


def get_charge_control_limit():
    """
    What:		/sys/class/power_supply/<supply_name>/charge_control_limit
    Date:		Oct 2012
    Contact:	linux-pm@vger.kernel.org
    Description:
        Maximum allowable charging current. Used for charge rate
        throttling for thermal cooling or improving battery health.

        Access: Read, Write
        Valid values: Represented in microamps
    """
    response = 0
    if os.path.exists(charge_control_limit_path):
        with open(charge_control_limit_path, 'r') as f:
            response = f.readline().rstrip()
            response = float(response) / 1000.0
    return response


def get_charge_control_limit_max():
    """
    What:		/sys/class/power_supply/<supply_name>/charge_control_limit_max
    Date:		Oct 2012
    Contact:	linux-pm@vger.kernel.org
    Description:
        Maximum legal value for the charge_control_limit property.

        Access: Read
        Valid values: Represented in microamps
    """
    response = 0
    if os.path.exists(charge_control_limit_max_path):
        with open(charge_control_limit_max_path, 'r') as f:
            response = f.readline().rstrip()
            response = float(response) / 1000.0
    return response


def get_charge_control_start_threshold():
    """
    What:		/sys/class/power_supply/<supply_name>/charge_control_start_threshold
    Date:		April 2019
    Contact:	linux-pm@vger.kernel.org
    Description:
        Represents a battery percentage level, below which charging will
        begin.

        Access: Read, Write
        Valid values: 0 - 100 (percent)
    """
    response = 0
    if os.path.exists(charge_control_start_threshold_path):
        with open(charge_control_start_threshold_path, 'r') as f:
            response = f.readline().rstrip()
    return response


def get_charge_control_end_threshold():
    """
    What:		/sys/class/power_supply/<supply_name>/charge_control_end_threshold
    Date:		April 2019
    Contact:	linux-pm@vger.kernel.org
    Description:
        Represents a battery percentage level, above which charging will
        stop.

        Access: Read, Write
        Valid values: 0 - 100 (percent)
    """
    response = 0
    if os.path.exists(charge_control_end_threshold_path):
        with open(charge_control_end_threshold_path, 'r') as f:
            response = f.readline().rstrip()
    return response


def get_charge_type():
    """
    What:		/sys/class/power_supply/<supply_name>/charge_type
    Date:		July 2009
    Contact:	linux-pm@vger.kernel.org
    Description:
        Represents the type of charging currently being applied to the
        battery. "Trickle", "Fast", and "Standard" all mean different
        charging speeds. "Adaptive" means that the charger uses some
        algorithm to adjust the charge rate dynamically, without
        any user configuration required. "Custom" means that the charger
        uses the charge_control_* properties as configuration for some
        different algorithm.

        Access: Read, Write
        Valid values: "Unknown", "N/A", "Trickle", "Fast", "Standard",
                "Adaptive", "Custom"
    """
    response = None
    if os.path.exists(charge_type_path):
        with open(charge_type_path, 'r') as f:
            response = f.readline().rstrip()
    return response


if __name__ == '__main__':
    # host = '192.168.1.120'
    host = '10.8.0.5'
    port = 1717

    _connecting = True
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.setblocking(False)
    mySocket.settimeout(1)
    print('Connecting to {}:{} ...'.format(host, port))
    while _connecting:
        try:
            mySocket.connect((host, port))
        except Exception as err:
            print(err)
            sleep(30)
        else:
            _connecting = False
            print('Connect :)')
    try:
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
            log.info(message)
            mySocket.send(message)
            sleep(1.5)
    except Exception as err:
        log.error(err)


