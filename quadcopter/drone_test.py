from ardrone import libardrone, mockardrone
import drone
from car.controls import *
from car import canbus
import time
import atexit

def loadControls(drone):
    def when(*args):
        return c.when(*args)

    c = Controls()

    when('handbrake', eq(1)).then(drone.takeoff)
    when('handbrake', eq(0)).then(drone.land)

    when('neutral', any()).then(echo("Neutral"))
    when('ingear', any()).then(echo("In Gear"))
    when('brake', any()).then(echo("Brake"))

    when('steering1', any()).then(drone.roll)

    return c

if __name__ == '__main__':
    d = None
    def shutdownHook():
        print "SHUTDOWN!"
        if d:
            d.land()
            d.halt()
    atexit.register(shutdownHook)

#    d = drone.Drone(mockardrone.MockARDrone())
    d = drone.Drone(libardrone.ARDrone())

    print "1) Launch"
    print "2) Land"
    res = raw_input("What to do?")
    if res == "1":
        c = loadControls(d)

        processor = ControlProcessor(c)


        print "Sleeping 3, then take off"
        time.sleep(3)

        #Handbrake on, takeoff
        print "Takeoff"
        processor.processMessage("39E 00 00 20 00 00 00 00 00")
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
                processor.processMessage(command)
                time.sleep(1)

        d.land()
        d.halt()

    else:
        d.land()
