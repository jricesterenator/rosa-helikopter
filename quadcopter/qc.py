import time
import sys
import atexit

import serial
from serial.tools import list_ports

from ardrone import libardrone, mockardrone
import drone
from car.controls import *
from car import canbus

#DEV = '/dev/tty.OBDLinkMX-STN-SPP'
#BAUD = 500000

DEV = '/tmp/fake2'
BAUD = 9600
MOCK_DRONE = True

class CAN:
    def __init__(self, writer, canProcessor):
        self.writer = writer
        self.canProcessor = canProcessor

    def setup(self):
        self.writer.sendCommand('atl1') #\r\n line endings
        self.writer.sendCommand('ati')
        self.writer.sendCommand('ath1') #headers on
        self.writer.sendCommand('ats1') #include spaces
        self.writer.sendCommand('atal') #allow long messages
        self.writer.sendCommand('atsp6') #set to protocol 6, (CAN 11bit ID, 500kbaud)

    def startMonitor(self, senderIds):
        #Clear filters
        self.writer.sendCommand('stfcp') #clear pass filters
        self.writer.sendCommand('stfcb') #clear blocking filters
        self.writer.sendCommand('stfcfc') #clear flow control filters

        #Add filters
        for id in senderIds:
            self.writer.sendCommand('stfap %s,fff' % hex(id)[2:])

        self.writer.sendAsyncCommand('stm', self.canProcessor.processMessage)


class App:
    def __init__(self, drone, controls):
        self.drone = drone
        self.controls = controls

    def connectToCar(self, dev, baud):
        self.serial = serial.Serial(dev, baud)

        self.readerThread = canbus.ReaderThread(self.serial)
        self.readerThread.start()

        self.writer = canbus.Writer(self.serial, self.readerThread)

        self.canProcessor = ControlProcessor(self.controls)

        self.can = CAN(self.writer, self.canProcessor)
        self.can.setup()

    def startCarMonitor(self):
        senderIds = self.controls.activeSenders()
        self.can.startMonitor(senderIds)

    def listSerialPorts(self):
        ports = [p[0] for p in list_ports.comports()]

        print "Available serial ports:"
        for p in ports:
            print "  " + p

    def destroy(self):
        self.writer.destroy()

        print "Waiting for reader thread to die.."
        self.readerThread.kill()
        self.readerThread.join()
        print "Dead"

        self.serial.close()
        print "Serial connection closed"


def loadControls(drone):
    def when(*args):
        return c.when(*args)

    c = Controls()

    when('handbrake', eq(1)).then(drone.takeoff)
    when('handbrake', eq(0)).then(drone.land)

    when('neutral', any()).then(echo("Neutral"))
    when('ingear', any()).then(echo("In Gear"))
    when('brake', any()).then(echo("Brake"))

    return c


if __name__ == '__main__':
    app = None

    def shutdownHook():
        print "SHUTDOWN!"
        if app:
            app.destroy()
    atexit.register(shutdownHook)

    if MOCK_DRONE:
        d = drone.Drone(mockardrone.MockARDrone())
    else:
        d = drone.Drone(libardrone.ARDrone())


    app = App(d, loadControls(d))
    app.listSerialPorts()

    app.connectToCar(DEV, BAUD)
    app.startCarMonitor()

    while True:
        time.sleep(.001)





