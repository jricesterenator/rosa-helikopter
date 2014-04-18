from serial.tools import list_ports
from controls import *
from canbus import *

def parseCANString(m):
    sender = int(m[:3], 16)
    hexmsg = int(m.replace(' ', '')[3:19], 16)
    return sender, hexmsg

def parseCANValue(hexMsg, byteIndex, mask):
    shiftedMsg = hexMsg >> (8 * (byteIndex-1))
    return shiftedMsg & mask

class Cars:

    class AbstractCar:
        def __init__(self, controls):
            self.controls = controls

        def getControlsList(self):
            return self.controls.values()

        def processMessages(self, msgs):
            for m in msgs:
                self.processMessage(m)

        """Override and implement this"""
        def processMessage(self, m):
            raise NotImplementedError()

    class SimpleCar(AbstractCar):
        def __init__(self, controlList):
            controls = {}
            for key, control_def in controlList.items():
                controls[key] = GenericValueHandler(control_def)

            Cars.AbstractCar.__init__(self, controls)

        def processMessage(self, msg):
            key, value = msg.split(",")

            if key not in self.controls:
                print "[WARNING] Unknown message key:", key
                return

            control = self.controls[key]
            if control.value.setNewValue(float(value)):
                print "   %s set to %s" % (key, value)
                control.notifyListeners()

    #JRTODO: Work off a queue instead of calling processMessages?
    class CANCar(AbstractCar):
        def __init__(self, controlList):
            controls = {}
            for key, control_def in controlList.items():
                controls[key] = CANMessageProcessor(control_def)

            Cars.AbstractCar.__init__(self, controls)

        def getSenders(self, debugAllControls=False):
            if debugAllControls:#follow all inputs, even if they don't have listeners
                ids = set()
                for control in self.controls.values():
                    ids.add(control.control_def.sender)
                return ids
            else:
                ids = set()
                for control in self.controls.values():
                    if control.listeners:
                        ids.add(control.sender)
                return ids

        def processMessage(self, m):
            try:
                sender, hexmsg = self._parseCANString(m)

            except ValueError:
                print "[WARNING]", m, "is not a CAN message."
                return

            except TypeError:
                print "[WARNING]", m, "is not a CAN message."
                return

            for control in self.controls.values():
                self._processCANMessage(control, sender, hexmsg)

        def _parseCANString(self, m):
            return parseCANString(m)

        def _processCANMessage(self, control, sender, hexmsg):
            control_def = control.control_def
            if control_def.senderMatches(sender):
                canValue = self._parseCANValue(hexmsg, control_def.byteIndex, control_def.mask)

                #JRTODO: If I need to sync the value changes between CAN and real,
                #JRTODO: only set the CAN value after processing the real value.
                #JRTODO: However, I don't think it will be a problem.

                #If CAN value changed, update the corrected value
                if control.canValue.setNewValue(canValue):

                    #Print updated CAN value info
                    self._printChangeInfo(control_def, control.canValue.prev, canValue)

##JRTODO does this section belong in the can control object?
                    #Update converted value
                    try:
                        convertedValue = control_def.getCorrectedValue(canValue)
                    except ValueError:
                        print "[WARNING] Unhandled value for %s: %s" % (control_def.name, canValue)
                        convertedValue = None

                    if control.setNewValue(convertedValue):
                        control.notifyListeners()


        def _parseCANValue(self, hexMsg, byteIndex, mask):
            return parseCANValue(hexMsg, byteIndex, mask)

        def _printChangeInfo(self, control_def, prevValue, newValue):

            def _getPrintableCANValue(value):
                string = "NOT_SET"
                if value != None:
                    string = hex(value)
                return string

            prevCorrected = control_def.getCorrectedValue(prevValue)
            newCorrected = control_def.getCorrectedValue(newValue)

            print "[INFO] %s changed from %s to %s (%s --> %s): %s" %\
                  (control_def.name,
                   _getPrintableCANValue(prevValue),
                   _getPrintableCANValue(newValue),
                   prevCorrected,
                   newCorrected,
                   newCorrected)


class CarConnectors:

    class BasicConnection:
        def connectToCar(self, car):
            print "Connected to Car"
            return car

        def destroy(self):
            print "Connection closed"


    class CANSerialConnection:
        def __init__(self, serial, debugAllControls):
            self.serial = serial
            self.debugAllControls = debugAllControls

        def connectToCar(self, can_car):
            self.canMonitor = Bus.CANBusMonitor(Bus.CANBus(self.serial))
            self.canMonitor.setup()
            self.canMonitor.startCANMonitor(can_car.getSenders(self.debugAllControls), can_car.processMessage)
            return can_car

        def listSerialPorts(self):
            ports = [p[0] for p in list_ports.comports()]

            print "Available serial ports:"
            for p in ports:
                print "  " + p

        def destroy(self):
            self.canMonitor.destroy()
            if self.serial:
                self.serial.close()
                print "Serial connection closed"
