import time
import atexit

import serial
from serial.tools import list_ports

from quadcopter.car.canbus import *
from car.car import *
from ardrone import libardrone, mockardrone
from quadcopter.controls.mazda3_2010 import *

#DEV = '/dev/tty.OBDLinkMX-STN-SPP'
#BAUD = 500000

DEV = '/tmp/fake2'
BAUD = 9600
MOCK_DRONE = True
CONTROLS = MAZDA_3_2010_CONTROLS

class CarThatControlsDrone:
    def __init__(self, car, drone):
        self.car = car
        self.drone = drone
        controls = self.car.controlMap

        when(controls['handbrake'], eq(1)).then(drone.takeoff)
        when(controls['handbrake'], eq(0)).then(drone.land)

        when(controls['neutral'], any()).then(echo("Neutral"))
        when(controls['ingear'], any()).then(echo("In Gear"))
        when(controls['brake'], any()).then(echo("Brake"))

        when(controls['steering1'], any()).then(drone.roll)

    def getSenders(self):
        return self.car.getSenders()

    def getControls(self):
        return self.car.getControls()

    def processMessage(self, m):
        self.car.processMessage(m)


class DroneControlledByCar:
    def __init__(self, drone):
        self.drone = drone

    def reset(self, value=None):
        self.drone.reset()

    def trim(self, value=None):
        self.drone.trim()

    def takeoff(self, value=None):
        print "Take Off!"
        self.drone.takeoff()

    def land(self, value=None):
        print "Land!"
        self.drone.land()

    def halt(self, value=None):
        self.drone.halt()

    """Values are -530 degrees to +530 degrees"""
    def roll(self, value):
        maxval = 45
        if value > maxval:
            value = maxval
        elif value < -maxval:
            value = -maxval


        #Within this window, call it TDC. Hover the drone.
        if -2 <= value <= 2:
            print "Hovering"
            self.drone.hover()
            return
        else:
            speed = abs(value/float(maxval))
            print "New speed (%s deg): %s" % (value, speed)

            self.drone.set_speed(speed)
            if value < 0:
                print "Moving left"
                self.drone.move_left()
            else:
                print "Moving right"
                self.drone.move_right()


class App:
    def __init__(self):
        self.drone = None
        self.quadCar = None
        self.serial = None
        self.canMonitor = None
        atexit.register(self._shutdownHook)

    def _shutdownHook(self):
        print "SHUTDOWN!"
        self.destroy()

    def start(self, droneClass):
        self._connectToDrone(droneClass)
        self._connectToCar(DEV, BAUD)

    def _connectToDrone(self, droneClass):
        self.drone = DroneControlledByCar(droneClass())
        print "Connected to drone."

    def _connectToCar(self, dev, baud):
        self.quadCar = CarThatControlsDrone(CANCar(CONTROLS), self.drone)

        self.serial = serial.Serial(dev, baud)
        self.canMonitor = CANBusMonitor(CANBus(self.serial))
        self.canMonitor.setup()
        self.canMonitor.startCANMonitor(self.quadCar.getSenders(), self.quadCar.processMessage)

    def listSerialPorts(self):
        ports = [p[0] for p in list_ports.comports()]

        print "Available serial ports:"
        for p in ports:
            print "  " + p

    def destroy(self):
        if self.drone:
            self.drone.halt()

        if self.canMonitor:
            self.canMonitor.destroy()

        if self.serial:
            self.serial.close()
            print "Serial connection closed"


if __name__ == '__main__':

    if MOCK_DRONE:
        d = mockardrone.MockARDrone
    else:
        d = libardrone.ARDrone

    app = App()
    app.listSerialPorts()
    app.start(d)

    raw_input("Press ENTER to force land and quit.")
    app.drone.land()
    app.drone.halt()

    app.destroy()





