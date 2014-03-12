
def Not(value):
    return value is not None and not value

class DroneStateControl:

    TAKE_OFF_ON_GROUND = 0
    TAKE_OFF_PENDING = -1
    TAKE_OFF_IN_AIR = 1

    VERTICAL_HOVER = 0
    VERTICAL_ASCEND = 1
    VERTICAL_DESCEND = -1

    STRAIGHT_HOVER = 0
    STRAIGHT_FWD = 1
    STRAIGHT_REVERSE = -1

    STRAFE_NONE = 0
    STRAFE_LEFT = -1
    STRAFE_RIGHT = 1

    ROTATE_NONE = 0
    ROTATE_LEFT = -1
    ROTATE_RIGHT = 1

    def __init__(self, inputs, drone):
        self.dstate = {
            'takeoff'   : self.TAKE_OFF_ON_GROUND,
            'emergency' : 0,
            'vertical_motion' : self.VERTICAL_HOVER,
            'straight_motion' : self.STRAIGHT_HOVER,
            'side_motion' : self.STRAFE_NONE,
            'rotation' : self.ROTATE_NONE,
            }
        self.drone = drone
        self.inputs = inputs

        self.dirty = True

    def print_state(self):
        print "----------------------"
        print "|STATE"
        for k,v in self.dstate.items():
            print "|",k,v
        print "----------------------"

    """Callback when any input changes"""
    def received_input(self, name, prev, curr):
        self.dirty = True

    def tick(self):
        self._tick()
        self.print_state()

    def _tick(self):

        #Only process when updates
        if not self.dirty:
            return

        def state(state, cmpVal=None):
            if cmpVal is not None:
                return self.dstate[state] == cmpVal
            return self.dstate[state]

        def i(name):
            return self.inputs.inputs[name]()

        #Emergency lock-down
        if state('emergency'):
            print "Emergency mode active. Can't do anything. Please reset."
        elif i('emergency_button'):
            self.emergency_stop()

        else:
            #Don't do anything while taking off
            if state('takeoff', self.TAKE_OFF_PENDING):
                return

            #Actions when the drone is on the ground
            elif state('takeoff', self.TAKE_OFF_ON_GROUND):
                if i('takeoff'):
                    self.takeoff()

            elif state('takeoff', self.TAKE_OFF_IN_AIR):

                if i('land'):
                    self.land()
                    return
                elif i('hover'):
                    self.hover()
                    return


                ###### STRAIGHT MOTION #####
                if state('straight_motion', self.STRAIGHT_HOVER):
                    if i('straight_motion_active'):
                        if i('reverse'):
                            self.reverse(0)
                        elif i('forward'):
                            self.forward(0)

                elif state('straight_motion', self.STRAIGHT_FWD):
                    if Not(i('straight_motion_active')):
                        self.forward(stop=True)
                    elif i('reverse'):
                        self.reverse(i('straight_speed'))
                    else:
                        self.forward(i('straight_speed'))

                elif state('straight_motion', self.STRAIGHT_REVERSE):
                    if Not(i('straight_motion_active')):
                        self.reverse(stop=True)
                    elif i('forward'):
                        self.forward(i('straight_speed'))
                    else:
                        self.reverse(i('straight_speed'))



                ###### VERTICAL MOTION #####
                if state('vertical_motion', self.VERTICAL_HOVER):
                    if i('vertical_motion_active'):
                        if i('up'):
                            self.ascend(0)
                        elif i('down'):
                            self.descend(0)

                elif state('vertical_motion', self.VERTICAL_ASCEND):
                    if Not(i('vertical_motion_active')):
                        self.ascend(stop=True)
                    elif i('down'):
                        self.descend(i('vertical_speed'))
                    else:
                        self.ascend(i('vertical_speed'))

                elif state('vertical_motion', self.VERTICAL_DESCEND):
                    if Not(i('vertical_motion_active')):
                        self.descend(stop=True)
                    elif Not(i('down')):
                        self.ascend(i('vertical_speed'))
                    else:
                        self.descend(i('vertical_speed'))



                ###### SIDE MOTION #####
                if state('side_motion', self.STRAFE_NONE):
                    if i('strafe_active'):
                        if i('strafe_left'):
                            self.strafe_left(0)
                        elif i('strafe_right'):
                            self.strafe_right(0)

                elif state('side_motion', self.STRAFE_LEFT):
                    if Not(i('strafe_active')):
                        self.strafe_left(stop=True)
                    elif i('strafe_right'):
                        self.strafe_right(i('strafe_speed'))
                    else:
                        self.strafe_left(i('strafe_speed'))

                elif state('side_motion', self.STRAFE_RIGHT):
                    if Not(i('strafe_active')):
                        self.strafe_right(stop=True)
                    elif i('strafe_left'):
                        self.strafe_left(i('strafe_speed'))
                    else:
                        self.strafe_right(i('strafe_speed'))


                ###### ROTATION #####
                if state('rotation', self.ROTATE_NONE):
                    if i('rotate_active'):
                        if i('rotate_left'):
                            self.rotate_left(0)
                        elif i('rotate_right'):
                            self.rotate_right(0)

                elif state('rotation', self.ROTATE_LEFT):
                    if Not(i('rotate_active')):
                        self.rotate_left(stop=True)
                    elif i('rotate_right'):
                        self.rotate_right(i('rotate_speed'))
                    else:
                        self.rotate_left(i('rotate_speed'))

                elif state('rotation', self.ROTATE_RIGHT):
                    if Not(i('rotate_active')):
                        self.rotate_right(stop=True)
                    elif i('rotate_left'):
                        self.rotate_left(i('rotate_speed'))
                    else:
                        self.rotate_right(i('rotate_speed'))



    def takeoff(self):
        self.dstate['takeoff'] = self.TAKE_OFF_PENDING
        self.reset_motion_stats()
        self.drone.takeoff() #JRTODO wait for takeoff
        self.dstate['takeoff'] = self.TAKE_OFF_IN_AIR

    def land(self):
        self.dstate['takeoff'] = self.TAKE_OFF_PENDING
        self.drone.land() #JRTODO wait for land
        self.reset_motion_stats()
        self.dstate['takeoff'] = self.TAKE_OFF_ON_GROUND

    def emergency_stop(self, force=False):
        print "Emergency mode active."
        self.dstate['emergency'] = 1

        #Don't reset if it's already on the ground. Should I force it?
        if force or self.dstate['takeoff'] != self.TAKE_OFF_ON_GROUND:
            self.drone.reset()

    def ascend(self, speed=0, stop=False):
        newState = self.VERTICAL_ASCEND
        if stop:
            newState = self.VERTICAL_HOVER
            speed = 0

        self.dstate['vertical_motion'] = newState
        self.set_speed(speed)
        self.drone.move_up()

    def descend(self, speed=0, stop=False):
        newState = self.VERTICAL_DESCEND
        if stop:
            newState = self.VERTICAL_HOVER
            speed = 0

        self.dstate['vertical_motion'] = newState
        self.set_speed(speed)
        self.drone.move_down()

    def forward(self, speed=0, stop=False):
        newState = self.STRAIGHT_FWD
        if stop:
            newState = self.STRAIGHT_HOVER
            speed = 0

        self.dstate['straight_motion'] = newState
        self.set_speed(speed)
        self.drone.move_forward()

    def reverse(self, speed=0, stop=False):
        newState = self.STRAIGHT_REVERSE
        if stop:
            newState = self.STRAIGHT_HOVER
            speed = 0

        self.dstate['straight_motion'] = newState
        self.set_speed(speed)
        self.drone.move_backward()

    def strafe_left(self, speed=0, stop=False):
        newState = self.STRAFE_LEFT
        if stop:
            newState = self.STRAFE_NONE
            speed = 0

        self.dstate['side_motion'] = newState
        self.set_speed(speed)
        self.drone.move_left()

    def strafe_right(self, speed=0, stop=False):
        newState = self.STRAFE_RIGHT
        if stop:
            newState = self.STRAFE_NONE
            speed = 0

        self.dstate['side_motion'] = newState
        self.set_speed(speed)
        self.drone.move_right()

    def rotate_left(self, speed=0, stop=False):
        newState = self.ROTATE_LEFT
        if stop:
            newState = self.ROTATE_NONE
            speed = 0

        self.dstate['rotation'] = newState
        self.set_speed(speed)
        self.drone.turn_left()

    def rotate_right(self, speed=0, stop=False):
        newState = self.ROTATE_RIGHT
        if stop:
            newState = self.ROTATE_NONE
            speed = 0

        self.dstate['rotation'] = newState
        self.set_speed(speed)
        self.drone.turn_right()

    def set_speed(self, speed):
        self.drone.set_speed(speed)

    def hover(self):
        self.drone.hover()
        self.reset_motion_stats()

    def reset_motion_stats(self):
        self.dstate['vertical_motion'] = self.VERTICAL_HOVER
        self.dstate['straight_motion'] = self.STRAIGHT_HOVER
        self.dstate['rotation'] = self.ROTATE_NONE
        self.dstate['side_motion'] = self.STRAFE_NONE

