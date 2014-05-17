LEFT_RIGHT = 0
FRONT_BACK = 1
VERTICAL = 2
ANGULAR = 3

#JRTODO: make this not a copy

class MockARDrone:

    def __init__(self, hd=False):
        self.speeds = [0, 0, 0, 0] #lr, fb, vv, va

        self.navdata = {}
        self.navdata['drone_state'] = {}
        self.navdata['drone_state']['fly_mask'] = 0

        self.hd = hd

    def get_image(self):
        return None

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

    def takeoff(self):
        print "takeoff"
        self.navdata['drone_state']['fly_mask'] = 1

    def land(self):
        print "land"
        self.navdata['drone_state']['fly_mask'] = 0

    def hover(self):
        print "hover"

    def reset(self):
        print "reset"

    def trim(self):
        pass

    def halt(self):
        print "Halting communication."

    def _move(self):
        print "MOVE:", self.speeds

    def at(self, cmd, *args, **kwargs):
        pass