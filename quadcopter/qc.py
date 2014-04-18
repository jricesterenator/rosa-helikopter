import time
import atexit

import serial

from state_control import DroneStateControl, Not
from car.canbus import *
from car.car import *
from ardrone import libardrone, mockardrone, myardrone
from controls.mazda3_2010 import *

class Inputs:
    def __init__(self, controls, inputs):
        self.controls = controls
        self.inputs = inputs

    def c(self, name):
        val = self.controls[name].value.value
        if val is None:
            return 0
        return val

class MyInputs(Inputs):

    def __init__(self, controls):
        Inputs.__init__(self, controls, self.load_inputs())

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
    def __init__(self):
        self.drone = None
        self.car = None
        self.isTicking = False
        atexit.register(self.destroy)

    def start(self):
        self.drone = DRONE()
        print "[DEBUG] Connected to Drone"

        car = CAR_CONNECTION.connectToCar(CAR)
        print "[DEBUG] Connected to Car"

        self.cs = DroneStateControl(INPUTS, self.drone)

        #Register all car controls with the listener.
        for control in car.getControlsList():
            control.registerListener(self.cs.received_input)

    def startTicking(self):
        self.isTicking = True
        while self.isTicking:
            self.cs.tick()
            time.sleep(1)

    def destroy(self):
        print "---------------- SHUTDOWN ---------------- "
        self.isTicking = False

        if self.drone:
            self.drone.halt()

        CAR_CONNECTION.destroy()



if __name__ == '__main__':


    ##########################################################################
    ##########################################################################
    global DEBUG_ALL_CONTROLS
    DEBUG_ALL_CONTROLS=True


##CAN Real setup - Real drone
    DEV = '/dev/tty.OBDLinkMX-STN-SPP'
    BAUD = 500000
#
#    CAR_CONNECTION = CarConnectors.CANSerialConnection(serial.Serial(DEV, BAUD))
#    CAR = Cars.CANCar(MAZDA_3_2010_CONTROLS)
#    INPUTS = MyInputs(CAR.controls)
#    DRONE = mockardrone.MockARDrone

##CAN mock setup - Mock drone
#    DEV = '/tmp/fake2'
#    BAUD = 9600
#
#    CAR_CONNECTION = CarConnectors.CANSerialConnection(serial.Serial(DEV, BAUD), debugAllControls=True)
#    CAR = Cars.CANCar(MAZDA_3_2010_CONTROLS)
#    INPUTS = MyInputs(CAR.controls)
#    DRONE = mockardrone.MockARDrone

#CAN Mock - REAL DRONE
#    CAR_CONNECTION = CarConnectors.CANSerialConnection(serial.Serial(DEV, BAUD))
#    CAR = Cars.CANCar(MAZDA_3_2010_CONTROLS)
#    INPUTS = MyInputs(CAR.controls)
#    DRONE = libardrone.ARDrone


#Test Setup - In-memory CAN testing
#    CAR_CONNECTION = CarConnectors.BasicConnection()
#    CAR = Cars.CANCar(MAZDA_3_2010_CONTROLS)
#    INPUTS = MyInputs(CAR.controls)
#    DRONE = mockardrone.MockARDrone




    CAR_CONNECTION = CarConnectors.CANSerialConnection(serial.Serial(DEV, BAUD), debugAllControls=True)
#    CAR_CONNECTION = CarConnectors.BasicConnection()
    CAR = Cars.CANCar(MAZDA_3_2010_CONTROLS)
#    CAR = Cars.SimpleCar(MAZDA_3_2010_GENERIC_CONTROLS)
    INPUTS = MyInputs(CAR.controlProcessors)
#    DRONE = myardrone.MyARDrone
    DRONE = mockardrone.MockARDrone



    #Test Setup - Fake car, fake drone
#    CAR_CONNECTION = CarConnectors.BasicConnection()
#    CAR = Cars.SimpleCar(MAZDA_3_2010_GENERIC_CONTROLS)
#    INPUTS = MyInputs(CAR.controls)
    ##########################################################################
    ##########################################################################

    app = App()
    app.start()

    while True:
        time.sleep(.001)
#    app.startTicking()






#
#    CAR.processMessage("999 00 00 00 00 00 00 00 01") #seatbelt
##    CAR.processMessage("998 00 00 00 00 00 00 00 01") #hazards
#    app.cs.tick()
#
#    CAR.processMessage("39E 00 00 20 00 00 00 00 00") #handbrake active
#    app.cs.tick()
#
#    CAR.processMessage("39E 00 00 00 00 00 00 00 00") #handbrake OFF
#    app.cs.tick()

    #Take off


#    #Take off
#    CAR.processMessage("seatbelt,1")
#    CAR.processMessage("handbrake,0")
#    app.cs.tick()
#
#    time.sleep(5)
#
#    #Land
#    CAR.processMessage("handbrake,1")
#    app.cs.tick()
#
#    time.sleep(5)



#
#    CAR.processMessage("neutral,1"); CAR.processMessage("ingear,0")
#    app.cs.tick()
#
#    CAR.processMessage("gas1,1")#should move up at 1
#    app.cs.tick()
#
#    CAR.processMessage("neutral,0")
#    CAR.processMessage("ingear,1")#out of vertical mode
#    app.cs.tick()
#
#    CAR.processMessage("gas1,.5")#should move fwd at .5
#    app.cs.tick()
#
#    CAR.processMessage("steering1,-.5")#should move fwd at .5
#    app.cs.tick()
#    CAR.processMessage("steering1,.5")#should move fwd at .5
#    app.cs.tick()


