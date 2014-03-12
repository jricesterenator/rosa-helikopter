class MockARDrone:

    def __init__(self):
        self.speed = .2

    def takeoff(self):
        print "takeoff"

    def land(self):
        print "land"

    def hover(self):
        print "hover"

    def move_left(self):
        print "move left at", self.speed

    def move_right(self):
        print "move right at", self.speed

    def move_up(self):
        print "move up at", self.speed

    def move_down(self):
        print "move down at", self.speed

    def move_forward(self):
        print "move forward at", self.speed

    def move_backward(self):
        print "move backward at", self.speed

    def turn_left(self):
        print "rotate left at", self.speed

    def turn_right(self):
        print "rotate right at", self.speed

    def reset(self):
        print "reset"

    def trim(self):
        pass

    def set_speed(self, speed):
        self.speed = speed
#        print "set speed to", speed

    def halt(self):
        print "halt communication"