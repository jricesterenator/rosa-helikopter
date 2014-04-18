import serial
import time
import sys
import threading
from serial.tools import list_ports

from ardrone import libardrone, mockardrone
import drone

from obdii import obdii
from obdii.controls import *

DEV = '/dev/tty.OBDLinkMX-STN-SPP'
BAUD = 500000


def listSerialPorts():
    ports = [p[0] for p in list_ports.comports()]

    print "Available serial ports:"
    for p in ports:
        print "  " + p

if __name__ == '__main__':
    print "MENU"
    print "1) Real Drone"
    print "2) Mock Drone"
    print "3) List Serial Ports"

    choice = raw_input(":: ")

    if choice == "1":
        drone = drone.Drone(libardrone.ARDrone())

#        q = obdii.QuadObdii()
#        run(q)

    elif choice == "2":
        drone = drone.Drone(mockardrone.MockARDrone())

    elif choice == "3":
        listSerialPorts()
        sys.exit(0)

    else:
        print "Invalid Choice"



    #Start stuff up

    controls = [

        Control(HANDBRAKE,
            [
                ValueListener(1, drone.takeoff).onValue,
                ValueListener(0, drone.land).onValue
            ])

    ]

    senderIds = set([c.controlDef.sender for c in controls])


    can = obdii.CANBus(DEV, BAUD)
    can.init()

    can.startMonitor(senderIds)




#    can = can.CANProcessor(controls)
#
#    raw_input("Press enter to set handbrake")
#    can.processMessages(['39E 00 00 20 00 00 00 00 00'])
#
#    raw_input("Press enter to UNset handbrake")
#    can.processMessages(['39E 00 00 00 00 00 00 00 00'])




