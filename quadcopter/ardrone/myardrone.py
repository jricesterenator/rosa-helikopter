from libardrone import ARDrone, at_pcmd

##JRTODO: how to detect when taken off, etc

LEFT_RIGHT = 0
FRONT_BACK = 1
VERTICAL = 2
ANGULAR = 3

class MyARDrone(ARDrone):

    def __init__(self, drone):
        ARDrone.__init__(self)
        self.speeds = [0, 0, 0, 0] #lr, fb, vv, va

    def _move(self):
        print "MOVE:", self.speeds
        self.at(at_pcmd, True,
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

    def land(self):
        print "JRTODO: Current fly state:", self.navdata['drone_state']['fly_mask']

        self.speeds = [0,0,0,0]
        self._move()
        ARDrone.land(self)

        import time
        time.sleep(5)#JRTODO
        print "JRTODO: Current fly state:", self.navdata['drone_state']['fly_mask']
