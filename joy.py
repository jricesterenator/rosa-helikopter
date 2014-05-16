import time

import pygame
import signal

from libardrone import libardrone
from mydrone import myardrone, mockardrone

VIDEO_ENABLE=True
DEBUG=False

DEADZONE = [.55, .550, .55, .55] #leftstick_x, leftstick_y, rightstick_x, rightstick_y


# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputing the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def printme(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10

class DroneControl:

    def __init__(self, drone):
        self.takingOff = False
        self.drone = drone

    def handleJoystickData(self):
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            axes = joystick.get_numaxes()
            for i in range(axes):
                axis = joystick.get_axis(i)
                self.updateAxis(i, axis)

            buttons = joystick.get_numbuttons()
            for i in range(buttons):
                button = joystick.get_button(i)
                self.updateButton(i, button)


    def updateButton(self, i, value):
        if i == 4: #start button
            global takingOff
            if value:
                if not takingOff:
                    self.drone.takeoff()
                    time.sleep(1)
                    takingOff = True
                elif not d.landed():
                    self.drone.land()
                    time.sleep(1)
                    takingOff = False

        elif i == 11: #Y
            if value:
                self.drone.hover()

        elif i == 13: #White
            if value:
                takingOff = False
                self.drone.clearEmergency()


    def updateAxis(self, i, value):

        def process(axis, value, negativefx, positivefx):
            if i == axis:
                neg = False
                if value < 0:
                    neg = True

                if -DEADZONE[axis] <= value <= DEADZONE[axis]:
                    value = 0
                    neg = False

                absval = abs(value)
                if neg:
                    negativefx(float(absval))
                else:
                    positivefx(float(absval))
                if DEBUG:
                    print axis, round(value, 2)

        process(2, value, d.turn_left, d.turn_right)
        process(1, value, d.move_forward, d.move_backward)
        process(0, value, d.move_left, d.move_right)
        process(3, value, d.move_up, d.move_down)


def updateJoystickDisplay():
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()
    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()
    textPrint.printme(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        textPrint.printme(screen, "Joystick {}".format(i))
        textPrint.indent()

        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.printme(screen, "Joystick name: {}".format(name))

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.printme(screen, "Number of axes: {}".format(axes))
        textPrint.indent()

        for i in range(axes):
            axis = joystick.get_axis(i)
            textPrint.printme(screen, "Axis {} value: {:>6.3f}".format(i, axis))
        textPrint.unindent()

        buttons = joystick.get_numbuttons()
        textPrint.printme(screen, "Number of buttons: {}".format(buttons))
        textPrint.indent()

        for i in range(buttons):
            button = joystick.get_button(i)
            textPrint.printme(screen, "Button {:>2} value: {}".format(i, button))
        textPrint.unindent()

        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        textPrint.printme(screen, "Number of hats: {}".format(hats))
        textPrint.indent()

        for i in range(hats):
            hat = joystick.get_hat(i)
            textPrint.printme(screen, "Hat {} value: {}".format(i, str(hat)))
        textPrint.unindent()

        textPrint.unindent()


    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

def mainloop(args=None):

    #Loop until the user clicks the close button.
    done = False

    # -------- Main Program Loop -----------
    while not done:
        # EVENT PROCESSING STEP
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop

            # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
            if event.type == pygame.JOYBUTTONDOWN:
                print "Joystick button pressed."
            if event.type == pygame.JOYBUTTONUP:
                print "Joystick button released."

        droneControl.handleJoystickData()
        updateJoystickDisplay()

        # Limit to 20 frames per second
        clock.tick(20)




if __name__ == '__main__':

#    d = myardrone.MyARDrone(libardrone.ARDrone2())
    d = myardrone.MyARDrone(mockardrone.MockARDrone())


    def signalHandler(signum, frame):
        d.halt()
        pygame.quit()
    signal.signal(signal.SIGINT, signalHandler)


    pygame.init()

    # Set the width and height of the screen [width,height]
    size = [500, 700]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("My Game")

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Initialize the joysticks
    pygame.joystick.init()

    # Get ready to print
    textPrint = TextPrint()
    droneControl = DroneControl(d)

    import thread
    thread.start_new_thread(mainloop, (None,))

    if VIDEO_ENABLE:
        import myvideo
        video = myvideo.MyVideoPane(fullscreen=False)
        video.enable_drone_video(d)
        video.start() #Blocking
    else:
        while True:
            time.sleep(.001)


    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()