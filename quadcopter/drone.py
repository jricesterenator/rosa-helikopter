
class Drone:

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
        if value <= 2 and value >= -2:
            print "Hovering"
            self.drone.hover()
            return
        else:
            speed = abs(value/float(maxval))
            print "New speed:", speed

            self.drone.set_speed(speed)
            if value < 0:
                print "Moving left"
                self.drone.move_left()
            else:
                print "Moving right"
                self.drone.move_right()
