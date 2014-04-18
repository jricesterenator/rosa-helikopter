import time
import atexit

import serial
from serial.tools import list_ports
from car.car import SimpleConnection, SimpleCar

from state_control import DroneStateControl, Not
from car.allcan import CANSerialConnection, CANCar
from ardrone import libardrone, mockardrone
from ardrone.myardrone import MyARDrone
from controls.mazda3_2010 import *

DEV_REAL = '/dev/tty.OBDLinkMX-STN-SPP'
BAUD_REAL = 500000

DEV_MOCK = '/tmp/fake2'
BAUD_MOCK = 9600


class Inputs:
    def __init__(self, controlProcessors, inputs):
        self.controlProcessors = controlProcessors
        self.inputs = inputs

    def c(self, name):
        val = self.controlProcessors[name].value.value
        if val is None:
            return 0
        return val

class MyInputs(Inputs):

    def __init__(self, car):
        Inputs.__init__(self, car.controlProcessors, self.load_inputs())

    def load_inputs(self):
        c = self.c #Convenience

        return {
            'emergency_button' : lambda : c('hazards'),

            'takeoff' : lambda : Not(c('handbrake')) and c('seatbelt'),
            'land' : lambda : c('handbrake'),
            'hover' : lambda : Not(c('seatbelt')),

            'strafe_active' : lambda : c('highbeams'), #If you have dedicated analog for this, set to True
            'strafe_speed' : lambda : abs(c('steering1')),
            'strafe_left' : lambda : c('steering1') < 0,
            'strafe_right' : lambda : c('steering1') >= 0,

            'rotate_active' : lambda : Not(c('highbeams')),
            'rotate_speed' : lambda : abs(c('steering1')),
            'rotate_left' : lambda : c('steering1') < 0,
            'rotate_right' : lambda  : c('steering1') >= 0,

            'straight_motion_active' : lambda : Not(c('neutral')),
            'straight_speed' : lambda : c('gas1'),
            'forward' : lambda : c('ingear') and Not(c('reverse')),
            'reverse' : lambda : c('reverse'),

            'vertical_motion_active' : lambda : c('neutral'),
            'vertical_speed' : lambda : self.vertical_speed(),
            'up' : lambda : not(c('brake') or c('left_blinker')), #not down
            'down' : lambda : c('brake') or c('left_blinker'),

            }

    def vertical_speed(self):
        c = self.c #convenience

        if self.inputs['up']():
            if c('right_blinker'):
                return .2
            else:
                return c('gas1')

        elif self.inputs['down']():
            if c('left_blinker'):
                return .2
            else:
                return c('gas1')


class App:
    def __init__(self, car, inputs, droneClass):
        self.car = car
        self.inputs = inputs
        self.drone = None

        self.droneClass = droneClass
        self.isTicking = False
        atexit.register(self.destroy)

    def start(self):
        if self.droneClass:
            self.drone = self.droneClass()
            print "[DEBUG] Connected to Drone"
        else:
            print "[DEBUG] No drone class selected. Not connecting to drone."

        self.car.connect()
        print "[DEBUG] Connected to Car"

        self.cs = DroneStateControl(self.inputs, self.drone)
        self.car.registerListener(self.cs.received_input)


    def startTicking(self):
        if self.drone:
            self.isTicking = True
            while self.isTicking:
                self.cs.tick()
                time.sleep(1)
        else:
            print "[WARNING] No drone connected, so not ticking drone states."
            while self.isTicking:
                time.sleep(.001)

    def destroy(self):
        print "---------------- SHUTDOWN ---------------- "
        self.isTicking = False

        if self.drone:
            self.drone.halt()

        self.car.disconnect()


def listSerialPorts():
    ports = [p[0] for p in list_ports.comports()]

    print "Available serial ports:"
    for p in ports:
        print "  " + p


if __name__ == '__main__':

    ##########################################################################
    ##########################################################################
    global DEBUG_ALL_CONTROLS
    DEBUG_ALL_CONTROLS=True

    print
    print "Mock or Real Drone?"
    print "1) Mock"
    print "2) Real"
    print "3) No drone"
    choice = raw_input("[none] : ")

    if choice == "1":
        print "Using mock drone"
        DRONE_CLASS = mockardrone.MockARDrone
    elif choice == "2":
        print "Using real drone"
        DRONE_CLASS = MyARDrone
    else:
        print "No drone connected."
        DRONE_CLASS = None


    print
    print "What type of car connection?"
    print "1) Simple Car, with simple messages (<input>,<value>)"
    print "2) Simple Car, with CAN messages"
    print "3) Serial Car"
    choice = raw_input("[Simple car, simple msgs] : ")

    if choice == "2":
        print "Using Simple Car, with CAN messages"
        """
            Use this to debug the real CAN controls and send real can messages without
            connecting to the car. Manually send messages with CAR.processMessage(<CAN Message>).
            Also, SimpleConnection() will prompt you to manually enter messages on the command line.
        """
        CONTROLS = MAZDA_3_2010_CAN_CONTROLS
        CONNECTION = SimpleConnection()
        CAR = CANCar(CONTROLS, CONNECTION)

    elif choice == "3":

        print
        print "Serial params?"
        print "1) %s @%skbps" % (DEV_REAL, BAUD_REAL)
        print "2) %s @%skbps" % (DEV_MOCK, BAUD_MOCK)
        print "3) Custom / List Ports"
        choice = raw_input("[%s @%skbps] : " % (DEV_REAL, BAUD_REAL))

        if choice == "2":
            DEV = DEV_MOCK
            BAUD = BAUD_MOCK

        elif choice == "3":
            listSerialPorts()

            DEV = ""
            while not len(DEV.strip()):
                DEV = raw_input("Device: ")
            BAUD = ""
            while not len(BAUD.strip()):
                BAUD = raw_input("Baud: ")

        else:
            DEV = DEV_REAL
            BAUD = BAUD_REAL

        print "Using Serial Car. (%s @%skbps)" % (DEV, BAUD)
        print "Connecting..."
        """
            Use this to actually connect over serial and read CAN messages.
            Pass the real DEVice to get the real car. Or pass a loopback DEVice
            and connect to a mock car implementation running elsewhere.
        """
        CONTROLS = MAZDA_3_2010_CAN_CONTROLS
        CONNECTION = CANSerialConnection(serial.Serial(DEV, BAUD), debugAllControls=True)
        CAR = CANCar(CONTROLS, CONNECTION)

    else:
        print "Using Simple Car, with simple messages (<input>,<value>)"
        """
            Use this to fully simulate the car. Useful when testing the drone because you
            don't care about the specific car messages going through. Can send messages
            via CAR.processMessage(<simple message>) or manually enter messages on the command line.
            Examples:
            handbrake,1  #set the handbrake
            seatbelt,1   #set the seatbelt
            gas1,.7      #set the gas pedal to 70%
        """
        CONTROLS = MAZDA_3_2010_SIMPLE_CONTROLS
        CONNECTION = SimpleConnection()
        CAR = SimpleCar(CONTROLS, CONNECTION)


    ##########################################################################
    ##########################################################################

    INPUTS = MyInputs(CAR)

    app = App(CAR, INPUTS, DRONE_CLASS)
    app.start()
    app.startTicking()
