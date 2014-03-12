import time
import atexit

import serial
from serial.tools import list_ports

from car.canbus import *
from car.car import *
from ardrone import libardrone, mockardrone
from controls.mazda3_2010 import *

DEV = '/dev/tty.OBDLinkMX-STN-SPP'
BAUD = 500000

CONTROLS = MAZDA_3_2010_CONTROLS

class App:

    def _connectToCar(self, dev, baud):
        self.serial = serial.Serial(dev, baud)
        self.bus = CANBus(self.serial)

    def listSerialPorts(self):
        ports = [p[0] for p in list_ports.comports()]

        print "Available serial ports:"
        for p in ports:
            print "  " + p


if __name__ == '__main__':
    a = App()
    a.listSerialPorts()
    a._connectToCar(DEV, BAUD)


    #    res =  a.bus.sendCommand('atl1')
#    print "ATL1 OUTPUT", res
#
#    res = a.bus.sendCommand("ati")
#    print "ATI OUTPUT", res

    def callback(m):
        print "####", m

    monitor = CANBusMonitor(a.bus)


    def shutdownHook(self):
        print "SHUTDOWN!"
        monitor.stopCANMonitor()
        a.serial.close()
    atexit.register(shutdownHook)



    monitor.setup()
    monitor.startCANMonitor([0x39E], callback)

    while True:
        time.sleep(1)

