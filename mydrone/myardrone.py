from libardrone.libardrone import at_pcmd, at_ref
import time

##JRTODO: how to detect when taken off, etc

LEFT_RIGHT = 0
FRONT_BACK = 1
VERTICAL = 2
ANGULAR = 3

class MyARDrone:
    def __init__(self, drone):
        self.drone = drone
        self.speeds = [0, 0, 0, 0] #lr, fb, vv, va

        #JRTODO wait for connection somehow
        self.clearEmergency()

    def get_battery(self):
        return self.drone.navdata[0]['battery']

    def isHD(self):
        return self.drone.hd

    def _move(self):
#        print "Setting speeds:", self.speeds
        self.drone.at(at_pcmd, True,
            self.speeds[LEFT_RIGHT],
            self.speeds[FRONT_BACK],
            self.speeds[VERTICAL],
            self.speeds[ANGULAR])

    def move_left(self, speed):
        self.speeds[LEFT_RIGHT] = -speed
        self._move()

    def move_right(self, speed):
        self.speeds[LEFT_RIGHT] = speed
        self._move()

    def move_up(self, speed):
        self.speeds[VERTICAL] = speed
        self._move()

    def move_down(self, speed):
        self.speeds[VERTICAL] = -speed
        self._move()

    def move_forward(self, speed):
        self.speeds[FRONT_BACK] = -speed
        self._move()

    def move_backward(self, speed):
        self.speeds[FRONT_BACK] = speed
        self._move()

    def turn_left(self, speed):
        self.speeds[ANGULAR] = -speed
        self._move()

    def turn_right(self, speed):
        self.speeds[ANGULAR] = speed
        self._move()

    def halt(self):
        print "Halting drone communications."

    """
        Returns if we have a connection to the drone. navdata will be populated
        if we do, else not.
    """
    def connected(self):
        return self.drone.navdata

    def landed(self):
#        print "FLIGHT STATUS:",self.drone.navdata['drone_state']['fly_mask']
        return not self.drone.navdata['drone_state']['fly_mask']

    def clearEmergency(self):
        #JRTODO: for whatever reason, the drone emergency thing is backwards. check it out
        self.drone.at(at_ref, False, True)
        time.sleep(1)

    def takeoff(self):
        print "Taking off..."
        self.speeds = [0,0,0,0]
        self._move()
        self.drone.takeoff()

    def land(self):
        print "Landing..."
        self.speeds = [0,0,0,0]
        self._move()
        self.drone.land()

    def reset(self):
        print "Resetting..."
        self.drone.reset()

    def hover(self):
        self.drone.hover()

    def get_image(self):
        return self.drone.get_image()