from ardrone import libardrone, mockardrone
from car.controls import *
from car.canbus import *
from car.car import *
import time
import atexit
from qc import DroneControlledByCar
from quadcopter.controls.mazda3_2010 import MAZDA_3_2010_CONTROLS

CONTROLS = MAZDA_3_2010_CONTROLS

def loadControls(drone):
    when(CONTROLS['handbrake'], eq(1)).then(drone.takeoff)
    when(CONTROLS['handbrake'], eq(0)).then(drone.land)

    when(CONTROLS['neutral'], any()).then(echo("Neutral"))
    when(CONTROLS['ingear'], any()).then(echo("In Gear"))
    when(CONTROLS['brake'], any()).then(echo("Brake"))

    when(CONTROLS['steering1'], any()).then(drone.roll)


def canTest(d):
    car = CANCar(CONTROLS, DummyCANBus(None, None))

    print "Sleeping 3, then take off"
    time.sleep(3)

    #Handbrake on, takeoff
    print "Takeoff"
    car.processMessage("39E 00 00 20 00 00 00 00 00")
    time.sleep(3)
    #        d.trim()


    cmds = [
        (5, "082 4B FC 00 00 FF 92 00 00", "0 degrees"), #0 deg
        (2, "082 4B FC 00 32 FF 92 00 00", "10 degrees"), #5 deg
        (5, "082 4B FC 00 00 FF 92 00 00", "0 degrees"), #0 deg
        (2, "082 4B FC FF CE FF 92 00 00", "-10 degrees"), #-5 deg
        (5, "082 4B FC 00 00 FF 92 00 00", "0 degrees"), #0 deg

    ]

    for times,command,msg in cmds:
        print "Executing", msg, command, times, "times"

        for i in range(times):
            print "Executing", msg, command, "-", i
            car.processMessage(command)
            time.sleep(1)

    d.land()
    d.halt()

def simpleTest(d):
    car = SimpleCar(CONTROLS)

    car.processMessage((CONTROLS['handbrake'], 1))
    car.processMessage((CONTROLS['steering1'], 0))
    car.processMessage((CONTROLS['steering1'], -5))
    car.processMessage((CONTROLS['steering1'], 0))
    car.processMessage((CONTROLS['steering1'], 5))
    car.processMessage((CONTROLS['steering1'], 0))
    car.processMessage((CONTROLS['handbrake'], 0))





if __name__ == '__main__':
    d = None
    def shutdownHook():
        print "SHUTDOWN!"
        if d:
            d.land()
            d.halt()
    atexit.register(shutdownHook)

    d = DroneControlledByCar(mockardrone.MockARDrone())
#    d = drone.Drone(libardrone.ARDrone())
    loadControls(d)

    print "1) Launch"
    print "2) Land"
    res = raw_input("What to do?")
    if res == "1":

#        canTest(d)
        simpleTest(d)

    else:
        d.land()
